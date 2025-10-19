from pymongo import MongoClient
from datetime import datetime

# reference: https://www.mongodb.com/docs/manual/reference/mql/query-predicates/

client = MongoClient("mongodb://localhost:27017")
db = client["shop"]
orders = db["orders"]

sample = [
    {
        "customer": "Ada",  "status": "COMPLETE",
        "total": 42.50,
        "items": [
            {"sku": "A1", "qty": 2, "price": 15.00},
            {"sku": "A2", "qty": 1, "price": 12.50}
        ],
        "created": datetime(2024, 5, 1, 9, 30)
    },
    {
        "customer": "Ben",  "status": "PENDING",
        "total": 19.99,
        "items": [
            {"sku": "B1", "qty": 1, "price": 19.99}
        ],
        "created": datetime(2024, 5, 2, 14, 00)
    },
    {
        "customer": "Cara", "status": "COMPLETE",
        "total": 105.00,
        "items": [
            {"sku": "C1", "qty": 1, "price": 75.00},
            {"sku": "C2", "qty": 3, "price": 10.00}
        ],
        "created": datetime(2024, 5, 3, 11, 45)
    },
    {
        "customer": "Dan",
        "status": "CANCELLED",
        "total": 5.99,
        "items": [
            {"sku": "D1", "qty": 1, "price": 5.99}
        ],
        "created": datetime(2024, 5, 4, 8, 15)},
    {
        "customer": "Eve",
        "status": "COMPLETE",
        "total": 999.00,
        "items": [
            {"sku": "E1", "qty": 1, "price": 999.00}
        ],
        "created": datetime(2024, 5, 5, 16, 20),
        "shipped": True
    }
]

# add documents to the orders collection
# orders.insert_many(sample)
# print("Inserted", len(sample), "orders")

# find order that are greater than $100
# use the $gt query predicate
docs = orders.find({"total": {"$eq": 999}})
# for doc in docs:
#     print(f"Order: {doc}")

# Find orders that have "C" in the SKU using the $in predicate
# hint the field match should be items.sku
print("orders with A1 or C1")
docs = orders.find({"items.sku": {"$in": ["A1", "C1"]}})
# for doc in docs:
#     print(f"Order: {doc}")

# Filter a date range - $gte greater than, $lte less than
# find orders that are greater than start and less than end
#print("\nOrders placed May 2-4:")
start = datetime(2024, 5, 2)
end   = datetime(2024, 5, 4, 23, 59)
docs = orders.find({"created": {"$gte": start, "$lte": end}})
# for doc in docs:
#     print(f"Order: {doc}")

# Get orders that have a certain field {"$exists": True}
# find orders with the "shipped" field
#print("\nOrders that have been shipped")
docs = orders.find({"shipped": {"$exists": True}})
for doc in docs:
    print(f"Order: {doc}")

# Use regex to search fields $regex
# find customer names that start with A or B
# hint regex match should be "^[AB]"
# print("Customers that start with A or B")

# Find Ada's order
# add {"sku": "A5", "qty": 1, "price": 2.00} to the items list
# add 2.00 to the total price
# use orders.update_one(filter={}, update={$push:{}, $inc: {}})

ada_new = orders.find_one({"customer": "Ada"})
# print("Shipped orders:")
# print(ada_new)

# create an index on customer field
# hint orders.create_index
orders.create_index("customer")

for idx in orders.list_indexes():
    print(idx)