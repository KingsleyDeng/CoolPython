import rawpy
import imageio
import os

# 将CR2文件无损压缩为JPG格式文件
def change(path1, path2):
    f = os.listdir(path1)
    for i in f:
        portion = os.path.splitext(i)
        if portion[1] == '.CR2':
            old = path1 + i
            raw = rawpy.imread(old)
            new = path2 + portion[0] + '.jpg'
            rgb = raw.postprocess()
            imageio.imsave(new, rgb)
            print("正在处理图片", old, "到处文jpg大小为", round(os.path.getsize(new) / 1024 / 1024, 2), 'MB')


if __name__ == '__main__':
    change('image/', 'image-new/')
