import os

def count_first_digits(folder_path):
    occurrences = {}  # 用于存储数字及其出现次数的字典

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):  # 只处理以 .txt 结尾的文件
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:  # 确保行不为空
                        first_digit = None

                        # 查找第一个数字
                        digits = line.split(' ')
                        for digit in digits:
                            if digit.isdigit():
                                first_digit = int(digit)
                                break

                        if first_digit is not None:
                            if first_digit in occurrences:
                                occurrences[first_digit] += 1
                            else:
                                occurrences[first_digit] = 1

    return occurrences


# 调用函数并打印结果
folder_path = 'E:\\datasets\\CottonWeedDet12\\CottonWeedDet12\\labels'  # 替换为您的文件夹路径
result = count_first_digits(folder_path)
print(result)
