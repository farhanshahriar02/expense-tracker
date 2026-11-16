"""
analysis.py
NumPy-based numerical analysis for expenses.
"""
import numpy as np

def summarize_expenses(expenses: list) -> dict:
    if not expenses:
        return {"count": 0, "total_income": 0.0, "total_expense": 0.0, "category_totals": {}}

    incomes = [e.amount for e in expenses if e.t_type == "Income"]
    outgoings = [e.amount for e in expenses if e.t_type == "Expense"]

    total_income = float(np.sum(incomes)) if incomes else 0.0
    total_expense = float(np.sum(outgoings)) if outgoings else 0.0

    category_totals = {}
    for category in set([e.category for e in expenses]):
        cat_amounts = [e.amount for e in expenses if e.category == category and e.t_type == "Expense"]
        if cat_amounts:
            category_totals[category] = float(np.sum(cat_amounts))

    return {
        "count": len(expenses),
        "total_income": total_income,
        "total_expense": total_expense,
        "average_expense": float(np.mean(outgoings)) if outgoings else 0.0,
        "highest_expense": float(np.max(outgoings)) if outgoings else 0.0,
        "category_totals": category_totals
    }