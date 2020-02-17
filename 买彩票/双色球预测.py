import re
import requests
from bs4 import BeautifulSoup as BS


def GetText():
    for i in range(1, 124):
        url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_{}.html'.format(i)
        print(url)
        text = GetPage(url)
        ems = text.find_all('em')
        divs = text.find_all('td', {'align': 'center'})

        n = 0
        with open('./lottery.txt', 'a') as f:
            for em in ems:
                print(em.get_text())
                message = em.get_text()
                n += 1
                if n == 7:
                    n = 0
                    message = message + "\n"
                else:
                    message += '\t'
                f.write(str(message))


def GetPage(url):
    headers = {
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'Host': 'kaijiang.zhcw.com'
    }

    response = requests.get(url, headers=headers)
    text = BS(response.text, 'lxml')
    return text

if __name__ == '__main__':
    GetText()