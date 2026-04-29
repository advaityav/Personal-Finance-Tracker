import os
os.system('cls')

import customtkinter as ctk
import json
from tkinter import messagebox, ttk, StringVar
from datetime import datetime

# --- Theme Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Personal Finance Manager Pro")
        self.geometry("750x950")
        self.file_path = "finance_data.json"

        self.data = self.load_data()

        if self.data["balance"] is None:
            self.ask_initial_balance()

        self.setup_ui()
        self.refresh_history()

    # ---------------- DATA ----------------
    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {"balance": None, "history": []}

    def save_data(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def parse_date(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M")

    # ---------------- SETUP ----------------
    def ask_initial_balance(self):
        dialog = ctk.CTkInputDialog(
            text="Enter your starting balance:",
            title="Setup Account"
        )
        input_val = dialog.get_input()
        try:
            self.data["balance"] = float(input_val)
        except:
            self.data["balance"] = 0.0

        self.save_data()

    def setup_ui(self):
        # Balance Display
        self.balance_card = ctk.CTkFrame(self, fg_color="#1f1f1f", corner_radius=20)
        self.balance_card.pack(pady=20, padx=20, fill="x")

        self.balance_label = ctk.CTkLabel(
            self.balance_card,
            text=f"Current Balance: ${self.data['balance']:.2f}",
            font=("Segoe UI", 28, "bold"),
            text_color="#2ecc71"
        )
        self.balance_label.pack(pady=20)

        # INPUT SECTION
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10)

        self.cat_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Category (Food, Rent, Salary...)",
            width=250
        )
        self.cat_entry.grid(row=0, column=0, padx=10)

        self.amt_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Amount",
            width=150
        )
        self.amt_entry.grid(row=0, column=1, padx=10)

        # BUTTONS
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame,
            text="Add Expense",
            command=lambda: self.process_money("expense"),
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=150
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Add Income",
            command=lambda: self.process_money("income"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=150
        ).grid(row=0, column=1, padx=10)

        # ---------------- ANALYTICS ----------------
        analytics_frame = ctk.CTkFrame(self)
        analytics_frame.pack(pady=15, padx=20, fill="x")

        ctk.CTkLabel(
            analytics_frame,
            text="Spending Analytics",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=5)

        self.category_dropdown = ctk.CTkEntry(
            analytics_frame,
            placeholder_text="Category (or type All)",
            width=250
        )
        self.category_dropdown.pack(pady=5)

        date_frame = ctk.CTkFrame(analytics_frame, fg_color="transparent")
        date_frame.pack()

        self.start_date = ctk.CTkEntry(date_frame, placeholder_text="Start YYYY-MM-DD", width=180)
        self.start_date.grid(row=0, column=0, padx=5)

        self.end_date = ctk.CTkEntry(date_frame, placeholder_text="End YYYY-MM-DD", width=180)
        self.end_date.grid(row=0, column=1, padx=5)

        self.result_label = ctk.CTkLabel(
            analytics_frame,
            text="Total Spending: $0.00",
            font=("Segoe UI", 16)
        )
        self.result_label.pack(pady=5)

        ctk.CTkButton(
            analytics_frame,
            text="Analyze Spending",
            command=self.analyze_spending
        ).pack(pady=5)

        # ---------------- HISTORY ----------------
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=30
        )
        style.map("Treeview", background=[('selected', '#3498db')])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Date", "Category", "Amount", "Balance"),
            show="headings"
        )

        for col in ("Date", "Category", "Amount", "Balance"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # RESET
        ctk.CTkButton(
            self,
            text="Clear All History",
            fg_color="#333",
            command=self.clear_all
        ).pack(pady=15)

    # ---------------- LOGIC ----------------
    def process_money(self, mode):
        category = self.cat_entry.get().strip()
        amount_text = self.amt_entry.get().strip()

        if not category:
            messagebox.showwarning("Error", "Enter category")
            return

        try:
            amount = float(amount_text)
        except:
            messagebox.showerror("Error", "Invalid amount")
            return

        if mode == "expense":
            if amount > self.data["balance"]:
                messagebox.showerror("Error", "Insufficient balance")
                return
            self.data["balance"] -= amount
            display_amount = f"-${amount:.2f}"
        else:
            self.data["balance"] += amount
            display_amount = f"+${amount:.2f}"

        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": category,
            "amount": display_amount,
            "balance_after": self.data["balance"]
        }

        self.data["history"].insert(0, entry)
        self.save_data()

        self.balance_label.configure(
            text=f"Current Balance: ${self.data['balance']:.2f}"
        )

        self.cat_entry.delete(0, "end")
        self.amt_entry.delete(0, "end")

        self.refresh_history()

    # ---------------- ANALYTICS ----------------
    def analyze_spending(self):
        category = self.category_dropdown.get().strip()
        start = self.start_date.get().strip()
        end = self.end_date.get().strip()

        try:
            start_dt = datetime.strptime(start, "%Y-%m-%d") if start else None
            end_dt = datetime.strptime(end, "%Y-%m-%d") if end else None
        except:
            messagebox.showerror("Error", "Use YYYY-MM-DD format")
            return

        total_expense = 0.0
        total_income = 0.0

        for item in self.data["history"]:
            item_date = self.parse_date(item["date"])

            if start_dt and item_date < start_dt:
                continue
            if end_dt and item_date > end_dt:
                continue

            if category and category.lower() != "all":
                if item["category"].lower() != category.lower():
                    continue

            amount = float(item["amount"].replace("$", "").replace("+", "").replace("-", ""))

            if item["amount"].startswith("-"):
                total_expense += amount
            else:
                total_income += amount

        net = total_income - total_expense

        self.result_label.configure(
            text=(
                f"Income: ${total_income:.2f} | "
                f"Expense: ${total_expense:.2f} | "
                f"Net: ${net:.2f}"
            )
        )

    # ---------------- HISTORY ----------------
    def refresh_history(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for item in self.data["history"]:
            self.tree.insert(
                "",
                "end",
                values=(
                    item["date"],
                    item["category"],
                    item["amount"],
                    f"${item['balance_after']:.2f}"
                )
            )

    # ---------------- RESET ----------------
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Reset everything?"):
            self.data = {"balance": None, "history": []}
            self.save_data()
            self.ask_initial_balance()
            self.refresh_history()


if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()