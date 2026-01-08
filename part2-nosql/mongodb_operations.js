// ============================================================================
// MongoDB Operations - FlexiMart Product Catalog
// ============================================================================
// This file contains MongoDB operations for managing product catalog data
// Database: fleximart
// Collection: products
// ============================================================================

// Connect to MongoDB
// Usage: mongosh < mongodb_operations.js
// Or: use fleximart; then run each operation

// ============================================================================
// Operation 1: Load Data
// Import the provided JSON file into collection 'products'
// ============================================================================

// Switch to fleximart database
use('fleximart');

// Clear existing collection (optional - remove if you want to append)
db.products.deleteMany({});

// Method 1: Using mongoimport command (Recommended - run from terminal)
// Navigate to the part2-nosql directory and run:
// mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray

// Method 2: Using MongoDB shell with load() function
// First, navigate to the directory containing products_catalog.json, then:
// load("products_catalog.json")
// Then run: db.products.insertMany(products)

// Method 3: Using Node.js script (if using MongoDB Node.js driver)
/*
const fs = require('fs');
const { MongoClient } = require('mongodb');

async function loadData() {
    const client = new MongoClient('mongodb://localhost:27017');
    await client.connect();
    const db = client.db('fleximart');
    const collection = db.collection('products');
    
    const data = JSON.parse(fs.readFileSync('products_catalog.json', 'utf8'));
    await collection.insertMany(data);
    
    console.log(`Loaded ${data.length} products into collection`);
    await client.close();
}

loadData();
*/

// Note: For direct execution in MongoDB shell, use mongoimport command (Method 1)
// The JSON file structure includes: product_id, name, category, subcategory, price, stock,
// specifications (object), reviews (array with user_id, username, rating, comment, date),
// tags (array), warranty_months, created_at, updated_at
// After loading data using mongoimport, verify the data was loaded:
print("Data loaded successfully!");
print(`Total products: ${db.products.countDocuments()}`);

// ============================================================================
// Operation 2: Basic Query
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
// ============================================================================

db.products.find(
    {
        category: "Electronics",
        price: { $lt: 50000 }
    },
    {
        _id: 0,
        name: 1,
        price: 1,
        stock: 1
    }
).pretty();

// Alternative: Using projection with explicit field names
/*
db.products.find(
    { category: "Electronics", price: { $lt: 50000 } },
    { _id: 0, name: 1, price: 1, stock: 1 }
).forEach(product => {
    print(`Name: ${product.name}, Price: ${product.price}, Stock: ${product.stock}`);
});
*/

// ============================================================================
// Operation 3: Review Analysis
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array
// ============================================================================

db.products.aggregate([
    // Unwind reviews array to work with individual reviews
    {
        $unwind: {
            path: "$reviews",
            preserveNullAndEmptyArrays: false
        }
    },
    // Group by product and calculate average rating
    {
        $group: {
            _id: "$product_id",
            name: { $first: "$name" },
            category: { $first: "$category" },
            avg_rating: { $avg: "$reviews.rating" },
            review_count: { $sum: 1 }
        }
    },
    // Filter products with average rating >= 4.0
    {
        $match: {
            avg_rating: { $gte: 4.0 }
        }
    },
    // Project final output
    {
        $project: {
            _id: 0,
            product_id: "$_id",
            name: 1,
            category: 1,
            avg_rating: { $round: ["$avg_rating", 2] },
            review_count: 1
        }
    },
    // Sort by average rating descending
    {
        $sort: { avg_rating: -1 }
    }
]).pretty();

// ============================================================================
// Operation 4: Update Operation
// Add a new review to product "ELEC001"
// Review: {user_id: "U999", username: "NewUser", rating: 4, comment: "Good value", date: ISODate()}
// Note: The JSON file uses user_id and username fields in reviews
// ============================================================================

db.products.updateOne(
    { product_id: "ELEC001" },
    {
        $push: {
            reviews: {
                user_id: "U999",
                username: "NewUser",
                rating: 4,
                comment: "Good value",
                date: new Date()  // ISODate() in MongoDB shell, new Date() in Node.js
            }
        }
    }
);

// Verify the update
db.products.findOne(
    { product_id: "ELEC001" },
    { _id: 0, product_id: 1, name: 1, reviews: 1 }
).pretty();

// ============================================================================
// Operation 5: Complex Aggregation
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending
// ============================================================================

db.products.aggregate([
    // Group by category and calculate statistics
    {
        $group: {
            _id: "$category",
            avg_price: { $avg: "$price" },
            product_count: { $sum: 1 },
            // Optional: include min and max prices for additional insights
            min_price: { $min: "$price" },
            max_price: { $max: "$price" }
        }
    },
    // Project final output with rounded average price
    {
        $project: {
            _id: 0,
            category: "$_id",
            avg_price: { $round: ["$avg_price", 2] },
            product_count: 1,
            min_price: 1,
            max_price: 1
        }
    },
    // Sort by average price descending
    {
        $sort: { avg_price: -1 }
    }
]).pretty();

// ============================================================================
// Additional Helper Queries (Optional)
// ============================================================================

// Count total products
// db.products.countDocuments();

// Find all categories
// db.products.distinct("category");

// Find products with no reviews
// db.products.find({ reviews: { $size: 0 } }).pretty();

// Find products with stock less than 100
// db.products.find({ stock: { $lt: 100 } }, { _id: 0, product_id: 1, name: 1, stock: 1 }).pretty();
