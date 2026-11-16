
class Expense:
    CATEGORIES = ("Food", "Transport", "Bills", "Shopping", "Health", "Education", "Entertainment", "Salary", "Freelance", "Other")
    TYPES = ("Expense", "Income")
    PAYMENTS = ("Cash", "Card", "Mobile Banking", "Bank Transfer")

    def __init__(self, expense_id: str, name: str, amount: float, category: str, date: str, t_type: str, payment: str):
        self.expense_id = str(expense_id).strip()
        self.name = str(name).strip()
        self.amount = float(amount)
        self.category = str(category).strip()
        self.date = str(date).strip()
        self.t_type = str(t_type).strip()
        self.payment = str(payment).strip()

    def to_dict(self) -> dict:
        return {
            "id": self.expense_id,
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "type": self.t_type,
            "payment": self.payment
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            expense_id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            amount=float(data.get("amount", 0)),
            category=str(data.get("category", "Other")),
            date=str(data.get("date", "")),
            t_type=str(data.get("type", "Expense")),
            payment=str(data.get("payment", "Cash"))
        )