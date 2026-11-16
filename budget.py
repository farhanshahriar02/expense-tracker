import json
import os

class Budget:
    def __init__(self, file_path="data/budget.json"):
        self.file_path = file_path
        self.monthly_budget = 0.0
        self.load_budget()

    def load_budget(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.monthly_budget = data.get("monthly_budget", 0.0)
        except Exception:
            self.monthly_budget = 0.0

    def save_budget(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump({"monthly_budget": self.monthly_budget}, f, indent=4)

    def set_budget(self, amount):
        if amount < 0:
            raise ValueError("Budget cannot be negative.")
        self.monthly_budget = amount
        self.save_budget()

    def check_limit(self, total_spent):
        if self.monthly_budget == 0:
            return "No monthly budget set."
        
        if total_spent > self.monthly_budget:
            return f"⚠️ WARNING: Exceeded budget by ৳{total_spent - self.monthly_budget:.2f}!"
        
        return f"Remaining budget: ৳{self.monthly_budget - total_spent:.2f}"