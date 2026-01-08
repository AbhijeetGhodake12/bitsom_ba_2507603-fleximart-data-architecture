# Part 1: Database ETL Pipeline

## Overview

This part implements a complete ETL (Extract, Transform, Load) pipeline for processing raw customer, product, and sales data. The pipeline handles data quality issues, standardizes formats, and loads cleaned data into a MySQL database.

## Files

- **etl_pipeline.py**: Main ETL pipeline implementation with Extract, Transform, and Load phases
- **schema_documentation.md**: Complete database schema documentation with entity descriptions and normalization explanation
- **business_queries.sql**: SQL queries for business intelligence (customer purchase history, product sales analysis, monthly sales trends)
- **requirements.txt**: Python dependencies
- **data_quality_report.txt**: Generated report documenting data quality issues and transformations

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the ETL pipeline (without database loading):
```bash
python etl_pipeline.py
```

3. To load data into MySQL, use the `--load-db` flag:
```bash
# Option 1: Prompt for password
python etl_pipeline.py --load-db

# Option 2: Provide password via command line
python etl_pipeline.py --load-db --password your_mysql_password

# Option 3: Use environment variable
export MYSQL_PASSWORD=your_mysql_password
python etl_pipeline.py --load-db

# Option 4: Custom database configuration
python etl_pipeline.py --load-db --host localhost --user root --database fleximart --password your_password
```

4. Additional options:
```bash
# Skip saving cleaned CSV files
python etl_pipeline.py --no-save

# Combine options
python etl_pipeline.py --load-db --password your_password --no-save
```

## Key Features

- **Data Quality Improvements**: Removes duplicates, handles missing values, standardizes formats
- **Phone Number Standardization**: Converts various formats to +91-XXXXXXXXXX
- **Date Standardization**: Normalizes dates to YYYY-MM-DD format
- **Category Standardization**: Converts category names to Title Case
- **Surrogate Key Generation**: Adds auto-incrementing IDs
- **MySQL Integration**: Creates database and tables, loads cleaned data

## Database Schema

The pipeline creates the following tables in the `fleximart` database:
- `customers`: Customer information
- `products`: Product catalog
- `orders`: Order headers
- `order_items`: Order line items

See `schema_documentation.md` for detailed schema documentation.
