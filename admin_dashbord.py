# admin_dashboard.py
from tkinter import *
from tkinter import messagebox
from db import connect_db
from utils import show_receipt

def open_admin_dashboard(username):
    admin = Tk()
    admin.title(f"Admin Dashboard - {username}")
    admin.geometry("850x500")
    admin.config(bg="blue")

    orders_listbox = Listbox(admin, width=100, height=20)
    orders_listbox.place(x=20, y=20)

    def load_orders():
        orders_listbox.delete(0, END)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        for row in rows:
            display = f"ID:{row[0]} | User:{row[1]} | Name:{row[2]} | Size:{row[4]} | Qty:{row[6]} | Total: ${row[7]}"
            orders_listbox.insert(END, display)
        conn.close()

    def delete_order():
        selection = orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Order", "Please select an order to delete.")
            return
        order_id = int(orders_listbox.get(selection[0]).split('|')[0].split(':')[1].strip())

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        load_orders()
        messagebox.showinfo("Deleted", f"Order {order_id} deleted.")

    def edit_order():
        selection = orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Order", "Please select an order to edit.")
            return
        order_id = int(orders_listbox.get(selection[0]).split('|')[0].split(':')[1].strip())

        # Fetch order
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
        row = cursor.fetchone()
        conn.close()

        # Create edit popup
        edit_win = Toplevel(admin)
        edit_win.title("Edit Order")
        edit_win.geometry("400x400")
        edit_win.config(bg="blue")

        name_var = StringVar(value=row[2])
        phone_var = StringVar(value=row[3])
        size_var = StringVar(value=row[4])
        toppings_var = StringVar(value=row[5])
        qty_var = IntVar(value=row[6])

        Label(edit_win, text="Customer Name").pack()
        Entry(edit_win, textvariable=name_var).pack()

        Label(edit_win, text="Phone").pack()
        Entry(edit_win, textvariable=phone_var).pack()

        Label(edit_win, text="Pizza Size").pack()
        Entry(edit_win, textvariable=size_var).pack()

        Label(edit_win, text="Toppings").pack()
        Entry(edit_win, textvariable=toppings_var).pack()

        Label(edit_win, text="Quantity").pack()
        Entry(edit_win, textvariable=qty_var).pack()

        def save_changes():
            new_total = ({"Small": 8, "Medium": 12, "Large": 15}.get(size_var.get(), 0) +
                         2 * len(toppings_var.get().split(","))) * qty_var.get()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE orders
                SET customer_name=?, phone=?, pizza_size=?, toppings=?, quantity=?, total_price=?
                WHERE id=?
            """, (name_var.get(), phone_var.get(), size_var.get(),
                  toppings_var.get(), qty_var.get(), new_total, order_id))
            conn.commit()
            conn.close()
            load_orders()
            messagebox.showinfo("Updated", "Order updated successfully.")
            edit_win.destroy()

        Button(edit_win, text="Save Changes", command=save_changes).pack(pady=10)

    def view_receipt():
        selection = orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Order", "Please select an order to view.")
            return
        order_id = int(orders_listbox.get(selection[0]).split('|')[0].split(':')[1].strip())

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        show_receipt(row[2], row[3], row[4], row[5].split(","), row[6], row[7], row[8])

    def logout():
        admin.destroy()
        import main
        main.__name__ == "__main__" and main

    Button(admin, text="Delete Order", bg="red", fg="white", command=delete_order).place(x=650, y=100)
    Button(admin, text="Edit Order", bg="orange", fg="white", command=edit_order).place(x=650, y=150)
    Button(admin, text="View Receipt", bg="white", fg="black", command=view_receipt).place(x=650, y=200)
    Button(admin, text="Logout", bg="gray", fg="white", command=logout).place(x=650, y=250)

    load_orders()
    admin.mainloop()