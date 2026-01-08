"""
ETL Pipeline for Data Quality Issues
Extract, Transform, and Load phases for customers, products, and sales data
"""

import pandas as pd
import re
from datetime import datetime
from typing import Tuple, Optional
import mysql.connector
from mysql.connector import Error


class ETLPipeline:
    def __init__(self, customers_path: str, products_path: str, sales_path: str,
                 db_config: Optional[dict] = None):
        """
        Initialize ETL Pipeline with file paths and database configuration
        
        Args:
            customers_path: Path to customers_raw.csv
            products_path: Path to products_raw.csv
            sales_path: Path to sales_raw.csv
            db_config: Dictionary with MySQL connection parameters:
                {
                    'host': 'localhost',
                    'user': 'root',
                    'password': 'password',
                    'database': 'etl_database'
                }
        """
        self.customers_path = customers_path
        self.products_path = products_path
        self.sales_path = sales_path
        
        # Database configuration
        self.db_config = db_config or {
            'host': 'localhost',
            'user': 'root',
            'password': 'password',
            'database': 'fleximart'
        }
        
        # DataFrames to store cleaned data
        self.customers_df = None
        self.products_df = None
        self.sales_df = None
        
        # Database connection
        self.connection = None
    
    def extract(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Extract: Read all three CSV files
        
        Returns:
            Tuple of (customers_df, products_df, sales_df)
        """
        print("=" * 60)
        print("EXTRACT PHASE")
        print("=" * 60)
        
        # Read CSV files
        customers_df = pd.read_csv(self.customers_path)
        products_df = pd.read_csv(self.products_path)
        sales_df = pd.read_csv(self.sales_path)
        
        print(f"\nCustomers: {len(customers_df)} records loaded")
        print(f"Products: {len(products_df)} records loaded")
        print(f"Sales: {len(sales_df)} records loaded")
        
        return customers_df, products_df, sales_df
    
    def standardize_phone(self, phone: str) -> str:
        """
        Standardize phone format to +91-9876543210
        
        Args:
            phone: Phone number in various formats
            
        Returns:
            Standardized phone number in format +91-XXXXXXXXXX
        """
        if pd.isna(phone) or phone == '':
            return None
        
        # Convert to string and remove all non-digit characters
        phone_str = str(phone)
        digits_only = re.sub(r'\D', '', phone_str)
        
        # Handle different formats
        if len(digits_only) == 10:
            # 10-digit number, add +91 prefix
            return f"+91-{digits_only}"
        elif len(digits_only) == 12 and digits_only.startswith('91'):
            # Already has 91 prefix
            return f"+91-{digits_only[2:]}"
        elif len(digits_only) == 11 and digits_only.startswith('0'):
            # Has leading 0
            return f"+91-{digits_only[1:]}"
        elif len(digits_only) >= 10:
            # Take last 10 digits
            return f"+91-{digits_only[-10:]}"
        else:
            # Invalid format, return None
            return None
    
    def standardize_category(self, category: str) -> str:
        """
        Standardize category names (e.g., "electronics" -> "Electronics")
        
        Args:
            category: Category name in various formats
            
        Returns:
            Standardized category name with proper capitalization
        """
        if pd.isna(category) or category == '':
            return None
        
        category_str = str(category).strip()
        
        # Convert to title case (first letter uppercase, rest lowercase)
        standardized = category_str.title()
        
        return standardized
    
    def standardize_date(self, date_str: str) -> str:
        """
        Convert date formats to YYYY-MM-DD
        
        Args:
            date_str: Date in various formats
            
        Returns:
            Date in YYYY-MM-DD format or None if invalid
        """
        if pd.isna(date_str) or date_str == '':
            return None
        
        date_str = str(date_str).strip()
        
        # Try different date formats
        date_formats = [
            '%Y-%m-%d',      # 2024-01-15
            '%d/%m/%Y',      # 15/01/2024
            '%m-%d-%Y',      # 01-22-2024
            '%d-%m-%Y',      # 15-04-2023
            '%m/%d/%Y',      # 02/02/2024
        ]
        
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # If no format matches, return None
        print(f"Warning: Could not parse date: {date_str}")
        return None
    
    def transform_customers(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform customers data:
        - Remove duplicates
        - Handle missing values
        - Standardize phone formats
        - Standardize date formats
        - Add surrogate key
        
        Args:
            customers_df: Raw customers DataFrame
            
        Returns:
            Transformed customers DataFrame
        """
        print("\n" + "=" * 60)
        print("TRANSFORM PHASE - CUSTOMERS")
        print("=" * 60)
        
        df = customers_df.copy()
        
        # Remove duplicate records
        initial_count = len(df)
        df = df.drop_duplicates(subset=['customer_id'], keep='first')
        duplicates_removed = initial_count - len(df)
        print(f"\nRemoved {duplicates_removed} duplicate customer records")
        
        # Handle missing emails - fill with default pattern
        missing_emails = df['email'].isna().sum()
        if missing_emails > 0:
            # Generate email from first_name.last_name@unknown.com
            mask = df['email'].isna()
            df.loc[mask, 'email'] = (
                df.loc[mask, 'first_name'].str.lower() + '.' + 
                df.loc[mask, 'last_name'].str.lower() + '@unknown.com'
            )
            print(f"Filled {missing_emails} missing emails with default pattern")
        
        # Standardize phone formats
        df['phone'] = df['phone'].apply(self.standardize_phone)
        print("Standardized phone formats to +91-XXXXXXXXXX")
        
        # Standardize date formats
        df['registration_date'] = df['registration_date'].apply(self.standardize_date)
        print("Standardized registration_date to YYYY-MM-DD format")
        
        # Add surrogate key (auto-incrementing ID starting from 1)
        df.insert(0, 'id', range(1, len(df) + 1))
        print(f"Added surrogate key 'id' (1 to {len(df)})")
        
        # Final count
        print(f"\nFinal customers count: {len(df)} records")
        
        return df
    
    def transform_products(self, products_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform products data:
        - Remove duplicates
        - Handle missing values (prices, stock)
        - Standardize category names
        - Add surrogate key
        
        Args:
            products_df: Raw products DataFrame
            
        Returns:
            Transformed products DataFrame
        """
        print("\n" + "=" * 60)
        print("TRANSFORM PHASE - PRODUCTS")
        print("=" * 60)
        
        df = products_df.copy()
        
        # Remove duplicate records
        initial_count = len(df)
        df = df.drop_duplicates(subset=['product_id'], keep='first')
        duplicates_removed = initial_count - len(df)
        print(f"\nRemoved {duplicates_removed} duplicate product records")
        
        # Handle missing prices - fill with median price of same category
        missing_prices = df['price'].isna().sum()
        if missing_prices > 0:
            # Calculate median price per category
            category_medians = df.groupby('category')['price'].median()
            
            # Fill missing prices with category median
            for idx, row in df[df['price'].isna()].iterrows():
                category = row['category']
                if category in category_medians.index and not pd.isna(category_medians[category]):
                    df.at[idx, 'price'] = category_medians[category]
                else:
                    # If category median is also NaN, use overall median
                    df.at[idx, 'price'] = df['price'].median()
            
            print(f"Filled {missing_prices} missing prices with category median/overall median")
        
        # Handle null stock values - fill with 0
        missing_stock = df['stock_quantity'].isna().sum()
        if missing_stock > 0:
            df['stock_quantity'] = df['stock_quantity'].fillna(0)
            print(f"Filled {missing_stock} null stock values with 0")
        
        # Standardize category names
        df['category'] = df['category'].apply(self.standardize_category)
        print("Standardized category names to Title Case")
        
        # Add surrogate key (auto-incrementing ID starting from 1)
        df.insert(0, 'id', range(1, len(df) + 1))
        print(f"Added surrogate key 'id' (1 to {len(df)})")
        
        # Final count
        print(f"\nFinal products count: {len(df)} records")
        
        return df
    
    def transform_sales(self, sales_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform sales data:
        - Remove duplicates
        - Handle missing values (customer_id, product_id)
        - Standardize date formats
        - Add surrogate key
        
        Args:
            sales_df: Raw sales DataFrame
            
        Returns:
            Transformed sales DataFrame
        """
        print("\n" + "=" * 60)
        print("TRANSFORM PHASE - SALES")
        print("=" * 60)
        
        df = sales_df.copy()
        
        # Remove duplicate records
        initial_count = len(df)
        df = df.drop_duplicates(subset=['transaction_id'], keep='first')
        duplicates_removed = initial_count - len(df)
        print(f"\nRemoved {duplicates_removed} duplicate transaction records")
        
        # Handle missing customer_id - drop records (can't infer customer)
        missing_customer_id = df['customer_id'].isna().sum()
        if missing_customer_id > 0:
            df = df.dropna(subset=['customer_id'])
            print(f"Dropped {missing_customer_id} records with missing customer_id")
        
        # Handle missing product_id - drop records (can't infer product)
        missing_product_id = df['product_id'].isna().sum()
        if missing_product_id > 0:
            df = df.dropna(subset=['product_id'])
            print(f"Dropped {missing_product_id} records with missing product_id")
        
        # Standardize date formats
        df['transaction_date'] = df['transaction_date'].apply(self.standardize_date)
        print("Standardized transaction_date to YYYY-MM-DD format")
        
        # Drop records with invalid dates
        invalid_dates = df['transaction_date'].isna().sum()
        if invalid_dates > 0:
            df = df.dropna(subset=['transaction_date'])
            print(f"Dropped {invalid_dates} records with invalid dates")
        
        # Add surrogate key (auto-incrementing ID starting from 1)
        df.insert(0, 'id', range(1, len(df) + 1))
        print(f"Added surrogate key 'id' (1 to {len(df)})")
        
        # Final count
        print(f"\nFinal sales count: {len(df)} records")
        
        return df
    
    def transform(self, customers_df: pd.DataFrame, products_df: pd.DataFrame, 
                  sales_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Transform all datasets
        
        Args:
            customers_df: Raw customers DataFrame
            products_df: Raw products DataFrame
            sales_df: Raw sales DataFrame
            
        Returns:
            Tuple of transformed DataFrames
        """
        self.customers_df = self.transform_customers(customers_df)
        self.products_df = self.transform_products(products_df)
        self.sales_df = self.transform_sales(sales_df)
        
        return self.customers_df, self.products_df, self.sales_df
    
    def save_transformed_data(self, output_dir: str = None):
        """
        Save transformed data to CSV files
        
        Args:
            output_dir: Directory to save output files (default: current directory)
        """
        if output_dir is None:
            import os
            output_dir = os.path.dirname(os.path.abspath(__file__))
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        if self.customers_df is not None:
            customers_output = os.path.join(output_dir, 'customers_cleaned.csv')
            self.customers_df.to_csv(customers_output, index=False)
            print(f"\nSaved cleaned customers data to: {customers_output}")
        
        if self.products_df is not None:
            products_output = os.path.join(output_dir, 'products_cleaned.csv')
            self.products_df.to_csv(products_output, index=False)
            print(f"Saved cleaned products data to: {products_output}")
        
        if self.sales_df is not None:
            sales_output = os.path.join(output_dir, 'sales_cleaned.csv')
            self.sales_df.to_csv(sales_output, index=False)
            print(f"Saved cleaned sales data to: {sales_output}")
    
    def connect_to_mysql(self) -> bool:
        """
        Connect to MySQL database
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # First connect without database to create it if needed
            temp_config = self.db_config.copy()
            database_name = temp_config.pop('database', 'fleximart')
            
            self.connection = mysql.connector.connect(**temp_config)
            
            if self.connection.is_connected():
                db_executor = self.connection.cursor()
                # Create database if it doesn't exist
                db_executor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
                db_executor.close()
                
                # Reconnect with database
                self.connection.close()
                self.connection = mysql.connector.connect(**self.db_config)
                
                if self.connection.is_connected():
                    print(f"Successfully connected to MySQL database: {database_name}")
                    return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
        
        return False
    
    def create_tables(self):
        """
        Create tables in MySQL database if they don't exist
        """
        if not self.connection or not self.connection.is_connected():
            print("Error: Not connected to database")
            return
        
        try:
            db_executor = self.connection.cursor()
            
            # Create customers table
            customers_table = """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                city VARCHAR(50),
                registration_date DATE
            )
            """
            db_executor.execute(customers_table)
            print("Created/Verified 'customers' table")
            
            # Create products table
            products_table = """
            CREATE TABLE IF NOT EXISTS products (
                product_id INT PRIMARY KEY AUTO_INCREMENT,
                product_name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                stock_quantity INT DEFAULT 0
            )
            """
            db_executor.execute(products_table)
            print("Created/Verified 'products' table")
            
            # Create orders table
            orders_table = """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT NOT NULL,
                order_date DATE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'Pending',
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
            """
            db_executor.execute(orders_table)
            print("Created/Verified 'orders' table")
            
            # Create order_items table
            order_items_table = """
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT PRIMARY KEY AUTO_INCREMENT,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
            """
            db_executor.execute(order_items_table)
            print("Created/Verified 'order_items' table")
            
            self.connection.commit()
            db_executor.close()
            
        except Error as e:
            print(f"Error creating tables: {e}")
            if self.connection:
                self.connection.rollback()
    
    def load_customers(self):
        """
        Load customers data into MySQL database
        Returns mapping from CSV customer_id (VARCHAR) to database customer_id (INT)
        """
        if self.customers_df is None or len(self.customers_df) == 0:
            print("No customers data to load")
            return {}
        
        if not self.connection or not self.connection.is_connected():
            print("Error: Not connected to database")
            return {}
        
        customer_id_mapping = {}  # Maps CSV customer_id (VARCHAR) to DB customer_id (INT)
        
        try:
            db_executor = self.connection.cursor()
            
            # Insert data (customer_id is auto-increment, so we don't specify it)
            insert_query = """
            INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            records_inserted = 0
            for _, row in self.customers_df.iterrows():
                values = (
                    str(row['first_name']),
                    str(row['last_name']),
                    str(row['email']),
                    row['phone'] if pd.notna(row['phone']) else None,
                    str(row['city']) if pd.notna(row['city']) else None,
                    row['registration_date'] if pd.notna(row['registration_date']) else None
                )
                db_executor.execute(insert_query, values)
                # Get the auto-generated customer_id
                csv_customer_id = str(row['customer_id'])
                db_customer_id = db_executor.lastrowid
                customer_id_mapping[csv_customer_id] = db_customer_id
                records_inserted += 1
            
            self.connection.commit()
            db_executor.close()
            print(f"Successfully inserted {records_inserted} customer records")
            return customer_id_mapping
            
        except Error as e:
            print(f"Error loading customers data: {e}")
            if self.connection:
                self.connection.rollback()
            return {}
    
    def load_products(self):
        """
        Load products data into MySQL database
        Returns mapping from CSV product_id (VARCHAR) to database product_id (INT)
        """
        if self.products_df is None or len(self.products_df) == 0:
            print("No products data to load")
            return {}
        
        if not self.connection or not self.connection.is_connected():
            print("Error: Not connected to database")
            return {}
        
        product_id_mapping = {}  # Maps CSV product_id (VARCHAR) to DB product_id (INT)
        
        try:
            db_executor = self.connection.cursor()
            
            # Insert data (product_id is auto-increment, so we don't specify it)
            insert_query = """
            INSERT INTO products (product_name, category, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
            """
            
            records_inserted = 0
            for _, row in self.products_df.iterrows():
                values = (
                    str(row['product_name']),
                    str(row['category']) if pd.notna(row['category']) else 'Unknown',
                    float(row['price']) if pd.notna(row['price']) else 0.0,
                    int(row['stock_quantity']) if pd.notna(row['stock_quantity']) else 0
                )
                db_executor.execute(insert_query, values)
                # Get the auto-generated product_id
                csv_product_id = str(row['product_id'])
                db_product_id = db_executor.lastrowid
                product_id_mapping[csv_product_id] = db_product_id
                records_inserted += 1
            
            self.connection.commit()
            db_executor.close()
            print(f"Successfully inserted {records_inserted} product records")
            return product_id_mapping
            
        except Error as e:
            print(f"Error loading products data: {e}")
            if self.connection:
                self.connection.rollback()
            return {}
    
    def transform_sales_to_orders(self, customer_id_mapping: dict, product_id_mapping: dict):
        """
        Transform sales data into orders and order_items DataFrames
        
        Args:
            customer_id_mapping: Maps CSV customer_id (VARCHAR) to DB customer_id (INT)
            product_id_mapping: Maps CSV product_id (VARCHAR) to DB product_id (INT)
            
        Returns:
            Tuple of (orders_df, order_items_df)
        """
        if self.sales_df is None or len(self.sales_df) == 0:
            return pd.DataFrame(), pd.DataFrame()
        
        # Filter out records with missing customer_id or product_id
        sales_df = self.sales_df[
            (self.sales_df['customer_id'].notna()) & 
            (self.sales_df['product_id'].notna())
        ].copy()
        
        # Map customer_id and product_id to database IDs
        sales_df['db_customer_id'] = sales_df['customer_id'].map(customer_id_mapping)
        sales_df['db_product_id'] = sales_df['product_id'].map(product_id_mapping)
        
        # Filter out records where mapping failed
        sales_df = sales_df[
            (sales_df['db_customer_id'].notna()) & 
            (sales_df['db_product_id'].notna())
        ].copy()
        
        # Calculate subtotal for each item
        sales_df['subtotal'] = sales_df['quantity'] * sales_df['unit_price']
        
        # Group by customer_id and transaction_date to create orders
        orders_list = []
        order_items_list = []
        order_id_counter = 1
        
        # Group sales by customer and date
        grouped = sales_df.groupby(['db_customer_id', 'transaction_date'])
        
        for (customer_id, order_date), group in grouped:
            # Calculate total amount for the order
            total_amount = group['subtotal'].sum()
            
            # Get status (use most common status, or 'Completed' as default)
            status = group['status'].mode()[0] if len(group['status'].mode()) > 0 else 'Completed'
            
            # Create order record
            orders_list.append({
                'order_id': order_id_counter,
                'customer_id': int(customer_id),
                'order_date': order_date,
                'total_amount': float(total_amount),
                'status': status
            })
            
            # Create order_items for this order
            for _, item in group.iterrows():
                order_items_list.append({
                    'order_id': order_id_counter,
                    'product_id': int(item['db_product_id']),
                    'quantity': int(item['quantity']),
                    'unit_price': float(item['unit_price']),
                    'subtotal': float(item['subtotal'])
                })
            
            order_id_counter += 1
        
        orders_df = pd.DataFrame(orders_list)
        order_items_df = pd.DataFrame(order_items_list)
        
        return orders_df, order_items_df
    
    def load_orders(self, orders_df: pd.DataFrame):
        """
        Load orders data into MySQL database
        """
        if orders_df is None or len(orders_df) == 0:
            print("No orders data to load")
            return
        
        if not self.connection or not self.connection.is_connected():
            print("Error: Not connected to database")
            return
        
        try:
            db_executor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO orders (customer_id, order_date, total_amount, status)
            VALUES (%s, %s, %s, %s)
            """
            
            order_id_mapping = {}  # Maps DataFrame order_id to DB order_id
            records_inserted = 0
            
            for _, row in orders_df.iterrows():
                values = (
                    int(row['customer_id']),
                    row['order_date'],
                    float(row['total_amount']),
                    str(row['status'])
                )
                db_executor.execute(insert_query, values)
                # Map DataFrame order_id to database order_id
                df_order_id = int(row['order_id'])
                db_order_id = db_executor.lastrowid
                order_id_mapping[df_order_id] = db_order_id
                records_inserted += 1
            
            self.connection.commit()
            db_executor.close()
            print(f"Successfully inserted {records_inserted} order records")
            return order_id_mapping
            
        except Error as e:
            print(f"Error loading orders data: {e}")
            if self.connection:
                self.connection.rollback()
            return {}
    
    def load_order_items(self, order_items_df: pd.DataFrame, order_id_mapping: dict):
        """
        Load order_items data into MySQL database
        
        Args:
            order_items_df: DataFrame with order items
            order_id_mapping: Maps DataFrame order_id to DB order_id
        """
        if order_items_df is None or len(order_items_df) == 0:
            print("No order items data to load")
            return
        
        if not self.connection or not self.connection.is_connected():
            print("Error: Not connected to database")
            return
        
        try:
            db_executor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            records_inserted = 0
            for _, row in order_items_df.iterrows():
                # Map DataFrame order_id to database order_id
                df_order_id = int(row['order_id'])
                db_order_id = order_id_mapping.get(df_order_id)
                
                if db_order_id is None:
                    print(f"Warning: Could not find order_id mapping for {df_order_id}")
                    continue
                
                values = (
                    int(db_order_id),
                    int(row['product_id']),
                    int(row['quantity']),
                    float(row['unit_price']),
                    float(row['subtotal'])
                )
                db_executor.execute(insert_query, values)
                records_inserted += 1
            
            self.connection.commit()
            db_executor.close()
            print(f"Successfully inserted {records_inserted} order item records")
            
        except Error as e:
            print(f"Error loading order_items data: {e}")
            if self.connection:
                self.connection.rollback()
    
    def load(self):
        """
        Load all transformed data into MySQL database
        """
        print("\n" + "=" * 60)
        print("LOAD PHASE")
        print("=" * 60)
        
        # Connect to database
        if not self.connect_to_mysql():
            print("Failed to connect to database. Skipping load phase.")
            return
        
        # Create tables
        print("\nCreating database tables...")
        self.create_tables()
        
        # Load data in correct order (parents first, then children)
        print("\nLoading data into database...")
        # First, clear existing data in correct order (children first to avoid FK violations)
        try:
            db_executor = self.connection.cursor()
            db_executor.execute("DELETE FROM order_items")  # Delete child tables first
            db_executor.execute("DELETE FROM orders")
            db_executor.execute("DELETE FROM customers")
            db_executor.execute("DELETE FROM products")
            self.connection.commit()
            db_executor.close()
            print("Cleared existing data from tables")
        except Error as e:
            print(f"Warning: Error clearing existing data: {e}")
            if self.connection:
                self.connection.rollback()
        
        # Load parent tables first and get ID mappings
        customer_id_mapping = self.load_customers()
        product_id_mapping = self.load_products()
        
        # Transform sales data into orders and order_items
        print("\nTransforming sales data into orders and order_items...")
        orders_df, order_items_df = self.transform_sales_to_orders(
            customer_id_mapping, product_id_mapping
        )
        
        # Load orders and get order_id mapping
        order_id_mapping = self.load_orders(orders_df)
        
        # Update order_items_df with database order_ids
        if len(order_items_df) > 0:
            order_items_df['order_id'] = order_items_df['order_id'].map(order_id_mapping)
            order_items_df = order_items_df.dropna(subset=['order_id'])
            # Load order items
            self.load_order_items(order_items_df, order_id_mapping)
        
        # Verify data was loaded
        self.verify_data_loaded()
        
        # Close connection
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("\nDatabase connection closed")
    
    def verify_data_loaded(self):
        """
        Verify that data was successfully loaded into the database
        """
        if not self.connection or not self.connection.is_connected():
            return
        
        try:
            db_executor = self.connection.cursor()
            
            # Count records in each table
            db_executor.execute("SELECT COUNT(*) FROM customers")
            customers_count = db_executor.fetchone()[0]
            
            db_executor.execute("SELECT COUNT(*) FROM products")
            products_count = db_executor.fetchone()[0]
            
            db_executor.execute("SELECT COUNT(*) FROM orders")
            orders_count = db_executor.fetchone()[0]
            
            db_executor.execute("SELECT COUNT(*) FROM order_items")
            order_items_count = db_executor.fetchone()[0]
            
            db_executor.close()
            
            # Calculate expected counts
            expected_customers = len(self.customers_df) if self.customers_df is not None else 0
            expected_products = len(self.products_df) if self.products_df is not None else 0
            
            # Expected orders: grouped by customer and date
            if self.sales_df is not None:
                sales_df = self.sales_df[
                    (self.sales_df['customer_id'].notna()) & 
                    (self.sales_df['product_id'].notna())
                ]
                expected_orders = sales_df.groupby(['customer_id', 'transaction_date']).ngroups
                expected_order_items = len(sales_df)
            else:
                expected_orders = 0
                expected_order_items = 0
            
            print("\n" + "=" * 60)
            print("DATA VERIFICATION")
            print("=" * 60)
            print(f"Customers in database: {customers_count} (Expected: {expected_customers})")
            print(f"Products in database: {products_count} (Expected: {expected_products})")
            print(f"Orders in database: {orders_count} (Expected: {expected_orders})")
            print(f"Order items in database: {order_items_count} (Expected: {expected_order_items})")
            
            # Verify counts match
            if (customers_count == expected_customers and
                products_count == expected_products and
                orders_count == expected_orders and
                order_items_count == expected_order_items):
                print("\n✓ All data successfully loaded and verified!")
            else:
                print("\n⚠ Warning: Record counts don't match. Please check the data.")
                
        except Error as e:
            print(f"Error verifying data: {e}")
    
    def run(self, save_output: bool = True, load_to_db: bool = False):
        """
        Run the complete ETL pipeline (Extract, Transform, and optionally Load phases)
        
        Args:
            save_output: Whether to save transformed data to CSV files
            load_to_db: Whether to load data into MySQL database
        """
        # Extract
        customers_df, products_df, sales_df = self.extract()
        
        # Transform
        self.transform(customers_df, products_df, sales_df)
        
        # Save transformed data
        if save_output:
            print("\n" + "=" * 60)
            print("SAVING TRANSFORMED DATA")
            print("=" * 60)
            self.save_transformed_data()
        
        # Load to database
        if load_to_db:
            self.load()
        
        print("\n" + "=" * 60)
        print("ETL PIPELINE COMPLETED")
        print("=" * 60)
        
        return self.customers_df, self.products_df, self.sales_df


def main():
    """
    Main function to run the ETL pipeline
    
    Usage:
        # Run without database loading (default)
        python etl_pipeline.py
        
        # Run with database loading
        python etl_pipeline.py --load-db
        
        # Run with database loading and custom password
        python etl_pipeline.py --load-db --password your_password
    """
    import os
    import sys
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run FlexiMart ETL Pipeline')
    parser.add_argument('--load-db', action='store_true', 
                       help='Load transformed data into MySQL database')
    parser.add_argument('--password', type=str, default=None,
                       help='MySQL password (or set via MYSQL_PASSWORD environment variable)')
    parser.add_argument('--host', type=str, default='localhost',
                       help='MySQL host (default: localhost)')
    parser.add_argument('--user', type=str, default='root',
                       help='MySQL user (default: root)')
    parser.add_argument('--database', type=str, default='fleximart',
                       help='MySQL database name (default: fleximart)')
    parser.add_argument('--no-save', action='store_true',
                       help='Skip saving cleaned CSV files')
    
    args = parser.parse_args()
    
    # File paths - using relative paths from part1-database-etl directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level from part1-database-etl to reach project root
    project_root = os.path.dirname(base_dir)
    data_dir = os.path.join(project_root, 'data')
    
    customers_path = os.path.join(data_dir, 'customers_raw.csv')
    products_path = os.path.join(data_dir, 'products_raw.csv')
    sales_path = os.path.join(data_dir, 'sales_raw.csv')
    
    # Verify data files exist
    if not os.path.exists(customers_path):
        print(f"Error: Customers file not found at {customers_path}")
        sys.exit(1)
    if not os.path.exists(products_path):
        print(f"Error: Products file not found at {products_path}")
        sys.exit(1)
    if not os.path.exists(sales_path):
        print(f"Error: Sales file not found at {sales_path}")
        sys.exit(1)
    
    # Database configuration
    # Get password from command line, environment variable, or prompt
    mysql_password = args.password
    if mysql_password is None:
        mysql_password = os.environ.get('MYSQL_PASSWORD')
    if mysql_password is None and args.load_db:
        # Prompt for password if loading to database
        import getpass
        mysql_password = getpass.getpass("Enter MySQL password: ")
    elif mysql_password is None:
        mysql_password = 'password'  # Default, but won't be used if not loading
    
    db_config = {
        'host': args.host,
        'user': args.user,
        'password': mysql_password,
        'database': args.database
    }
    
    # Create ETL pipeline instance
    etl = ETLPipeline(customers_path, products_path, sales_path, db_config=db_config)
    
    # Run pipeline
    save_output = not args.no_save
    load_to_db = args.load_db
    
    print("\n" + "=" * 60)
    print("ETL PIPELINE CONFIGURATION")
    print("=" * 60)
    print(f"Save cleaned CSV files: {save_output}")
    print(f"Load to MySQL database: {load_to_db}")
    if load_to_db:
        print(f"Database: {args.database} on {args.host}")
    print("=" * 60)
    
    etl.run(save_output=save_output, load_to_db=load_to_db)
    
    # Display sample of transformed data
    if etl.customers_df is not None and etl.products_df is not None and etl.sales_df is not None:
        print("\n" + "=" * 60)
        print("SAMPLE OF TRANSFORMED DATA")
        print("=" * 60)
        
        print("\n--- Customers (first 5 rows) ---")
        print(etl.customers_df.head())
        
        print("\n--- Products (first 5 rows) ---")
        print(etl.products_df.head())
        
        print("\n--- Sales (first 5 rows) ---")
        print(etl.sales_df.head())


if __name__ == "__main__":
    main()
