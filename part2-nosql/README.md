# Part 2: NoSQL Implementation

## Overview

This part demonstrates the use of MongoDB for managing a flexible product catalog with varying attributes. It includes analysis of RDBMS limitations, NoSQL benefits, and practical MongoDB operations.

## Files

- **nosql_analysis.md**: Analysis document explaining RDBMS limitations, NoSQL benefits, and trade-offs
- **mongodb_operations.js**: MongoDB operations including data loading, queries, aggregations, and updates
- **products_catalog.json**: Sample product catalog data with nested reviews

## Setup

1. Ensure MongoDB is installed and running:
```bash
mongod
```

2. Import product catalog:
```bash
cd part2-nosql
mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray
```

3. Run MongoDB operations:
```bash
mongosh < mongodb_operations.js
```

Or connect to MongoDB shell and run operations manually:
```bash
mongosh
use fleximart
```

## Key Features

- **Flexible Schema**: Products with different attributes (Electronics vs Fashion)
- **Embedded Documents**: Customer reviews stored within product documents
- **Aggregation Queries**: Product performance analysis with average ratings
- **Update Operations**: Adding new reviews to products
- **Category Analysis**: Revenue analysis by product category

## Operations Included

1. **Load Data**: Import JSON file into MongoDB collection
2. **Basic Query**: Find products by category and price range
3. **Review Analysis**: Find products with average rating >= 4.0 using aggregation
4. **Update Operation**: Add new reviews to products
5. **Complex Aggregation**: Calculate average price by category
