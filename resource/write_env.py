#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
选择图片文件夹，然后遍历文件夹下所有.bmp文件，生成pic变量
请注意文件夹和文件名的格式
1.文件夹和文件名请不要带有空格-->因为变量名是不能含空格
2.文件夹和文件名请不要带除'_'下划线以外的符号-->变量名不能用'-'横线
3.文件夹和文件名请不要带中文，windows系统编码不是用的UTF-8,用中文很可能会乱码，识别不了
4.请注意图片重名的情况，如果两张图片重名(即使在不同文件夹)，那第二个文件生成的变量名会不能使用。
"""

import os

from tkinter import filedialog

# 通过Filedialog选择文件夹
directory_path = filedialog.askdirectory(title='请选择图片文件夹', initialdir=r"D:\git_repository\adam\resource\pic")

# 生成pic文件
txt_path = directory_path + '.txt'
# 如果pic.txt已经存在，把之前的内容重写为空白
with open(txt_path, 'w+') as file:
    file.write('')

# 遍历选定文件夹下所有.bmp图片
prefix = ''
for root, dirs, files in os.walk(directory_path):
    if files:
        # root为所有文件夹的绝对路径,下面替换掉前面一部分，形成以选定文件夹为根目录的相对路径
        if root != directory_path:
            root = root.replace(directory_path + '\\', '')
            prefix = root + '/'
            prefix = prefix.replace('\\', '/')
            with open(txt_path, 'a')as file:
                file.write('# ' + prefix + '\n')
        else:
            with open(txt_path, 'a')as file:
                file.write('# root\n')
        for file_name in files:
            # variable 变量名
            # prefix 文件路径前缀
            # file_name 文件名
            if '.bmp' in file_name:
                # 去掉后缀
                variable = file_name.replace(r'.bmp', '')
                # 拼接path语句
                full_str = "{0} = os.path.join(prefix, '{1}{2}')\n".format(variable, prefix, file_name)
                # 写入到pic.txt
                with open(txt_path, 'a') as file:
                    file.write(full_str)
        # 每个文件夹中间空两行
        with open(txt_path, 'a')as file:
            file.write('\n' + '\n')
