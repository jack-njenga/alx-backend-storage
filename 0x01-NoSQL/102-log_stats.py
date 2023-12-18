#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present
IPs in the collection nginx of the database logs
"""
from pymongo import MongoClient


def logging_stats():
    """
    Printing Logging details and Stats
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    logs = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    path = logs_collection.count_documents(
        {"method": "GET", "path": "/status"})

    print(f"{logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")


if __name__ == "__main__":
    logging_stats()
