from app.enums.transaction import TransactionType
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import SessionLocal
from app.models.categories import Category

EXPENSE_CATEGORIES = [
    "Groceries",
    "Restaurants & Cafes",
    "Transportation",
    "Fuel",
    "Housing",
    "Utilities",
    "Phone & Internet",
    "Healthcare",
    "Clothing & Shoes",
    "Entertainment",
    "Subscriptions",
    "Education",
    "Travel",
    "Gifts",
    "Bank Fees",
    "Other Expenses",
]

INCOME_CATEGORIES = [
    "Salary",
    "Bonus",
    "Freelance",
    "Investments",
    "Interest",
    "Gifts",
    "Refunds",
    "Other Income",
]


DEFAULT_LIST = []

for category in EXPENSE_CATEGORIES:
    category_data = {"name": category,
         "type": TransactionType.EXPENSE,
         "user_id": None}
    DEFAULT_LIST.append(category_data)

for category in INCOME_CATEGORIES:
    category_data = {"name": category,
         "type": TransactionType.INCOME,
         "user_id": None}
    DEFAULT_LIST.append(category_data)


# print(DEFAULT_LIST)

def insert_category():
    with SessionLocal() as connection:
        try:
            stmt = insert(Category).values(DEFAULT_LIST)
            stmt = stmt.on_conflict_do_nothing(index_elements=["name", "type"], index_where=text("user_id IS NULL"))

            connection.execute(stmt)
            connection.commit()
            print("Operation complete")
        except IntegrityError as e:
            print(f"Somethings goes wrong: {e}")
            connection.rollback()
        except SQLAlchemyError as e:
            print(f"Somethings goes wrong: {e}")
            connection.rollback()

if __name__ == "__main__":
    insert_category()