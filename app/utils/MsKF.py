# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : MsKF.py
# Time       ：2025/6/10 17:27
# Author     ：Carl
# Description：
"""
import os
import subprocess
from tkinter import messagebox
from pathlib import Path

def kf_branch_parent_file():
    code_file = Path.home() / "code"
    if code_file:
        pass
    else:
        os.mkdir(code_file)

def mkdir_kf_pro_file(branch=None):
    # 使用 Path 直接拼接路径，更安全的方式
    pro_file = Path.home() / "code" / str(branch)  # 显式转换为字符串

    # 检查目录是否存在
    if not pro_file.exists():
        try:
            pro_file.mkdir(parents=True)  # 自动创建父目录
            print(f"目录已创建: {pro_file}")
        except Exception as e:
            print(f"创建目录失败: {e}")
    else:
        print(f"目录已存在: {pro_file}")

    return pro_file

def run_commands_in_dir(directory, commands):
    """在指定目录下按顺序执行多个命令"""
    original_dir = os.getcwd()  # 保存当前目录
    success = True

    try:
        # 切换到目标目录
        os.chdir(directory)
        print(f"当前目录: {os.getcwd()}")

        # 执行命令
        for command in commands:
            print(f"执行命令: {' '.join(command)}")
            try:
                result = subprocess.run(
                    command,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.stdout:
                    # print("标准输出:")
                    print(result.stdout)
                    messagebox.showinfo(message=result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"命令执行失败: {e.returncode}")
                if e.stdout:
                    print("标准输出:")
                    print(e.stdout)
                if e.stderr:
                    print("标准错误:")
                    print(e.stderr)
                success = False
                # 可选：是否继续执行剩余命令
                # break

    finally:
        # 无论成功与否，都切回原目录
        os.chdir(original_dir)
        print(f"已切回原目录: {os.getcwd()}")

    return success

if __name__ == '__main__':
    pro_file = "feat-mine-clearance"
    mkdir_kf_pro_file(branch=pro_file)
    target_dir = Path.home() / "code" / pro_file
    script_path = Path(__file__).parent.parent / "scripts/kf.sh"
    print(script_path)
    # result = subprocess.run(["/bin/bash", str(script_path.resolve())],)
    # 定义要执行的命令列表，每个命令是一个字符串列表
    commands_to_run = [
        ["echo", "开始执行命令"],
        ["ms", "_kf", "%s"%(pro_file)]
    ]
    # 执行命令
    success = run_commands_in_dir(target_dir, commands_to_run)
    if success:
        print("所有命令执行完毕")
    else:
        print("命令执行过程中出错")