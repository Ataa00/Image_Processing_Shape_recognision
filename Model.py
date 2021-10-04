from tkinter.filedialog import askopenfilename
import cv2
from pubsub import pub
import PIL.ImageTk, PIL.Image
import numpy as np

class Model:
    def __init__(self):
        self.flag_load_image = False
        return

    def load_image(self):
        path = askopenfilename(initialdir="./",
                               filetypes=[("Image File","*.JPG"), ("All Files", "*.*")],
                               title="Choose a file.")
        if len(path)>0:
            print(path)
            self.originalImg = cv2.imread(path)
            pub.sendMessage("Module_Set", data=self.toTkImg(self.originalImg))
            self.currentImg = self.originalImg.copy()
            self.modifaied_img = self.originalImg.copy()
            pub.sendMessage("Module_Update", data=self.toTkImg(self.currentImg))
        self.flag_load_image = True


    def bit_planes_scalling(self):
        if self.flag_load_image:
            lst = []
            img = cv2.cvtColor(self.currentImg, cv2.COLOR_BGR2GRAY)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    lst.append(np.binary_repr(img[i][j], width=8))
            eight_bit_img = (np.array([int(i[0]) for i in lst], dtype=np.uint8) * 128).reshape(img.shape[0], img.shape[1])
            seven_bit_img = (np.array([int(i[1]) for i in lst], dtype=np.uint8) * 64).reshape(img.shape[0], img.shape[1])
            six_bit_img = (np.array([int(i[2]) for i in lst], dtype=np.uint8) * 32).reshape(img.shape[0], img.shape[1])
            five_bit_img = (np.array([int(i[3]) for i in lst], dtype=np.uint8) * 16).reshape(img.shape[0], img.shape[1])
            four_bit_img = (np.array([int(i[4]) for i in lst], dtype=np.uint8) * 8).reshape(img.shape[0], img.shape[1])
            three_bit_img = (np.array([int(i[5]) for i in lst], dtype=np.uint8) * 4).reshape(img.shape[0], img.shape[1])
            two_bit_img = (np.array([int(i[6]) for i in lst], dtype=np.uint8) * 2).reshape(img.shape[0], img.shape[1])
            one_bit_img = (np.array([int(i[7]) for i in lst], dtype=np.uint8) * 1).reshape(img.shape[0], img.shape[1])

            finalr = cv2.hconcat([eight_bit_img, seven_bit_img, six_bit_img, five_bit_img])
            finalv = cv2.hconcat([four_bit_img, three_bit_img, two_bit_img, one_bit_img])

            final = cv2.vconcat([finalr, finalv])
            pub.sendMessage("bitplanswindow", data=final)

    def thresholdingModel(self, minimum, maximum):
        if self.flag_load_image:
            img = self.currentImg
            ret, th = cv2.threshold(img, minimum, maximum, cv2.THRESH_BINARY)
            pub.sendMessage("Module_Update", data=self.toTkImg(th))

    def BrightnessContrast(self, brightness=255, contrast=127):

        if self.flag_load_image:
            img = self.currentImg

            if brightness!=0:
                if brightness > 0:
                    shadow = brightness
                    max = 255
                else:
                    shadow = 0
                    max = 255 + brightness

                alpha = (max-shadow)/255
                gamma = shadow
                cal = cv2.addWeighted(img, alpha, img, 0, gamma)
            else:
                cal = img

            if contrast != 0:
                Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
                Gamma = 127 * (1 - Alpha)

                cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)

            cv2.putText(cal, 'B:{},C:{}'.format(brightness,
                                                contrast), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            self.modifaied_img = cal
            pub.sendMessage("Module_Update", data=self.toTkImg(cal))

    def toTkImg(self, img):
        b, g, r = cv2.split(img)
        img = cv2.merge((r, g, b))
        im = PIL.Image.fromarray(img)
        imgtk = PIL.ImageTk.PhotoImage(image=im)
        return imgtk
