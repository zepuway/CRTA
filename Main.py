import interfaceUI03
import login
import model
from login import *
from login import Ui_login
from interfaceUI03 import *
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import json
import sqlite3
import os
import torch
from model import Classifier
print(torch.__version__)

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'crta')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# login界面
class login_window(login.Ui_login, QMainWindow):
    switch_window = QtCore.pyqtSignal(int, float)

    def __init__(self):
        super(login_window, self).__init__()
        self.setupUi(self)
        self.center()
        self.oldPos = self.pos()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


# Maininterface界面
class Main_window(interfaceUI03.Ui_MainWindow, QMainWindow):
    def __init__(self, user_id, balance):
        super().__init__()
        # 在这里实例化Classifier类
        self.lineEdit_Classify = QtWidgets.QLineEdit(self)
        self.classifier = Classifier()
        self.user_id = user_id
        self.balance = balance
        self.identified_item = None  # 初始化identified_item属性为None
        self.setupUi(self)

        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建模型文件的绝对路径
        model_path = os.path.join(current_dir, 'model_pytorch.pth')

        # 使用绝对路径加载 PyTorch 模型
        self.model = torch.load(model_path, map_location='cuda:0')
        self.model.eval()  # Set the model to evaluation mode

        self.center()
        self.oldPos = self.pos()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


# 主控调度:定义一个名为Controller的Python类
class Controller:
    # 类的构造函数，用于初始化Controller类的实例
    def __init__(self):
        # 创建一个Login_window对象，并将其赋值给self.login
        self.login = login_window()
        # 创建一个Main_window对象，并将其赋值给self.window
        self.window = None
        # Main_window()
        # 将Login_window的switch_window信号连接到show_Mininterface_window方法
        self.login.switch_window.connect(self.show_Mininterface_window)
        # 显示login窗口
        self.login.show()

    # 显示login窗口的方法
    def show_login_window(self):
        # 如果 self.window 不是 None，则关闭 Main_window 窗口
        if self.window is not None:
            self.window.close()
        # 隐藏Login_window窗口的widget_3小部件:注册小窗口
        self.login.widget_3.hide()
        # 将Login_window的switch_window信号连接到show_Mininterface_window方法
        self.login.switch_window.connect(self.show_Mininterface_window)
        self.login.show()

    def show_Mininterface_window(self, user_id, balance):

        self.user_id = user_id
        self.balance = balance

        # 打印调试信息
        print("User ID:", self.user_id)
        print("Balance:", self.balance)
        print("CUDA available:", torch.cuda.is_available())

        # 关闭login窗口
        self.login.close()
        # 创建 Main_window 对象并传入 user_id 和 balance
        self.window = Main_window(self.user_id,self.balance)
        # 将窗口的switch_window信号连接到show_login_window函数
        self.window.switch_window.connect(self.show_login_window)
        # 显示窗口
        self.window.show()

    # 从json文件中读取设置
    def readJson(self, jsonFile):
        # 打开json文件
        f = open(jsonFile)
        # 加载文件中的json数据
        settings = json.load(f)
        # 关闭文件
        f.close()
        # 返回json数据
        return settings


# login界面入口
if __name__ == '__main__':
    # 创建一个Qt应用程序
    app = QApplication(sys.argv)
    # 创建一个Controller对象
    controller = Controller()
    # 显示login窗口
    controller.show_login_window()
    # 运行应用程序，并在退出时返回状态码
    sys.exit(app.exec_())

