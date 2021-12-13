# importing tkinter module
from tkinter import *
#from tkinter.ttk import *
from tkinter import ttk
# creating tkinter window
import time
from tkinter import messagebox as ms
from PIL import ImageTk, Image 

white= "#ffffff"
lightBlue2= "#adc5ed"
font= "Constantia"
fontButtons= (font, 12)
maxWidth= 1200

maxHeight= 600

a=1

def popup_window():
  popuproot=Tk()
  popuproot.title('FACE MASK')
  popuproot.iconbitmap('mask icon.ico')
  popuproot.resizable(False,False)
  # Progress bar widget
  progress = ttk.Progressbar(popuproot, orient = HORIZONTAL,length = 1000, mode = 'determinate')

  # Function responsible for the updation
  # of the progress bar value

     
     
  lb1=Label(popuproot,text='',fg='black',width = 25,height = 1,font=('calibri', 25 ))
         
  def bar():
    lb1.config(text="starting app")
    progress['value'] = 20
    popuproot.update_idletasks()
    # Ignore  the warnings
    import warnings
    warnings.filterwarnings('always')
    warnings.filterwarnings('ignore')

    
    time.sleep(1)
    lb1.config(text="Loading basic packages")

    progress['value'] = 40
    popuproot.update_idletasks()
    # data visualisation and manipulation
    import numpy as np
    import cv2      
    import smtplib 
    from email.mime.multipart import MIMEMultipart 
    from email.mime.text import MIMEText 
    from email.mime.base import MIMEBase 
    from email import encoders
    
    import os 
    from PIL import Image
    import matplotlib.pyplot as plt

    time.sleep(1)
    lb1.config(text="Loading Deep learning packages")

    progress['value'] = 50
    popuproot.update_idletasks()
    import keras
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    time.sleep(1)
    lb1.config(text="Loading trained model")

    progress['value'] = 60
    popuproot.update_idletasks()
    model = load_model('model2.h5')
    time.sleep(1)
    lb1.config(text="loading the Application")

    def send_an_email(file_path):
      email_user = 'aeroapj@gmail.com'
      email_password = 'demdum*&987'
      email_send = "aeroapj@gmail.com"
      subject = 'No mask detected'
      msg = MIMEMultipart()
      msg['From'] = email_user
      msg['To'] = email_send
      msg['Subject'] = subject
      body = 'Absence of mask detected!'
      msg.attach(MIMEText(body,'plain'))
      filename=file_path
      attachment  =open(filename,'rb')
      part = MIMEBase('application','octet-stream')
      part.set_payload((attachment).read())
      encoders.encode_base64(part)
      part.add_header('Content-Disposition',"attachment; filename= "+filename)
      msg.attach(part)
      text = msg.as_string()
      server = smtplib.SMTP('smtp.gmail.com',587)
      server.starttls()
      server.login(email_user,email_password)
      server.sendmail(email_user,email_send,text)
      server.quit()

    def TrackImages():
      
      harcascadePath="haarcascade_frontalface_default.xml"
      faceCascade = cv2.CascadeClassifier(harcascadePath);    
      


      mainWindow=Toplevel(popuproot)
      mainWindow.title("face mask Management")
      mainWindow.iconbitmap('mask icon.ico')
      mainWindow.configure(bg='white')
      mainWindow.geometry('%dx%d+%d+%d' % (maxWidth,maxHeight,0,0))


      #mainWindow.resizable(0,0)
      mainWindow.grid_rowconfigure(0, weight=1)
      mainWindow.grid_columnconfigure(0, weight=1)

      #load2 = Image.open('libpic2.jpg')
      #render2 = ImageTk.PhotoImage(load2)

      #img1 = Label(mainWindow, image=render2)
      #img1.place(x=0, y=0, relwidth=1, relheight=1)

      mainFrame = Frame(mainWindow)


      mainFrame.place(x=20, y=20)                


      lmain = Label(mainFrame)

      #lmain.grid(row=0, column=0)
      lmain.pack(side=LEFT)

      cam = cv2.VideoCapture(0)
      font = cv2.FONT_HERSHEY_SIMPLEX
      
      



      def show_frame():
          global a
          

          ret, im =cam.read()
          if im.size>0:
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)
            
            for(x,y,w,h) in faces:
                #rol_gray=gray[y:y + h,x:x + w]
                rol_color=im[y-20:y + h+20,x-20:x + w+20]
                print("scanning for no mask")                   
                print("Checking for non wearing mask")
                cv2.imwrite("mask_check/"+ str(a) + ".jpg",rol_color)        



                #imgr=cv2.imread("mask_check/"+ str(a) + ".jpg")
                #print(a)
                #image =cv2.imread("mask_check/"+ str(a) + ".jpg",0)
                #histr = cv2.calcHist([image],[0],None,[256],[0,256])

                X=cv2.imread("mask_check/"+ str(a) + ".jpg",3)

                X=cv2.resize(X,(150,150))
                
                #X=cv2.cvtColor(X, cv2.COLOR_BGR2HSV)
                X = np.array(X)
                #X = X/255
                X = np.expand_dims(X, axis=0)

                #print(np.round(model.predict(X)))
                #face=int(np.round(model.predict(X))[0][0])
                face=(model.predict(X))[0]
                
                #faceperval=round(max(face)*100,2)
                faceperval=round(face[1]*100,2)
               
                if faceperval>80:
                    cv2.rectangle(im,(x-20,y-20),(x+w+20,y+h+20),(0,0,255),2)
                    cv2.putText(im,str("No Mask"),(x-20,y+h+20), font, 1,(0,0,255),2) 
                    print("Absence of mask detected")
                    print("send text alert to email")
                    
                    # opens the image
                    img2 = Image.open("mask_check/"+ str(a) + ".jpg",'r')

                    # resize the image and apply a high-quality down sampling filter
                    img2 = img2.resize((300, 300), Image.ANTIALIAS)

                    # PhotoImage class is used to add image to widgets, icons etc
                    img2 = ImageTk.PhotoImage(img2)

                    # create a label
                    panel = Label(mainWindow, image = img2)

                    # set the image as img 
                    panel.image = img2
                    panel.place(x=800,y=100)
                    try:                    
                      send_an_email("mask_check/"+ str(a) + ".jpg")
                      print("mail send")
                    except:
                      print("issue in mail send")               

                    faceper="It's {} no face mask detected".format(faceperval)                    

                    lbl2.config(text=faceper)
                    
                    txt3.config(text="mail has been forwarded")
                    a+=1
                else:
                    cv2.rectangle(im,(x-20,y-20),(x+w+20,y+h+20),(255,255,255),2)
                    cv2.putText(im,str("detected face"),(x-20,y+h+20), font, 1,(255,255,255),2)
                
                
              
            cv2image   = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
            img   = Image.fromarray(cv2image).resize((650,450))
            imgtk = ImageTk.PhotoImage(image = img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            #roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          lmain.after(10, show_frame)

     
      

      #mainWindow.mainloop()



      closeButton = Button(mainWindow, text = "close", font = ('calibri',18,'bold'), bg = "lightblue",activebackground="red",activeforeground="white", width = 20)
      closeButton.configure(command= lambda: [cam.release(),mainWindow.destroy()])              
      closeButton.place(x=230,y=500)
      
    

      ldl1 = Label(mainWindow, text="Face mask detection"  ,height=2  ,fg="black"  ,bg="lightblue" ,font=('calibri', 15, ' bold ') ) 
      ldl1.place(x=850, y=20)
      
      lb = Label(mainWindow,text='',bg='lightblue',width=50,height=23)
      lb.place(x=780,y=80)

      lbl2 =Label(mainWindow, text="",width=35 ,fg="black"  ,bg="lightblue"  ,height=2 ,font=('calibri', 15, ' bold ')) 
      lbl2.place(x=780, y=450)

     

      lbl3 =Label(mainWindow, text="Mail: ",width=13  ,fg="black"  ,bg="lightblue"  ,height=2 ,font=('calibri', 15, ' bold ')) 
      lbl3.place(x=620, y=520)

      txt3 =Label(mainWindow, text="" ,bg="lightblue"  ,fg="black"  ,width=35  ,height=2, activebackground = "lightblue" ,font=('calibri', 15, ' bold ')) 
      txt3.place(x=780, y=520)

      show_frame()
      
      mainWindow.mainloop()




    progress['value'] = 80
    popuproot.update_idletasks()
    time.sleep(1)
    lb1.config(text="process completed")
    progress['value'] = 100
    TrackImages()
          
          

  progress.pack(side=TOP,padx=21,pady = 10)
  lb1.pack(side=TOP,pady = 10)

     
     

  # This button will initialize
  # the progress bar
     
  Button(popuproot, text = 'Start',width = 10,height = 1,fg="black"  ,bg="lightblue" ,font=('calibri', 15, ' bold '), command = bar).pack(side=BOTTOM,pady = 10)
  popuproot.mainloop()

popup_window()
