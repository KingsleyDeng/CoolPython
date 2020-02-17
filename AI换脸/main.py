import requests
import json
import base64
import os
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import tkinter as tk

root = tk.Tk()
root.withdraw()


#  获取人脸关键点
def find_face(imgpath, api_key, api_secret):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "image_url": imgpath,
        "return_landmark": 1
    }

    files = {"image_file": open(imgpath, "rb")}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = json.JSONDecoder().decode(req_con)
    this_json = json.dumps(req_dict)

    this_json2 = json.loads(this_json)
    print(this_json2)
    faces = this_json2['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle']
    return rectangle


# 第2步
# number表示换脸的相似度
def merge_face(api_key, api_secret, image_url1, image_url2, image_url, number):
    ff1 = find_face(image_url1, api_key, api_secret)
    ff2 = find_face(image_url2, api_key, api_secret)

    rectangle1 = str(str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height']))
    rectangle2 = str(ff2['top']) + "," + str(ff2['left']) + "," + str(ff2['width']) + "," + str(ff2['height'])
    url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
    f1 = open(image_url1, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()
    f2 = open(image_url2, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    data = {"api_key": api_key,
            "api_secret": api_secret,
            "template_base64": f1_64, "template_rectangle": rectangle1,
            "merge_base64": f2_64, "merge_rectangle": rectangle2, "merge_rate": number}

    response = requests.post(url_add, data=data)
    req_con1 = response.content.decode('utf-8')
    req_dict = json.JSONDecoder().decode(req_con1)
    result = req_dict['result']
    imgdata = base64.b64decode(result)
    file = open(image_url, 'wb')
    file.write(imgdata)
    file.close()
    print('fakeface.jpg 图片合成成功')


if __name__ == '__main__':
    api_key = '6r-ZVioGpbnuXj26jEMr-hmnCeAEYQIS'
    api_secret = 'C_EWq_-nx3-9pIjxQKgmQuBZLSyV2eFO'

    print('请选择模板图片')
    image1 = askopenfilename()
    print('请选择要融合的图片')
    image2 = askopenfilename()

    number = int(input('请输入融合比例%(0-100)'))
    while number < 0 or number > 100:
        number = int(input('请重新输入融合比例%(0-100)'))
    # 最后生成图片名
    image = '%s/%s.jpg' % (os.path.split(image1)[0], 'faceface1')
    print('合成中。。。。')
    merge_face(api_key, api_secret, image1, image2, image, number)
