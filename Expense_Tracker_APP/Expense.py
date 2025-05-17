class Expense :
    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = float(amount)
    
    def __repr__(self) -> str:
        return f"""\n Expense -->\n Expense name = {self.name},
                     \n Expense category = {self.category},
                     \n Expense amount = ₹{self.amount}\n"""