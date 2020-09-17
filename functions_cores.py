def Test_token(secretToken):
 	return len(secretToken) == 59

def read_last():
	file = open("last_new.txt",'r')
	content = file.read()
	file.close()
	content = int(content)
	file = open("last_new.txt",'w')
	if content == 2:
		file.write("0")
	else:
		file.write(str(content+1))
	file.close()
	return int(content)

"""
in_list permet de savoir si un arg se trouve dans une liste lis
return -> bolean
lis    <- list[a]
arg    <- a

f <= anonymus function
"""
def in_list(lis,arg, f=(lambda x : x)):
	length = len(lis)
	i = 0
	while (i<length and f(lis[i]) != arg):
		i += 1
	return i<length