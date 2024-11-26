import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            self.connection.close()
    

    def check_wallet(self, user_id):
        try:
            wallet_data = self.cursor.execute("SELECT wallet_ton, wallet_trc20 FROM wallets WHERE user_id = ?", (user_id,)).fetchone()
            logger.debug(f"Wallet data for user {user_id}: {wallet_data}")
            return wallet_data
        except sqlite3.Error as e:
            logger.error(f"Error getting wallet data for user {user_id}: {e}")
            return None
        
    def create_wallet_ton(self, user_id, wallet_ton):
        try:
            try: 
                result = self.cursor.execute("INSERT INTO wallets (user_id, wallet_ton) VALUES (?, ?)", (user_id, wallet_ton)).fetchone()
                logger.debug(f"Wallet data for user {user_id}: {result}")
            except:
                result = self.cursor.execute("UPDATE wallets SET wallet_ton = ? WHERE user_id = ?", (wallet_ton, user_id)).fetchone()
            self.connection.commit()
            return result
        except sqlite3.Error as e:
            logger.error(f"Error creating wallet data for user {user_id}: {e}")
            return None

    def create_wallet_tron(self, user_id, wallet_trc20):
        try:
            try: 
                result = self.cursor.execute("INSERT INTO wallets (user_id, wallet_trc20) VALUES (?, ?)", (user_id, wallet_trc20)).fetchone()
                logger.debug(f"Wallet data for user {user_id}: {result}")
            except:
                result = self.cursor.execute("UPDATE wallets SET wallet_trc20 = ? WHERE user_id = ?", (wallet_trc20, user_id)).fetchone()
            self.connection.commit()
            return result
        except sqlite3.Error as e:
            logger.error(f"Error creating wallet data for user {user_id}: {e}")
            return None
    
    def create_balance(self, user_id):
        try:
            result = self.cursor.execute("INSERT INTO balance (user_id) VALUES (?, ?)", (user_id,)).fetchone()
            logger.debug(f"Wallet data for user {user_id}: {result}")
            
            return result
        except sqlite3.Error as e:
            logger.error(f"Error creating balance data for user {user_id}: {e}")
            return None
        
    def update_balance(self, user_id, balance):
        try:
            wallet_balance = self.get_balance(user_id)
            balance = balance + wallet_balance[0]

            self.cursor.execute("UPDATE balance SET usdt = ? WHERE user_id = ?", (balance, user_id))
            logger.debug(f"Wallet data for user {user_id}")

            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating balance data for user {user_id}: {e}")
            return None
        
    def withdraw_balance(self, user_id, balance):
        try:
            wallet_balance = self.get_balance(user_id)
            balance =  wallet_balance[0] - balance

            self.cursor.execute("UPDATE balance SET usdt = ? WHERE user_id = ?", (balance, user_id))
            logger.debug(f"Wallet data for user {user_id}")

            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error withdrawing balance data for user {user_id}: {e}")
            return None

    def get_balance(self, user_id):
        try:
            balance = self.cursor.execute("SELECT usdt FROM balance WHERE user_id = ?", (user_id,)).fetchone()
            logger.debug(f"Wallet data for user {user_id}: {balance}")
            return balance
        except sqlite3.Error as e:
            logger.error(f"Error getting balance data for user {user_id}: {e}")
            return None