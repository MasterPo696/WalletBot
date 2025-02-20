import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "app/db/sqldatabase.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._connect()

    def _connect(self) -> None:
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def check_wallet(self, user_id: int) -> tuple[str, str] | None:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user_id")

        try:
            wallet_data = self.cursor.execute(
                "SELECT wallet_ton, wallet_trc20 FROM wallets WHERE user_id = ?", 
                (user_id,)
            ).fetchone()
            logger.debug(f"Wallet data for user {user_id}: {wallet_data}")
            return wallet_data
        except sqlite3.Error as e:
            logger.error(f"Error getting wallet data for user {user_id}: {e}")
            return None
        
    def create_wallet_ton(self, user_id: int, wallet_ton: str) -> bool:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user_id")
        if not wallet_ton or not isinstance(wallet_ton, str):
            raise ValueError("Invalid wallet_ton address")

        try:
            self.cursor.execute("""
                INSERT INTO wallets (user_id, wallet_ton) 
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET wallet_ton = ?
            """, (user_id, wallet_ton, wallet_ton))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error creating/updating TON wallet for user {user_id}: {e}")
            return False

    def create_wallet_tron(self, user_id: int, wallet_trc20: str) -> bool:
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
    
    def create_balance(self, user_id: int) -> bool:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user_id")

        try:
            self.cursor.execute(
                "INSERT INTO balance (user_id, usdt) VALUES (?, 0)", 
                (user_id,)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error creating balance for user {user_id}: {e}")
            return False
        
    def update_balance(self, user_id: int, amount: float) -> bool:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user_id")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Invalid amount")

        try:
            current_balance = self.get_balance(user_id)
            if current_balance is None:
                return False
                
            new_balance = current_balance[0] + amount
            self.cursor.execute(
                "UPDATE balance SET usdt = ? WHERE user_id = ?",
                (new_balance, user_id)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating balance for user {user_id}: {e}")
            return False
        
    def withdraw_balance(self, user_id: int, balance: float) -> bool:
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

    def get_balance(self, user_id: int) -> float | None:
        try:
            balance = self.cursor.execute("SELECT usdt FROM balance WHERE user_id = ?", (user_id,)).fetchone()
            logger.debug(f"Wallet data for user {user_id}: {balance}")
            return balance
        except sqlite3.Error as e:
            logger.error(f"Error getting balance data for user {user_id}: {e}")
            return None