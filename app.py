import customtkinter as ctk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BillingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Professional Invoice & Billing System")
        self.geometry("550x650")
        
        # Grid weight configuration taake resize hone par content center mein rahe
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.items = []

        # Heading
        self.heading = ctk.CTkLabel(self.main_frame, text="INVOICE GENERATOR", font=ctk.CTkFont(size=22, weight="bold"))
        self.heading.pack(pady=15)

        # Customer Details Frame
        self.cust_frame = ctk.CTkFrame(self.main_frame)
        self.cust_frame.pack(pady=10, padx=20, fill="x")

        self.cust_name = ctk.CTkEntry(self.cust_frame, placeholder_text="Customer Name")
        self.cust_name.pack(pady=10, padx=10, fill="x")

        # Item Details Frame
        self.item_frame = ctk.CTkFrame(self.main_frame)
        self.item_frame.pack(pady=10, padx=20, fill="x")

        self.item_name = ctk.CTkEntry(self.item_frame, placeholder_text="Item Name")
        self.item_name.pack(pady=5, padx=10, fill="x")

        self.item_price = ctk.CTkEntry(self.item_frame, placeholder_text="Price ($)")
        self.item_price.pack(pady=5, padx=10, fill="x")

        self.item_qty = ctk.CTkEntry(self.item_frame, placeholder_text="Quantity")
        self.item_qty.pack(pady=5, padx=10, fill="x")

        self.add_btn = ctk.CTkButton(self.item_frame, text="Add Item", command=self.add_item, fg_color="green")
        self.add_btn.pack(pady=10)

        # Items List Display
        self.list_box = ctk.CTkTextbox(self.main_frame, height=120)
        self.list_box.pack(pady=10, padx=20, fill="both", expand=True)
        self.list_box.insert("0.0", "Items List:\n" + "-"*50 + "\n")

        # Action Buttons
        self.generate_btn = ctk.CTkButton(self.main_frame, text="Generate PDF Bill", command=self.generate_pdf, font=ctk.CTkFont(size=14, weight="bold"))
        self.generate_btn.pack(pady=15)

    def add_item(self):
        name = self.item_name.get()
        price = self.item_price.get()
        qty = self.item_qty.get()

        if not name or not price or not qty:
            messagebox.showwarning("Warning", "Please fill all item fields!")
            return

        try:
            price = float(price)
            qty = int(qty)
            total = price * qty
            self.items.append((name, price, qty, total))

            self.list_box.insert("end", f"{name} - {qty} x ${price:.2f} = ${total:.2f}\n")

            self.item_name.delete(0, 'end')
            self.item_price.delete(0, 'end')
            self.item_qty.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Price and Quantity must be numbers!")

    def generate_pdf(self):
        customer = self.cust_name.get()
        if not customer or not self.items:
            messagebox.showwarning("Warning", "Add customer name and at least one item!")
            return

        file_name = f"Bill_{customer.replace(' ', '_')}.pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 20)
        c.drawString(200, 750, "INVOICE RECEIPT")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 710, f"Customer Name: {customer}")
        c.drawString(50, 690, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        c.line(50, 675, 550, 675)
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 655, "Item")
        c.drawString(250, 655, "Price")
        c.drawString(350, 655, "Qty")
        c.drawString(450, 655, "Total")
        c.line(50, 645, 550, 645)

        y = 625
        grand_total = 0
        c.setFont("Helvetica", 12)
        for item in self.items:
            c.drawString(50, y, str(item[0]))
            c.drawString(250, y, f"${item[1]:.2f}")
            c.drawString(350, y, str(item[2]))
            c.drawString(450, y, f"${item[3]:.2f}")
            grand_total += item[3]
            y -= 25

        c.line(50, y, 550, y)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(350, y - 30, f"Grand Total: ${grand_total:.2f}")

        c.save()
        messagebox.showinfo("Success", f"Invoice saved successfully as:\n{file_name}")

if __name__ == "__main__":
    app = BillingApp()
    app.mainloop()
