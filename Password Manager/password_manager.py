import random as r
import os
from cryptography.fernet import Fernet

# This creates a string variable that stores the name of a directory where passwords will be stored.
passwords_folder = "passwords"


# This is a function that reads in a key from a file named "key.key" and returns it.
def load_key():
	file = open("key.key", "rb")
	key = file.read()
	file.close()
	return key


# This is a function that prompts the user to enter information about a new password (platform, username, desired length, etc.)
# and generates a random password based on that information.
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


# This for loop is used to generate a random password.
# It repeats num_of_characters times (which is set by the user) and randomly selects characters to add to the password
# based on the types of characters specified by the user.
	for times in range(num_of_characters):
		character = str(types_of_characters[r.randint(0, len(types_of_characters) - 1)])
		if character == "s_l":
			password += english_alphabet[r.randint(0, len(english_alphabet) - 1)]
		elif character == "c_l":
			password += english_alphabet[r.randint(0, len(english_alphabet) - 1)].upper()
		else:
			password += str(r.randint(0, 9))
	if not os.path.exists(passwords_folder):  # This creates the passwords directory if it doesn't already exist.
		os.makedirs(passwords_folder)
	os.chdir(passwords_folder)
	# This creates a new file in the passwords directory with a unique name based on the number of files already in the directory.
	# It then writes encrypted data to the file.
	with open(f"password{len(os.listdir()) + 1}", "x") as f:
		f.write(f"{str(fernet.encrypt(platform.encode()).decode())}\n{fernet.encrypt(username.encode()).decode()}\n{str(fernet.encrypt(password.encode()).decode())}")


# This is a function that reads in encrypted data from the password files, decrypts it, and displays the decrypted information to the user.
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

# This prompts the user to enter a master password, combines it with the key loaded from the "key.key" file,
# and creates a new Fernet object for encrypting and decrypting data.
master_password = input("Password: ")
key = load_key() + master_password.encode()
fernet = Fernet(key)


# This is the main function that prompts the user to choose between creating a new password or decrypting an existing one,
# and calls the appropriate function based on the user's choice.
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


# This checks whether the current script is being run as the main program (as opposed to being imported as a module by another program)
# and calls the main() function if it is.
if __name__ == "__main__":
	main()
