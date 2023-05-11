# import sys
# sys.path.append('C:/Users/ASUS/anaconda3/envs/global_env/Lib/site-packages')

import numpy
import base64
import torch, glob, cv2
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
import os
from PyQt5 import QtCore

class Classifier(QtCore.QObject):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(Classifier, self).__init__()

        self.classes = ['书包',
                        '塑料瓶',
                        '塑料餐盒',
                        '手机',
                        '易拉罐',
                        '橡皮',
                        '毛巾',
                        '毛绒玩具',
                        '泡沫塑料',
                        '玻璃瓶',
                        '电池',
                        '笔',
                        '笔记本电脑',
                        '纸',
                        '罐头盒',
                        '衣服'
                        ]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = "D:\\crta\\model_pytorch.pth"
        self.model = torch.load(self.model_path, map_location=self.device)
        self.model.eval()
        self.model = self.model.to(self.device)

    def predict_one_img(self, img_path):
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        tran = transforms.ToTensor()
        img = tran(img)
        img = img.to(self.device)
        img = img.view(1, 3, 224, 224)
        out1 = self.model(img)
        out1 = F.softmax(out1, dim=1)
        proba, class_ind = torch.max(out1, 1)
        class_ind = int(class_ind)
        return self.classes[class_ind]

    def classify_image(self, image_path):
        results = self.predict_one_img(image_path)
        return results
