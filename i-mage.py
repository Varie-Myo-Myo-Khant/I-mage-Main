import tkinter
from tkinter import *
import time
import customtkinter
from customtkinter import *
from PIL import Image, ImageTk
from MainPage import main

splash_root = Tk()
splash_root.title("i-Mage")
splash_root.iconbitmap("Image/favicon.ico")
splash_root.configure(bg="#181818")
width = 600
height = 400
x = (splash_root.winfo_screenwidth()/2)-(width/2)
y = (splash_root.winfo_screenheight()/2)-(height/2)
splash_root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
splash_root.resizable(width=FALSE, height=FALSE)


Frame(splash_root, width=800, height=600, bg="#181818").place(x=0, y=0)
brand = CTkImage(Image.open("Image/i-logo.png"), size=(350, 130))
logo = CTkLabel(splash_root, image=brand, text="")
logo.place(x=126, y=80)


loading = Label(splash_root, text="loading...", bg='#181818',
                fg="white", font=("Poppins", 16))
loading.place(x=20, y=350)

# Animation
image_a = ImageTk.PhotoImage((Image.open("Image/c1.png")), size=(10, 10))
image_b = ImageTk.PhotoImage((Image.open("Image/c2.png")), size=(10, 10))

# for i in range(2):
#     i1=Label(bg,text="",image=image_a,bg="#181818").place(x=240,y=200)
#     i2 =Label(bg, text="", image=image_b,bg="#181818").place(x=270, y=200)
#     i3 = Label(bg, text="", image=image_b,bg="#181818").place(x=300, y=200)
#     i4 = Label(bg, text="", image=image_b,bg="#181818").place(x=330, y=200)
#     root.update_idletasks()
#     time.sleep(0.5)
#
#     i1 = Label(bg, text="", image=image_b, bg="#181818").place(x=240, y=200)
#     i2 = Label(bg, text="", image=image_a, bg="#181818").place(x=270, y=200)
#     i3 = Label(bg, text="", image=image_b, bg="#181818").place(x=300, y=200)
#     i4 = Label(bg, text="", image=image_b, bg="#181818").place(x=330, y=200)
#     root.update_idletasks()
#     time.sleep(0.5)
#
#     i1 = Label(bg, text="", image=image_b, bg="#181818").place(x=240, y=200)
#     i2 = Label(bg, text="", image=image_b, bg="#181818").place(x=270, y=200)
#     i3 = Label(bg, text="", image=image_a, bg="#181818").place(x=300, y=200)
#     i4 = Label(bg, text="", image=image_b, bg="#181818").place(x=330, y=200)
#     root.update_idletasks()
#     time.sleep(0.5)
#
#     i1 = Label(bg, text="", image=image_b, bg="#181818").place(x=240, y=200)
#     i2 = Label(bg, text="", image=image_b, bg="#181818").place(x=270, y=200)
#     i3 = Label(bg, text="", image=image_b, bg="#181818").place(x=300, y=200)
#     i4 = Label(bg, text="", image=image_a, bg="#181818").place(x=330, y=200)
#     root.update_idletasks()
#     time.sleep(0.5)


for i in range(2):
    i1 = Label(splash_root, text="", image=image_a,
               bg="#181818").place(x=250, y=220)
    i2 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=280, y=220)
    i3 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=310, y=220)
    i4 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=340, y=220)
    splash_root.update_idletasks()
    time.sleep(0.5)

    i1 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=250, y=220)
    i2 = Label(splash_root, text="", image=image_a,
               bg="#181818").place(x=280, y=220)
    i3 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=310, y=220)
    i4 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=340, y=220)
    splash_root.update_idletasks()
    time.sleep(0.5)

    i1 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=250, y=220)
    i2 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=280, y=220)
    i3 = Label(splash_root, text="", image=image_a,
               bg="#181818").place(x=310, y=220)
    i4 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=340, y=220)
    splash_root.update_idletasks()
    time.sleep(0.5)

    i1 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=250, y=220)
    i2 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=280, y=220)
    i3 = Label(splash_root, text="", image=image_b,
               bg="#181818").place(x=310, y=220)
    i4 = Label(splash_root, text="", image=image_a,
               bg="#181818").place(x=340, y=220)
    splash_root.update_idletasks()
    time.sleep(0.5)


def welcomeFrame():
    splash_root.destroy()
    welcome_root = CTk()
    welcome_root.title("i-Mage")
    welcome_root.iconbitmap("Image/favicon.ico")
    set_appearance_mode("dark")
    set_default_color_theme("green")

    width = 900
    height = 600
    x = (welcome_root.winfo_screenwidth() // 2) - (width // 2)
    y = (welcome_root.winfo_screenheight() // 2) - (height // 2)
    welcome_root.geometry(f"{width}x{height}+{x+80}+{y}")
    welcome_root.resizable(width=FALSE, height=FALSE)

    backImage = CTkImage(Image.open("Image/landing_bg.png"), size=(900, 600))
    main_Canva = CTkLabel(welcome_root, image=backImage, text="")
    main_Canva.pack()
    brand = CTkImage(Image.open("Image/i-logo.png"), size=(180, 60))

    w_Frame = CTkFrame(master=main_Canva, width=500, height=350, bg_color="#2B2B2B", border_width=1,
                       border_color="#00A36C", corner_radius=12)
    w_Frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    logo = CTkLabel(master=w_Frame, image=brand, text="")
    logo.place(x=160, y=40)

    header = CTkLabel(master=w_Frame, text="Welcome", font=("Poppins", 38, "bold"), bg_color="transparent",
                      text_color="#ffffff")
    header.place(x=170, y=120)

    subHeader = CTkLabel(master=w_Frame,
                         text=" A program to provide image processing services\n for a wide range of users.",
                         font=("Poppins", 16), text_color="#ffffff")

    subHeader.place(x=80, y=184)

    def goToMain():
        welcome_root.destroy()
        main()

    startButton = CTkButton(master=w_Frame, text="Get Started", fg_color="#00A36C", width=160, height=50,
                            font=("Poppins", 16), hover_color="#00A36C", command=goToMain)
    startButton.place(x=170, y=260)

    welcome_root.mainloop()


splash_root.after(100, welcomeFrame)

splash_root.mainloop()
