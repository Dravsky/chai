# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name:** Erik Woodland

## Lab 1: Flat-File Persistence

This lab focuses on building the foundational persistence layer using a simple flat-file (JSON) system. The goal is to establish a performance baseline for file I/O operations, which will serve as a benchmark for subsequent labs involving more advanced database technologies.

## Question 1: Performance Analysis (5 points)
Run performance_test.py and record the results. What did you observe about:
    - How append times changed as the number of messages grew for flat files vs MongoDB?
    - The difference in read times for retrieving the full conversation?
Explain why you see these performance characteristics.

The append times changed in that for 10 message pairs and 50 message pairs, MongoDB averaged to be about 21 times faster than the flat file management system. However, when increasing to 100 message pairs, MongoDB was slower, to aboyt 16 times faster than the flat file management system. This is because the averages for the flat file management stayed about the same, but MongoDB's average was increasing (getting slower). MongoDB is much faster here since it doesn't have to read and overwrite the whole file when appending, like the FlatFileManager does. Using $push, MongoDB just overwrites and appends the data needed. I'll be honest in that I'm not 100% sure why MongoDB slows down. My best guess has to do with it reallocating memory as more appends are made.

I feel that my performance data is a little off, since I'm running MongoDB locally on my machine. If I were using a cloud service such as Azure, it'd take much longer. However, because MongoDB is designed to be much more efficient in general, when running locally, it's faster than the basic file I/O of the flat file system manager. I believe the tests were designed with cloud services in mind, so I've decided to post my results here to corroborate what I'm saying above:

================================================================================
TEST 1: Incremental Append Performance (Simulating Real Chat Usage)
================================================================================
This simulates a user chatting in real-time, adding messages one at a time.


--- Testing with 10 message pairs ---
Flat File:
  - Avg append: 0.0140s
  - Min append: 0.0005s
  - Max append: 0.0221s
  - Full read:  0.0151s
  - Final msgs: 20
MongoDB:
  - Avg append: 0.0007s
  - Min append: 0.0004s
  - Max append: 0.0014s
  - Full read:  0.0004s
  - Final msgs: 20

✓ MongoDB is 20.53x faster for incremental appends at 10 messages

--- Testing with 50 message pairs ---
Flat File:
  - Avg append: 0.0132s
  - Min append: 0.0005s
  - Max append: 0.0191s
  - Full read:  0.0124s
  - Final msgs: 100
MongoDB:
  - Avg append: 0.0006s
  - Min append: 0.0004s
  - Max append: 0.0014s
  - Full read:  0.0005s
  - Final msgs: 100

✓ MongoDB is 21.30x faster for incremental appends at 50 messages

--- Testing with 100 message pairs ---
Flat File:
  - Avg append: 0.0135s
  - Min append: 0.0005s
  - Max append: 0.0204s
  - Full read:  0.0130s
  - Final msgs: 200
MongoDB:
  - Avg append: 0.0008s
  - Min append: 0.0004s
  - Max append: 0.0022s
  - Full read:  0.0005s
  - Final msgs: 200

✓ MongoDB is 16.19x faster for incremental appends at 100 messages

---

5. READ PERFORMANCE (Loading Conversation):
   ----------------------------------------------------------------------------
   MongoDB is 24.80x FASTER for reading full conversations
   • Flat File @ 100 msgs: 13.01ms
   • MongoDB @ 100 msgs:   0.52ms
   • Note: Both are fast; difference is network vs disk I/O

## Question 2: Atomic Operations (5 points)
In MongoDBManager, we use the $push operator in append_message(). Research what "atomic operations" means in the context of databases. Why is this important for a chat application where multiple messages might be added rapidly?

Atomic operations define an operation that cannot be interrupted, meaning no reading or writing of that operation's data until the process is complete. This is important in this use case as it's highly important that each and every message is stored properly in the database, and in the right order. When sending the conversation history to an AI model, it's highly important that not only is the data formatted right, but that it's in the right order so it can properly formulate a response. If the data is partial or incomplete, it'll result in errors. Rapid back-and-forth messaging makes this paramount, as information will be very quickly need to be stored. Keeping the operations atomic means this will happen consistently. "Atomic" operations reminds me of ACID's "atomicity" from class, meaning "all or nothing." These relate in how atomic operations will either arrive in full, or not at all (if there's some network error blocking the operation).

## Question 3: Scalability (5 points)
Imagine your chat application goes viral and now has 1 million users, each with an average of 10 conversation threads containing 500 messages each.
Compare how FlatFileManager and MongoDBManager would handle:
    - Finding all threads for a specific user
    - Loading a specific conversation
    - Storage organization and file system limits

Since FlatFileManager stores all thread mappings in one JSON, it'd take a long time O(n) to find a single conversation for a single user since it'd iterate through the entire list until it found its entries. MongoDBManager, since it's using MongoDB, has a much faster lookup through using a Binary Tree and hashing (with the user_id field), meaning its time complexting for finding all threads for a specific user would be about O(log(n)). 

Loading a specific conversation for each should be O(1) since, assuming all the conversations have already been retrieved, it's just accessing a single file. The limitation here is retrieving those conversations, which I've described above. That makes the fact they'd be about equally as fast a moot point (not including issues from storage). Speaking of...

...most file system struggle having millions and millions of files, and especially since in the FlatFileManager we're storing them using JSON files, the space isn't even very efficient. Much, much more memory will be required to store all the information compared to MongoDB's BSON files, which are much more compact (as we learned in class). The FlatFileManager just cannot scale as well as MongoDB can, even if it is more efficient for smaller use cases (low users, low conversations, low load).

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
    The .find_one() method we use retrieves the entire conversation at once, which is fast for small chats where we simply want to load everything immediately. It also keeps everything in one place, which is neater for storage purposes. It adheres to the idea that what's accessed together should be stored together, like we learned in class. It also means the AI is taking in all the conversation, although it could overload the context window of the model if the chat is too long.
    2. One advantage of the separate message documents design
    This is much more scalable, as in the instance where there's a million messages between the user and the AI, it'll take long time to load, and is much more feasible to merely load the most recent messages (say, 50). We don't always need to load the entire conversation, and this kind of design is used in most chat applications that I know of nowadays.
    3. A scenario where you would choose the separate messages design instead
    As mentioned above, chat applications like Discord store lots and lots of messages between users. It'd be ridicolusly slow to load everyone's FULL chat history every time they click on someone's profile to message them. Same goes for chats in servers, group chats, etc. It's much, much better to only load the most recent messages instead, and if the user scrolls up, load more dynamically.