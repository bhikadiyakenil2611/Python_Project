import mysql.connector


class Transaction:
    """
    Represents a single financial transaction.
    """

    def __init__(self, date, description, amount):
        """
        Initializes a transaction with date, description, and amount.

        Args:
            date (str): Date of the transaction in YYYY-MM-DD format.
            description (str): Description of the transaction.
            amount (float): Amount of the transaction.
        """
        self.date = date
        self.description = description
        self.amount = amount


class FinanceManager:
    """
    Manages financial transactions and provides functionalities to add transactions, view transaction history, and calculate balance.
    """

    def __init__(self):
        """
        Initializes the FinanceManager with an empty list of transactions.
        """
        # Establish connection to the MySQL database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="fmdb"
        )

        # Create cursor object to execute SQL queries
        self.cursor = self.connection.cursor()
        self.transactions = []

    def add_transaction(self, date, t_type, description, amount, aid):
        """
        Adds a new transaction to the Database.

        Args:
            date (str): Date of the transaction in YYYY-MM-DD format.
            t_type(str): u have to pass Income / Expense (lowercase + string)
            description (str): Description of the transaction.
            amount (float): Amount of the transaction.
            aid (int): Account number in which u want to add Transaction
        """
        try:
            # self.transactions.append(Transaction(date, description, amount))
            insert_trans_qry = "Insert into transactions (amount, transaction_type, date, account_id, description) values (%s, %s, %s, %s, %s)"
            data = (amount, t_type, date, aid, description)
            self.cursor.execute(insert_trans_qry, data)
            self.connection.commit()
            print("Transaction added successfully!")
        except mysql.connector.Error as err:
            print("Error : ", err)

    def view_transactions(self, aid):
        """
        Displays the transaction history.

        Args:
            aid (int): Account number Of which You Want to see Transactions


        """
        aid = [aid]
        try:
            self.cursor.execute("Select * from transactions where account_id = %s", aid)
            trans = self.cursor.fetchall()
            print("    transaction_Date, Transaction_amount, Transaction_description")
            for tran in trans:
                print(f"{tran[2][0].upper()} - Date: {tran[3].day}/{tran[3].month}/{tran[3].year}, Amount: {tran[1]}, Description: {tran[5]}")

        except mysql.connector.Error as err:
            print("Error : ", err)

    def calculate_balance(self, aid):
        """
        Calculates the total income, total expenses, and current balance.

        Args:
            aid: Account_id, of which you want to calculate balance!
        """
        try:
            self.cursor.execute("select sum(amount) from transactions where transaction_type = 'income' and account_id = %s", [aid])
            income = self.cursor.fetchone()[0]
            self.cursor.execute("select sum(amount) from transactions where transaction_type = 'expense' and account_id = %s", [aid])
            expense = self.cursor.fetchone()[0]
            self.cursor.execute("select balance from balance where account_id = %s", [aid])
            balance = self.cursor.fetchone()[0]
            print(f"\nTotal Income: {income}")
            print(f"Total Expenses: {expense}")
            print(f"Current Balance: {balance}")
        except mysql.connector.Error as err:
            print("Error : ", err)


    def add_customer(self, name, bal=0):
        """
                Calculates the total income, total expenses, and current balance.

                Args:
                    name: Name of Customer Who wants to open new Account!
                    bal: Initial Balance, of newly opened Account!
                """
        try:
            data = [name, bal]
            self.cursor.execute("INSERT INTO balance(account_name, balance) VALUES (%s, %s)", data)
            self.connection.commit()
            self.cursor.execute("select account_id from balance where account_name = %s and balance = %s", data)
            newId = self.cursor.fetchall()
            print(f"Your Account ID = {newId[0][0]}, Kindly Remember This number for Further Interaction!")

        except mysql.connector.Error as err:
            print("Error : ", err)
            self.connection.rollback()


def main():
    """
    Main function to run the Personal Finance Manager.
    """
    global finance_manager
    try:

        finance_manager = FinanceManager()

        while True:
            print("\n===== Personal Finance Manager =====")

            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Transactions")
            print("4. Calculate Balance")
            print("5. Add new Account")
            print("6. Exit")

            choice = input("Enter your choice: ")
            if choice not in ["5", "6"]:
                aid = int(input("Kindly Enter Your A/c No. : "))

            if choice == "1":
                date = input("Enter date (YYYY-MM-DD): ")
                description = input("Enter description: ")
                amount = float(input("Enter income amount: "))
                finance_manager.add_transaction(date, 'income', description, amount, aid)
            elif choice == "2":
                date = input("Enter date (YYYY-MM-DD): ")
                description = input("Enter description: ")
                amount = float(input("Enter expense amount: "))
                finance_manager.add_transaction(date, 'expense', description, amount, aid)
            elif choice == "3":
                finance_manager.view_transactions(aid)
            elif choice == "4":
                finance_manager.calculate_balance(aid)
            elif choice == "5":
                name = input("Kindly Enter Your Name: ")
                bal = input("How much you're having income currently: ")
                finance_manager.add_customer(name,bal)
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    except mysql.connector.Error as error:
        # Handle connection or execution errors
        print("Error:", error)

    finally:
        # Close cursor and connection regardless of success or failure
        if finance_manager.connection.is_connected():
            finance_manager.cursor.close()
            finance_manager.connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    main()
