from Database.db_config import get_db_connection

class AdminFunctions:
    DENOMINATIONS = [500000, 200000, 100000, 50000, 20000, 10000]
    
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT user_id, username, full_name, balance, is_admin, created_at 
                FROM users
                ORDER BY created_at DESC
            """)
            
            users = []
            for row in cursor.fetchall():
                users.append({
                    'user_id': row[0],
                    'username': row[1],
                    'full_name': row[2],
                    'balance': row[3],
                    'is_admin': row[4],
                    'created_at': row[5]
                })
            
            return True, users
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def add_user(username, password, full_name, is_admin=False):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if username exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return False, "Username already exists"
            
            # Insert new user
            cursor.execute(
                "INSERT INTO users (username, password, full_name, is_admin) VALUES (%s, %s, %s, %s)",
                (username, password, full_name, is_admin)
            )
            conn.commit()
            return True, "User added successfully"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update_user(user_id, username, full_name, is_admin):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if username exists (excluding current user)
            cursor.execute(
                "SELECT user_id FROM users WHERE username = %s AND user_id != %s",
                (username, user_id)
            )
            if cursor.fetchone():
                return False, "Username already exists"
            
            # Update user
            cursor.execute(
                "UPDATE users SET username = %s, full_name = %s, is_admin = %s WHERE user_id = %s",
                (username, full_name, is_admin, user_id)
            )
            conn.commit()
            return True, "User updated successfully"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                return False, "User not found"
            
            # Delete user
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            return True, "User deleted successfully"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_cash_balance():
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT denomination, quantity FROM banknotes ORDER BY denomination DESC")
            banknotes = {row[0]: row[1] for row in cursor.fetchall()}
            
            total = sum(denom * count for denom, count in banknotes.items())
            
            return True, {
                'banknotes': banknotes,
                'total': total
            }
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def add_cash(deposit_notes):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Update ATM cash
            for denom, count in deposit_notes.items():
                cursor.execute(
                    "UPDATE banknotes SET quantity = quantity + %s WHERE denomination = %s",
                    (count, denom)
                )
            
            conn.commit()
            return True, "Cash added successfully"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_all_transactions():
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT t.transaction_id, t.transaction_type, t.amount, t.transaction_date,
                       u1.username as sender_username, u1.full_name as sender_name,
                       u2.username as recipient_username, u2.full_name as recipient_name
                FROM transactions t
                JOIN users u1 ON t.user_id = u1.user_id
                LEFT JOIN users u2 ON t.recipient_id = u2.user_id
                ORDER BY t.transaction_date DESC
                LIMIT 100
            """)
            
            transactions = []
            for row in cursor.fetchall():
                transactions.append({
                    'transaction_id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'date': row[3],
                    'sender_username': row[4],
                    'sender_name': row[5],
                    'recipient_username': row[6],
                    'recipient_name': row[7]
                })
            
            return True, transactions
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()