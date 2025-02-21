import os
import platform

class CommonFunc():
    '''通用功能封装'''

    def runCmd(self, master):
        '''执行cmd'''
        return os.popen(master).read()

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