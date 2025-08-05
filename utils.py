from tkinter import Toplevel, Label

def show_receipt(name, phone, size, toppings, quantity, total, order_datetime):
    receipt_win = Toplevel()
    receipt_win.title("Order Receipt")
    receipt_win.geometry("350x400")
    receipt_win.config(bg="blue")

    Label(receipt_win, text="--- Pizza Order Receipt ---", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
    Label(receipt_win, text=f"Customer: {name}", bg="white").pack()
    Label(receipt_win, text=f"Phone: {phone}", bg="white").pack()
    Label(receipt_win, text=f"Date & Time: {order_datetime}", bg="white").pack(pady=5)
    Label(receipt_win, text=f"Pizza Size: {size}", bg="white").pack()
    Label(receipt_win, text=f"Toppings: {', '.join(toppings)}", bg="white").pack()
    Label(receipt_win, text=f"Quantity: {quantity}", bg="white").pack()
    Label(receipt_win, text=f"Total Price: ${total:.2f}", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
    Label(receipt_win, text="Thank you for your order!", bg="white", fg="green").pack(pady=20)