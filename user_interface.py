from tkinter import *
from tkinter import messagebox, simpledialog, filedialog, Toplevel, Label
from db import connect_db
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3

def open_user_interface(username):
    window = Tk()
    window.title(f"Pizza Order - Logged in as {username}")
    window.geometry("500x600")
    window.config(bg="blue")

    # Variables
    size_var = StringVar()
    quantity_var = IntVar(value=1)
    toppings_var = []
    customer_name = StringVar()
    customer_phone = StringVar()
    topping_options = ["Cheese", "Pepperoni", "Mushrooms", "Olives", "Peppers"]

    def calculate_price():
        size = size_var.get()
        base_price = {"Small": 8, "Medium": 12, "Large": 15}.get(size, 0)
        topping_count = sum(var.get() for var in toppings_var)
        total = (base_price + (topping_count * 2)) * quantity_var.get()
        return total

    def place_order():
        size = size_var.get()
        quantity = quantity_var.get()
        selected_toppings = [topping_options[i] for i, var in enumerate(toppings_var) if var.get()]
        toppings_str = ", ".join(selected_toppings)
        total = calculate_price()
        name = customer_name.get().strip()
        phone = customer_phone.get().strip()
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not name or not phone or not size:
            messagebox.showerror("Error", "Please fill all fields and select a pizza size.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (username, customer_name, phone, pizza_size, toppings, quantity, total_price, order_datetime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, name, phone, size, toppings_str, quantity, total, order_time))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Order placed successfully!")

    def view_receipt():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM orders 
            WHERE username = ? 
            ORDER BY order_datetime DESC 
            LIMIT 1
        """, (username,))
        order = cursor.fetchone()
        conn.close()

        if order:
            order_id = order[0]
            customer_name_val = order[2]
            phone = order[3]
            size = order[4]
            toppings = order[5]
            quantity = order[6]
            total_price = order[7]
            order_time = order[8]

            receipt_content = f"""
            --- Pizza Order Receipt ---
            Order ID: {order_id}
            Name: {customer_name_val}
            Phone: {phone}
            Pizza Size: {size}
            Toppings: {toppings}
            Quantity: {quantity}
            Total Price: ${total_price:.2f}
            Order Time: {order_time}
            """

            receipt_win = Toplevel()
            receipt_win.title("Receipt")
            Label(receipt_win, text=receipt_content, justify="left", font=("Courier", 12)).pack(padx=20, pady=20)

            file_format = simpledialog.askstring("Save Format", "Enter file format (txt or pdf):")
            if not file_format:
                return
            file_format = file_format.lower()

            if file_format not in ("txt", "pdf"):
                messagebox.showerror("Invalid Format", "Please enter 'txt' or 'pdf'")
                return

            file_ext = ".txt" if file_format == "txt" else ".pdf"
            file_path = filedialog.asksaveasfilename(
                defaultextension=file_ext,
                filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")],
                initialfile=f"receipt_order_{order_id}{file_ext}"
            )

            if not file_path:
                return

            if file_format == "txt":
                with open(file_path, "w") as file:
                    file.write(receipt_content.strip())
            else:
                c = canvas.Canvas(file_path, pagesize=letter)
                c.setFont("Helvetica", 12)
                y = 750
                for line in receipt_content.strip().splitlines():
                    c.drawString(50, y, line.strip())
                    y -= 20
                c.save()

            messagebox.showinfo("Saved", f"Receipt saved to:\n{file_path}")
        else:
            messagebox.showinfo("No Orders", "No recent order found for your account.")

    def logout():
        window.destroy()
        import main
        if main.__name__ == "__main__":
            main

    # --- Widgets ---
    Label(window, text="Pizza Order Form", font=("Arial Black", 16), bg="white").place(x=150, y=20)

    Label(window, text="Customer Name:", bg="white").place(x=50, y=70)
    Entry(window, textvariable=customer_name).place(x=200, y=70)

    Label(window, text="Phone Number:", bg="white").place(x=50, y=110)
    Entry(window, textvariable=customer_phone).place(x=200, y=110)

    Label(window, text="Select Size:", bg="white").place(x=50, y=160)
    OptionMenu(window, size_var, "Small", "Medium", "Large").place(x=200, y=155)

    Label(window, text="Select Toppings:", bg="white").place(x=50, y=210)
    for i, topping in enumerate(topping_options):
        var = IntVar()
        toppings_var.append(var)
        Checkbutton(window, text=topping, variable=var, bg="white").place(x=200, y=210 + (i * 30))

    Label(window, text="Quantity:", bg="white").place(x=50, y=380)
    Spinbox(window, from_=1, to=10, textvariable=quantity_var, width=5).place(x=200, y=380)

    Button(window, text="Place Order", bg="green", fg="white", command=place_order).place(x=100, y=430)
    Button(window, text="View Receipt", bg="black", fg="white", command=view_receipt).place(x=200, y=430)
    Button(window, text="Logout", bg="red", fg="white", command=logout).place(x=320, y=430)

    window.mainloop()