from flask import Blueprint, render_template, request, redirect, session, flash
from ..db import connect_db, fetch_user_info

dashboard_bp = Blueprint('dashboard', __name__)

# ----------------------------
# Dashboard View
# ----------------------------
@dashboard_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')

    # Get user data
    balance, transactions, budgets, savings = fetch_user_info(user_id)

    # Calculate totals from transaction list
    income = sum(t['amount'] for t in transactions if t['type'] == "Income")
    expenses = sum(t['amount'] for t in transactions if t['type'] == "Expense")
    net_balance = income - expenses

    return render_template(
        'dashboard.html',
        balance=net_balance,  # replacing outdated DB balance field
        transactions=transactions,
        budgets=budgets,
        savings=savings,
        monthly_income=income,
        monthly_expenses=expenses,
        active_goals=len(savings)
    )

# ----------------------------
# Add Monthly Income (as transaction)
# ----------------------------
@dashboard_bp.route('/add_income', methods=['POST'])
def add_income():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')

    try:
        amount = float(request.form['amount'])
        conn = connect_db()
        cursor = conn.cursor()

        # Add income transaction (no direct balance update)
        cursor.execute("""
            INSERT INTO transactions (user_id, amount, type, category, description, date)
            VALUES (%s, %s, 'Income', 'Salary', 'Monthly salary', NOW())
        """, (user_id, amount))
        conn.commit()

        flash("Income recorded successfully!", "success")
    except Exception as e:
        print(f"Income error: {e}")
        flash("Error recording income", "error")
    finally:
        conn.close()
    return redirect('/dashboard')

# ----------------------------
# Add Budget
# ----------------------------
@dashboard_bp.route('/add_budget', methods=['POST'])
def add_budget():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')

    try:
        category = request.form['category']
        amount = float(request.form['amount'])
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO budgets (user_id, category, amount)
            VALUES (%s, %s, %s)
        """, (user_id, category, amount))
        conn.commit()
        flash("Budget saved successfully!", "success")
    except Exception as e:
        print(f"Budget error: {e}")
        flash("Error saving budget", "error")
    finally:
        conn.close()
    return redirect('/dashboard')

# ----------------------------
# Add Savings Goal
# ----------------------------
@dashboard_bp.route('/add_savings', methods=['POST'])
def add_savings():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')

    try:
        goal = request.form['goal_name']
        target = float(request.form['target_amount'])
        deadline = request.form['deadline']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO savings (user_id, name, target_amount, saved_amount, deadline)
            VALUES (%s, %s, %s, 0, %s)
        """, (user_id, goal, target, deadline))
        conn.commit()
        flash("Savings goal added successfully!", "success")
    except Exception as e:
        print(f"Savings error: {e}")
        flash("Error adding savings goal", "error")
    finally:
        conn.close()
    return redirect('/dashboard')
