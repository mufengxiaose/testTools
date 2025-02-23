import os

# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)
# 获取当前脚本所在文件夹的路径
current_folder_path = os.path.dirname(current_script_path)
# 获取当前文件夹的父级路径
parent_folder_path = os.path.dirname(current_folder_path)

print("当前脚本的绝对路径:", current_script_path)
print("当前脚本所在文件夹的路径:", current_folder_path)
print("当前文件夹的父级路径:", parent_folder_path)