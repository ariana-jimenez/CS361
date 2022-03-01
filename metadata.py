# This program allows the user to upload an image and select
# from four options: view, encrypt, decrypt, or delete metadata.
# Used https://pysimplegui.readthedocs.io/en/latest/#pysimplegui-users-manual
# as reference for implementing the GUI.

import PySimpleGUI as sg
from PIL import Image
import exif
import csv
import operator
import io
import os
import subprocess
import time
import re


# Index of exif module attribute tags 
tags = {
    "Lens Make": "lens_make",
    "Lens Model": "model",
    "Focal Length": "focal_length",
    "White Balance": "white_balance",
    "Orientation": "orientation",
    "Date Time": "datetime_original",
    "Brightness": "brightness_value",
    "Shutter Speed": "shutter_speed_value",
    "Aperture": "aperture_value",
    "Flash": "datetime_digitized",
    "GPS Latitude": "gps_latitude",
    "GPS Longitude": "gps_longitude",
    "GPS Timestamp": "gps_timestamp",
    "GPS Speed": "gps_speed",
    "GPS Altitude": "gps_altitude",
    "GPS Direction": "gps_img_direction",
    "Exposure Time": "exposure_time",
    "Exposure Program": "exposure_program",
    "OS Version": "software",
    "Color": "color_space",
    "F Number": "f_number",
}


def view_window(imgpath): 
    """
    This function opens the View Metadata window to display image 
    exif data. Referred to https://exif.readthedocs.io/en/latest/usage.html 
    for reference on using the exif module to access exif data in image.
    """
    
    # Open image file
    with open(imgpath, "rb") as img_file:
        current_image = exif.Image(img_file)

    # Check if image has EXIF data
    data = []
    if (current_image.has_exif):

        # Extract EXIF data from image
        for key, val in tags.items():
            x = current_image.get(val, 'Unknown')
            data.append([key, x])
       
    else:
        sg.popup('Image does not contain any EXIF data.')
        

    # Write EXIF data to CSV file
    with open("data.csv", "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)

    
    # Window layout
    layout = [
        [sg.Text("Image Name: " + os.path.basename(imgpath), pad=(5,15))],
        [sg.Table(values=data, headings=["TAG", "DATA"], auto_size_columns=True, justification='left', key="-TABLE-")],
        [sg.Button("Sort Alphabetical", pad=(25,25))],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("View Metadata", layout, grab_anywhere=False)

    while True:
        event, values = window.read()
        
        if event == "Sort Alphabetical":

            # Run the alphabetical sorting microservice as a separate process
            p = subprocess.Popen('py alphabetical_sorting.py', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            # Read microservice output 
            output = p.stdout.read()
            p.stdout.flush()
            p.terminate()

            # Remove all brackets and quotes from stringified list to convert back to list
            str = re.sub(r"[\['\]]", "", output)
            str = str.split(', ')

            # Create new nested list so that attributes and values are paired together
            sorted_data = []
            i = 0
            j = 1
            length = len(str)/2
            for elem in range(int(length)):
                sorted_data.append([str[i], str[j]])
                i = i + 2
                j = j + 2
 
            # Display list in table   
            window['-TABLE-'].update(values=sorted_data)
        

        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()


def encrypt_window(imgpath):
    """
    This function opens the Encrypt Metadata window to allow user
    to create a password and encrypt image EXIF data.
    """

    # Window layout
    layout = [
        [sg.Text("Image Name: " + os.path.basename(imgpath), pad=(5,15))],
        [sg.Text("Instructions: First create a password or get a random generated one.\n"
        "Please be aware this password will be required for decrypting.", pad=(5,15))],
        [sg.Text("1. Create a password:")],
        [sg.Input(size=(30, 1), key="-PASSWORD-", pad=(10,0)), sg.Button("Generate random password")],
        [sg.Text("2. Click 'Encrypt' button below to continue:", pad=(0,15))], 
        [sg.Button("Encrypt", pad=(10,0))],
        [sg.VPush()],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Encrypt Metadata", layout, size=(450,300))

    while True:
        event, values = window.read()

        # Make sure password.txt file is clear
        file = open('password.txt','w')
        file.close()

        if event == "Generate random password":

            # Compile and run microservice in separate process
            x = subprocess.run('g++ -std=c++11 password_generator.cpp -o password_generator.exe')
            p = subprocess.Popen('password_generator.exe', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            # Read microservice prompts into program dialog
            output = p.stdout.read(92)
            p.stdout.flush()
            password_length = sg.popup_get_text(output)
            p.stdin.write(password_length + '\n')
            p.stdin.flush()

            # Validate input if invalid size entered
            while (int(password_length) < 8 or int(password_length) > 30):
                password_length = sg.popup_get_text(p.stdout.read(103))
                p.stdout.flush()
                p.stdin.write(password_length + '\n')
                p.stdin.flush()

            # Terminate subprocess
            p.terminate()
            time.sleep(1)

            # Open text file, read generated password, fill in text box
            file = open('password.txt','r')
            random_password = file.readline()
            file.close()

            # Enter random password in text box
            window["-PASSWORD-"].update(value=random_password)

        if event == "Encrypt":
            
            # Open image file and access EXIF data
            with open(imgpath, "rb") as img_file:
                current_image = exif.Image(img_file)

            if (current_image.has_exif):
                
                # Encryption function will go here

                # Save changes
                with open(imgpath, 'wb') as updated_image:
                    updated_image.write(current_image.get_file())

                # Notify success message
                sg.popup('Encryption Successful!')

            else:
                sg.popup('Image does not contain any EXIF data.')

        if event == "Close" or event == sg.WIN_CLOSED:
            break    

    window.close()


def decrypt_window(image_name):
    """
    This function opens the Decrypt Metadata window to allow user
    to enter a password to decrypt image EXIF data.
    """

    # Window layout
    layout = [
        [sg.Text("Image Name: " + image_name, pad=(5,15))],
        [sg.Text("Enter the password to decrypt metadata for this image:")],
        [sg.Input(size=(25, 1), pad=(5,25)), sg.Button("Decrypt", pad=(10,0))],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Decrypt Metadata", layout)

    while True:
        event, values = window.read()
        
        if event == "Decrypt":

            # Decrypt function will go here

            sg.popup('Decryption Successful!')

        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()


def delete_window(image_name):
    """
    This function opens the Delete Metadata window to allow user
    to delete image EXIF data.
    """

    # Window layout
    layout = [
        [sg.Text("Image Name: " + image_name, pad=(5,15))],
        [sg.Text("*** Warning ***")],
        [sg.Text("This action will remove all metadata for this image and cannot be undone.")],
        [sg.Text("Click 'YES' to confirm or 'NO' to return to the main menu.")],
        [sg.Column([[sg.Button("Yes", pad=(10,25)), sg.Button("No", pad=(10,25))]], element_justification='center', expand_x=True)],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Delete Metadata", layout)

    while True:
        event, values = window.read()

        if event == "No":
            break
        
        if event == "Yes":

            # Function to delete EXIF data will go here

            sg.popup('All metadata deleted.')

        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()


def help_window():
    """
    This function displays the help documentation
    """

    # Read text file containing user guide
    file = open('guide.txt','r')
    guide = file.read()
    file.close()

    # Window layout
    layout = [
        [sg.Text(guide)],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("User Guide", layout)

    while True:
        event, values = window.read()

        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()


# Main screen layout
column1 = [
    [sg.Text("Upload an image:")],
    [
        sg.Input(size=(25, 1), enable_events=True, key="-FILE-", tooltip="You can enter the file path here"),
        sg.FileBrowse(tooltip="Click here to browse and select an image"),
    ],
]

column2 = [
    [sg.Image(key="-IMAGE-")], 
    [sg.pin(sg.Button("View Metadata", key="-VIEW-", tooltip="View EXIF data for this image", visible=False)), 
    sg.pin(sg.Button("Encrypt Metadata", key="-ENCRYPT-", tooltip="Encrypt the EXIF data for this image", visible=False)), 
    sg.pin(sg.Button("Decrypt Metadata", key="-DECRYPT-", tooltip="Decrypt the EXIF data for this image", visible=False)),
    sg.pin(sg.Button("Delete Metadata", key="-DELETE-", tooltip="Delete the EXIF data for this image", visible=False))],
]

layout = [
    [
        [sg.Button(" ? ", key="-HELP-", tooltip="Need help? Click here!")],
        sg.VPush(),
        sg.Column(column1),
        sg.VSeperator(),
        sg.Column(column2, element_justification='c'),
    ]
]

window = sg.Window("Image Metadata Manager", layout, size=(800,600))

while True:
    event, values = window.read()

    # Browse for file    
    if event == "-FILE-":

        filename = values["-FILE-"]

        # Adapted code from the following website to convert and display jpg images in GUI:
        # https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-convert_to_bytes-function-pil-image-viewer
        if os.path.exists(filename):    
            img = Image.open(values["-FILE-"])
            img.thumbnail((400, 400))
            pic = io.BytesIO()
            img.save(pic, format="PNG")
            window["-IMAGE-"].update(data=pic.getvalue())
            window["-VIEW-"].update(visible=True)
            window["-ENCRYPT-"].update(visible=True)
            window["-DECRYPT-"].update(visible=True)
            window["-DELETE-"].update(visible=True)

    image_path = values["-FILE-"]
    image_name = os.path.basename(image_path)

    if event == "-VIEW-":
        view_window(image_path)
    
    if event == "-ENCRYPT-":
        encrypt_window(image_path)

    if event == "-DECRYPT-":
        decrypt_window(image_name)
    
    if event == "-DELETE-":
        delete_window(image_name)

    if event == "-HELP-":
        help_window()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
