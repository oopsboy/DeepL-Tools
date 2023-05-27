import os

path = 'D:\\datasets\\数据集\\neworange2apple'  # 需要处理的文件路径
filelist = os.listdir(path)  # 打印所有文件夹下的内容，可以不要这3行代码
for file in filelist:
    print(file)
for file in filelist:  # 遍历所有文件
    Olddir = os.path.join(path, file)  # 原来的文件路径
    if os.path.isdir(Olddir):  # 如果是文件夹则跳过
        continue
    filename = os.path.splitext(file)[0]  # 分离文件名与扩展名;得到文件名
    filetype = os.path.splitext(file)[1]  # 文件扩展名
    Newdir = os.path.join(path, filename[:-7] + filetype)  # filename[:-3]是原文件去掉倒数3位
    os.rename(Olddir, Newdir)  # 重命名，替换原图片
