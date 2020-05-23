# myqr http://www.dujiaolong.cn -p happy.gif -n dujiaolong.gif -c
# 一行命令 完成动态二维码

from MyQR import myqr

# 使用前需要先安装myqr模块，终端里运行：pip install myqr

myqr.run(
    words='https://a.scene.eprezi.com/s/XteInz0v?adpop=1',
    # 输入链接或者句子作为参数，扫描二维码后显示
    version=5,
    # 控制边长，范围是1到40，数字越大边长越大，默认边长是取决于你输入的信息的长度和使用的纠错等级。
    level='H',
    # 控制纠错水平，范围是L、M、Q、H，从左到右依次升高
    picture='love.gif',
    # 将QR二维码图像与一张同目录下的图片相结合，此处设置该图片
    colorized=True,
    # 默认是黑白(False)，可以选择彩色(True)
    contrast=1.0,
    # 调节图片的对比度，1.0 表示原始图片，更小的值表示更低对比度，更大反之。默认为1.0。
    brightness=1.0,
    # 调节图片的亮度，用法与contrast相同。
    save_name='xinxin.gif',
    # 输出文件名，格式可以是 .jpg， .png ，.bmp ，.gif ；
)

# myqr.run(words='https://www.cnblogs.com/Estate-47/')
