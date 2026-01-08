# Part 3: Data Warehouse

## Overview

This part implements a star schema data warehouse for business intelligence and analytics. It includes schema design, data loading, and analytical queries for sales analysis.

## Files

- **star_schema_design.md**: Complete star schema design documentation with entity descriptions, design decisions, and sample data flow
- **warehouse_schema.sql**: SQL script to create data warehouse tables (dim_date, dim_product, dim_customer, fact_sales)
- **warehouse_data.sql**: Sample data for all dimension and fact tables
- **analytics_queries.sql**: Analytical queries for business intelligence

## Setup

1. Create data warehouse database:
```bash
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"
```

2. Create schema:
```bash
mysql -u root -p fleximart_dw < warehouse_schema.sql
```

3. Load data:
```bash
mysql -u root -p fleximart_dw < warehouse_data.sql
```

4. Run analytics queries:
```bash
mysql -u root -p fleximart_dw < analytics_queries.sql
```

## Star Schema Design

### Fact Table
- **fact_sales**: Transaction line-item level grain with measures (quantity_sold, unit_price, discount_amount, total_amount)

### Dimension Tables
- **dim_date**: Time dimension for temporal analysis
- **dim_product**: Product dimension with category and subcategory
- **dim_customer**: Customer dimension with geographic and segment information

## Analytics Queries

1. **Monthly Sales Drill-Down**: Year → Quarter → Month analysis
2. **Top 10 Products by Revenue**: Product performance with revenue percentage
3. **Customer Segmentation**: High/Medium/Low value customer analysis

## Key Features

- **Drill-Down Capabilities**: Time-based analysis from year to month
- **Product Performance**: Revenue analysis with percentage contributions
- **Customer Segmentation**: Value-based customer classification
- **Star Schema Benefits**: Fast queries with denormalized dimensions
