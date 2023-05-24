from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2 as cv
MAX_SIZE = 800

img = cv.imread("C:/Users/sinyb/Desktop/background.jpg") # 이미지 읽은 결과 저장
imgPath = ""  # 이미지 경로 저장

def saveImg(): # 이미지 저장
    imgPath = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Image files", "*.png;*.jpg*.jpeg")])
    if imgPath:
        cv.imwrite(imgPath, img)
        
def openImg(): # file Path 탐색 및 이미지 열기
    imgPath = filedialog.askopenfilename(initialdir="/", title="파일 선택",
                                      filetypes=(('jpg files', '*.jpg'), ('png files', '*.png'), ('all files', '*.*')))
    if imgPath: # 이미지 읽기, 보여주기
        img = cv.imread(imgPath)
        showImage(img)


def showImage(img): # 이미지 크기 조절, 보여주기
    # show_image -> 사용자에게 보여주는 이미지, resize
    show_image = img

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
        show_image = cv.resize(img, (new_width, new_height))
    image_pil = Image.fromarray(cv.cvtColor(show_image, cv.COLOR_BGR2RGB))
    selectedImage = ImageTk.PhotoImage(image_pil)
    
    canvas.delete("all") 
    canvas.create_image(MAX_SIZE/2, MAX_SIZE/2, anchor="center", image=selectedImage)
    canvas.image = selectedImage
    

win = Tk() # Tkinter 창 생성
win.title("ArtisticPhotoshop")
win.geometry("1200x800+150+100") # pixel

canvas = Canvas(win, width=MAX_SIZE, height=MAX_SIZE)
canvas.grid(row=5, column=5)

menubar = Menu(win)
menubar.add_command(label="Open", command=openImg) # Open -> 이미지 select & show
menubar.add_command(label="Save", command=saveImg) # Save -> 수정된 이미지 저장

win.config(menu=menubar)
win.mainloop()