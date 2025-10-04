from datetime import datetime
import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Rickie@1",
            database="finance_manager",
            charset='utf8mb4'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def add_budget_to_db(user_id, category, amount):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO budgets (user_id, category, amount)
                VALUES (%s, %s, %s)
            """, (user_id, category, amount))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error adding budget to the database: {err}")
        finally:
            conn.close()

def add_transaction_to_db(user_id, amount, type_, category, description):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO transactions (user_id, amount, type, category, description, date)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (user_id, amount, type_, category, description))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error adding transaction to the database: {err}")
        finally:
            conn.close()

def add_savings_goal_to_db(user_id, goal_name, target_amount, saved_amount, deadline):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO savings (user_id, name, target_amount, saved_amount, deadline)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, goal_name, target_amount, saved_amount, deadline))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error adding savings goal: {err}")
        finally:
            conn.close()

def update_balance_in_db(user_id, new_balance):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET balance = %s WHERE user_id = %s", (new_balance, user_id))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error updating balance in the database: {err}")
        finally:
            conn.close()

def fetch_user_info(user_id):
    conn = connect_db()
    if not conn:
        return 0.0, [], [], []

    cursor = conn.cursor(dictionary=True)

    try:
        # Balance
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()
        balance = balance['balance'] if balance else 0.0

        # Transactions
        cursor.execute("SELECT transaction_id, amount, type, category, date FROM transactions WHERE user_id = %s", (user_id,))
        transactions = cursor.fetchall()

        # Budgets
        cursor.execute("SELECT category, amount FROM budgets WHERE user_id = %s", (user_id,))
        budgets = cursor.fetchall()

        # Savings Goals
        cursor.execute("SELECT name, target_amount, saved_amount, deadline FROM savings WHERE user_id = %s", (user_id,))
        savings_goals = cursor.fetchall()

        return balance, transactions, budgets, savings_goals

    except Exception as e:
        print(f"Error fetching user info: {e}")
        return 0.0, [], [], []
    finally:
        conn.close()
