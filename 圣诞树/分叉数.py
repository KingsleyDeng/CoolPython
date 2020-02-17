import turtle


# def draw_brach(brach_length):
#     if brach_length > 5:
#         if brach_length < 40:
#             turtle.color('green')
#         else:
#             turtle.color('red')
#         # 绘制右侧的树枝
#         turtle.forward(brach_length)
#         print('向前', brach_length)
#         turtle.right(25)
#         print('右转20')
#         draw_brach(brach_length - 15)
#         # 绘制左侧的树枝
#         turtle.left(50)
#         print('左转40')
#         draw_brach(brach_length - 15)
#
#         if brach_length < 40:
#             turtle.color('green')
#
#         else:
#             turtle.color('red')
#
#         # 返回之前的树枝上
#         turtle.right(25)
#         print('右转20')
#         turtle.backward(brach_length)
#         print('返回', brach_length)

def draw_brach(s):
    if s > 5:
        if s < 40:
            turtle.color('green')
        else:
            turtle.color('red')
        turtle.forward(s)
        turtle.right(25)
        draw_brach(s - 20)

        turtle.left(50)

        draw_brach(s - 20)

        if s < 40:
            turtle.color('green')
        else:
            turtle.color('red')
        turtle.right(25)
        turtle.backward(s)


def main():
    turtle.speed(0)
    turtle.left(90)
    turtle.penup()
    turtle.backward(150)
    turtle.pendown()
    turtle.color('red')

    draw_brach(100)

    turtle.exitonclick()


if __name__ == '__main__':
    main()
