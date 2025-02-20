# 🤖 Telegram Wallet Bot

A sophisticated Telegram bot for managing cryptocurrency wallets and balances, supporting TON and TRC20 networks. Built with Python and aiogram framework.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### 💼 Wallet Management
- Secure wallet binding for TON and TRC20 networks
- Advanced address validation with regex patterns
- Multi-wallet support per user
- Automated wallet ownership verification

### 💰 Balance Operations
- Real-time USDT balance tracking
- Secure deposit and withdrawal system
- Transaction verification with blockchain APIs
- Support for both TON and TRON USDT transfers

### 🔐 Security
- Robust transaction validation
- Secure state management
- Rate limiting and spam protection
- Automated verification processes

### 📊 Additional Features
- Real-time logging system
- Interactive sticker animations
- CEX deposit support
- Multi-currency conversion

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- SQLite3
- Telegram Bot Token
- TON/TRON API Keys

### Installation

1. **Clone the Repository**
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
