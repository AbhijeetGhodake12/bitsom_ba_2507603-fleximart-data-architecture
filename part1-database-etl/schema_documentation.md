# Database Schema Documentation - FlexiMart

## Entity-Relationship Description (Text Format)

### ENTITY: customers

**Purpose:** Stores customer information and personal details for the e-commerce platform.

**Attributes:**
- `customer_id` (INT, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each customer. Automatically generated sequential integer.
- `first_name` (VARCHAR(50), NOT NULL): Customer's first name. Required field.
- `last_name` (VARCHAR(50), NOT NULL): Customer's last name. Required field.
- `email` (VARCHAR(100), UNIQUE, NOT NULL): Customer's email address. Must be unique across all customers and is required for account identification.
- `phone` (VARCHAR(20)): Customer's contact phone number. Optional field, stored in standardized format (+91-XXXXXXXXXX).
- `city` (VARCHAR(50)): City where the customer is located. Optional field for demographic analysis.
- `registration_date` (DATE): Date when the customer registered on the platform. Used for customer lifecycle analysis.

**Relationships:**
- One customer can place MANY orders (1:M relationship with orders table)
- The relationship is enforced through the `customer_id` foreign key in the orders table

---

### ENTITY: products

**Purpose:** Stores product catalog information including pricing and inventory details.

**Attributes:**
- `product_id` (INT, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each product. Automatically generated sequential integer.
- `product_name` (VARCHAR(100), NOT NULL): Name of the product. Required field for product identification.
- `category` (VARCHAR(50), NOT NULL): Product category classification (e.g., Electronics, Fashion, Groceries). Required field, standardized to Title Case.
- `price` (DECIMAL(10,2), NOT NULL): Product unit price in currency. Required field, stored with 2 decimal precision.
- `stock_quantity` (INT, DEFAULT 0): Current inventory quantity available. Defaults to 0 if not specified.

**Relationships:**
- One product can appear in MANY order items (1:M relationship with order_items table)
- The relationship is enforced through the `product_id` foreign key in the order_items table

---

### ENTITY: orders

**Purpose:** Stores order header information representing a customer's purchase transaction on a specific date.

**Attributes:**
- `order_id` (INT, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each order. Automatically generated sequential integer.
- `customer_id` (INT, NOT NULL, FOREIGN KEY): Reference to the customer who placed the order. Links to customers table.
- `order_date` (DATE, NOT NULL): Date when the order was placed. Required field for order tracking and reporting.
- `total_amount` (DECIMAL(10,2), NOT NULL): Total monetary value of the order. Calculated as sum of all order items' subtotals.
- `status` (VARCHAR(20), DEFAULT 'Pending'): Current status of the order (e.g., Pending, Completed, Cancelled). Defaults to 'Pending' if not specified.

**Relationships:**
- One order belongs to ONE customer (M:1 relationship with customers table)
- One order can contain MANY order items (1:M relationship with order_items table)
- Foreign key constraint ensures referential integrity with customers table

---

### ENTITY: order_items

**Purpose:** Stores individual line items within an order, representing each product purchased and its details.

**Attributes:**
- `order_item_id` (INT, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each order item. Automatically generated sequential integer.
- `order_id` (INT, NOT NULL, FOREIGN KEY): Reference to the parent order. Links to orders table.
- `product_id` (INT, NOT NULL, FOREIGN KEY): Reference to the product being ordered. Links to products table.
- `quantity` (INT, NOT NULL): Number of units of the product ordered. Must be a positive integer.
- `unit_price` (DECIMAL(10,2), NOT NULL): Price per unit at the time of order. Stored to maintain historical pricing accuracy.
- `subtotal` (DECIMAL(10,2), NOT NULL): Calculated value (quantity × unit_price) for this line item. Stored for performance and audit purposes.

**Relationships:**
- One order item belongs to ONE order (M:1 relationship with orders table)
- One order item references ONE product (M:1 relationship with products table)
- Foreign key constraints ensure referential integrity with both orders and products tables

---

## Normalization Explanation

### Third Normal Form (3NF) Justification

The FlexiMart database schema is designed in Third Normal Form (3NF), which requires that the database be in Second Normal Form (2NF) and that all non-key attributes are non-transitively dependent on the primary key. This design eliminates data redundancy and prevents update, insert, and delete anomalies.

**Functional Dependencies Identified:**

1. **customers table:** `customer_id → {first_name, last_name, email, phone, city, registration_date}`
   - All attributes are directly dependent on the primary key `customer_id`
   - No transitive dependencies exist

2. **products table:** `product_id → {product_name, category, price, stock_quantity}`
   - All attributes are directly dependent on the primary key `product_id`
   - No transitive dependencies exist

3. **orders table:** `order_id → {customer_id, order_date, total_amount, status}`
   - All attributes are directly dependent on the primary key `order_id`
   - `customer_id` is a foreign key, not a transitive dependency

4. **order_items table:** `order_item_id → {order_id, product_id, quantity, unit_price, subtotal}`
   - All attributes are directly dependent on the primary key `order_item_id`
   - `order_id` and `product_id` are foreign keys, not transitive dependencies
   - `subtotal` is calculated from `quantity` and `unit_price`, but stored for performance

**Anomaly Prevention:**

- **Update Anomalies Avoided:** Product information (name, category, price) is stored only in the products table. If a product's price changes, it only needs to be updated in one place. Historical order prices are preserved in order_items through the `unit_price` field.

- **Insert Anomalies Avoided:** New products can be added without requiring an order. New customers can be registered without placing orders. The normalized structure allows independent insertion of entities.

- **Delete Anomalies Avoided:** Deleting an order does not delete customer or product information due to proper foreign key constraints with appropriate referential actions. Customer and product data remain intact even if all related orders are removed.

The separation of orders and order_items into two tables (normalization) prevents storing redundant customer and product information with each transaction, while maintaining data integrity through foreign key relationships.

---

## Sample Data Representation

### customers Table

| customer_id | first_name | last_name | email | phone | city | registration_date |
|-------------|------------|-----------|-------|-------|------|-------------------|
| 1 | Rahul | Sharma | rahul.sharma@gmail.com | +91-9876543210 | Bangalore | 2023-01-15 |
| 2 | Priya | Patel | priya.patel@yahoo.com | +91-9988776655 | Mumbai | 2023-02-20 |
| 3 | Amit | Kumar | amit.kumar@unknown.com | +91-9765432109 | Delhi | 2023-03-10 |

### products Table

| product_id | product_name | category | price | stock_quantity |
|------------|---------------|----------|-------|----------------|
| 1 | Samsung Galaxy S21 | Electronics | 45999.00 | 150 |
| 2 | Nike Running Shoes | Fashion | 3499.00 | 80 |
| 3 | Apple MacBook Pro | Electronics | 32999.00 | 45 |

### orders Table

| order_id | customer_id | order_date | total_amount | status |
|----------|-------------|------------|--------------|--------|
| 1 | 1 | 2024-01-15 | 45999.00 | Completed |
| 2 | 2 | 2024-01-16 | 5998.00 | Completed |
| 3 | 3 | 2024-01-15 | 52999.00 | Completed |

### order_items Table

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|---------------|----------|-------------|----------|------------|----------|
| 1 | 1 | 1 | 1 | 45999.00 | 45999.00 |
| 2 | 2 | 4 | 2 | 2999.00 | 5998.00 |
| 3 | 3 | 7 | 1 | 52999.00 | 52999.00 |

---

## Relationship Summary

```
customers (1) ────────< (M) orders
                              │
                              │ (1)
                              │
                              │
                              └───────< (M) order_items
                                        │
                                        │ (M)
                                        │
products (1) ──────────────────────────┘
```

**Legend:**
- (1) = One
- (M) = Many
- ──────── = Relationship line
- < = "Many" side of relationship

---

## Notes

- All primary keys are auto-incrementing integers for efficient indexing and uniqueness
- Foreign key constraints ensure referential integrity across related tables
- The `unit_price` in order_items preserves historical pricing, independent of current product prices
- The `subtotal` field in order_items is denormalized for performance but maintains data consistency
- Email addresses are unique to prevent duplicate customer accounts
- Date fields use standard DATE format (YYYY-MM-DD) for consistency
