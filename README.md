# Personal Expense Tracker

A Python desktop application for recording income and expenses, managing a monthly budget, and viewing expense summaries.

## Technologies
- Python
- Tkinter (GUI)
- NumPy (numerical analysis)
- JSON (persistent data storage)

## Features
- Add, view, search, update, and delete transactions
- Record income and expenses
- Save and load data using JSON
- Set a monthly budget and receive an over-budget warning
- View total income, total expenses, balance, and monthly analysis
- Validate input and handle common errors

## Requirements
Python 3.9 or later is recommended.

Install NumPy:
```bash
python -m pip install numpy
```

Tkinter is included with most standard Python installations. On some Linux distributions it may need to be installed separately.

## Run
Open a terminal in the `ExpenseTracker` folder and run:
```bash
python main.py
```

Transaction data is stored in `data/expenses.json`. The monthly budget is stored in `data/budget.json`.

## Note
The included transactions are sample records. Replace them with your own test data before your final demonstration. Add your group members' details and actual screenshots to the project report.
