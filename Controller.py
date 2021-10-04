from View import View
from Model import Model
from tkinter import *
from pubsub import pub
import cv2

class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.model = Model()
        self.view = View(parent)
        self.view.setup()

        pub.subscribe(self.openfile_btn_pressed, "OpenFile_Button_Pressed")
        pub.subscribe(self.BrightnessContrastController, "Brightness_Button_Pressed")
        pub.subscribe(self.thresholdingController, "Thresholding_Button_Pressed")
        pub.subscribe(self.bit_planes_scalling, "Bit_Plans_Scalling")
        pub.subscribe(self.set_orig_image, "Module_Set")
        pub.subscribe(self.save_btn, "Save_btn_Pressed")
        pub.subscribe(self.model_change_handler, "Module_Update")
        pub.subscribe(self.show_bit_planes_window, "bitplanswindow")

    def save_btn(self):
        if self.model.flag_load_image:
            print("Controller save")
            cv2.imwrite("effect.JPG", self.model.modifaied_img)

    def show_bit_planes_window(self, data):
        while(1):
            cv2.imshow("Effect", data)
            k = cv2.waitKey(1)
            if k == ord('s'):
                cv2.imwrite("processed_Image.JPG", data)
                break
            if k == 27:
                break
        cv2.destroyAllWindows()

    def set_orig_image(self, data):
        self.view.setOriginalImage(data)

    def openfile_btn_pressed(self):
        print("Controller openfile")
        self.model.load_image()

    def bit_planes_scalling(self):
        print("controller Bit plans")
        self.model.bit_planes_scalling()

    def thresholdingController(self):
        print("Controller thresholding")
        minimum = self.view.scaleThresholdingMin.get()
        maximum = self.view.scaleThresholdingMax.get()
        print(maximum)
        print(minimum)
        self.model.thresholdingModel(minimum, maximum)

    def BrightnessContrastController(self):
        brightness = self.view.scaleBrightness.get()
        contrast = self.view.scaleContrast.get()
        print(brightness)
        print(contrast)
        self.model.BrightnessContrast(brightness, contrast)

    def model_change_handler(self, data):
        self.view.updateImg(data)


if __name__ == "__main__" :
    mainwindow = Tk()
    width = 1700
    height = 900
    mainwindow.geometry("%sx%s" % (width, height))
    mainwindow.title("Effect")

    app = Controller(mainwindow)

    mainwindow.mainloop()

