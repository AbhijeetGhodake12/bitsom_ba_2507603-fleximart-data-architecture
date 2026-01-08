# NoSQL Justification Report - FlexiMart Product Catalog

## Section A: Limitations of RDBMS (150 words)

Relational databases struggle with diverse product catalogs where **different product types require different attributes**. Laptops need RAM and processor specifications, while shoes require size and color. A rigid schema forces sparse tables with many NULL values or separate tables per product type, leading to complex joins and inefficient queries. This design becomes unwieldy as product diversity increases.

**Frequent schema changes** become problematic when adding new product categories. Altering table structures requires downtime, migration scripts, and can break existing applications. For an e-commerce platform constantly expanding inventory, this rigidity creates operational bottlenecks and slows time-to-market for new product lines.

**Storing nested data like customer reviews** is challenging. Reviews contain ratings, text, timestamps, and user information - a natural hierarchical structure. RDBMS requires normalization across multiple tables (products, reviews, customers) with foreign keys, making simple operations like "show product with all reviews" require complex joins. This increases query complexity, reduces performance, and makes the data model less intuitive for developers working with inherently nested business data.

---

## Section B: NoSQL Benefits (150 words)

MongoDB's **flexible document schema** elegantly solves attribute variation problems. Each product document can have different fields - a laptop document includes `ram`, `processor`, and `storage`, while a shoe document contains `size`, `color`, and `material`. No schema migration is needed when adding new product types; simply insert documents with the required attributes. This flexibility accelerates development and accommodates rapid catalog expansion without database restructuring.

**Embedded documents** enable storing reviews directly within product documents as arrays. A product document can contain a `reviews` array where each review is a nested document with rating, comment, date, and customer information. This eliminates joins, improves read performance for "product with reviews" queries, and matches the natural data structure. Related data stays together, making the model intuitive and efficient.

**Horizontal scalability** allows MongoDB to distribute data across multiple servers (sharding) as the catalog grows. Unlike MySQL's vertical scaling limitations, MongoDB can handle massive product catalogs by adding commodity servers, providing linear performance improvements and cost-effective growth for large-scale e-commerce platforms.

---

## Section C: Trade-offs (100 words)

**Loss of ACID Transactions:** MongoDB's document-level transactions are weaker than MySQL's row-level ACID guarantees. Complex operations spanning multiple documents (like updating inventory and creating orders simultaneously) lack the same transactional integrity, potentially leading to data inconsistencies in high-concurrency scenarios. This makes MongoDB less suitable for financial transactions requiring strict consistency.

**No Standardized Query Language:** While MongoDB's query language is powerful, it lacks SQL's universal standardization. Teams familiar with SQL face a learning curve, and existing SQL-based tools and reporting systems cannot directly query MongoDB. This increases training costs and requires additional middleware for business intelligence and analytics integration, adding complexity to the technology stack.

---

## Summary

While MySQL excels at structured, transactional data with fixed schemas, MongoDB's flexibility makes it superior for diverse product catalogs with varying attributes, frequent schema evolution, and nested data structures. The choice depends on prioritizing data consistency and SQL compatibility versus schema flexibility and scalability.
