# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
CAMERA_STATUS = ''

from tkinter import *

# import module
from tkinter import filedialog
from tkinter import messagebox

from PIL import ImageTk, Image

import cv2
import threading
from trt_yolo import main,VIDEO_NAME,MODEL_DETECTION,MODEL_TRACKING

def runModel():
    MODEL_DETECTION = modelDetectionChosen.get()
    MODEL_TRACKING = modelTrackingChosen.get()
    if MODEL_DETECTION == "Select model detection":
        messagebox.showinfo("Hint", "Select a model detection")
    elif MODEL_TRACKING == "Select model tracking":
        messagebox.showinfo("Hint", "Select a model tracking")
    elif len(VIDEO_NAME) == 0 or CAMERA_STATUS is False:
        messagebox.showinfo("Hint", "Open camera or select a video")
    else:
        main(VIDEO_NAME,MODEL_DETECTION,MODEL_TRACKING)

def pre_runModel():
    func_runModel = threading.Thread(target=runModel)
    func_runModel.daemon = True
    func_runModel.start()
    return lambda:func_runModel

# Function for opening the
# file explorer window
def browseFiles():
    global VIDEO_NAME
    filename = filedialog.askopenfilename(
                                        title = "Select a File",
                                        filetypes = (("Video files","*.mp4*"),
                                                     ("All files","*.*"),
                                                     ))
    if filename:
        # Change label contents
        labelTitleVideoCamera.configure(text="Video path: "+filename)
    else: # avoid error when click "Cancel", return tuple instead of str
        # Change label contents
        labelTitleVideoCamera.configure(text="Video path: ")
    VIDEO_NAME = filename
    

def isCameraOpened():
    global VIDEO_NAME
    VIDEO_NAME = ''
    
    try:
        vid = cv2.VideoCapture(-1)
        ret, _ = vid.read()
    except:
        pass
    
    CAMERA_STATUS = ret
    
    if CAMERA_STATUS:
        labelTitleVideoCamera.configure(text="Camera status: camera is connected.")
    else:
        labelTitleVideoCamera.configure(text="Camera status: camera is not connected.")

# Create the root window
root = Tk()

# Set window title
root.title('Application')

# Set window size
root.geometry("600x520")

#Set window background color
root.config(background = "white")

# Create a label line
frame_labelLine = Frame(root,background = "green",height = 3)
frame_labelLine.pack(fill = BOTH)

# Create a label contain logo
frame_labelTitle = Frame(root,background = "white",)
frame_labelTitle.pack()

logo_HCMUTE = Image.open("logo_HCMUTE.png")
width, height = logo_HCMUTE.size
logo_HCMUTE = logo_HCMUTE.resize((int(width/2),int(height/2)))
logo_HCMUTE = ImageTk.PhotoImage(logo_HCMUTE)

label = Label(frame_labelTitle, image = logo_HCMUTE)
label.pack(pady = (15,0))

# Create a label contain title
frame_labelTitle = Frame(root,background = "white",)
frame_labelTitle.pack()

projectName = "ĐỀ TÀI: PHÁT TRIỂN ỨNG DỤNG HỆ THỐNG HỖ TRỢ NGƯỜI LÁI XE DÙNG HỌC SÂU"
authorName = "HỌ VÀ TÊN HỌC VIÊN: PHẠM TRẦN MINH HOÀNG - MSSV: 1980702\n"
teacherName = "HỌ VÀ TÊN GIẢNG VIÊN HƯỚNG DẪN: TS. TRẦN VŨ HOÀNG"

labelTitle = Label(frame_labelTitle,
                            text = projectName,
                            background = "white",
                            font='bold',
                            fg = "red")
labelTitle.pack(pady = (15,15))

labelTitle = Label(frame_labelTitle,
                            text = authorName + teacherName,
                            background = "white",
                            fg = "black")
labelTitle.pack(pady = (0,15))

# Create a label line
frame_labelLine = Frame(root,background = "green",height = 3)
frame_labelLine.pack(fill = BOTH)

# Create a drop list contain model detection
frame_dropListModelDetection = Frame(root,background = "white",)
frame_dropListModelDetection.pack()

label_dropListModelDetection = Label(frame_dropListModelDetection,
                            text = "1)",
                            background = "white",
                            font = ('',12),
                            fg = "black")
label_dropListModelDetection.pack(pady = (15,0), side = LEFT)

list_model_detection = [
# "yolov4",
"yolov4-288",
"yolov4-416",
# "yolov4-tiny",
"yolov4-tiny-288",
"yolov4-tiny-416",
] #etc

modelDetectionChosen = StringVar(frame_dropListModelDetection)
modelDetectionChosen.set("Select model detection") # default value

dropListModelDetection = OptionMenu(frame_dropListModelDetection, modelDetectionChosen, *list_model_detection)
dropListModelDetection.config(width=20)
dropListModelDetection.pack(pady = (15,0))

# Create a drop list contain model tracking
frame_dropListModelTracking = Frame(root,background = "white",)
frame_dropListModelTracking.pack()

label_dropListModelTracking = Label(frame_dropListModelTracking,
                            text = "2)",
                            background = "white",
                            font = ('',12),
                            fg = "black")
label_dropListModelTracking.pack(pady = (15,0), side = LEFT)

list_model_tracking = [
"MOSSE",
"MedianFlow",
"Detect only",
] #etc

modelTrackingChosen = StringVar(frame_dropListModelTracking)
modelTrackingChosen.set("Select model tracking") # default value

dropListModelTracking = OptionMenu(frame_dropListModelTracking, modelTrackingChosen, *list_model_tracking)
dropListModelTracking.config(width=20)
dropListModelTracking.pack(pady = (15,0))

# Create frame for button camera, video and label between 2 button
frame_buttonVideoCamera = Frame(root,background = "white",)
frame_buttonVideoCamera.pack()

labelTitleDroplist = Label(frame_buttonVideoCamera,
                            text = "3)",
                            background = "white",
                            font = ('',12),
                            fg = "black")
labelTitleDroplist.pack(pady = (15,0), side = LEFT)

# Create a button to use camera
buttonCamera = Button(frame_buttonVideoCamera,
                        text = "Open camera",
                        width = 10,
                        command = isCameraOpened)
buttonCamera.pack(padx = (0,10), pady = (15,0),side = LEFT)

# Create a label between button camera and button video
labelTitleVideoCamera = Label(frame_buttonVideoCamera,
                            text = "or",
                            background = "white",
                            fg = "black")
labelTitleVideoCamera.pack(pady = (15,0), side = LEFT)

# Create a button to import video
buttonVideo = Button(frame_buttonVideoCamera,
                        text = "Import video",
                        width = 10,
                        command = browseFiles)
buttonVideo.pack(padx = 10,pady=(15,0), side = LEFT)

# Create a label contain title
frame_labelTitleVideoCamera = Frame(root,background = "white",)
frame_labelTitleVideoCamera.pack()

labelTitleVideoCamera = Label(frame_labelTitleVideoCamera,
                            text = 'Camera status / Video path: ...',
                            fg = "blue")
labelTitleVideoCamera.pack()

# Create a button to run model
frame_buttonRunModel = Frame(root,background = "white",)
frame_buttonRunModel.pack()

labelTitleRunModel = Label(frame_buttonRunModel,
                            text = "4)",
                            background = "white",
                            font = ('',12),
                            fg = "black")
labelTitleRunModel.pack(pady = (15,0), side = LEFT)

buttonRunModel = Button(frame_buttonRunModel,
                        text = "Run model",
                        width = 10,
                        # command = pre_runModel)
                        command = runModel)
buttonRunModel.pack(pady=(15,0))

# Create a label contain title
frame_labelTitleRunModel = Frame(root,background = "white",)
frame_labelTitleRunModel.pack()

labelTitleRunModel = Label(frame_labelTitleRunModel,
                            text = '(Hint) When video pop-ups:\n'
                                   '- Press "a" to pause\n'
                                   '- Press "s" to run each frame\n'
                                   '- Press "d" to resume all frame\n'
                                   '- Press "q" to quit',
                            justify=LEFT,
                            fg = "blue")
labelTitleRunModel.pack()

# Let the window wait for any events
root.mainloop()
