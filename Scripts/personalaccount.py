import json
import hashlib
import os

class personalaccount:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump({}, file)

    def load_accounts(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def save_accounts(self, accounts):
        with open(self.file_path, 'w') as file:
            json.dump(accounts, file, indent=4)

    def create_account(self, username, password, role):
        accounts = self.load_accounts()
        if username in accounts:
            return "Аккаунт уже существует!"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        accounts[username] = {"password": hashed_password, "role": role}
        self.save_accounts(accounts)
        return "Аккаунт успешно создан!"

    def authenticate(self, username, password):
        accounts = self.load_accounts()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username in accounts and accounts[username]['password'] == hashed_password:
            return f"Добро пожаловать, {username}!"
        return "Неверный логин или пароль."

    def get_role(self, username):
        accounts = self.load_accounts()
        if username in accounts:
            return accounts[username].get("role", "unknown")
        return None
