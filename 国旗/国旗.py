import turtle
# 定义一个函数,可以画五角星
def picture(x1,y1,x,y):
    turtle.up()
    turtle.goto(x1, y1)
    turtle.down()
#用于填充颜色
    turtle.begin_fill()
    turtle.fillcolor("yellow")
    for i in range(5):
        turtle.forward(x)
        turtle.left(y)
    turtle.end_fill()
# 速度为3
turtle.speed(3)
# 背景红色
turtle.bgcolor("red")
# 画笔颜色
turtle.color("yellow")
picture(-250,230,100,144)
picture(-31,290,60,144)
picture(-30,181,60,144)
picture(-100,81,60,144)
picture(-210,65,60,144)

turtle.hideturtle()
turtle.done()