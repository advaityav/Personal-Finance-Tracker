import os
os.system('cls')

import customtkinter as ctk
import json
from tkinter import messagebox, ttk
from datetime import datetime

# --- Theme Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Personal Finance Tracker")
        self.geometry("700x900")
        self.file_path = "finance_data.json"

        self.data = self.load_data()

        if self.data["balance"] is None:
            self.ask_initial_balance()

        self.setup_ui()
        self.refresh_history()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {"balance": None, "history": []}

    def save_data(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

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
        self.balance_card.pack(pady=30, padx=20, fill="x")

        self.balance_label = ctk.CTkLabel(
            self.balance_card,
            text=f"Current Balance: ${self.data['balance']:.2f}",
            font=("Segoe UI", 28, "bold"),
            text_color="#2ecc71"
        )
        self.balance_label.pack(pady=25)

        # Input Section
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10, padx=20)

        # CATEGORY INPUT (REQUIRED NOW)
        self.cat_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter Category (e.g. Food, Salary, Rent)",
            width=250,
            corner_radius=10
        )
        self.cat_entry.grid(row=0, column=0, padx=10)

        # AMOUNT INPUT
        self.amt_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Amount",
            width=150,
            corner_radius=10
        )
        self.amt_entry.grid(row=0, column=1, padx=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.spend_btn = ctk.CTkButton(
            btn_frame,
            text="Add Expense",
            command=lambda: self.process_money("expense"),
            height=45,
            width=150,
            corner_radius=22,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.spend_btn.grid(row=0, column=0, padx=10)

        self.income_btn = ctk.CTkButton(
            btn_frame,
            text="Add Income",
            command=lambda: self.process_money("income"),
            height=45,
            width=150,
            corner_radius=22,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.income_btn.grid(row=0, column=1, padx=10)

        # History Table
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
            show='headings'
        )

        for col in ("Date", "Category", "Amount", "Balance"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Reset Button
        self.reset_btn = ctk.CTkButton(
            self,
            text="Clear All History",
            command=self.clear_all,
            fg_color="#333333",
            corner_radius=10
        )
        self.reset_btn.pack(pady=20)

    def process_money(self, mode):
        category = self.cat_entry.get().strip()
        amount_text = self.amt_entry.get().strip()

        # Validate category
        if not category:
            messagebox.showwarning("Error", "Please enter a category.")
            return

        # Validate amount
        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        # Expense logic
        if mode == "expense":
            if amount > self.data["balance"]:
                messagebox.showerror("Error", "Insufficient Balance!")
                return
            self.data["balance"] -= amount
            display_amount = f"-${amount:.2f}"

        # Income logic
        else:
            self.data["balance"] += amount
            display_amount = f"+${amount:.2f}"

        # Save entry
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": category,
            "amount": display_amount,
            "balance_after": self.data["balance"]
        }

        self.data["history"].insert(0, new_entry)
        self.save_data()

        # Update UI
        self.balance_label.configure(
            text=f"Current Balance: ${self.data['balance']:.2f}"
        )

        self.cat_entry.delete(0, "end")
        self.amt_entry.delete(0, "end")

        self.refresh_history()

    def refresh_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

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

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Reset everything?"):
            self.data = {"balance": None, "history": []}
            self.save_data()
            self.ask_initial_balance()

            self.balance_label.configure(
                text=f"Current Balance: ${self.data['balance']:.2f}"
            )

            self.refresh_history()


if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()