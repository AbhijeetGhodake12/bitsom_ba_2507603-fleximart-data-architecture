-- Warehouse Data - FlexiMart Data Warehouse
-- Database: fleximart_dw

-- ============================================================================
-- DIM_DATE: 30 dates (January-February 2024)
-- ============================================================================

INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, false),
(20240102, '2024-01-02', 'Tuesday', 2, 1, 'January', 'Q1', 2024, false),
(20240103, '2024-01-03', 'Wednesday', 3, 1, 'January', 'Q1', 2024, false),
(20240104, '2024-01-04', 'Thursday', 4, 1, 'January', 'Q1', 2024, false),
(20240105, '2024-01-05', 'Friday', 5, 1, 'January', 'Q1', 2024, false),
(20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, true),
(20240107, '2024-01-07', 'Sunday', 7, 1, 'January', 'Q1', 2024, true),
(20240108, '2024-01-08', 'Monday', 8, 1, 'January', 'Q1', 2024, false),
(20240109, '2024-01-09', 'Tuesday', 9, 1, 'January', 'Q1', 2024, false),
(20240110, '2024-01-10', 'Wednesday', 10, 1, 'January', 'Q1', 2024, false),
(20240111, '2024-01-11', 'Thursday', 11, 1, 'January', 'Q1', 2024, false),
(20240112, '2024-01-12', 'Friday', 12, 1, 'January', 'Q1', 2024, false),
(20240113, '2024-01-13', 'Saturday', 13, 1, 'January', 'Q1', 2024, true),
(20240114, '2024-01-14', 'Sunday', 14, 1, 'January', 'Q1', 2024, true),
(20240115, '2024-01-15', 'Monday', 15, 1, 'January', 'Q1', 2024, false),
(20240116, '2024-01-16', 'Tuesday', 16, 1, 'January', 'Q1', 2024, false),
(20240117, '2024-01-17', 'Wednesday', 17, 1, 'January', 'Q1', 2024, false),
(20240118, '2024-01-18', 'Thursday', 18, 1, 'January', 'Q1', 2024, false),
(20240119, '2024-01-19', 'Friday', 19, 1, 'January', 'Q1', 2024, false),
(20240120, '2024-01-20', 'Saturday', 20, 1, 'January', 'Q1', 2024, true),
(20240121, '2024-01-21', 'Sunday', 21, 1, 'January', 'Q1', 2024, true),
(20240122, '2024-01-22', 'Monday', 22, 1, 'January', 'Q1', 2024, false),
(20240123, '2024-01-23', 'Tuesday', 23, 1, 'January', 'Q1', 2024, false),
(20240124, '2024-01-24', 'Wednesday', 24, 1, 'January', 'Q1', 2024, false),
(20240125, '2024-01-25', 'Thursday', 25, 1, 'January', 'Q1', 2024, false),
(20240126, '2024-01-26', 'Friday', 26, 1, 'January', 'Q1', 2024, false),
(20240127, '2024-01-27', 'Saturday', 27, 1, 'January', 'Q1', 2024, true),
(20240128, '2024-01-28', 'Sunday', 28, 1, 'January', 'Q1', 2024, true),
(20240201, '2024-02-01', 'Thursday', 1, 2, 'February', 'Q1', 2024, false),
(20240202, '2024-02-02', 'Friday', 2, 2, 'February', 'Q1', 2024, false);

-- ============================================================================
-- DIM_PRODUCT: 15 products across 3 categories
-- ============================================================================

INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('P001', 'Samsung Galaxy S21', 'Electronics', 'Smartphones', 45999.00),
('P002', 'Apple MacBook Pro', 'Electronics', 'Laptops', 189999.00),
('P003', 'Sony WH-1000XM5', 'Electronics', 'Audio', 29990.00),
('P004', 'Dell 27-inch Monitor', 'Electronics', 'Monitors', 32999.00),
('P005', 'OnePlus Nord CE 3', 'Electronics', 'Smartphones', 26999.00),
('P006', 'Nike Air Max 270', 'Fashion', 'Footwear', 12995.00),
('P007', 'Levi\'s 511 Jeans', 'Fashion', 'Clothing', 3499.00),
('P008', 'Adidas Originals T-Shirt', 'Fashion', 'Clothing', 1499.00),
('P009', 'Puma RS-X Sneakers', 'Fashion', 'Footwear', 8999.00),
('P010', 'H&M Formal Shirt', 'Fashion', 'Clothing', 1999.00),
('P011', 'Basmati Rice 5kg', 'Groceries', 'Food', 650.00),
('P012', 'Organic Almonds 500g', 'Groceries', 'Food', 899.00),
('P013', 'Organic Honey 500g', 'Groceries', 'Food', 450.00),
('P014', 'Masoor Dal 1kg', 'Groceries', 'Food', 120.00),
('P015', 'Olive Oil 1L', 'Groceries', 'Food', 599.00);

-- ============================================================================
-- DIM_CUSTOMER: 12 customers across 4 cities
-- ============================================================================

INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001', 'Rahul Sharma', 'Mumbai', 'Maharashtra', 'Regular'),
('C002', 'Priya Patel', 'Mumbai', 'Maharashtra', 'VIP'),
('C003', 'Amit Kumar', 'Delhi', 'Delhi', 'Regular'),
('C004', 'Sneha Reddy', 'Hyderabad', 'Telangana', 'New'),
('C005', 'Vikram Singh', 'Chennai', 'Tamil Nadu', 'Regular'),
('C006', 'Anjali Mehta', 'Mumbai', 'Maharashtra', 'VIP'),
('C007', 'Ravi Verma', 'Delhi', 'Delhi', 'Regular'),
('C008', 'Pooja Iyer', 'Chennai', 'Tamil Nadu', 'New'),
('C009', 'Karthik Nair', 'Hyderabad', 'Telangana', 'Regular'),
('C010', 'Deepa Gupta', 'Delhi', 'Delhi', 'VIP'),
('C011', 'Arjun Rao', 'Hyderabad', 'Telangana', 'Regular'),
('C012', 'Lakshmi Krishnan', 'Chennai', 'Tamil Nadu', 'New');

-- ============================================================================
-- FACT_SALES: 40 sales transactions
-- ============================================================================

INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- January 2024 - Weekdays (lower volume)
(20240101, 1, 1, 1, 45999.00, 0.00, 45999.00),
(20240102, 6, 2, 1, 12995.00, 500.00, 12495.00),
(20240103, 11, 3, 3, 650.00, 0.00, 1950.00),
(20240104, 2, 4, 1, 189999.00, 5000.00, 184999.00),
(20240105, 7, 5, 2, 3499.00, 0.00, 6998.00),
(20240108, 3, 6, 1, 29990.00, 1000.00, 28990.00),
(20240109, 12, 7, 5, 899.00, 0.00, 4495.00),
(20240110, 8, 8, 3, 1499.00, 0.00, 4497.00),
(20240111, 4, 9, 1, 32999.00, 0.00, 32999.00),
(20240112, 13, 10, 10, 450.00, 0.00, 4500.00),
(20240115, 5, 11, 1, 26999.00, 0.00, 26999.00),
(20240116, 9, 12, 1, 8999.00, 500.00, 8499.00),
(20240117, 14, 1, 8, 120.00, 0.00, 960.00),
(20240118, 10, 2, 2, 1999.00, 0.00, 3998.00),
(20240119, 15, 3, 2, 599.00, 0.00, 1198.00),
(20240122, 1, 4, 1, 45999.00, 2000.00, 43999.00),
(20240123, 6, 5, 2, 12995.00, 0.00, 25990.00),
(20240124, 11, 6, 5, 650.00, 0.00, 3250.00),
(20240125, 7, 7, 1, 3499.00, 0.00, 3499.00),
(20240126, 3, 8, 1, 29990.00, 0.00, 29990.00),
-- January 2024 - Weekends (higher volume)
(20240106, 2, 9, 1, 189999.00, 10000.00, 179999.00),
(20240106, 6, 10, 1, 12995.00, 0.00, 12995.00),
(20240107, 8, 11, 4, 1499.00, 0.00, 5996.00),
(20240107, 12, 12, 3, 899.00, 0.00, 2697.00),
(20240113, 1, 1, 1, 45999.00, 0.00, 45999.00),
(20240113, 9, 2, 2, 8999.00, 1000.00, 16998.00),
(20240114, 4, 3, 1, 32999.00, 0.00, 32999.00),
(20240114, 10, 4, 3, 1999.00, 0.00, 5997.00),
(20240120, 5, 5, 1, 26999.00, 0.00, 26999.00),
(20240120, 7, 6, 2, 3499.00, 500.00, 6498.00),
(20240121, 11, 7, 4, 650.00, 0.00, 2600.00),
(20240121, 13, 8, 6, 450.00, 0.00, 2700.00),
(20240127, 2, 9, 1, 189999.00, 0.00, 189999.00),
(20240127, 6, 10, 1, 12995.00, 0.00, 12995.00),
(20240128, 8, 11, 2, 1499.00, 0.00, 2998.00),
(20240128, 15, 12, 3, 599.00, 0.00, 1797.00),
-- February 2024
(20240201, 1, 1, 1, 45999.00, 0.00, 45999.00),
(20240201, 3, 2, 1, 29990.00, 0.00, 29990.00),
(20240202, 4, 3, 1, 32999.00, 1500.00, 31499.00),
(20240202, 9, 4, 1, 8999.00, 0.00, 8999.00);
