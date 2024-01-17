import turtle

def pentag(t, color):
    t.penup()
    t.backward(15)
    t.right(90)
    t.forward(20)
    t.left(90)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for i in range(5):
        t.forward(30)
        t.left(72)
    t.end_fill()

def move(t,x,y):
    t.penup()
    t.goto(x, y)
    t.pendown()

pen = turtle.Turtle()
pen.speed(50)
move(pen, 0, -100)

pen.fillcolor("#FCD757")
pen.begin_fill()
pen.circle(100)
pen.end_fill()

move(pen, 0, 0)
pentag(pen, 'blue')

ang = 122.5
pen.right(ang)
move(pen, -75, 40)
pentag(pen, 'blue')
pen.left(ang)

ang = 180
pen.right(ang)
move(pen, 0, 90)
pentag(pen, 'blue')
pen.left(ang)

ang = 22.5
pen.right(ang)
move(pen, 75, 40)
pentag(pen, 'blue')
pen.left(ang)

ang = 0
pen.right(ang)
move(pen, 75, -30)
pentag(pen, 'blue')
pen.right(ang)



##pen.right(90)
##move(pen,0, 100)
##pen.forward(200)
##move(pen, -100, 0)
##pen.left(90)
##pen.forward(200)
##
##pen.hideturtle()
turtle.done()

