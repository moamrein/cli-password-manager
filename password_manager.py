import sqlite3
from cryptography.fernet import Fernet

# Generate a key and write it to a file (Run this once)
# key = Fernet.generate_key()
# with open("secret.key", "wb") as key_file:
#     key_file.write(key)

# Load the encryption key
def load_key():
    return open("secret.key", "rb").read()

key = load_key()
cipher_suite = Fernet(key)

# Connect to SQLite Database
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS credentials (site TEXT, username TEXT, password TEXT)")
conn.commit()

def save_password(site, username, password):
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    cursor.execute("INSERT INTO credentials VALUES (?, ?, ?)", (site, username, encrypted_password))
    conn.commit()

def retrieve_password(site):
    cursor.execute("SELECT username, password FROM credentials WHERE site=?", (site,))
    result = cursor.fetchone()
    if result:
        username, encrypted_password = result
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        print(f"Site: {site}\nUsername: {username}\nPassword: {decrypted_password}")
    else:
        print("No credentials found.")

if __name__ == "__main__":
    while True:
        choice = input("1: Save Password\n2: Retrieve Password\n3: Exit\nChoose an option: ")
        if choice == "1":
            site = input("Enter site name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            save_password(site, username, password)
        elif choice == "2":
            site = input("Enter site name to retrieve credentials: ")
            retrieve_password(site)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
