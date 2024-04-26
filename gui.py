import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database connection function
def db_connect():
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Replace with your host, usually 'localhost'
            database='olist',  # Your database name
            user='root',  # Your database username
            password='SQL@123'  # Your database password
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Execute read query
def execute_read_query(query, data=None):
    conn = db_connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(query, data or ())
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

# Execute write query
def execute_write_query(query, data):
    conn = db_connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute(query, data)
            conn.commit()
            return f"Query successful: {cursor.rowcount} rows affected."
        except mysql.connector.Error as e:
            st.error(f"SQL Error: {e}")  # Display SQL errors in Streamlit
            return f"An error occurred: {e}"
        finally:
            cursor.close()
            conn.close()


# Define your management functions, they should use 'st' to display on the main screen

def manage_categories():
    st.header("Category Management")
    action = st.radio("Action", ["Add", "Update", "Delete"])

    if action == "Add":
        with st.form("add_category"):
            product_category_name = st.text_input("Category Name")
            product_category_name_english = st.text_input("Category Name in English")
            submit_button = st.form_submit_button("Add Category")
            if submit_button:
                # Database code to add a category
                query = """
                INSERT INTO category_name_translation (product_category_name, product_category_name_english)
                VALUES (%s, %s)
                """
                result = execute_write_query(query, (product_category_name, product_category_name_english))
                st.success("Category added successfully!")

    elif action == "Update":
        with st.form("update_category"):
            category_name = st.selectbox("Select Category", [x[0] for x in execute_read_query("SELECT product_category_name FROM category_name_translation")])
            product_category_name_english = st.text_input("New Category Name in English", key="update_english_name")
            submit_button = st.form_submit_button("Update Category")
            if submit_button:
                # Database code to update a category
                query = """
                UPDATE category_name_translation SET product_category_name_english = %s WHERE product_category_name = %s
                """
                result = execute_write_query(query, (product_category_name_english, category_name))
                st.success("Category updated successfully!")

    elif action == "Delete":
        with st.form("delete_category"):
            category_name = st.selectbox("Select Category to Delete", [x[0] for x in execute_read_query("SELECT product_category_name FROM category_name_translation")], key="delete_category")
            submit_button = st.form_submit_button("Delete Category")
            if submit_button:
                # Database code to delete a category
                query = "DELETE FROM category_name_translation WHERE product_category_name = %s"
                result = execute_write_query(query, (category_name,))
                st.success("Category deleted successfully!")

def manage_products():
    st.header("Product Management")
    action = st.radio("Action", ["Add", "Update", "Delete"], key='product_action')

    if action == "Add":
        with st.form("add_product_form"):
            product_id = st.text_input("Product ID", max_chars=32)
            categories = execute_read_query("SELECT product_category_name FROM category_name_translation")
            product_category_name = st.selectbox("Category Name", [x[0] for x in categories])
            product_name_length = st.number_input("Product Name Length", min_value=0, max_value=100)
            product_description_length = st.number_input("Product Description Length", min_value=0, max_value=1000)
            product_photos_qty = st.number_input("Product Photos Quantity", min_value=0, max_value=10)
            product_weight_g = st.number_input("Product Weight (g)", min_value=0.0, step=0.1)
            product_length_cm = st.number_input("Product Length (cm)", min_value=0.0, step=0.1)
            product_height_cm = st.number_input("Product Height (cm)", min_value=0.0, step=0.1)
            product_width_cm = st.number_input("Product Width (cm)", min_value=0.0, step=0.1)
            submit_button = st.form_submit_button("Add Product")

            if submit_button:
                if len(product_id) != 32:
                    st.error("Error: The Product ID must have exactly 32 characters.")
                else:
                    query = """
                    INSERT INTO products (product_id, product_category_name, product_name_length, product_description_length, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    try:
                        result = execute_write_query(query, (product_id, product_category_name, product_name_length, product_description_length, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm))
                        st.success("Product added successfully!")
                    except Error as e:
                        st.error(f"An error occurred: {e}")

    elif action == "Update":
        with st.form("update_product_form"):
            product_list = execute_read_query("SELECT product_id FROM products")
            selected_product = st.selectbox("Select Product ID", [p[0] for p in product_list])
            categories = execute_read_query("SELECT product_category_name FROM category_name_translation")
            new_product_category_name = st.selectbox("New Category Name", [x[0] for x in categories])
            new_product_name_length = st.number_input("New Product Name Length", min_value=0, max_value=100)
            new_product_description_length = st.number_input("New Product Description Length", min_value=0, max_value=1000)
            new_product_photos_qty = st.number_input("New Product Photos Quantity", min_value=0, max_value=10)
            new_product_weight_g = st.number_input("New Product Weight (g)", min_value=0.0, step=0.1)
            new_product_length_cm = st.number_input("New Product Length (cm)", min_value=0.0, step=0.1)
            new_product_height_cm = st.number_input("New Product Height (cm)", min_value=0.0, step=0.1)
            new_product_width_cm = st.number_input("New Product Width (cm)", min_value=0.0, step=0.1)
            submit_button = st.form_submit_button("Update Product")

            if submit_button:
                query = """
                UPDATE products SET
                    product_category_name = %s, 
                    product_name_length = %s, 
                    product_description_length = %s, 
                    product_photos_qty = %s, 
                    product_weight_g = %s, 
                    product_length_cm = %s, 
                    product_height_cm = %s, 
                    product_width_cm = %s
                WHERE product_id = %s
                """
                try:
                    result = execute_write_query(query, (new_product_category_name, new_product_name_length, new_product_description_length, new_product_photos_qty, new_product_weight_g, new_product_length_cm, new_product_height_cm, new_product_width_cm, selected_product))
                    st.success("Product updated successfully!")
                except Error as e:
                    st.error(f"An error occurred: {e}")

    elif action == "Delete":
        with st.form("delete_product_form"):
            product_list = execute_read_query("SELECT product_id FROM products")
            selected_product = st.selectbox("Select Product ID to Delete", [p[0] for p in product_list])
            submit_button = st.form_submit_button("Delete Product")

            if submit_button:
                query = "DELETE FROM products WHERE product_id = %s"
                try:
                    result = execute_write_query(query, (selected_product,))
                    st.success("Product deleted successfully!")
                except Error as e:
                    st.error(f"An error occurred: {e}")


def manage_customers():
    st.header("Customer Management")
    action = st.radio("Action", ["Add", "Update", "Delete"], key='customer_action')

    if action == "Add":
        with st.form("add_customer_form"):
            customer_perorder_id = st.text_input("Customer Per-Order ID", max_chars=32)
            customer_unique_id = st.text_input("Customer Unique ID", max_chars=32)
            customer_zip_code_prefix = st.text_input("Zip Code Prefix")
            customer_city = st.text_input("City")
            customer_state = st.text_input("State", max_chars=2)
            submit_button = st.form_submit_button("Add Customer")

            if submit_button:
                if len(customer_perorder_id) != 32 or len(customer_unique_id) != 32:
                    st.error("Error: The 'Customer Per-Order ID' and 'Customer Unique ID' must each have exactly 32 characters.")
                else:
                    query = """
                    INSERT INTO customers (customer_perorder_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    try:
                        result = execute_write_query(query, (customer_perorder_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state))
                        st.success("Customer added successfully!")
                    except Error as e:
                        st.error(f"An error occurred: {e}")

    elif action == "Update":
        with st.form("update_customer_form"):
            customer_list = execute_read_query("SELECT customer_perorder_id FROM customers")
            selected_customer = st.selectbox("Choose a Customer ID", [c[0] for c in customer_list])
            
            # Allow the user to decide which fields to update
            st.markdown("#### Update Fields for Customer")
            new_unique_id = st.text_input("New Customer Unique ID", max_chars=32, key='new_unique_id')
            new_zip_code_prefix = st.text_input("New Zip Code Prefix", key='new_zip_code')
            new_city = st.text_input("New City", key='new_city')
            new_state = st.text_input("New State", max_chars=2, key='new_state')
            fields_to_update = {}
            if new_unique_id:
                fields_to_update['customer_unique_id'] = new_unique_id
            if new_zip_code_prefix:
                fields_to_update['customer_zip_code_prefix'] = new_zip_code_prefix
            if new_city:
                fields_to_update['customer_city'] = new_city
            if new_state:
                fields_to_update['customer_state'] = new_state

            submit_button = st.form_submit_button("Update Customer")

            if submit_button and fields_to_update:
                update_clauses = ', '.join(f"{k} = %s" for k in fields_to_update.keys())
                values = list(fields_to_update.values()) + [selected_customer]
                query = f"UPDATE customers SET {update_clauses} WHERE customer_perorder_id = %s"
                try:
                    result = execute_write_query(query, values)
                    st.success("Customer updated successfully!")
                except Error as e:
                    st.error(f"An error occurred: {e}")

    elif action == "Delete":
        with st.form("delete_customer_form"):
            customer_list = execute_read_query("SELECT customer_perorder_id FROM customers")
            selected_customer = st.selectbox("Choose a Customer ID to Delete", [c[0] for c in customer_list], key='del_customer')
            submit_button = st.form_submit_button("Delete Customer")

            if submit_button:
                query = "DELETE FROM customers WHERE customer_perorder_id = %s"
                try:
                    result = execute_write_query(query, (selected_customer,))
                    st.success("Customer deleted successfully!")
                except Error as e:
                    st.error(f"An error occurred: {e}")



def manage_orders():
    st.header("Order Management")
    action = st.radio("Action", ["Add", "Update", "Delete"], key='order_action')

    if action == "Add":
        with st.form("add_order_form"):
            order_id = st.text_input("Order ID")
            customer_perorder_id = st.selectbox("Customer Per-Order ID", [x[0] for x in execute_read_query("SELECT customer_perorder_id FROM customers")])
            order_status = st.selectbox("Order Status", ["pending", "delivered", "canceled", "returned"])
            order_purchase_timestamp = st.date_input("Purchase Timestamp")
            order_approved_at = st.date_input("Order Approved At")
            order_delivered_carrier_date = st.date_input("Order Delivered Carrier Date")
            order_estimated_delivery_date = st.date_input("Order Estimated Delivery Date")
            submit_button = st.form_submit_button("Add Order")

            if submit_button:
                # Database code to add an order
                query = """
                INSERT INTO orders (order_id, customer_perorder_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_estimated_delivery_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                result = execute_write_query(query, (order_id, customer_perorder_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_estimated_delivery_date))
                st.success("Order added successfully!")

    elif action == "Update":
        with st.form("update_order_form"):
            order_list = execute_read_query("SELECT order_id FROM orders")
            order_id = st.selectbox("Choose an Order ID", [oid[0] for oid in order_list])
            new_status = st.selectbox("New Order Status", ["pending", "delivered", "canceled", "returned"], key='new_status')
            submit_button = st.form_submit_button("Update Order")

            if submit_button:
                # Database code to update an order
                query = "UPDATE orders SET order_status = %s WHERE order_id = %s"
                result = execute_write_query(query, (new_status, order_id))
                st.success("Order updated successfully!")

    elif action == "Delete":
        with st.form("delete_order_form"):
            order_list = execute_read_query("SELECT order_id FROM orders")
            order_id = st.selectbox("Choose an Order ID to Delete", [oid[0] for oid in order_list], key='del_order')
            submit_button = st.form_submit_button("Delete Order")

            if submit_button:
                # Database code to delete an order
                query = "DELETE FROM orders WHERE order_id = %s"
                result = execute_write_query(query, (order_id,))
                st.success("Order deleted successfully!")


def manage_sellers():
    st.header("Seller Management")
    action = st.radio("Action", ["Add", "Update", "Delete"], key='seller_action')

    if action == "Add":
        with st.form("add_seller_form"):
            seller_id = st.text_input("Seller ID")
            seller_zip_code_prefix = st.text_input("Zip Code Prefix")
            seller_city = st.text_input("City")
            seller_state = st.text_input("State", max_chars=2)
            submit_button = st.form_submit_button("Add Seller")

            if submit_button:
                query = """
                INSERT INTO sellers (seller_id, seller_zip_code_prefix, seller_city, seller_state)
                VALUES (%s, %s, %s, %s)
                """
                result = execute_write_query(query, (seller_id, seller_zip_code_prefix, seller_city, seller_state))
                st.success("Seller added successfully!")

    elif action == "Update":
        with st.form("update_seller_form"):
            seller_list = execute_read_query("SELECT seller_id FROM sellers")
            seller_id = st.selectbox("Choose a Seller ID", [s[0] for s in seller_list])
            new_city = st.text_input("New City", key='new_seller_city')
            new_state = st.text_input("New State", max_chars=2, key='new_seller_state')
            submit_button = st.form_submit_button("Update Seller")

            if submit_button:
                query = "UPDATE sellers SET seller_city = %s, seller_state = %s WHERE seller_id = %s"
                result = execute_write_query(query, (new_city, new_state, seller_id))
                st.success("Seller updated successfully!")

    elif action == "Delete":
        with st.form("delete_seller_form"):
            seller_list = execute_read_query("SELECT seller_id FROM sellers")
            seller_id = st.selectbox("Choose a Seller ID to Delete", [s[0] for s in seller_list], key='del_seller')
            submit_button = st.form_submit_button("Delete Seller")

            if submit_button:
                query = "DELETE FROM sellers WHERE seller_id = %s"
                result = execute_write_query(query, (seller_id,))
                st.success("Seller deleted successfully!")


def manage_order_items():
    st.header("Order Item Management")
    action = st.radio("Action", ["Add", "Update", "Delete"], key='order_item_action')

    if action == "Add":
        with st.form("add_order_item_form"):
            order_list = execute_read_query("SELECT order_id FROM orders")
            product_list = execute_read_query("SELECT product_id FROM products")
            seller_list = execute_read_query("SELECT seller_id FROM sellers")
            order_id = st.selectbox("Order ID", [o[0] for o in order_list])
            item_number = st.number_input("Item Number", min_value=1)
            product_id = st.selectbox("Product ID", [p[0] for p in product_list])
            seller_id = st.selectbox("Seller ID", [s[0] for s in seller_list])
            shipping_limit_date = st.date_input("Shipping Limit Date")
            price = st.number_input("Price", min_value=0.0, step=0.01)
            freight_value = st.number_input("Freight Value", min_value=0.0, step=0.01)
            submit_button = st.form_submit_button("Add Order Item")

            if submit_button:
                query = """
                INSERT INTO order_items (order_id, item_number, product_id, seller_id, shipping_limit_date, price, freight_value)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                result = execute_write_query(query, (order_id, item_number, product_id, seller_id, shipping_limit_date, price, freight_value))
                st.success("Order item added successfully!")

    elif action == "Update":
        with st.form("update_order_item_form"):
            order_item_list = execute_read_query("SELECT order_id, item_number FROM order_items")
            order_item_id = st.selectbox("Select Order Item", ["{}-{}".format(oi[0], oi[1]) for oi in order_item_list], key='update_order_item')
            new_price = st.number_input("New Price", min_value=0.0, step=0.01, key='new_item_price')
            new_freight_value = st.number_input("New Freight Value", min_value=0.0, step=0.01, key='new_freight_value')
            submit_button = st.form_submit_button("Update Order Item")

            if submit_button:
                order_id, item_number = order_item_id.split('-')
                query = """
                UPDATE order_items SET price = %s, freight_value = %s WHERE order_id = %s AND item_number = %s
                """
                result = execute_write_query(query, (new_price, new_freight_value, order_id, item_number))
                st.success("Order item updated successfully!")

    elif action == "Delete":
        with st.form("delete_order_item_form"):
            order_item_list = execute_read_query("SELECT order_id, item_number FROM order_items")
            order_item_id = st.selectbox("Select Order Item to Delete", ["{}-{}".format(oi[0], oi[1]) for oi in order_item_list], key='delete_order_item')
            submit_button = st.form_submit_button("Delete Order Item")

            if submit_button:
                order_id, item_number = order_item_id.split('-')
                query = "DELETE FROM order_items WHERE order_id = %s AND item_number = %s"
                result = execute_write_query(query, (order_id, item_number))
                st.success("Order item deleted successfully!")


def manage_order_payments():
    st.header("Order Payments Management")
    action = st.radio("Action", ["Add", "Update", "Delete"], key='order_payment_action')

    if action == "Add":
        with st.form("add_order_payment_form"):
            order_list = execute_read_query("SELECT order_id FROM orders")
            order_id = st.selectbox("Order ID", [o[0] for o in order_list])
            payment_sequential = st.number_input("Payment Sequential", min_value=1, key='payment_seq_add')
            payment_type = st.selectbox("Payment Type", ['credit_card', 'debit_card', 'voucher', 'boleto', 'not_defined'])
            payment_installments = st.number_input("Payment Installments", min_value=1)
            payment_value = st.number_input("Payment Value", min_value=0.0, step=0.01)
            submit_button = st.form_submit_button("Add Payment")

            if submit_button:
                query = """
                INSERT INTO order_payments (order_id, payment_sequential, payment_type, payment_installments, payment_value)
                VALUES (%s, %s, %s, %s, %s)
                """
                result = execute_write_query(query, (order_id, payment_sequential, payment_type, payment_installments, payment_value))
                st.success("Order payment added successfully!")

    elif action == "Update":
        with st.form("update_order_payment_form"):
            payment_keys = execute_read_query("SELECT order_id, payment_sequential FROM order_payments")
            selected_payment = st.selectbox("Select Payment", ["{}-{}".format(pk[0], pk[1]) for pk in payment_keys], key='update_payment')
            new_payment_value = st.number_input("New Payment Value", min_value=0.0, step=0.01, key='new_payment_value')
            submit_button = st.form_submit_button("Update Payment")

            if submit_button:
                selected_order_id, selected_payment_seq = selected_payment.split('-')
                query = """
                UPDATE order_payments SET payment_value = %s WHERE order_id = %s AND payment_sequential = %s
                """
                result = execute_write_query(query, (new_payment_value, selected_order_id, selected_payment_seq))
                st.success("Order payment updated successfully!")

    elif action == "Delete":
        with st.form("delete_order_payment_form"):
            payment_keys = execute_read_query("SELECT order_id, payment_sequential FROM order_payments")
            selected_payment = st.selectbox("Select Payment to Delete", ["{}-{}".format(pk[0], pk[1]) for pk in payment_keys], key='delete_payment')
            submit_button = st.form_submit_button("Delete Payment")

            if submit_button:
                selected_order_id, selected_payment_seq = selected_payment.split('-')
                query = "DELETE FROM order_payments WHERE order_id = %s AND payment_sequential = %s"
                result = execute_write_query(query, (selected_order_id, selected_payment_seq))
                st.success("Order payment deleted successfully!")



import re
import pandas as pd

def manage_order_reviews():
    st.header("Order Reviews Management")
    action = st.radio("Action", ["Add", "Update", "Delete"], key='order_review_action')

    if action == "Add":
        with st.form("add_order_review_form"):
            review_id = st.text_input("Review ID")
            order_list = execute_read_query("SELECT order_id FROM orders")
            order_id = st.selectbox("Order ID", [o[0] for o in order_list])
            review_score = st.slider("Review Score", 1, 5)
            review_comment_title = st.text_input("Comment Title")
            review_comment_message = st.text_area("Comment Message")
            review_creation_date = st.date_input("Review Creation Date")
            submit_button = st.form_submit_button("Add Review")

            if submit_button:
                query = """
                INSERT INTO order_reviews (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                # Note that the review_answer_timestamp is not included in the INSERT statement
                try:
                    result = execute_write_query(query, (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date))
                    st.success("Order review added successfully!")
                except Error as e:
                    st.error(f"An error occurred: {e}")

    elif action == "Update":
        with st.form("update_order_review_form"):
            review_list = execute_read_query("SELECT review_id FROM order_reviews")
            selected_review = st.selectbox("Select Review ID", [r[0] for r in review_list], key='update_review')
            new_review_score = st.slider("New Review Score", 1, 5)
            new_review_comment_title = st.text_input("New Comment Title", key='new_review_title')
            new_review_comment_message = st.text_area("New Comment Message", key='new_review_message')
            submit_button = st.form_submit_button("Update Review")

            if submit_button:
                query = """
                UPDATE order_reviews 
                SET review_score = %s, 
                    review_comment_title = %s, 
                    review_comment_message = %s 
                WHERE review_id = %s
                """
                try:
                    result = execute_write_query(query, (new_review_score, new_review_comment_title, new_review_comment_message, selected_review))
                    st.success("Order review updated successfully!")
                except Error as e:
                    st.error(f"An error occurred: {e}")

    elif action == "Delete":
        with st.form("delete_order_review_form"):
            review_list = execute_read_query("SELECT review_id FROM order_reviews")
            selected_review = st.selectbox("Select Review ID to Delete", [r[0] for r in review_list], key='delete_review')
            submit_button = st.form_submit_button("Delete Review")

            if submit_button:
                query = "DELETE FROM order_reviews WHERE review_id = %s"
                try:
                    result = execute_write_query(query, (selected_review,))
                    st.success("Order review deleted successfully!")
                except Error as e:
                    st.error(f"An error occurred: {e}")



# Main app interface
def main():
    st.sidebar.title("Database Management")

    # Sidebar navigation
    options = ["Manage Categories", "Manage Products", "Manage Customers", "Manage Orders",
               "Manage Sellers", "Manage Order Items", "Manage Order Payments", "Manage Order Reviews"]
    choice = st.sidebar.selectbox("Select an option", options)

    # Display the corresponding management function in the main area
    if choice == "Manage Categories":
        manage_categories()
    elif choice == "Manage Products":
        manage_products()
    elif choice == "Manage Customers":
        manage_customers()
    elif choice == "Manage Orders":
        manage_orders()
    elif choice == "Manage Sellers":
        manage_sellers()
    elif choice == "Manage Order Items":
        manage_order_items()
    elif choice == "Manage Order Payments":
        manage_order_payments()
    elif choice == "Manage Order Reviews":
        manage_order_reviews()

if __name__ == "__main__":
    main()