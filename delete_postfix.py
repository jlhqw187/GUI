import os
import re
# 指定文件夹的路径
folder_path = r"F:\xtad\debug_class"  # 替换为实际文件夹路径

# 获取文件夹中所有文件的列表（包括子文件夹中的文件）
file_list = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_list.append(os.path.join(root, file))

# 定义一个函数来重命名文件
def rename_files(file_path, new_name):
    try:
        os.rename(file_path, new_name)
        print(f"已将文件重命名为: {new_name}")
    except Exception as e:
        print(f"无法重命名文件: {file_path}")
        print(f"错误信息: {str(e)}")

# 遍历文件列表并为每个文件重命名
for file_path in file_list:
    # 根据需要定义新的文件名规则
    # 这里使用了一个示例规则，将文件名前加上"prefix_"前缀
    file_name = os.path.basename(file_path)
    # new_file_name = file_name.split("_")[0] + ".jpg"  # 修改为您的新文件名规则
    new_file_name = re.sub(r'(_[1-9])\.jpg', '.jpg', file_name)

    # 拼接新的文件路径
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

    # 重命名文件
    rename_files(file_path, new_file_path)
