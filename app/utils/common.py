import os
import platform
import subprocess

class CommonFunc():
    '''通用功能封装'''

    def runCmd(self, content):
        '''执行cmd'''
        return os.popen(content).read()

    def creatFile(self, file_path):
        """判断目录是否存在，没有则创建"""
        self._file = os.getcwd() + file_path
        try:
            if not os.path.exists(self._file):
                return os.mkdir(self._file)
        except OSError as e:
            print(f"创建目录失败{e}")

    def getSystemName(self):
        '''获取电脑系统名称'''
        return platform.system()
    
    def run_subprocess_popen(self, args):
        process = subprocess.Popen(args=args,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout, stderr
