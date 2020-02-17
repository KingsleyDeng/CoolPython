# -*- coding: utf-8 -*-#

import time
import wave
from pyaudio import PyAudio, paInt16

from aip import AipSpeech
import requests
import json
import speech_recognition as sr
import win32com.client

# 初始化语音
speaker = win32com.client.Dispatch("SAPI.SpVoice")

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = 'output.wav'


# def save_wave_file(filepath, data):
#     wf = wave.open(filepath, 'wb')
#     wf.setnchannels(channels)
#     wf.setsampwidth(sampwidth)
#     wf.setframerate(framerate)
#     wf.writeframes(b''.join(data))
#     wf.close()

# # 录音
# def my_record():
#     pa = PyAudio()
#     # 打开一个新的音频stream
#     stream = pa.open(format=paInt16, channels=channels,
#                      rate=framerate, input=True, frames_per_buffer=num_samples)
#     my_buf = []  # 存放录音数据
#
#     t = time.time()
#     print('正在录音...')
#
#     while time.time() < t + 10:  # 设置录音时间（秒）
#         # 循环read，每次read 2000frames
#         string_audio_data = stream.read(num_samples)
#         my_buf.append(string_audio_data)
#     print('录音结束.')
#     save_wave_file(FILEPATH, my_buf)
#     stream.close()


# 1、语音生成音频文件,录音并以当前时间戳保存到voices文件中
# Use SpeechRecognition to record 使用语音识别录制
def my_record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    with open("output.wav", "wb") as f:
        f.write(audio.get_wav_data())


# 2、音频文件转文字：采用百度的语音识别python-SDK
# 导入我们需要的模块名，然后将音频文件发送给出去，返回文字。
# 百度语音识别API配置参数
APP_ID = '16809164'
API_KEY = 'R7KI0nvzUINCMy2BSWdMUx3z'
SECRET_KEY = '3q6fjA62CqUd7E7Km4kYyAPKxwNdDAuP'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
path = 'output.wav'


# 将语音转文本STT
def listen():
    # 读取录音文件
    with open(path, 'rb') as fp:
        voices = fp.read()
    try:
        # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
        result = client.asr(voices, 'wav', 16000, {'dev_pid': 1537, })
        # result = CLIENT.asr(get_file_content(path), 'wav', 16000, {'lan': 'zh', })
        # print(result)
        # print(result['result'][0])
        # print(result)
        result_text = result["result"][0]
        print("you said: " + result_text)
        return result_text
    except KeyError:
        print("KeyError")
        speaker.Speak("我没有听清楚，请再说一遍...")


# 3、与机器人对话：调用的是图灵机器人
# 图灵机器人的API_KEY、API_URL
turing_api_key = "f976101f2ce84570ba82670272958981"
api_url = "http://openapi.tuling123.com/openapi/api/v2"  # 图灵机器人api网址
headers = {'Content-Type': 'application/json;charset=UTF-8'}


# 图灵机器人回复
def Turing(text_words=""):
    req = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text_words
            },

            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "车公庄"
                }
            }
        },
        "userInfo": {
            "apiKey": turing_api_key,  # 你的图灵机器人apiKey
            "userId": "Nieson"  # 用户唯一标识(随便填, 非密钥)
        }
    }

    req["perception"]["inputText"]["text"] = text_words
    response = requests.request("post", api_url, json=req, headers=headers)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI Robot said: " + result)
    return result


# 语音合成，输出机器人的回答
while True:
    my_record()
    request = listen()
    response = Turing(request)
    speaker.Speak(response)
