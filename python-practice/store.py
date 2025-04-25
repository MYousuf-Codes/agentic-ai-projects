import tkinter as tk
from tkinter import messagebox

class GeneralStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("General Store")

        # Store products and their details
        self.products = {
            "Apple": {"price": 2.5, "stock": 100},
            "Banana": {"price": 1.2, "stock": 150},
            "Bread": {"price": 1.5, "stock": 50},
            "Milk": {"price": 3.0, "stock": 75},
            "Eggs": {"price": 2.0, "stock": 60}
        }
        self.cart = {}

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Product List
        self.product_listbox = tk.Listbox(self.root, width=50, height=10)
        self.product_listbox.grid(row=0, column=0, padx=10, pady=10)

        for product in self.products:
            self.product_listbox.insert(tk.END, f"{product} - ${self.products[product]['price']} - Stock: {self.products[product]['stock']}")

        # Quantity Entry
        self.quantity_label = tk.Label(self.root, text="Enter Quantity:")
        self.quantity_label.grid(row=1, column=0, padx=10, pady=10)

        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add to Cart Button
        self.add_to_cart_button = tk.Button(self.root, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Cart Listbox
        self.cart_listbox = tk.Listbox(self.root, width=50, height=10)
        self.cart_listbox.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        # Checkout Button
        self.checkout_button = tk.Button(self.root, text="Checkout", command=self.checkout)
        self.checkout_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_to_cart(self):
        # Get the selected product and quantity
        selected_product = self.product_listbox.get(tk.ACTIVE).split(' - ')[0]
        quantity = self.quantity_entry.get()

        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Invalid Quantity", "Please enter a valid quantity.")
            return

        quantity = int(quantity)

        if selected_product not in self.products:
            messagebox.showerror("Product Not Found", "Selected product is not available.")
            return

        # Check stock availability
        if quantity > self.products[selected_product]["stock"]:
            messagebox.showerror("Insufficient Stock", f"Only {self.products[selected_product]['stock']} units are available.")
            return

        # Add to cart
        if selected_product in self.cart:
            self.cart[selected_product]["quantity"] += quantity
        else:
            self.cart[selected_product] = {"price": self.products[selected_product]["price"], "quantity": quantity}

        # Update product stock
        self.products[selected_product]["stock"] -= quantity

        # Clear the cart and quantity entry
        self.quantity_entry.delete(0, tk.END)
        self.update_cart()

    def update_cart(self):
        self.cart_listbox.delete(0, tk.END)

        total = 0
        for product, details in self.cart.items():
            self.cart_listbox.insert(tk.END, f"{product}: {details['quantity']} x ${details['price']} = ${details['price'] * details['quantity']}")
            total += details['price'] * details['quantity']

        self.cart_listbox.insert(tk.END, f"Total: ${total:.2f}")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Your cart is empty. Please add items to the cart.")
            return

        # Calculate total price
        total = sum(details['price'] * details['quantity'] for details in self.cart.values())

        # Ask for payment
        payment = simpledialog.askfloat("Checkout", f"Your total is ${total:.2f}. Enter payment amount:")

        if payment is None:
            return

        if payment < total:
            messagebox.showerror("Insufficient Funds", "You don't have enough money.")
        else:
            change = payment - total
            messagebox.showinfo("Payment Successful", f"Thank you for your purchase! Your change is ${change:.2f}")
            self.cart.clear()
            self.update_cart()

            # Reset the stock and cart
            self.reset_stock()

    def reset_stock(self):
        self.products = {
            "Apple": {"price": 2.5, "stock": 100},
            "Banana": {"price": 1.2, "stock": 150},
            "Bread": {"price": 1.5, "stock": 50},
            "Milk": {"price": 3.0, "stock": 75},
            "Eggs": {"price": 2.0, "stock": 60}
        }

        self.product_listbox.delete(0, tk.END)
        for product in self.products:
            self.product_listbox.insert(tk.END, f"{product} - ${self.products[product]['price']} - Stock: {self.products[product]['stock']}")

# Run the store app
if __name__ == "__main__":
    import tkinter.simpledialog as simpledialog
    root = tk.Tk()
    app = GeneralStoreApp(root)
    root.mainloop()
