from cryptography.fernet import Fernet
import os

# Function to generate a key and save it in a file (only once)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key from the file
def load_key():
    return open("secret.key", "rb").read()

# Function to encrypt the password
def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Function to decrypt the password
def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Function to save the password to a file
def save_password(website, password):
    encrypted_password = encrypt_password(password)
    with open("passwords.txt", "a") as file:
        file.write(f"{website}|{encrypted_password.decode()}\n")

# Function to view the stored passwords
def view_passwords():
    if not os.path.exists("passwords.txt"):
        print("No passwords saved yet.")
        return

    with open("passwords.txt", "r") as file:
        for line in file:
            website, encrypted_password = line.strip().split("|")
            decrypted_password = decrypt_password(encrypted_password.encode())
            print(f"Website: {website} - Password: {decrypted_password}")

# Main function to run the password manager
def password_manager():
    if not os.path.exists("secret.key"):
        print("No encryption key found. Generating a new key...")
        generate_key()

    while True:
        print("\nPassword Manager")
        print("1. Add a new password")
        print("2. View saved passwords")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            website = input("Enter the website/service name: ")
            password = input("Enter the password: ")
            save_password(website, password)
            print(f"Password for {website} saved successfully!")
        elif choice == '2':
            view_passwords()
        elif choice == '3':
            print("Exiting the password manager.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the password manager
if __name__ == "__main__":
    password_manager()
