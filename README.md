# Telegram Wallet Bot

## Project Overview

A Telegram bot for managing cryptocurrency wallets and balances. Key features include wallet binding (TON, TRC20), balance tracking, deposits, withdrawals, and interaction via Telegram commands.

---

## Features

1. **Wallet Management:**
   - Bind wallets for TON and TRC20 networks.
   - Validate TON wallet addresses with regex.

2. **Balance Operations:**
   - Create, update, deposit, or withdraw USDT balances.
   - Fetch the current balance.

3. **Logging and Animations:**
   - Logs wallet and balance activities.
   - Displays state changes with stickers.

---

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone <REPO_URL>
   cd <PROJECT_NAME>
   ```

2. **Install Dependencies:**
   Ensure Python 3.10+ is installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Define these in `.env` or directly in the script:
   - `TOKEN`: Telegram bot token.
   - `CHANNEL_ID`, `WITHDRAW_GROUP_ID`, `GROUP_CHAT_ID`: Telegram group/channel IDs.
   - `ETH_WALLET`, `TRON_WALLET`, `TON_WALLET`: Wallet addresses.
   - `API_TRON_KEY`, `API_TON_KEY`: TRON and TON API keys.
   - `TON_USDT_KEY`: API URL for TON/USDT exchange rate.

4. **Initialize Database:**
   Create the SQLite database with schema:
   ```bash
   sqlite3 database.db < schema.sql
   ```

5. **Run the Bot:**
   ```bash
   python bot.py
   ```

---

## Usage

- **Bind Wallet:**  
  Example for TON wallet binding:
  ```
  /set_wallet TON <wallet_address>
  ```

- **Check Balance:**  
  ```
  /get_balance
  ```

- **Deposit or Withdraw USDT:**  
  Deposit:
  ```
  /deposit <amount>
  ```
  Withdraw:
  ```
  /withdraw <amount>
  ```

---

## Files

- `database.py`: Handles database interactions (wallets, balances).
- `bot.py`: Main bot logic.
- `requirements.txt`: Dependency list.

---

Let me know if additional details are needed!