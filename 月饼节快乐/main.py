# Python 烟花特效
import sys
import time
import math
import random
import tkinter as tk
from PIL import Image, ImageTk


# 烟花颗粒
class particle():

    def __init__(self, **kwargs):
        # 编号
        self.idx = kwargs.get('idx')
        self.num_particles = kwargs.get('num_particles')
        # 初始位置
        self.init_x = kwargs.get('init_x')
        self.init_y = kwargs.get('init_y')
        # 可生存时间
        self.alive_span = kwargs.get('alive_span')
        # 用于扩散的时间
        self.spread_span = 1.2
        # 当前已生存时间
        self.alive_time = 0.
        # 画布
        self.canvas = kwargs.get('canvas')
        # 颜色
        self.color = kwargs.get('color')
        # 扩散速度
        self.speed = kwargs.get('speed')
        # 下落速度
        self.down_x = 0.
        self.down_y = kwargs.get('down_y')
        # 重力
        self.g = 0.05
        # 烟花粒的大小
        self.size = kwargs.get('size')
        # 烟花粒
        self.oval = self.canvas.create_oval(self.init_x - self.size,
                                            self.init_y - self.size,
                                            self.init_x + self.size,
                                            self.init_y + self.size,
                                            fill=self.color)

    # 更新
    def update(self, dt):
        self.alive_time += dt
        if not self.alive():
            self.canvas.delete(self.oval)
            return False
        if self.is_spread():
            x = math.cos(math.radians(self.idx * 360. / self.num_particles)) * self.speed
            y = math.sin(math.radians(self.idx * 360. / self.num_particles)) * self.speed
            self.canvas.move(self.oval, x, y)
            self.down_x = x / (dt * 1000.)
            return True
        x = math.cos(math.radians(self.idx * 360. / self.num_particles)) + self.down_x
        self.down_y += self.g * dt
        y = self.down_y
        self.canvas.move(self.oval, x, y)
        return True

    # 判断烟花是否处在扩散期
    def is_spread(self):
        return self.alive_time <= self.spread_span

    # 判断该烟花粒是否还存活
    def alive(self):
        return self.alive_time <= self.alive_span


# 烟花效果实现
def play(params):
    canvas, root = params
    t0 = time.time()
    particles = []
    num_firework = random.randint(6, 12)
    num_particles = random.randint(10, 50)
    all_firework = []
    for i in range(num_firework):
        firework = []
        color = random.choice(
            ['red', 'blue', 'cornflowerblue', 'yellow', 'orange', 'white', 'green', 'seagreen', 'purple', 'indigo'])
        speed = random.uniform(0.2, 0.95)
        down_y = random.uniform(0.5, 1.5)
        size = random.uniform(0.5, 3)
        init_x = random.randint(50, 750)
        init_y = random.randint(50, 180)
        for j in range(num_particles):
            alive_span = random.uniform(0.6, 1.75)
            p = particle(idx=j,
                         canvas=canvas,
                         num_particles=num_particles,
                         color=color,
                         speed=speed,
                         down_y=down_y,
                         size=size,
                         alive_span=alive_span,
                         init_x=init_x,
                         init_y=init_y
                         )
            firework.append(p)
        all_firework.append(firework)
    total_time = 0
    while total_time < 1.8:
        time.sleep(0.01)
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        for firework in all_firework:
            for p in firework:
                q = p.update(dt)
        canvas.update()
        total_time += dt
    root.after(random.randint(10, 100), play, [canvas, root])


def quit(root):
    root.quit()
    sys.exit(-1)


# 主函数
def main():
    root = tk.Tk()
    canvas = tk.Canvas(root, height=468, width=800)
    bg_img = ImageTk.PhotoImage(Image.open('bg.jpg'))
    canvas.create_image(0, 0, image=bg_img, anchor='nw')
    # 将Canvas添加到主窗口
    canvas.pack()
    # 绘制文字
    canvas.create_text(400, 250, text='Kingsley老师祝:大家国庆节快乐', font=('微软雅黑', 24), fill='white')
    root.protocol("WM_DELETE_WINDOW", lambda: quit(root))
    root.after(100, play, [canvas, root])
    root.mainloop()


if __name__ == '__main__':
    main()
