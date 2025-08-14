#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# File       : AdbFunction.py
# Time       ：2025/7/10 17:45
# Author     ：Carl
# Description：ADB日志收集工具（带日志轮转功能）
"""
import subprocess
import threading
import time


class LogcatReader:
    def __init__(self, callback=None):
        self.process = None
        self.callback = callback
        self._stop_event = threading.Event()

    def start(self):
        self.process = subprocess.Popen(
            ['adb', 'shell', 'logcat', '-v', 'threadtime'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        threading.Thread(target=self._read_output, daemon=True).start()

    def _read_output(self):
        while not self._stop_event.is_set() and self.process.poll() is None:
            line = self.process.stdout.readline()
            if line and self.callback:
                self.callback(line.strip())

    def stop(self):
        self._stop_event.set()
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()


# 使用示例
if __name__ == "__main__":
    def print_log(line):
        print(f"LOG: {line}")


    reader = LogcatReader(callback=print_log)
    reader.start()

    try:
        # 让日志运行10秒
        time.sleep(10)
    finally:
        reader.stop()