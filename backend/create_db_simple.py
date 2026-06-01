#!/usr/bin/env python3
import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        charset='utf8mb4'
    )

    print("Connected to MySQL successfully")

    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS pbl CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("Database 'pbl' created successfully")

        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("Available databases:")
        for db in databases:
            print(f"  - {db[0]}")

    connection.commit()
    connection.close()
    print("MySQL database setup complete!")

except Exception as e:
    print(f"Error: {e}")
    print("Please check MySQL connection and credentials")