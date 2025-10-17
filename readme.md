# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name:** [TODO: Add Your Name Here]

## Lab 1: Flat-File Persistence

This lab focuses on building the foundational persistence layer using a simple flat-file (JSON) system. The goal is to establish a performance baseline for file I/O operations, which will serve as a benchmark for subsequent labs involving more advanced database technologies.

## Question 1: Performance Analysis (5 points)
Run performance_test.py and record the results. What did you observe about:
    - How append times changed as the number of messages grew for flat files vs MongoDB?
    - The difference in read times for retrieving the full conversation?
Explain why you see these performance characteristics.

## Question 2: Atomic Operations (5 points)
In MongoDBManager, we use the $push operator in append_message(). Research what "atomic operations" means in the context of databases. Why is this important for a chat application where multiple messages might be added rapidly?

## Question 3: Scalability (5 points)
Imagine your chat application goes viral and now has 1 million users, each with an average of 10 conversation threads containing 500 messages each.
Compare how FlatFileManager and MongoDBManager would handle:
    - Finding all threads for a specific user
    - Loading a specific conversation
    - Storage organization and file system limits

## Question 4: Data Modeling Design Challenge (5 points)
Currently, each conversation is stored as a single document with an embedded array of messages:
{
  "_id": "user_123_work",
  "messages": [...]
}
An alternative design would be to store each message as its own document:
{
  "_id": "msg_001",
  "conversation_id": "user_123_work",
  "role": "user",
  "content": "Hello!",
  "timestamp": "..."
}
Describe:
    1. One advantage of the embedded messages design (what we currently use)
    2. One advantage of the separate message documents design
    3. A scenario where you would choose the separate messages design instead