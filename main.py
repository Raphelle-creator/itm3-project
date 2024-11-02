from fastapi import FastAPI, HTTPException, Depends
from typing import List
import mysql.connector
from datetime import datetime
from schemas import (
    UserCreate, UserResponse, UserUpdate,
    BudgetCreate, BudgetUpdate, BudgetResponse,
    TransactionCreate, TransactionResponse,
    NotificationCreate, NotificationUpdate, NotificationResponse
)

app = FastAPI()


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'budgets_db'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (user.name, user.email, user.password)
    )
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**user.dict(), "id": user_id, "created_at": datetime.now()}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    cursor.close()
    connection.close()
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "User deleted successfully"}

@app.post("/budgets/", response_model=BudgetResponse)
def create_budget(budget: BudgetCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO budgets (user_id, month, year, target_budget) VALUES (%s, %s, %s, %s)",
        (budget.user_id, budget.month, budget.year, budget.target_budget)
    )
    connection.commit()
    budget_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**budget.dict(), "id": budget_id, "created_at": datetime.now(), "updated_at": datetime.now()}

@app.get("/budgets/{budget_id}", response_model=BudgetResponse)
def get_budget(budget_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM budgets WHERE id = %s", (budget_id,))
    budget = cursor.fetchone()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    cursor.close()
    connection.close()
    return budget

@app.put("/budgets/{budget_id}", response_model=BudgetResponse)
def update_budget(budget_id: int, budget_update: BudgetUpdate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "UPDATE budgets SET actual_spent = %s WHERE id = %s",
        (budget_update.actual_spent, budget_id)
    )
    connection.commit()
    cursor.execute("SELECT * FROM budgets WHERE id = %s", (budget_id,))
    updated_budget = cursor.fetchone()
    if not updated_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    cursor.close()
    connection.close()
    return updated_budget

@app.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM budgets WHERE id = %s", (budget_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Budget deleted successfully"}

@app.post("/notifications/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO notifications (user_id, month, year, message) VALUES (%s, %s, %s, %s)",
        (notification.user_id, notification.month, notification.year, notification.message)
    )
    connection.commit()
    notification_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**notification.dict(), "id": notification_id, "created_at": datetime.now()}

@app.get("/notifications/{user_id}/{month}/{year}", response_model=List[NotificationResponse])
def get_notifications(user_id: int, month: str, year: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM notifications WHERE user_id = %s AND month = %s AND year = %s",
        (user_id, month, year)
    )
    notifications = cursor.fetchall()
    cursor.close()
    connection.close()
    return notifications


@app.get("/users/", response_model=List[UserResponse])
def list_all_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        (user_update.name, user_update.email, user_id)
    )
    connection.commit()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    updated_user = cursor.fetchone()
    cursor.close()
    connection.close()
    return updated_user

@app.get("/budgets/user/{user_id}", response_model=List[BudgetResponse])
def list_budgets_for_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM budgets WHERE user_id = %s", (user_id,))
    budgets = cursor.fetchall()
    cursor.close()
    connection.close()
    return budgets

@app.post("/transactions/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO transactions (budget_id, amount, description, date) VALUES (%s, %s, %s, %s)",
        (transaction.budget_id, transaction.amount, transaction.description, transaction.date)
    )
    connection.commit()
    transaction_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**transaction.dict(), "id": transaction_id}

@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
    transaction = cursor.fetchone()
    cursor.close()
    connection.close()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@app.get("/transactions/budget/{budget_id}", response_model=List[TransactionResponse])
def list_transactions_by_budget(budget_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE budget_id = %s", (budget_id,))
    transactions = cursor.fetchall()
    cursor.close()
    connection.close()
    return transactions

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Transaction deleted successfully"}

# 17. Monthly Spending Summary
@app.get("/budgets/{user_id}/{month}/{year}/summary", response_model=dict)
def monthly_spending_summary(user_id: int, month: str, year: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT SUM(amount) as total_spent FROM transactions WHERE budget_id IN "
        "(SELECT id FROM budgets WHERE user_id = %s AND month = %s AND year = %s)",
        (user_id, month, year)
    )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return {"total_spent": result["total_spent"] or 0}

@app.put("/budgets/{budget_id}/achieve")
def set_budget_as_achieved(budget_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE budgets SET achieved = TRUE WHERE id = %s", (budget_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Budget marked as achieved"}

@app.put("/notifications/{notification_id}", response_model=NotificationResponse)
def update_notification(notification_id: int, notification_update: NotificationUpdate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "UPDATE notifications SET message = %s WHERE id = %s",
        (notification_update.message, notification_id)
    )
    connection.commit()
    cursor.execute("SELECT * FROM notifications WHERE id = %s", (notification_id,))
    updated_notification = cursor.fetchone()
    cursor.close()
    connection.close()
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification

@app.get("/notifications/user/{user_id}", response_model=List[NotificationResponse])
def list_all_notifications_for_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications WHERE user_id = %s", (user_id,))
    notifications = cursor.fetchall()
    cursor.close()
    connection.close()
    return notifications

@app.get("/budgets/{budget_id}/achieved", response_model=dict)
def is_budget_achieved(budget_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT achieved FROM budgets WHERE id = %s", (budget_id,))
    budget = cursor.fetchone()
    cursor.close()
    connection.close()
    return {"achieved": budget["achieved"] if budget else False}