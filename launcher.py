import functions_cores
secret_token = ""
while not functions_cores.Test_token(secret_token):
	if not secret_token == "":
		print("This is not a token. Please retry... \n" + str(len(secret_token)))
	secret_token = input("Please enter your Secret Token here:")
	print("\n")

print("Your secret token is valid. Metis is launching... \n")

print("Sorry, Metis is not avalidable right now...")