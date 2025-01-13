import sqlite3

def delete_order(order_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    try:
        # Delete order from orders table
        c.execute('DELETE FROM orders WHERE orderId = ?', (order_id,))
        # Delete order from archive table
        c.execute('DELETE FROM archive WHERE orderId = ?', (order_id,))
        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

delete_order('1002108368732')
