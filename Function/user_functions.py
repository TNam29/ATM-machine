from Database.db_config import get_db_connection

class UserFunctions:
    DENOMINATIONS = [500000, 200000, 100000, 50000, 20000, 10000]

    @staticmethod
    def register_user(username, password, full_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return False, "Username already exists"

            cursor.execute(
                "INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s)",
                (username, password, full_name)
            )
            conn.commit()
            return True, "Registration successful"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def authenticate_user(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT user_id, full_name, is_admin FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            if user:
                return True, {
                    'user_id': user[0],
                    'full_name': user[1],
                    'is_admin': user[2]
                }
            return False, "Invalid username or password"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_balance(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
            balance = cursor.fetchone()[0]
            return True, balance
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def withdraw(user_id, amount):
        if amount % 10000 != 0:
            return False, "Amount must be a multiple of 10,000"

        if amount <= 0:
            return False, "Amount must be positive"

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT balance FROM users WHERE user_id = %s FOR UPDATE", (user_id,))
            balance = cursor.fetchone()[0]

            if balance - amount < 50000:
                return False, "Minimum balance must be 50,000 after withdrawal"

            cursor.execute("SELECT denomination, quantity FROM banknotes ORDER BY denomination DESC")
            banknotes = {row[0]: row[1] for row in cursor.fetchall()}

            remaining = amount
            withdrawal_notes = {}

            for denom in sorted(banknotes.keys(), reverse=True):
                if remaining <= 0:
                    break
                if banknotes[denom] > 0 and denom <= remaining:
                    count = min(remaining // denom, banknotes[denom])
                    withdrawal_notes[denom] = count
                    remaining -= denom * count

            if remaining != 0:
                return False, "ATM doesn't have enough bills to process this withdrawal"

            cursor.execute(
                "UPDATE users SET balance = balance - %s WHERE user_id = %s",
                (amount, user_id)
            )

            for denom, count in withdrawal_notes.items():
                cursor.execute(
                    "UPDATE banknotes SET quantity = quantity - %s WHERE denomination = %s",
                    (count, denom)
                )

            cursor.execute(
                "INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, 'withdrawal', %s)",
                (user_id, amount)
            )

            conn.commit()
            return True, withdrawal_notes
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def transfer(sender_id, recipient_username, amount):
        if amount <= 0:
            return False, "Amount must be positive"

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT balance FROM users WHERE user_id = %s FOR UPDATE", (sender_id,))
            sender_balance = cursor.fetchone()[0]

            if sender_balance - amount < 50000:
                return False, "Minimum balance must be 50,000 after transfer"

            cursor.execute("SELECT user_id FROM users WHERE username = %s FOR UPDATE", (recipient_username,))
            recipient = cursor.fetchone()
            if not recipient:
                return False, "Recipient not found"
            recipient_id = recipient[0]

            if sender_id == recipient_id:
                return False, "Cannot transfer to yourself"

            cursor.execute(
                "UPDATE users SET balance = balance - %s WHERE user_id = %s",
                (amount, sender_id)
            )

            cursor.execute(
                "UPDATE users SET balance = balance + %s WHERE user_id = %s",
                (amount, recipient_id)
            )

            cursor.execute(
                "INSERT INTO transactions (user_id, transaction_type, amount, recipient_id) VALUES (%s, 'transfer_sent', %s, %s)",
                (sender_id, amount, recipient_id)
            )

            cursor.execute(
                "INSERT INTO transactions (user_id, transaction_type, amount, recipient_id) VALUES (%s, 'transfer_received', %s, %s)",
                (recipient_id, amount, sender_id)
            )

            conn.commit()
            return True, "Transfer successful"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def change_pin(user_id, new_pin):
        if len(new_pin) != 6 or not new_pin.isdigit():
            return False, "PIN must be 6 digits"

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET password = %s WHERE user_id = %s",
                (new_pin, user_id)
            )

            cursor.execute(
                "INSERT INTO transactions (user_id, transaction_type) VALUES (%s, 'pin_change')",
                (user_id,)
            )

            conn.commit()
            return True, "PIN changed successfully"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deposit(user_id, amount, deposit_notes):
        if amount <= 10000:
            return False, "Minimum deposit is 10,000"

        calculated_amount = sum(denom * count for denom, count in deposit_notes.items())
        if calculated_amount != amount:
            return False, "Deposit notes don't match the amount"

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET balance = balance + %s WHERE user_id = %s",
                (amount, user_id)
            )

            for denom, count in deposit_notes.items():
                cursor.execute(
                    "UPDATE banknotes SET quantity = quantity + %s WHERE denomination = %s",
                    (count, denom)
                )

            cursor.execute(
                "INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, 'deposit', %s)",
                (user_id, amount)
            )

            conn.commit()
            return True, "Deposit successful"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_transaction_history(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT t.transaction_type, t.amount, t.transaction_date, 
                       u.username as recipient_name
                FROM transactions t
                LEFT JOIN users u ON t.recipient_id = u.user_id
                WHERE t.user_id = %s
                ORDER BY t.transaction_date DESC
                LIMIT 20
            """, (user_id,))

            transactions = []
            for row in cursor.fetchall():
                transactions.append({
                    'type': row[0],
                    'amount': row[1],
                    'date': row[2],
                    'recipient': row[3]
                })

            return True, transactions
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
