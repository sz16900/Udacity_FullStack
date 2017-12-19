# http://openbookproject.net/thinkcs/python/english3e/recursion.html

import turtle 

def draw_square(t, length):
	t.shape("turtle")
	t.color("yellow")
	x = 0
	while(x < 4):
		t.forward(length)
		t.right(90)
		x += 1

def draw_circle(t, radius):
	t.shape("arrow")
	t.color("blue")
	t.circle(radius)

def draw_triangle(t, length):
	t.color("green")
	x = 0
	while(x < 3):
		t.backward(length)
		t.right(120)
		x += 1

def koch(t, order, size):
	if order == 0:
		t.forward(size)
	else:
		for angle in [60, -120, 60, 0]:
			koch(t, order-1, size/3)
			t.left(angle)

def init_window():
	window = turtle.Screen()
	window.bgcolor("red")
	chad = turtle.Turtle()
	koch(chad, 3, 100)
	window.exitonclick()

init_window()