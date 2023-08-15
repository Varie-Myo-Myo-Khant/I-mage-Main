import tkinter
import customtkinter
from PIL.ImageTk import PhotoImage
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from tkinter import filedialog
import pytesseract


# path for pytesseract for Image to Text
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


# Declaring icons as public from the start
uploadIcon = CTkImage(Image.open("Image/upload.png"), size=(30, 30))
downloadIcon = CTkImage(Image.open("Image/download.png"), size=(22, 22))
logo = CTkImage(Image.open("Image/i-logo.png"), size=(140, 50))
linkicon = CTkImage(Image.open("Image/link.png"), size=(20, 20))
plusicon = CTkImage(Image.open("Image/plus_icon.png"), size=(20, 20))
rightArrowIcon = CTkImage(Image.open("Image/arrow_right.png"), size=(40, 40))
smileIcon = CTkImage(Image.open("Image/smile.png"), size=(20, 20))
scannerQRPhoto = CTkImage(Image.open("Image/scanner_qr.png"), size=(300, 300))
# Tab Button colors variables
active_btn_color = "#00BB6D"
inactive_tab_color = "transparent"

# Creating for User Uploaded Image Variable as public to use in another places.
uploaded_image = None

# Creating after image (after changing) to be implement download function
after_image = None
extractedText=None
# Functions

# Function for changing frame


def on_tab_click(sectionframes, sectionbuttons, currentFrame, currentbutton):
    global after_image

    #to get return from extracted text and passed it into save text function
    
    # Forgetting all Frames
    for frame in sectionframes:
        frame.pack_forget()
        
    
    
    # Setting Inactive Tab Button Color
    for button in sectionbuttons:
        button.configure(fg_color=inactive_tab_color)

    # Setting current Frame and Button Color
    currentFrame.pack(expand=1, fill="both")
    currentbutton.configure(fg_color=active_btn_color)

    # Setting Left Icon in every frame
    # Brand Logo
    brand_logo = CTkLabel(currentFrame, image=logo, text="")
    brand_logo.place(x=26, y=26)

    '''Middle Section : Where main function work'''

    # As 6 frames don't have same functionality, following if are to hide/show button,slider

    if currentFrame != sectionframes[5]:

        # Result Image Frame
        resultFrame = CTkFrame(currentFrame, width=680, height=470,
                               bg_color="#121212", border_width=1, border_color="#00BB6D")
        resultFrame.place(x=800, y=120)

        # Result Image Label Frame
        result_label = CTkLabel(resultFrame, text="", width=600, height=400)
        result_label.place(x=38, y=32)
        after_image = None
        # creating before image upload frame
        create_before_image_frame(currentFrame, result_label)

        # Middle Right Arrow Icon Creation
        arrow_label = CTkLabel(
            currentFrame, image=rightArrowIcon, text="", bg_color="transparent")
        arrow_label.place(x=740, y=350)

        # result text
        resultText = CTkLabel(result_label, text="Result  ", image=smileIcon, compound="right", font=("Poppins", 16),
                              text_color="#EDEADE")
        resultText.place(x=270, y=200)

        #fucntion to get extracted text when user clicked generated text button
        def generate_text_btn_clicked():
            global extractedText
            extractedText = generate_text(
                currentFrame, result_label, uploaded_image, resultText)
            
        if currentFrame == sectionframes[0]:
            print("lol", currentFrame == sectionframes[0])
            # Generate Button for Image to Cartoon
            generate_Cartoon_Button = CTkButton(currentFrame, text=" Generate", font=("Poppins", 20), border_width=0, corner_radius=32,
                                                fg_color="#00BB6D", width=600, height=50, hover_color="null", command=lambda: generate_cartoon(currentFrame, result_label, uploaded_image, resultText))
            generate_Cartoon_Button.place(x=460, y=630)

        elif currentFrame == sectionframes[1]:
            # Generate Button for Image to Text
            generate_Text_Button = CTkButton(currentFrame, text=" Generate", font=("Poppins", 20), border_width=0, corner_radius=32,
                                             fg_color="#00BB6D", width=600, height=50, hover_color="null", command=generate_text_btn_clicked)
            
            generate_Text_Button.place(x=460, y=630)
            
        elif currentFrame == sectionframes[2]:
            brightness_slider = CTkSlider(
                currentFrame, from_=-255, to=255, width=600, command=lambda val: process_and_display_image(currentFrame, 'Brightness', brightness_slider.get(), uploaded_image, result_label, resultText))
            brightness_slider.set(0)
            brightness_slider.place(x=460, y=630)

        elif currentFrame == sectionframes[3]:
            contrast_slider = CTkSlider(
                currentFrame, from_=0.1, to=3.0, width=600, command=lambda val: process_and_display_image(currentFrame, 'Contrast', contrast_slider.get(), uploaded_image, result_label, resultText))
            contrast_slider.set(1.0)
            contrast_slider.place(x=460, y=630)

        elif currentFrame == sectionframes[4]:
            blur_slider = CTkSlider(currentFrame, from_=2, to=25, width=600, command=lambda val: process_and_display_image(currentFrame,
                                                                                                                           'Blur', blur_slider.get(), uploaded_image, result_label, resultText))
            blur_slider.set(2)
            blur_slider.place(x=460, y=630)

        if currentFrame != sectionframes[1]:
            # Download Button
            download_Button = CTkButton(currentFrame, text="Download", font=("Poppins", 20), image=downloadIcon, compound="right",
                                        border_width=1, border_color="#00BB6D", corner_radius=32,
                                        fg_color="transparent", width=600, height=50, hover_color="null", command=lambda: download_image(currentFrame, uploaded_image))
            download_Button.place(x=460, y=696)
        else:
            saveText_Button = CTkButton(currentFrame, text="Save Text", font=("Poppins", 20), image=downloadIcon, compound="right",
                                        border_width=1, border_color="#00BB6D", corner_radius=32,
                                        fg_color="transparent", width=600, height=50, hover_color="null", command=lambda: save_text(currentFrame, extractedText, uploaded_image))
            saveText_Button.place(x=460, y=696)

    else:
        scanQRSection(currentFrame)

# Function for document scanner frame to only create QR code to redirect the mobile app.


def scanQRSection(currentFrame):
    # Before Image Frame
    scanFrame = CTkFrame(currentFrame, width=600, height=530,
                         bg_color="#121212", border_width=0.6, border_color="#00BB6D")
    scanFrame.place(x=450, y=180)

    # Before Image Label
    scan_label = CTkLabel(scanFrame, text="", width=550,
                          height=480, justify="center")
    scan_label.place(x=10, y=10)

    # To show Browse Your Image button and after User uploaded the button will destory and the image will show in the imagelabel.
    scanQrimg = CTkButton(scan_label, text="Scan Me ! ", font=("Poppins", 30), image=scannerQRPhoto,
                          fg_color="transparent", hover_color="null", compound="bottom", anchor="end", text_color="#EDEADE",
                          corner_radius=32)
    scanQrimg.place(x=120, y=15)

    # result text
    resultText = CTkLabel(scan_label, text="Scan the QR code with your mobile camera \nto instantly download our Document Scanner App,\nwhich effortlessly transforms physical documents \ninto digital PDF versions.", font=("Poppins", 20),
                          width=500, justify="center")
    resultText.place(x=30, y=390)

# Function for brightness, contrast,blur processing.


def process_and_display_image(currentFrame, imgSetting, value, uploaded_image, result_label, resultText):

    global after_image
   
    # if user click generate button without uploading image, it will alert to choose image first.
    if uploaded_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")

        t.iconbitmap("Image/favicon.ico")

        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x + 120}+{y}")

        t.resizable(width=False, height=False)

        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Generate!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=74, y=60)
        alertLabel2 = CTkLabel(t, text="Please choose your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", hover_color="null", font=("Poppins", 16), border_color="#00BB6D",
                                border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)
        t.mainloop()

    else:

        if imgSetting == "Brightness":
            cvProcessed_image = cv2.convertScaleAbs(
                uploaded_image, alpha=1, beta=value)

        elif imgSetting == "Contrast":
            cvProcessed_image = cv2.convertScaleAbs(
                uploaded_image, alpha=value, beta=0)

        elif imgSetting == "Blur":
            cvProcessed_image = None
            value = int(value)
            if value > 2:
                value = value*2+1
                cvProcessed_image = cv2.GaussianBlur(
                    uploaded_image, (value, value), 0)

        # Storing the after image for download before changing into image object
        after_image = cvProcessed_image

        # Convert processed image to RGB for PIL
        processed_rgb = cv2.cvtColor(cvProcessed_image, cv2.COLOR_BGR2RGB)
        # Convert to a PIL Image object
        processed_image_pil = Image.fromarray(processed_rgb)

        # Resize image if necessary
        max_size = 500
        if max(processed_image_pil.size) > max_size:
            processed_image_pil.thumbnail((max_size, max_size))

        # Convert to a PhotoImage object
        processed_image = ImageTk.PhotoImage(processed_image_pil)

        # Update the result_label widget with the cartoon image
        result_label.configure(image=processed_image)
        result_label.image = processed_image

        # Destroy the resultText widget (optional)
        resultText.destroy()

# Image to Cartoon to use in generate_cartoon function


def convert_to_cartoon(uploaded_image):

    # for after changing image for download
    global after_image

    # Convert the image to grayscale
    gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

    # Apply a median blur
    gray = cv2.medianBlur(gray, 5)

    # Detect the edges in the image
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply a bilateral filter to the original image
    color = cv2.bilateralFilter(uploaded_image, 9, 250, 250)

    # Combine the edges with the original image
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # Increase the color saturation
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
    cartoon[:, :, 1] = cartoon[:, :, 1]*1.5
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_HSV2BGR)

    # Clip any pixel values that fall outside the range [0, 255]
    cartoon = np.clip(cartoon, 0, 255)

    # Storing the cartoonized image for download before changing into image object
    after_image = cartoon

    # After above, cartoon image came out and the following are changing into photo

    # Convert cartoon image to RGB for PIL
    cartoon_image = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)

    # Convert to a PIL Image object
    cartoon_image_pil = Image.fromarray(cartoon_image)

    # Resize image if necessary
    max_size = 500
    if max(cartoon_image_pil.size) > max_size:
        cartoon_image_pil.thumbnail((max_size, max_size))

    # Convert to a PhotoImage object
    cartoon_image_photo = ImageTk.PhotoImage(cartoon_image_pil)

    return cartoon_image_photo

# Function for generating image to cartoon button
def generate_cartoon(currentFrame, result_label, uploaded_image, resultText):

    # if user click generate button without uploading image, it will alert to choose image first.
    if uploaded_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")

        t.iconbitmap("Image/favicon.ico")

        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x + 120}+{y}")

        t.resizable(width=False, height=False)

        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Generate!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=74, y=60)
        alertLabel2 = CTkLabel(t, text="Please choose your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16), hover_color="null", border_color="#00BB6D",
                                border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)
        t.mainloop()

    else:
        cartoon_image = convert_to_cartoon(uploaded_image)
        # Update the result_label widget with the cartoon image
        result_label.configure(image=cartoon_image)
        result_label.image = cartoon_image

        # Destroy the resultText widget (optional)
        resultText.destroy()


# Function for generating image to carton button
def generate_text(currentFrame, result_label, uploaded_image, resultText):
    
    # if user click generate button without uploading image, it will alert to choose image first.
    if uploaded_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")

        t.iconbitmap("Image/favicon.ico")

        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x + 120}+{y}")

        t.resizable(width=False, height=False)

        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Generate!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=74, y=60)
        alertLabel2 = CTkLabel(t, text="Please choose your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16),hover_color="null", border_color="#00BB6D",
                                border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)
        t.mainloop()

    else:

        # Convert the image to grayscale
        gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

        # Use Tesseract OCR to extract text from the image
        extracted_text = pytesseract.image_to_string(gray)

        #if no text in the image, we will add alert message in the textbox field.
        if not extracted_text.strip():
            extracted_text = "There is no text in your uploaded image! Please try with another photo."
        
            # Destroy the resultText widget (optional)
            resultText.destroy()

            # Creating Text Box for Extracted text and it will display in the result_label
            text_box = CTkTextbox(result_label,  width=600, height=500, font=("Poppins", 24),
                                text_color="red")
            text_box.place(x=10, y=10)
            text_box.insert("0.0", extracted_text)

        else:
            # Destroy the resultText widget (optional)
            resultText.destroy()

            # Creating Text Box for Extracted text and it will display in the result_label
            text_box = CTkTextbox(result_label,  width=600, height=500, font=("Poppins", 24),
                                  text_color="#EDEADE")
            text_box.place(x=10, y=10)
            text_box.insert("0.0", extractedText)

        return extracted_text

# Function for saving text from the after generating image to text
def save_text(currentFrame, extractedText,uploaded_image):

    # # if user click save button without uploading image, it will alert to choose image first.
    if uploaded_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")
        t.iconbitmap("favicon.ico")
        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x+120}+{y}")

        t.resizable(width=False, height=False)
        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Save!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=100, y=60)
        alertLabel2 = CTkLabel(t, text="Please choose your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16), hover_color="null",
                                border_color="#00BB6D", border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)

        t.mainloop()

    # when user uploaded the image and didn't click the generate button and click save button first, it will alert to generate first.
    elif extractedText is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")

        t.iconbitmap("Image/favicon.ico")

        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x+120}+{y}")

        t.resizable(width=False, height=False)
        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Save!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=100, y=60)
        alertLabel2 = CTkLabel(t, text="Please generate your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16), hover_color="null",
                                border_color="#00BB6D", border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)

        t.mainloop()

    elif extractedText is not None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(extractedText)

    
# Function for downloading the after image
def download_image(currentFrame, uploaded_image):

    # # if user click download button without uploading image, it will alert to choose image first.
    if uploaded_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")
        t.iconbitmap("favicon.ico")
        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x+120}+{y}")

        t.resizable(width=False, height=False)
        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Download!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=74, y=60)
        alertLabel2 = CTkLabel(t, text="Please choose your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16),hover_color="null",
                                border_color="#00BB6D", border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)

        t.mainloop()

    # when user uploaded the image and didn't click the generate button and click download button first, it will alert to generate first.
    elif after_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")

        t.iconbitmap("Image/favicon.ico")

        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x+120}+{y}")

        t.resizable(width=False, height=False)
        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Download!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=74, y=60)
        alertLabel2 = CTkLabel(t, text="Please generate your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16), hover_color="null",
                                border_color="#00BB6D", border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)

        t.mainloop()

    elif after_image is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            cv2.imwrite(save_path, after_image)

# Uploading Image for first time function


def addImage(image_label, addPhoto):

    # calling global uploaded_image variable to use in another places
    global uploaded_image

    file_path = filedialog.askopenfilename(
        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:

        uploaded_image = cv2.imread(file_path)

        # Convert image to RGB for PIL
        rgbimage = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)

        # Convert to a PIL Image object
        image_pil = Image.fromarray(rgbimage)

        # Resize image if necessary
        max_size = 500
        if max(image_pil.size) > max_size:
            image_pil.thumbnail((max_size, max_size))

        # Convert to a PhotoImage object
        image_photo = ImageTk.PhotoImage(image_pil)

        # Update label and add the image
        image_label.configure(image=image_photo)
        image_label.image = image_photo

        addPhoto.destroy()

# Function for uploading new photo
def browse_new_image(result_label, image_label, addPhoto):
    # calling global uploaded_image variable to use in another places
    global uploaded_image
    # checking if the image is uploaded, if there is already an uploaded image, it will upload new image. Unless it will pass.
    if image_label.cget("image") and result_label.cget("image"):
        file_path = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])

        if file_path:

            uploaded_image = cv2.imread(file_path)

            # Convert image to RGB for PIL
            rgbimage = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)

            # Convert to a PIL Image object
            image_pil = Image.fromarray(rgbimage)

            # Resize image if necessary
            max_size = 500
            if max(image_pil.size) > max_size:
                image_pil.thumbnail((max_size, max_size))

            # Convert to a PhotoImage object
            image_photo = ImageTk.PhotoImage(image_pil)

            # Update label and add the image
            image_label.configure(image=image_photo)
            image_label.image = image_photo

            addPhoto.destroy()
            result_label.configure(image="")  # clear before result image
    else:
        pass

# Function for Creating Frame for Upload Image Section and Showing Uploaded Image


def create_before_image_frame(currentFrame, result_label):
    # Before Image Frame
    imageFrame = CTkFrame(currentFrame, width=680, height=470,
                          bg_color="#121212", border_width=0.6, border_color="#00BB6D")
    imageFrame.place(x=39, y=120)

    # Before Image Label
    image_label = CTkLabel(imageFrame, text="", width=600,
                           height=400, justify="center")
    image_label.place(x=38, y=32)

    # To show Browse Your Image button and after User uploaded the button will destory and the image will show in the imagelabel.
    addPhoto = CTkButton(image_label, text="Browse Your Image ", font=("Poppins", 16), image=uploadIcon,
                         fg_color="transparent", hover_color="null", compound="top", anchor="end", text_color="#EDEADE",
                         corner_radius=32, command=lambda: addImage(image_label, addPhoto))
    addPhoto.place(x=208, y=166)

    # For adding new images
    browse_new = CTkButton(currentFrame, text="Select new image", image=plusicon, compound="right", text_color="#00BB6D", font=(
        "Poppins", 15), hover_color="null", bg_color="transparent", fg_color="transparent", command=lambda: browse_new_image(result_label, image_label, addPhoto))
    browse_new.place(x=36, y=600)


def main():

    # Creating Frames as public for 6 sections to change Frame According to current Button
    root = CTk()
    # Setting window Title,Icon, appearance mode and color theme
    root.title("I-mage")
    root.iconbitmap("Image/favicon.ico")
    root.geometry("{}x{}+0+0".format(root.winfo_screenwidth(),
                                     root.winfo_screenheight()))
    set_appearance_mode("dark")
    set_default_color_theme("green")
    root.resizable(width=FALSE, height=FALSE)

    # Image to Cartoon Frame
    imgCarFrame = CTkFrame(root, fg_color="transparent")
    imgCarFrame.pack(expand=1, fill="both")
    # Image to Text Frame
    imgTextFrame = CTkFrame(root, fg_color="transparent")
    imgTextFrame.pack(expand=1, fill="both")
    # Brightness Frame
    brightFrame = CTkFrame(root, fg_color="transparent")
    brightFrame.pack(expand=1, fill="both")
    # Contrast Frame
    contrastFrame = CTkFrame(root, fg_color="transparent")
    contrastFrame.pack(expand=1, fill="both")
    # Blur Frame
    blurFrame = CTkFrame(root, fg_color="transparent")
    blurFrame.pack(expand=1, fill="both")
    # Document Scanner Frame
    scannerFrame = CTkFrame(root, fg_color="transparent")
    scannerFrame.pack(expand=1, fill="both")

    '''Header section Start : Including Each Section Button'''

    # setting all to frame into the list for on tab click function
    sectionframes = [imgCarFrame, imgTextFrame,
                     brightFrame, contrastFrame, blurFrame, scannerFrame]

    # Image to Cartoon Button
    imgCarBtn = CTkButton(root, text="Image-to-Cartoon", font=("Poppins", 14), border_color="#00BB6D", border_width=1,
                          fg_color=active_btn_color, corner_radius=32,
                          hover_color="null",
                          command=lambda: on_tab_click(sectionframes, sectionbuttons, imgCarFrame, imgCarBtn))
    imgCarBtn.place(x=350, y=45)

    # Image to Text Button
    imgTextBtn = CTkButton(root, text="Image-to-Text", font=("Poppins", 14), border_color="#00BB6D", border_width=1,
                           fg_color="transparent",
                           hover_color="null", corner_radius=32,
                           command=lambda: on_tab_click(sectionframes, sectionbuttons, imgTextFrame, imgTextBtn))
    imgTextBtn.place(x=500, y=45)

    # Brightness Button
    brightBtn = CTkButton(root, text="Brightness", font=("Poppins", 14), border_color="#00BB6D", border_width=1,
                          fg_color="transparent",
                          hover_color="null", corner_radius=32,
                          command=lambda: on_tab_click(sectionframes, sectionbuttons, brightFrame, brightBtn))
    brightBtn.place(x=650, y=45)

    # Contrast Button
    contrastBtn = CTkButton(root, text="Contrast", font=("Poppins", 14), border_color="#00BB6D", border_width=1,
                            fg_color="transparent",
                            hover_color="null", corner_radius=32,
                            command=lambda: on_tab_click(sectionframes, sectionbuttons, contrastFrame, contrastBtn))
    contrastBtn.place(x=800, y=45)

    # Blur Button
    blurBtn = CTkButton(root, text="Blur", font=("Poppins", 14), border_color="#00BB6D", border_width=1,
                        fg_color="transparent",
                        hover_color="null", corner_radius=32,
                        command=lambda: on_tab_click(sectionframes, sectionbuttons, blurFrame, blurBtn))
    blurBtn.place(x=950, y=45)

    # Link to Document Scanner App Button

    scannerBtn = CTkButton(root, text="Document Scanner", font=("Poppins", 14),
                           fg_color="transparent", image=linkicon, compound="left", height=35,
                           hover_color="null", corner_radius=32, border_color="#00BB6D", border_width=1,
                           command=lambda: on_tab_click(sectionframes, sectionbuttons, scannerFrame, scannerBtn))
    scannerBtn.place(x=1270, y=40)

    # setting all to tab buttons into the list for on tab click function
    sectionbuttons = [imgCarBtn, imgTextBtn,
                      brightBtn, contrastBtn, blurBtn, scannerBtn]

    # Setting image to cartoon frame as current frame
    on_tab_click(sectionframes, sectionbuttons, imgCarFrame, imgCarBtn)

    '''Header section End'''

    root.mainloop()

