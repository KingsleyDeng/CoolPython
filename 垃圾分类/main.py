import requests
from bs4 import BeautifulSoup
from urllib.request import quote
import tkinter
from tkinter import Tk, Button, Entry, Label, Text, END


def crawl(word):
    # -------------加了requests headers
    params = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,es-US;q=0.6,es;q=0.5',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'lajifenleiapp.com',
        'Referer': 'https://lajifenleiapp.com/',
        'Upgrade - Insecure - Requests': '1',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    }

    url = 'https://lajifenleiapp.com/sk/' + quote(word)

    res0 = requests.get(url, params=params)
    res = BeautifulSoup(res0.text, "html.parser")
    a = res.find_all(class_="col-md-12")
    print(a[0].text)

    if a[0].text != '未查到完全匹配字段。':
        b = res.find_all("li")
        '''
        for i in range(10):
            print(i, '\n',a[i])
        '''
        # ------------严重错误!!!!!!!!!, IndexError: list index out of range, 从4,5,6,7,8改成了3,4,5,6,7
        print(a[0].text, a[1].text, a[3].text, a[4].text, a[5].text, a[6].text, a[7].text)
        return "相似物品:\n" + a[0].text.strip().replace("\n", " ").replace("相关查询：", "") + "\n\n\n" + a[1].text + "\n\n" + \
               a[3].text + "\n\n" + a[4].text + "\n\n" + a[5].text + "\n" + a[6].text + "\n" + a[7].text + "\n" + b[
                   0].text + "\n\n" + b[1].text
    else:
        return word + "可不是什么垃圾，哼，请重新搜索"


win = tkinter.Tk()
win.title("垃圾分拣查询器")
# 设置大小和位置
# 长400，宽400，距离左侧200，距离顶部50
win.geometry("400x400+200+50")
win.minsize(310, 470)
win.maxsize(310, 470)
result_text1 = Text(win, background='azure')
result_text1.place(x=10, y=5, width=285, height=70)
result_text1.bind("<Key-Return>", "submit1")
title_label = Label(win, text=u'垃圾分类查询结果：')
title_label.place(x=10, y=100)
# 翻译结果

result_text = Text(win, background='light cyan')
result_text.place(x=10, y=120, width=285, height=325)


def submit1():
    content = result_text1.get(0.0, END).strip().replace("\n", " ")
    # 把这个值传送给服务器进行翻译
    result = crawl(content)
    result_text.delete(0.0, END)
    result_text.insert(END, result)


def submit():
    content = result_text1.get(0.0, END).strip().replace("\n", " ")

    result = crawl(content)
    result_text.delete(0.0, END)
    result_text.insert(END, result)


def clean():
    result_text1.delete(0.0, END)
    result_text.delete(0.0, END)


submit_btn = Button(win, text=u'查询', command=submit)
submit_btn.place(x=205, y=80, width=35, height=25)
submit_btn2 = Button(win, text=u'清空', command=clean)
submit_btn2.place(x=250, y=80, width=35, height=25)

win.mainloop()
