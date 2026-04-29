# Personal Finance Tracker

Personal Finance Manager Pro is a desktop-based application developed using Python and CustomTkinter. The application is designed to help users efficiently manage their financial activities by tracking income, expenses, and overall balance, along with providing basic analytical insights.

---

## Features

* Real-time balance tracking with automatic updates
* Recording of income and expense transactions
* Categorization of financial entries
* Transaction history with date and time stamps
* Spending analysis based on category and date range
* Data persistence using JSON storage
* Option to reset and reinitialize all financial data

---

## Technologies Used

* Python
* CustomTkinter
* Tkinter (Treeview widget)
* JSON for data storage

---

## Project Structure

```
finance-tracker/
│── main.py
│── finance_data.json
│── README.md
```

---

## Installation and Execution

1. Clone the repository:

```
git clone https://github.com/your-username/your-repo-name.git
```

2. Navigate to the project directory:

```
cd your-repo-name
```

3. Install required dependencies:

```
pip install customtkinter
```

4. Run the application:

```
python main.py
```

---

## Working Principle

The application allows users to input financial transactions by specifying a category and an amount. Based on the selected operation (income or expense), the system updates the current balance and records the transaction along with a timestamp. All data is stored locally in a JSON file to ensure persistence.

The analytics feature enables users to filter transactions based on category and date range, providing a summary of total income, total expenses, and net balance.

---

## Input Validation

* Category field must not be empty
* Amount must be a valid numeric value
* Expense transactions cannot exceed the available balance

---

## Future Enhancements

* Graphical representation of financial data
* Export functionality (CSV or Excel)
* Cloud-based data synchronization
* Mobile application support

---

## Author

This project was developed as part of a practical implementation of Python programming concepts, focusing on GUI development and data management.

---

## Note

This application stores all data locally and does not transmit any user information externally.

