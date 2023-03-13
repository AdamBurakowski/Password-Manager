import random as r
import os
from cryptography.fernet import Fernet

# path to directory with passwords
passwords_folder = "passwords"


# function responsible for loading tey used for encryption and decryption of data
def load_key():
	file = open("key.key", "rb")
	key = file.read()
	file.close()
	return key


# function responsible for creating new data and encrypting it
def create_password():
	platform = input("Type name of the platform in which you are creating account: ")
	username = input("Type your username on that platform: ")
	num_of_characters = int(input("Type how long do you want your password to be: "))
	english_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
						"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
	types_of_characters = ["s_l"]  # list containing types of characters possible to use while generating password
	password = ""
	if input("Do you want capital letters in your password y/n? ") == "y":
		types_of_characters.append("c_l")
	if input("Do you want numbers in your password y/n? ") == "y":
		types_of_characters.append("n")

# generating password
	for times in range(num_of_characters):
		character = str(types_of_characters[r.randint(0, len(types_of_characters) - 1)])
		if character == "s_l":
			password += english_alphabet[r.randint(0, len(english_alphabet) - 1)]
		elif character == "c_l":
			password += english_alphabet[r.randint(0, len(english_alphabet) - 1)].upper()
		else:
			password += str(r.randint(0, 9))
	if not os.path.exists(passwords_folder):  # creates passwords folder if not present
		os.makedirs(passwords_folder)
	os.chdir(passwords_folder)
	with open(f"password{len(os.listdir()) + 1}", "x") as f:
		# writing encrypted data to the new file
		f.write(f"{str(fernet.encrypt(platform.encode()).decode())}\n{fernet.encrypt(username.encode()).decode()}\n{str(fernet.encrypt(password.encode()).decode())}")


# function responsible for decrypting and showing data from passwords directory
def decrypt_password():
	descriptions = {1: "platform: ", 2: "username: ", 3: "password: "}  # tells program what to write depending on a line in a file
	files = os.listdir(passwords_folder)  # finds all files in a password directory
	os.chdir(passwords_folder)
	for file in files:
		line_count = 1
		with open(file, "r") as f:
			contents = f.readlines()
			for line in contents:
				line = line.strip()
				print(descriptions[line_count] + fernet.decrypt(line.encode()).decode())
				line_count += 1
			print("\n-------------------------------------------------------------------------------\n")


master_password = input("Password: ") # master password is used as part of a key
key = load_key() + master_password.encode()  # master password is combined with a key
fernet = Fernet(key)


# function responsible for choosing type of action
def main():
	valid_option = False
	while not valid_option:
		action = input(
			"Type \"c\" if you want to create new record, or \"d\" if you want to decrypt one of your current passwords (or q to quit) ")
		if action == "c":
			print("\n\n\n")
			create_password()
			valid_option = True
		elif action == "d":
			print("\n\n\n")
			decrypt_password()
			valid_option = True
		elif action == "q":
			valid_option = True
		else:
			print("Invalid command. Please try again.\n\n\n")


if __name__ == "__main__":
	main()
