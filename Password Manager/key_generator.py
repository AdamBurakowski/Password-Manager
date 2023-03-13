# with this script you can generate new key for the password manager
# but remember that passwords generated with other keys won't work
from cryptography.fernet import Fernet


def main():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


if __name__ == "__main__":
    main()
