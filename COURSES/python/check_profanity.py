import urllib.request

def read_text():
	quotes = open('/home/seth/Udacity_FullStack/Python/words.txt')
	file_content = quotes.read()
	file_content = file_content.replace(" ", "+")
	quotes.close()
	check_profanity(file_content)

def check_profanity(text_to_check):
	connection = urllib.request.urlopen('http://www.wdylike.appspot.com/?q='+text_to_check)
	output = connection.read() 
	connection.close()
	if output == b"true":
		print("Profanity Alert!!!")
	elif output == b"false":
		print("Everything is OK")
	else:
		print("Could not read your file. Something went wrong!")

read_text()