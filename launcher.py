#modules for Metis
import Data
import functions_cores

#MAIN
if functions_cores.Test_token(Data.secret_token):
	print("Your secret token is valid. Metis is launching... \n")
	import Metis

else :
	print("This is not a token. Please retry... \n")