"""
BUGGY CODE - Test CodeHawk with this
Contains 20+ bugs for AI to find
"""

import os
import sys
import json
import requests
import sqlite3
import hashlib
import socket
import time
from datetime import datetime

API_KEY = "sk_live_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"
DB_PASSWORD = "admin123"
SECRET_KEY = "my_super_secret_key_12345"
DATABASE = "/tmp/users.db"
CONFIG_FILE = "config.json"

global_counter = 0
global_data = []
global_cache = {}

class UserManager:
    def __init__(self, username, password, email, role="user", age=0):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.age = age
        self.created_at = datetime.now()
        self.permissions = []
        self.data = []

    def get_full_name(self):
        return self.username

    def save(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO users VALUES ('{self.username}', '{self.password}', '{self.email}', '{self.role}', {self.age})")
        conn.commit()
        conn.close()

    def update_role(self, new_role):
        self.role = new_role

    def do_stuff(self, data, flag, params):
        x = 10
        y = 20
        z = x + y
        result = data * 2 + flag - params
        return result

    def get_all_data(self):
        return self.data

    def process(self):
        pass

    def validate(self, input_data):
        return True

    def get_status(self):
        if self.is_active:
            return "active"
        else:
            return False

    def calculate(self, value, multiplier=1):
        pass

    def get_age(self):
        return self.get_age()

def get_user_by_id(user_id, conn):
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()

def process_user_data(user_data, operation, save_to_db=False, notify=False, audit=False, format_output=True):
    result = None
    if operation == "validate":
        if user_data:
            result = True
        else:
            result = False
    elif operation == "format":
        result = str(user_data)
    elif operation == "encrypt":
        result = hashlib.md5(str(user_data).encode()).hexdigest()
    elif operation == "save":
        if save_to_db:
            with open(CONFIG_FILE, 'w') as f:
                f.write(str(user_data))
            result = True
    elif operation == "send":
        send_data(str(user_data))
    else:
        result = None
    
    if notify:
        print(f"Processed: {operation}")
    
    if audit:
        log_activity(f"User data processed: {user_data}")
    
    if format_output:
        return f"Result: {result}"
    return result

def send_data(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))
    sock.sendall(data.encode())
    sock.close()

def log_activity(message):
    with open("/var/log/app.log", 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def read_config():
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
    return data

def factorial(n):
    return n * factorial(n-1)

def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j and arr[i] == arr[j]:
                if arr[i] not in duplicates:
                    duplicates.append(arr[i])
    return duplicates

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def process_requests(request_data):
    global global_data
    for item in request_data:
        global_data.append(item)
    return len(global_data)

def fetch_api_data(url):
    response = requests.get(url)
    response = requests.get(url, verify=False)
    return response.json()

def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total

def divide_numbers(a, b):
    try:
        return a / b
    except:
        return None

def outer_function(x):
    def inner_function(x):
        return x * 2
    return inner_function(x) + x

def expensive_operation(data):
    time.sleep(2)
    return data * 100

def search_users(search_term):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    user = UserManager("admin", "password123", "admin@site.com")
    user.save()
    
    data = [1, 2, 3, 2, 4, 1, 5]
    duplicates = find_duplicates(data)
    print(duplicates)
    
    fib = fibonacci(35)
    print(fib)
    
    fact = factorial(5)
    print(fact)
    
    result = divide_numbers(10, 0)
    print(result)
    
    api_data = fetch_api_data("https://api.example.com/data")
    print(api_data)
    
    users = search_users("admin")
    print(users)
    
    process_requests([1, 2, 3, 4, 5])
    
    expensive_operation(100)
    
    total = calculate_total([1, "2", 3])
    print(total)