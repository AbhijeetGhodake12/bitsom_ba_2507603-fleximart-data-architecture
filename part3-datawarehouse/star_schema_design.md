# Star Schema Design Documentation - FlexiMart Data Warehouse

## Section 1: Schema Overview

### FACT TABLE: fact_sales

**Grain:** One row per product per order line item

**Business Process:** Sales transactions

**Measures (Numeric Facts):**
- `quantity_sold` (INT): Number of units sold in this transaction line item
- `unit_price` (DECIMAL(10,2)): Price per unit at the time of sale
- `discount_amount` (DECIMAL(10,2)): Discount applied to this line item (default: 0.00)
- `total_amount` (DECIMAL(10,2)): Final amount calculated as (quantity_sold × unit_price - discount_amount)

**Foreign Keys:**
- `date_key` (INT): References dim_date.date_key (surrogate key for order date)
- `product_key` (INT): References dim_product.product_key (surrogate key for product)
- `customer_key` (INT): References dim_customer.customer_key (surrogate key for customer)

---

### DIMENSION TABLE: dim_date

**Purpose:** Date dimension for time-based analysis and reporting

**Type:** Conformed dimension (shared across multiple fact tables)

**Attributes:**
- `date_key` (INT, PRIMARY KEY): Surrogate key in format YYYYMMDD (e.g., 20240115 for January 15, 2024)
- `full_date` (DATE): Actual calendar date
- `day_of_week` (VARCHAR(10)): Day name (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)
- `day_of_month` (INT): Day number (1-31)
- `month` (INT): Month number (1-12)
- `month_name` (VARCHAR(10)): Full month name (January, February, March, etc.)
- `quarter` (VARCHAR(2)): Quarter identifier (Q1, Q2, Q3, Q4)
- `year` (INT): Year (2023, 2024, etc.)
- `is_weekend` (BOOLEAN): True if Saturday or Sunday, False otherwise

---

### DIMENSION TABLE: dim_product

**Purpose:** Product dimension containing all product attributes for analysis

**Type:** Slowly Changing Dimension (SCD) Type 2 (tracks historical changes)

**Attributes:**
- `product_key` (INT, PRIMARY KEY): Surrogate key (auto-increment)
- `product_id` (VARCHAR(20)): Natural key from source system
- `product_name` (VARCHAR(100)): Name of the product
- `category` (VARCHAR(50)): Product category (Electronics, Fashion, Groceries)
- `subcategory` (VARCHAR(50)): Product subcategory (Smartphones, Laptops, Clothing, Footwear, etc.)
- `unit_price` (DECIMAL(10,2)): Current unit price of the product

---

### DIMENSION TABLE: dim_customer

**Purpose:** Customer dimension containing customer demographic and geographic information

**Type:** Slowly Changing Dimension (SCD) Type 1 (overwrites historical data)

**Attributes:**
- `customer_key` (INT, PRIMARY KEY): Surrogate key (auto-increment)
- `customer_id` (VARCHAR(20)): Natural key from source system
- `customer_name` (VARCHAR(100)): Full name of the customer
- `city` (VARCHAR(50)): City where customer is located
- `state` (VARCHAR(50)): State or province
- `customer_segment` (VARCHAR(20)): Customer segment classification (New, Regular, VIP, etc.)

---

## Section 2: Design Decisions

The star schema is designed with transaction line-item granularity to capture the most detailed level of sales data. This granularity enables flexible analysis - we can aggregate up to order level, customer level, product level, or time periods, but cannot drill down below the line item. This design choice supports comprehensive reporting while maintaining data integrity.

Surrogate keys are used instead of natural keys for several critical reasons. Natural keys like customer_id or product_id can change in source systems, causing referential integrity issues. Surrogate keys provide stability, improve join performance with integer-based keys, and enable handling of historical data changes through Slowly Changing Dimensions (SCD). For example, if a product's category changes, SCD Type 2 allows tracking both old and new category values while maintaining historical fact table relationships.

The star schema design inherently supports drill-down and roll-up operations through its hierarchical dimension structure. Users can roll up from daily sales to monthly, quarterly, or yearly aggregations using the date dimension. Similarly, they can drill down from category to subcategory to individual products using the product dimension. The denormalized dimension tables eliminate complex joins, making these operations fast and intuitive for business users and reporting tools.

---

## Section 3: Sample Data Flow

### Source Transaction (Operational Database)

**Order Table:**
```
order_id: 101
customer_id: C012
order_date: 2024-01-15
status: Completed
```

**Order Items Table:**
```
order_item_id: 45
order_id: 101
product_id: P001
quantity: 2
unit_price: 50000.00
subtotal: 100000.00
```

**Customer Table:**
```
customer_id: C012
first_name: John
last_name: Doe
email: john.doe@email.com
city: Mumbai
```

**Product Table:**
```
product_id: P001
product_name: Laptop
category: Electronics
price: 50000.00
```

### Transformation Process

1. **Date Dimension Lookup:**
   - Extract date: 2024-01-15
   - Lookup or create date_key: 20240115
   - Retrieve date dimension attributes

2. **Product Dimension Lookup:**
   - Natural key: P001
   - Lookup product_key: 5 (surrogate key)
   - Retrieve product dimension attributes

3. **Customer Dimension Lookup:**
   - Natural key: C012
   - Lookup customer_key: 12 (surrogate key)
   - Retrieve customer dimension attributes

### Data Warehouse Representation

**fact_sales:**
```json
{
  "date_key": 20240115,
  "product_key": 5,
  "customer_key": 12,
  "quantity_sold": 2,
  "unit_price": 50000.00,
  "discount_amount": 0.00,
  "total_amount": 100000.00
}
```

**dim_date:**
```json
{
  "date_key": 20240115,
  "full_date": "2024-01-15",
  "day_of_week": "Monday",
  "day_of_month": 15,
  "month": 1,
  "month_name": "January",
  "quarter": "Q1",
  "year": 2024,
  "is_weekend": false
}
```

**dim_product:**
```json
{
  "product_key": 5,
  "product_id": "P001",
  "product_name": "Laptop",
  "category": "Electronics",
  "subcategory": "Laptops",
  "unit_price": 50000.00
}
```

**dim_customer:**
```json
{
  "customer_key": 12,
  "customer_id": "C012",
  "customer_name": "John Doe",
  "city": "Mumbai",
  "state": "Maharashtra",
  "customer_segment": "Regular"
}
```

### Analysis Capabilities

With this star schema structure, analysts can now perform:

- **Time-based Analysis:** "Total sales in Q1 2024" by joining fact_sales with dim_date where quarter = 'Q1' and year = 2024
- **Product Analysis:** "Sales by product category" by joining fact_sales with dim_product and grouping by category
- **Customer Analysis:** "Sales by customer city" by joining fact_sales with dim_customer and grouping by city
- **Multi-dimensional Analysis:** "Sales of Electronics products in Mumbai during Q1 2024" by joining all three dimensions

The star schema enables fast, intuitive queries without complex joins between multiple normalized tables, making it ideal for business intelligence and reporting applications.
