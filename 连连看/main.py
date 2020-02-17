import random, sys
import tkinter as tk
import tkinter.messagebox
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk


class MainWindow():
    def __init__(self):
        self.title = "连连看游戏"
        self.windowWidth = 700
        self.windowWidth = 700
        self.windowHeigth = 500
        self.root = tk.Tk()
        self.root.title(self.title)
        self.CWindow(self.windowWidth, self.windowHeigth)
        self.root.minsize(460, 460)
        self.pics = []
        self.primary = askyesno(title='选择第一关', message='第一关(yes) 第二关(no)')
        self.Interface()
        if self.primary == False:
            self.picsize = 10  # 每行每列的图片数量
            self.num = 4
            self.picWidth = 40  # 小图片的宽
            self.picHeight = 40  # 小图片的宽
        else:
            self.picsize = 8  # 每行每列的图片数量
            self.num = 4
            self.picWidth = 50  # 小图片的宽
            self.picHeight = 50  # 小图片的宽
        self.picsKind = self.picsize * self.picsize / self.num  # 小图片种类数量
        self.picsmap = []  # 游戏地图
        self.margin = 25
        self.firstClick = True
        self.start = False
        self.lastPoint = None
        self.none = -1
        self.noLink = 0
        self.lineLink = 1
        self.L_Link = 2
        self.U_link = 3

        self.put_pic_in_pics()
        self.root.mainloop()

    def Interface(self):
        self.menu = tk.Menu(self.root, bg="lightgrey", fg="black")
        self.list_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
        self.list_menu.add_command(label="开始游戏", command=self.game_start, accelerator="Ctrl+N")
        self.list_menu.add_command(label="退出", command=self.game_stop, accelerator="Ctrl+M")
        self.menu.add_cascade(label="游戏", menu=self.list_menu)
        self.root.configure(menu=self.menu)

        self.canvas = tk.Canvas(self.root, bg='white', width=450, height=450)
        self.canvas.pack(side=tk.TOP, pady=5)
        self.canvas.bind('<Button-1>', self.clickCanvas)

    def CWindow(self, w, h):  # 设置屏幕的位置
        swidth = self.root.winfo_screenwidth()
        sheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (w, h, (swidth - w) / 2, (sheight - h) / 2)
        self.root.geometry(size)

    def game_start(self):
        self.ini_game()
        self.put_pics_on_canvas()
        self.start = True

    def game_stop(self):
        sys.exit()

    def clickCanvas(self, event):
        if self.start:
            point = self.get_index_coord(Point(event.x, event.y))  # 返回鼠标点击的位置到底是哪一幅图片。例如[0,0]代表左上角第一幅
            # 有效点击坐标
            if point.isUserful() and not self.check_none(point):
                if self.firstClick:  # 如果是第一次点击图片，那么就画一个红框
                    self.draw_red_rectangle(point)
                    self.firstClick = False
                    self.lastPoint = point
                else:
                    if self.lastPoint.isEqual(point):  # 如果连续点击同一小图片两次的话，就将话得红框去掉
                        self.firstClick = True
                        self.canvas.delete("rectRedOne")
                    else:
                        linkType = self.get_link_type(self.lastPoint, point)
                        if linkType['type'] != self.noLink:
                            # TODO Animation
                            self.delete_linked_points(self.lastPoint, point)
                            self.canvas.delete("rectRedOne")
                            self.firstClick = True
                            if self.check_end():
                                tk.messagebox.showinfo("You Win!", "Tip")
                                self.start = False
                        else:
                            self.lastPoint = point
                            self.canvas.delete("rectRedOne")
                            self.draw_red_rectangle(point)

    # 判断游戏是否结束
    def check_end(self):
        for y in range(0, self.picsize):
            for x in range(0, self.picsize):
                if self.picsmap[y][x] != self.none:
                    return False
        return True

    def put_pic_in_pics(self):  # 将小头像放到pics数组里面
        ori_image = Image.open(r'./pic/img.png')
        if self.primary == True:  # 如果是第一关的话，需要将原始图片扩大之后再进行剪裁。
            ori_image = ori_image.resize((1250, 50), Image.NEAREST)
        for i in range(0, int(self.picsKind)):
            pic = ori_image.crop((self.picWidth * i, 0,
                                  self.picWidth * i + self.picWidth - 1, self.picHeight - 1))
            self.pics.append(ImageTk.PhotoImage(pic))

    def ini_game(self):  # 初始化地图
        self.picsmap = []  # 重置地图
        index1 = []
        indexs = []
        for i in range(0, int(self.picsKind)):
            for j in range(0, self.num):
                index1.append(i)  # 向tmpRecords里添加小图片索引，每一个种类的图片都添加self.num个

        total = self.picsize * self.picsize  # 总共的图片数量
        print('tmpRecords', index1)
        for x in range(0, total):
            index = random.randint(0, total - x - 1)  # 打乱顺序
            indexs.append(index1[index])  # 向records里添加小图片的索引
            del index1[index]
        print('records', indexs)
        print(len(indexs))
        # 一维数组转为二维，y为高维度
        for y in range(0, self.picsize):  # 将小图片转化为二维矩阵形式
            for x in range(0, self.picsize):
                if x == 0:
                    self.picsmap.append([])
                self.picsmap[y].append(indexs[x + y * self.picsize])

    def put_pics_on_canvas(self):  # 根据地图绘制图像
        self.canvas.delete("all")
        for y in range(0, self.picsize):
            for x in range(0, self.picsize):
                point = self.get_left_top_point(Point(x, y))  # 获取小图片应该放在什么位置（左上角的坐标）
                self.canvas.create_image((point.x, point.y),
                                         image=self.pics[self.picsmap[y][x]], anchor='nw',
                                         tags='im%d%d' % (x, y))  # 将小图片放入指定位置

    def get_left_top_point(self, point):  # 获取对应矩形的左上角顶点坐标
        return Point(self.getx(point.x), self.gety(point.y))

    def getx(self, x):  # 更新x的位置
        return x * self.picWidth + self.margin

    def gety(self, y):  # 更新y的位置
        return y * self.picHeight + self.margin

    def get_index_coord(self, point):  # 获取内部坐标
        x = -1
        y = -1

        for i in range(0, self.picsize):
            x1 = self.getx(i)
            x2 = self.getx(i + 1)
            if point.x >= x1 and point.x < x2:
                x = i

        for j in range(0, self.picsize):
            j1 = self.gety(j)
            j2 = self.gety(j + 1)
            if point.y >= j1 and point.y < j2:
                y = j

        return Point(x, y)

    def draw_red_rectangle(self, point):  # 选择的区域变红，point为内部坐标
        pointLT = self.get_left_top_point(point)  # 获取小图片的左上角坐标
        pointRB = self.get_left_top_point(Point(point.x + 1, point.y + 1))  # 在小图片的左上角坐标上（x，y）分别加一
        self.canvas.create_rectangle(pointLT.x, pointLT.y,
                                     pointRB.x - 1, pointRB.y - 1, outline='red',
                                     tags="rectRedOne")  # 以（x+1，y+1）为左上角坐标，画圆

    def delete_linked_points(self, p1, p2):  # 消除连通的两个块
        self.picsmap[p1.y][p1.x] = self.none
        self.picsmap[p2.y][p2.x] = self.none
        self.canvas.delete('im%d%d' % (p1.x, p1.y))
        self.canvas.delete('im%d%d' % (p2.x, p2.y))

    def check_none(self, point):  # 判断图上该点是否为空
        if self.picsmap[point.y][point.x] == self.none:
            return True
        else:
            return False

    def get_link_type(self, p1, p2):  # 判断两个点连通类型
        # 首先判断两个方块中图片是否相同
        if self.picsmap[p1.y][p1.x] != self.picsmap[p2.y][p2.x]:  # 这里运用的很巧妙，利用数字索引来判断是否为同一类型图片。如果不是，肯定无法连接
            return {'type': self.noLink}

        if self.line_link_type(p1, p2):
            return {
                'type': self.lineLink
            }
        res = self.L_Link_type(p1, p2)
        if res:
            return {
                'type': self.L_Link,
                'p1': res
            }
        res = self.U_Link_type(p1, p2)
        if res:
            return {
                'type': self.U_link,
                'p1': res['p1'],
                'p2': res['p2']
            }
        return {
            'type': self.noLink
        }

    def line_link_type(self, p1, p2):  # 直线相连，判断两幅图的前进道路上是否有图片阻拦。
        # 水平
        if p1.y == p2.y:
            # 大小判断
            if p2.x < p1.x:
                start = p2.x
                end = p1.x
            else:
                start = p1.x
                end = p2.x
            for x in range(start + 1, end):
                if self.picsmap[p1.y][x] != self.none:
                    return False
            return True
        elif p1.x == p2.x:
            if p1.y > p2.y:
                start = p2.y
                end = p1.y
            else:
                start = p1.y
                end = p2.y
            for y in range(start + 1, end):
                if self.picsmap[y][p1.x] != self.none:
                    return False
            return True
        return False

    def L_Link_type(self, p1, p2):  # 一个拐弯相连，类似于“L”型
        corner = Point(p1.x, p2.y)
        if self.line_link_type(p1, corner) and self.line_link_type(corner, p2) and self.check_none(corner):
            return corner

        corner = Point(p2.x, p1.y)
        if self.line_link_type(p1, corner) and self.line_link_type(corner, p2) and self.check_none(corner):
            return corner

    def U_Link_type(self, p1, p2):  # # 两个个拐弯相连，类似于“U”型
        for y in range(-1, self.picsize + 1):
            corner1 = Point(p1.x, y)
            corner2 = Point(p2.x, y)
            if y == p1.y or y == p2.y:
                continue
            if y == -1 or y == self.picsize:
                if self.line_link_type(p1, corner1) and self.line_link_type(corner2, p2):
                    return {'p1': corner1, 'p2': corner2}
            else:
                if self.line_link_type(p1, corner1) and self.line_link_type(corner1,
                                                                            corner2) and self.line_link_type(
                    corner2, p2) and self.check_none(corner1) and self.check_none(corner2):
                    return {'p1': corner1, 'p2': corner2}

        # 横向判断
        for x in range(-1, self.picsize + 1):
            corner1 = Point(x, p1.y)
            corner2 = Point(x, p2.y)
            if x == p1.x or x == p2.x:
                continue
            if x == -1 or x == self.picsize:
                if self.line_link_type(p1, corner1) and self.line_link_type(corner2, p2):
                    return {'p1': corner1, 'p2': corner2}
            else:
                if self.line_link_type(p1, corner1) and self.line_link_type(corner1,
                                                                            corner2) and self.line_link_type(
                    corner2, p2) and self.check_none(corner1) and self.check_none(corner2):
                    return {'p1': corner1, 'p2': corner2}


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isUserful(self):  # 坐标x和y都大于0
        if self.x >= 0 and self.y >= 0:
            return True
        else:
            return False

    def isEqual(self, point):  # 判断两个点是否相同
        if self.x == point.x and self.y == point.y:
            return True
        else:
            return False

    def clone(self):  # 克隆一份对象
        return Point(self.x, self.y)

    def changeTo(self, point):  # 改为另一个对象
        self.x = point.x
        self.y = point.y


if __name__ == '__main__':
    MainWindow()
