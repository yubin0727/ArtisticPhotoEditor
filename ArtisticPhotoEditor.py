from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2 as cv
import numpy as np
MAX_SIZE = 800

## Save & Open Image
def saveImg(): # 이미지 저장
    imgPath = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Image files", "*.png;*.jpg*.jpeg")])
    if imgPath:
        cv.imwrite(imgPath, img)
        
def openImg(): # file Path 탐색 및 이미지 열기
    global img, imgPath
    imgPath = filedialog.askopenfilename(initialdir="/", title="파일 선택",
                                      filetypes=(('jpg files', '*.jpg'), ('png files', '*.png'), ('all files', '*.*')))
    if imgPath: # 이미지 읽기, 보여주기
        img = cv.imread(imgPath)
        showImg()

def showImg(): # 이미지 크기 조절, 보여주기
    global canvas, ratio, img, startx, starty, endx, endy
    # show_image -> 사용자에게 보여주는 이미지, resize
    showImg = img

    height, width = img.shape[:2]
    if width > MAX_SIZE or height > MAX_SIZE:
        if width > height:
            ratio = MAX_SIZE / width
            new_width = MAX_SIZE
            new_height = int(height * ratio)
        else:
            ratio = MAX_SIZE / height
            new_height = MAX_SIZE
            new_width = int(width * ratio)
        showImg = cv.resize(img, (new_width, new_height))
    image_pil = Image.fromarray(cv.cvtColor(showImg, cv.COLOR_BGR2RGB))
    selectedImage = ImageTk.PhotoImage(image_pil)
    
    canvas.delete("all") 
    canvas.create_image(MAX_SIZE/2, MAX_SIZE/2, anchor="center", image=selectedImage)
    canvas.image = selectedImage
    startx = int((800 - showImg.shape[1]) / 2)
    starty = int((800 - showImg.shape[0]) / 2)
    endx = 800 - startx
    endy = 800 - starty

## Edit Image
curBtn = None
area = True
top, bottom = (0, 0), (0, 0)

def clearFrame():
    global editFrame
    for widget in editFrame.winfo_children():
        widget.destroy()

def changeColor(btn): # button up&down
    global curBtn
    
    clearFrame()
    if curBtn == btn:
        btn["background"] = "#D3D3D3"
        btn["relief"] = "raised"
        curBtn=None
    else:
        if curBtn:
            curBtn["background"] = "#D3D3D3"
            curBtn["relief"] = "raised"
        btn["background"] = "#ECE6CC"
        btn["relief"] = "sunken"
        curBtn=btn

def startRectangle(event):
    global top, bottom, area, canvas
    if not area:
        top = (event.x, event.y)
        area = True

def drawRectangle(event):
    global top, bottom, area, canvas
    if area:
        bottom = (event.x, event.y)
        canvas.delete("rectangle")
        if top!=(0, 0):
            canvas.create_rectangle(top[0], top[1], event.x, event.y, outline="white", width=2, tags="rectangle")

def areaImg(btn): # 이미지 영역 선택
    global area, top, bottom, canvas
    
    if btn["background"] == "#D3D3D3":
        area=False
        btn["background"] = "#ECE6CC"
        btn["relief"] = "sunken"
    else:
        area=True
        btn["background"] = "#D3D3D3"
        btn["relief"] = "raised"
        top = (0,0)
        bottom = (0,0)
        canvas.delete("rectangle")
    
def cropImg(btn, areaBtn): # 이미지 자르기
    global img, top, bottom, ratio, area, curBtn
    
    clearFrame()
    
    if areaBtn["background"] != "#D3D3D3":
        area = True
        areaBtn["background"] = "#D3D3D3"
        areaBtn["relief"] = "raised"
    
    if curBtn:
        curBtn["background"] = "#D3D3D3"
        curBtn["relief"] = "raised"
        curBtn = None
    
    if top != (0,0) and bottom != (0,0):
        left_x, left_y = int((top[0]-startx)/ratio), int((top[1]-starty)/ratio)
        if left_x < 0: left_x = 0
        if left_y < 0: left_y = 0
        
        right_x, right_y = int((bottom[0] - startx)/ratio), int((bottom[1]-starty)/ratio)
        if right_x > endx/ratio: right_x = int(endx/ratio)
        if right_y > endy/ratio: right_y = int(endy/ratio)
        img = img[left_y:right_y, left_x:right_x]
    top = (0, 0)
    bottom = (0, 0)
    showImg()      

def rotaImg(btn):
    global img, curBtn
    
    clearFrame()
    if curBtn:
        curBtn["background"] = "#D3D3D3"
        curBtn["relief"] = "raised"
        curBtn = None
    
    img = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
    showImg()

def makeEndMode(btn):
    global editFrame
    endBtn = Button(editFrame, text="OK", width=8, height=2, padx=0, pady=0, relief="raised", font="Arial 9", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:finishImg(btn))
    endBtn.grid(row=0, column=2)
    mode = Label(editFrame, text=btn["text"], width=20, height=3, anchor="w", font=('Arial', 12))
    mode.grid(row=0, column=0, columnspan=2, padx=10)

def finishImg(btn):
    global curBtn, img, editedImg
    
    btn["background"] = "#D3D3D3"
    btn["relief"] = "raised"
    curBtn = None
    
    img = editedImg
    clearFrame()
    showImg()
    
def persImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        endBtn = Button(editFrame, text="OK", width=8, height=2, padx=0, pady=0, relief="raised", font="Arial 9", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:finishImg(btn))
        endBtn.grid(row=0, column=2)
        mode = Label(editFrame, text="Horizontal", width=20, height=3, anchor="w", font=('Arial', 12))
        mode.grid(row=0, column=0, columnspan=2, padx=10)
        editedImg = img
        persX = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        persX.grid(row=1, column=0, columnspan=3)
        persX.set(0)
        mode2 = Label(editFrame, text="Vertical", width=20, height=3, anchor="w", font=('Arial', 12))
        mode2.grid(row=2, column=0, columnspan=2, padx=10)    
        persY = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        persY.grid(row=3, column=0, columnspan=3)
        persX.set(0)
    showImg()

def brigImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        brigScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        brigScale.grid(row=1, column=0, columnspan=3)
        brigScale.set(0)
    showImg()
    
def contImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        contScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        contScale.grid(row=1, column=0, columnspan=3)
        contScale.set(0)
    showImg()
    
def expoImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        expoScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        expoScale.grid(row=1, column=0, columnspan=3)
        expoScale.set(0)
    showImg()
    
def satuImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        satuScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        satuScale.grid(row=1, column=0, columnspan=3)
        satuScale.set(0)
    showImg()

def highImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        highScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        highScale.grid(row=1, column=0, columnspan=3)
        highScale.set(0)
    showImg()
    
def shadImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        shadScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        shadScale.grid(row=1, column=0, columnspan=3)
        shadScale.set(0)
    showImg()
    
def sharImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        sharScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        sharScale.grid(row=1, column=0, columnspan=3)
        sharScale.set(0)
    showImg()

def blurImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        blurScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        blurScale.grid(row=1, column=0, columnspan=3)
        blurScale.set(0)
    showImg()
    
def grayImg(btn):
    global editFrame, editedImg, img
    changeColor(btn)
    if btn["background"] == "#ECE6CC":
        makeEndMode(btn)
        editedImg = img
        grayScale = Scale(editFrame, from_=-50, to=50, orient='horizontal', length=300)
        grayScale.grid(row=1, column=0, columnspan=3)
        grayScale.set(0)
    showImg()
    
def photoEditor():
    global editFrame
    menubar = Menu(win)
    menubar.add_command(label="Open", command=openImg) # Open -> 이미지 select & show
    menubar.add_command(label="Save", command=saveImg) # Save -> 수정된 이미지 저장
 
    buttonFrame = Frame(win)
    buttonFrame.grid(row=0, column=1, rowspan=10, sticky="n")
    editFrame = Frame(win)
    editFrame.grid(row=10, column=1, rowspan=10, sticky="n")
    
    areaBtn = Button(buttonFrame, text="Area", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:areaImg(areaBtn)) # 이미지 영역 선택
    areaBtn.grid(row=0, column=0, padx=10, pady=10)
    cropBtn = Button(buttonFrame, text="Crop", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:cropImg(cropBtn, areaBtn)) # 이미지 자르기    
    cropBtn.grid(row=0, column=1, padx=10, pady=10)    

    rotaBtn = Button(buttonFrame, text="Rotate(Clock)", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10",bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:rotaImg(rotaBtn)) # 이미지 회전
    persBtn = Button(buttonFrame, text="Perspective", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10",bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:persImg(persBtn)) # 원근감(수평, 수직)
    rotaBtn.grid(row=1, column=0, padx=10, pady=10)
    persBtn.grid(row=1, column=1, padx=10, pady=10)
    
    brigBtn = Button(buttonFrame, text="Brightness", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:brigImg(brigBtn)) # 밝기
    contBtn = Button(buttonFrame, text="Contrast", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:contImg(contBtn)) # 대비
    expoBtn = Button(buttonFrame, text="Exposure", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:expoImg(expoBtn)) # 노출
    brigBtn.grid(row=2, column=0, padx=10, pady=10)
    contBtn.grid(row=2, column=1, padx=10, pady=10)
    expoBtn.grid(row=2, column=2, padx=10, pady=10)
    
    satuBtn = Button(buttonFrame, text="Saturation", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:satuImg(satuBtn)) # 채도
    highBtn = Button(buttonFrame, text="Highlight", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:highImg(highBtn)) # 하이라이트
    shadBtn = Button(buttonFrame, text="Shadow", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:shadImg(shadBtn)) # 그림자
    satuBtn.grid(row=3, column=0, padx=10, pady=10)
    highBtn.grid(row=3, column=1, padx=10, pady=10)
    shadBtn.grid(row=3, column=2, padx=10, pady=10)
    
    sharBtn = Button(buttonFrame, text="Sharpness", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:sharImg(sharBtn)) # 선명하게
    blurBtn = Button(buttonFrame, text="Blur", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:blurImg(blurBtn)) # 흐릿하게
    grayBtn = Button(buttonFrame, text="Gray", width=10, height=3, padx=0, pady=0, relief="raised", font="Arial 10", bg="#D3D3D3", activebackground="#ECE6CC", command=lambda:grayImg(grayBtn)) # 그레이
    sharBtn.grid(row=4, column=0, padx=10, pady=10)
    blurBtn.grid(row=4, column=1, padx=10, pady=10)
    grayBtn.grid(row=4, column=2, padx=10, pady=10)
        
    win.config(menu=menubar)
   
if __name__ == '__main__':
    win = Tk() # Tkinter 창 생성
    win.title("ArtisticPhotoEditor")
    win.geometry("1200x800+150+100") # pixel
    
    global img, imgPath, canvas
    img = np.zeros(1)
    imgPath = "" # 이미지 경로 지정
    
    canvas = Canvas(win, width=MAX_SIZE, height=MAX_SIZE)
    canvas.grid(row=0, column=0, rowspan=20, padx=10)
    canvas.bind("<ButtonPress-1>", startRectangle)
    canvas.bind("<ButtonRelease-1>", drawRectangle)
    photoEditor()
    win.mainloop()