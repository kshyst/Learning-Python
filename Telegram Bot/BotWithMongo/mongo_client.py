import pymongo


class ExpenseMongoClient:
    def __init__(
            self,
            host: str,
            port: int,
            db_name: str = "telegram_bot",
            collection_name: str = "expenses",
    ):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    def add_expense(self, user_id: int, amount: int, category: str, description: str):
        self.collection.insert_one({"user_id": user_id,
                                    "amount": amount,
                                    "category": category,
                                    "description": description})

    def get_expenses(self, user_id: int) -> list:
        results = self.collection.find({"user_id": user_id})
        expenses = []
        for res in results:
            expenses.append({"amount": res["amount"],
                             "category": res["category"],
                             "description": res["description"]})
        return expenses

    def get_categories(self, user_id: int) -> list:
        results = self.collection.find({"user_id": user_id})
        categories = []
        for res in results:
            if res["category"] not in categories:
                categories.append(res["category"])
        return categories

    def get_expenses_by_category(self, user_id: int, category: str) -> list:
        results = self.collection.find({"user_id": user_id, "category": category})
        expenses = []
        for res in results:
            expenses.append({"amount": res["amount"],
                             "category": res["category"],
                             "description": res["description"]})
        return expenses

    def get_total_expense(self, user_id: int):
        results = self.collection.find({"user_id": user_id})
        total = 0
        for res in results:
            total += res["amount"]
        return total

    def get_total_expense_by_category(self, user_id: int):
        results = self.collection.find({"user_id": user_id})
        total_by_category = {}
        for res in results:
            if res["category"] not in total_by_category:
                total_by_category[res["category"]] = 0
            total_by_category[res["category"]] += res["amount"]
        return total_by_category


if __name__ == "__main__":
    expense_mongo_client = ExpenseMongoClient("localhost", 27017)
    expense_mongo_client.add_expense(123, 100, "غذا", "ناهار")
    expense_mongo_client.add_expense(123, 200, "غذا", "شام")
    expense_mongo_client.add_expense(123, 300, "سفر", "پرواز")
    expense_mongo_client.add_expense(321, 400, "غذا", "ناهار")
    expense_mongo_client.add_expense(321, 500, "سفر", "پرواز")

    print("Expenses of 123")
    print(expense_mongo_client.get_expenses(123))

    print("Categories of 123")
    print(expense_mongo_client.get_categories(123))

    print("Total expense of 321")
    print(expense_mongo_client.get_total_expense(321))

    print("Total expense by category of 321")
    print(expense_mongo_client.get_total_expense_by_category(321))

    print("Expenses by category of 123")
    print(expense_mongo_client.get_expenses_by_category(123, "غذا"))
