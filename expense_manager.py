from expense import Expense
from file_handler import FileHandler
from analysis import summarize_expenses
from datetime import datetime

class ExpenseManager:
    def __init__(self, file_path: str):
        self.file_handler = FileHandler(file_path)
        self.expenses = {}        
        self.used_ids = set()     
        self.load_data()

    def load_data(self):
        records, _ = self.file_handler.load()
        self.expenses.clear()
        self.used_ids.clear()
        for record in records:
            try:
                expense = Expense.from_dict(record)
                if expense.expense_id and expense.name:
                    self.expenses[expense.expense_id] = expense
                    self.used_ids.add(expense.expense_id)
            except Exception:
                continue

    def save_data(self):
        records = [expense.to_dict() for expense in self.expenses.values()]
        return self.file_handler.save(records)

    def add_expense(self, expense_id, name, amount, category, date, t_type, payment):
        if not expense_id or not name or not date:
            raise ValueError("Required fields cannot be empty.")
        if expense_id in self.used_ids:
            raise ValueError("Duplicate ID!")
        
        try:
            val_amount = float(amount)
            if val_amount <= 0: raise ValueError("Amount must be > 0")
        except ValueError:
            raise ValueError("Amount must be a valid number.")

        expense = Expense(expense_id, name, val_amount, category, date, t_type, payment)
        self.expenses[expense_id] = expense
        self.used_ids.add(expense_id)
        self.save_data()
        return expense

    def get_all(self):
        
        return sorted(self.expenses.values(), key=lambda x: int(x.expense_id) if x.expense_id.isdigit() else x.expense_id)

    def update_expense(self, expense_id, name, amount, category, date, t_type, payment):
        if expense_id not in self.expenses:
            raise KeyError("Record not found")
        
        try:
            val_amount = float(amount)
            if val_amount <= 0: raise ValueError("Amount must be > 0")
        except ValueError:
            raise ValueError("Amount must be a valid number.")

        e = self.expenses[expense_id]
        e.name, e.amount, e.category, e.date, e.t_type, e.payment = name, val_amount, category, date, t_type, payment
        self.save_data()

    def delete_expense(self, expense_id):
        if expense_id in self.expenses:
            del self.expenses[expense_id]
            self.used_ids.discard(expense_id)
            self.save_data()
            return True
        return False

    def search(self, query):
        query = str(query).lower().strip()
        results = []
        
        for e in self.expenses.values():
            eid = str(e.expense_id).lower().strip()
            
           
            if query.isdigit():
                if query == eid:
                    results.append(e)
            
            else:
                ename = str(e.name).lower()
                ecat = str(e.category).lower()
                edate = str(e.date).lower()
                etype = str(e.t_type).lower()
                epay = str(e.payment).lower()

                if (query in ename or 
                    query in ecat or 
                    query in edate or 
                    query in etype or 
                    query in epay):
                    results.append(e)
                    
        return results

    def get_dashboard_stats(self):
        total_income = sum(e.amount for e in self.expenses.values() if e.t_type == "Income")
        total_expense = sum(e.amount for e in self.expenses.values() if e.t_type == "Expense")
        balance = total_income - total_expense
        
        current_month = datetime.now().strftime("%Y-%m")
        this_month_expense = sum(e.amount for e in self.expenses.values() if e.t_type == "Expense" and e.date.startswith(current_month))
        
        return total_income, total_expense, balance, this_month_expense

    def get_analysis(self):
        return summarize_expenses(list(self.expenses.values()))