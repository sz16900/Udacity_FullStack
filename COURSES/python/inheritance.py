class Parent():
	def __init__(self, last_name, eye_color):
		print("Parent constructor called!")
		self.last_name = last_name
		self.eye_color = eye_color

	def show_info(self):
		print("Last Name: " + self.last_name)
		print("Eye Color: " + self.eye_color)

class Child(Parent):
	def __init__(self, last_name, eye_color, number_of_toys):
		print("Child constructor called!")
		# Inherit from parent
		Parent.__init__(self, last_name, eye_color)
		self.number_of_toys = number_of_toys

	# Method Overriding
	def show_info(self):
		print("Last Name: " + self.last_name)
		print("Eye Color: " + self.eye_color)
		print("Number of toys: " + str(self.number_of_toys))


jon_doe = Parent("Doe", "brown")
# print(jon_doe.last_name)
# jon_doe.show_info()

tom_doe = Child("Doe", "Brown", 1234)
tom_doe.show_info()
# print(tom_doe.last_name)
# print(tom_doe.number_of_toys)

