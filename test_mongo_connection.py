import os
from pymongo import MongoClient

# Update this connection string for your MongoDB setup
# For local: "mongodb://localhost:27017/"

connection_string = "mongodb://localhost:27017/"

try:
    client = MongoClient(connection_string)
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    client.close()
except Exception as e:
    print(f"Failed to connect: {e}")