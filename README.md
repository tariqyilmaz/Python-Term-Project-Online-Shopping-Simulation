# Python-Term-Project-Online-Shopping-Simulation
Shopping Simulation Project
This is a simple e-commerce and shop management system built with Python. I organized the code into different modules (cart, catalog, orders, admin) to simulate how a real-world application handles data.

🌟 Features
Shopping Experience: You can browse products, add specific quantities to your cart, and the system checks if there is enough stock.

Math Accuracy: I used the Decimal library for all price calculations to avoid those weird rounding errors you sometimes get with floats.

Discounts & Tax: It automatically calculates VAT and allows you to use promo codes for discounts.

Orders & Receipts: Once a purchase is finished, it generates a unique order ID and saves a text-based receipt in the receipts/ folder.

Admin Panel: There is a hidden dashboard (password: 1234) where you can check total earnings, see top-selling items, and add new products to the shop.

📁 Project Structure
main.py: The main entry point of the program.

data/: Holds the products.json file and the orders.json history.

receipts/: This is where all customer receipts are saved as .txt files.

Other .py files: These handle the "behind the scenes" logic for the cart, catalog, and admin tools.

🛠 How to Run
Make sure you have Python installed.

Check that the data/ and receipts/ folders exist in your project directory.

Important: Make sure data/orders.json contains at least an empty list [] so the program doesn't crash on the first run.

Run the project by typing python main.py in your terminal.
