import tkinter as tk
from tkinter import *
from pubsub import pub


class View:
    def __init__(self, parent):
        self.container = parent
        return

    def setup(self):
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.topFrame = Frame(self.container, borderwidth=2, highlightbackground="black", highlightcolor="red", highlightthickness=1, width=800, height=500)
        self.buttomFrame = Frame(self.container, borderwidth=2, highlightbackground="black", highlightcolor="red", highlightthickness=1, width=800, height=520)
        self.topFrame2 = Frame(self.topFrame)
        self.buttun_loadimage = tk.Button(self.topFrame2, text="Load Image", command=self.loadImg)
        self.scaleBrightness = tk.Scale(self.topFrame, from_=-255, to_=255, orient= HORIZONTAL, length=510, label="Brightness", command=self.BrightnessContrast)
        self.scaleBrightness.set(0)
        self.scaleContrast = tk.Scale(self.topFrame, from_=-127, to_=127, orient= HORIZONTAL, length=255, label="Contrast", command=self.BrightnessContrast)
        self.scaleContrast.set(0)
        self.scaleThresholdingMin = tk.Scale(self.topFrame, from_=0, to_=255, orient=HORIZONTAL, length=255, label="Minimum Thresholding", command=self.thresholding_func)
        self.scaleThresholdingMin.set(127)
        self.scaleThresholdingMax = tk.Scale(self.topFrame, from_=0, to_=255, orient=HORIZONTAL, length=255, label="Maximum Thresholding", command=self.thresholding_func)
        self.scaleThresholdingMax.set(255)
        self.bit_planes_btn = tk.Button(self.topFrame,text="Bit Planes Scalling", command=self.bit_plancs_func)
        self.original_image_panel = tk.Label(self.buttomFrame, text="Original Image")
        self.effect_image_panel = tk.Label(self.buttomFrame, text="Effect Image")
        self.save_btn = tk.Button(self.topFrame, text="Save", command=self.save_btn_func)

    def loadImg(self):
        print("view - loading")
        pub.sendMessage("OpenFile_Button_Pressed")

    def save_btn_func(self, arg2=0):
        print("View Saved")
        pub.sendMessage("Save_btn_Pressed")

    def bit_plancs_func(self, arg2=0):
        print("view bit planes scalling")
        pub.sendMessage("Bit_Plans_Scalling")

    def thresholding_func(self, arg2):
        print("view - threshold")
        pub.sendMessage("Thresholding_Button_Pressed")

    def BrightnessContrast(self, brightness=0):
        print("view - Changed")
        pub.sendMessage("Brightness_Button_Pressed")


    def updateImg(self, img):
        self.effect_image_panel.configure(image=img)
        self.effect_image_panel.image = img

    def setOriginalImage(self, img):
        self.original_image_panel.configure(image=img)
        self.original_image_panel.image = img

    def setup_layout(self):
        self.topFrame.pack(side=TOP)
        self.buttomFrame.pack(side=BOTTOM)
        self.topFrame2.pack(side=TOP)
        self.buttun_loadimage.pack(side=LEFT)
        self.scaleBrightness.pack(side=TOP)
        self.scaleContrast.pack(side=TOP)
        self.scaleThresholdingMin.pack(side=TOP)
        self.scaleThresholdingMax.pack(side=TOP)
        self.bit_planes_btn.pack(side=TOP)
        self.original_image_panel.pack(side=LEFT)
        self.effect_image_panel.pack(side=RIGHT)
        self.save_btn.pack(side=BOTTOM)


if __name__ == "__main__":

    mainwindow = Tk()
    width = 1700
    height = 900
    mainwindow.geometry("%sx%s" % (width, height))
    mainwindow.title("Open CV")

    view = View(mainwindow)
    view.setup()
    mainwindow.mainloop()
