class Myrot:

	def rotters(self, message):
		the_message = ""
		for ch in message:
			# ASCII lower 97-122 (a-z)
			char_ascii = ord(ch)
			if char_ascii >= 97 and char_ascii <=122:

				if (char_ascii + 13) >= 110 and (char_ascii + 13) <= 122:
					the_message = the_message + chr(char_ascii + 13)
				elif (char_ascii - 13) <= 109 and (char_ascii + 13) >= 97:
					the_message = the_message +  chr(char_ascii - 13)

			# ASCII lower 65-90 (A-Z)
			elif char_ascii >= 65 and char_ascii <= 90:
				if (char_ascii + 13) >= 78 and (char_ascii + 13) <= 90:
					the_message = the_message +  chr(char_ascii + 13)
				elif (char_ascii - 13) <= 77 and (char_ascii + 13) >= 65:
					the_message = the_message +  chr(char_ascii - 13)
			else:
				the_message = the_message +  chr(char_ascii)

		return the_message