-- ============================================================================
-- Analytics Queries - FlexiMart Data Warehouse
-- Database: fleximart_dw
-- ============================================================================

-- Query 1: Monthly Sales Drill-Down Analysis
-- Business Scenario: "The CEO wants to see sales performance broken down by 
-- time periods. Start with yearly total, then quarterly, then monthly sales 
-- for 2024."
-- Demonstrates: Drill-down from Year to Quarter to Month

SELECT
    d.year,
    d.quarter,
    d.month_name,
    SUM(fs.total_amount) AS total_sales,
    SUM(fs.quantity_sold) AS total_quantity
FROM
    fact_sales fs
    INNER JOIN dim_date d ON fs.date_key = d.date_key
WHERE
    d.year = 2024
GROUP BY
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY
    d.year ASC,
    d.quarter ASC,
    d.month ASC;

-- ============================================================================

-- Query 2: Top 10 Products by Revenue
-- Business Scenario: "The product manager needs to identify top-performing 
-- products. Show the top 10 products by revenue, along with their category, 
-- total units sold, and revenue contribution percentage."
-- Includes: Revenue percentage calculation

SELECT
    p.product_name,
    p.category,
    SUM(fs.quantity_sold) AS units_sold,
    SUM(fs.total_amount) AS revenue,
    ROUND(
        (SUM(fs.total_amount) * 100.0 / 
         (SELECT SUM(total_amount) FROM fact_sales)), 
        2
    ) AS revenue_percentage
FROM
    fact_sales fs
    INNER JOIN dim_product p ON fs.product_key = p.product_key
GROUP BY
    p.product_key,
    p.product_name,
    p.category
ORDER BY
    revenue DESC
LIMIT 10;


-- ============================================================================

-- Query 3: Customer Segmentation Analysis
-- Business Scenario: "Marketing wants to target high-value customers. 
-- Segment customers into 'High Value' (>₹50,000 spent), 'Medium Value' 
-- (₹20,000-₹50,000), and 'Low Value' (<₹20,000). Show count of customers 
-- and total revenue in each segment."
-- Segments: High/Medium/Low value customers

SELECT
    CASE
        WHEN customer_total_spending > 50000 THEN 'High Value'
        WHEN customer_total_spending >= 20000 AND customer_total_spending <= 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*) AS customer_count,
    SUM(customer_total_spending) AS total_revenue,
    ROUND(AVG(customer_total_spending), 2) AS avg_revenue
FROM (
    SELECT
        c.customer_key,
        c.customer_name,
        SUM(fs.total_amount) AS customer_total_spending
    FROM
        fact_sales fs
        INNER JOIN dim_customer c ON fs.customer_key = c.customer_key
    GROUP BY
        c.customer_key,
        c.customer_name
) AS customer_spending
GROUP BY
    CASE
        WHEN customer_total_spending > 50000 THEN 'High Value'
        WHEN customer_total_spending >= 20000 AND customer_total_spending <= 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END
ORDER BY
    CASE
        WHEN customer_segment = 'High Value' THEN 1
        WHEN customer_segment = 'Medium Value' THEN 2
        WHEN customer_segment = 'Low Value' THEN 3
    END;
