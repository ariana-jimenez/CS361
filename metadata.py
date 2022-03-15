# This program allows the user to select an image and select from four options:
# view metadata, delete metadata, encrypt an image, or decrypt an image.
# Used https://pysimplegui.readthedocs.io/en/latest/#pysimplegui-users-manual
# as reference for implementing the GUI.

import PySimpleGUI as sg
from PIL import Image
import base64
import csv
import exif
import io
import math
import os
import re
import subprocess
import time

# Index that is used for converting a character to a number
convert_to_nums = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8,
    'I': 9,
    'J': 10,
    'K': 11,
    'L': 12,
    'M': 13,
    'N': 14,
    'O': 15,
    'P': 16,
    'Q': 17,
    'R': 18,
    'S': 19,
    'T': 20,
    'U': 21,
    'V': 22,
    'W': 23,
    'X': 24,
    'Y': 25,
    'Z': 26,
    'a': 27,
    'b': 28,
    'c': 29,
    'd': 30,
    'e': 31,
    'f': 32,
    'g': 33,
    'h': 34,
    'i': 35,
    'j': 36,
    'k': 37,
    'l': 38,
    'm': 39,
    'n': 40,
    'o': 41,
    'p': 42,
    'q': 43,
    'r': 44,
    's': 45,
    't': 46,
    'u': 47,
    'v': 48,
    'w': 49,
    'x': 50,
    'y': 51,
    'z': 52,
    '0': 53,
    '1': 54,
    '2': 55,
    '3': 56,
    '4': 57,
    '5': 58,
    '6': 59,
    '7': 60,
    '8': 61,
    '9': 62,
    '+': 63,
    '/': 64,
    '=': 65,
    '!': 66,
    '@': 67,
    '#': 68,
    '$': 69,
    '%': 70,
    '^': 71,
    '&': 72,
    '*': 73,
    '(': 74,
    ')': 75,
    '_': 76,
    '-': 77,
    ' ': 78,
    '?': 79,
    '.': 80,
    ',': 81,
    ':': 82,
}

# Index that is used for converting a number to a character
convert_to_chars = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
    6: 'F',
    7: 'G',
    8: 'H',
    9: 'I',
    10: 'J',
    11: 'K',
    12: 'L',
    13: 'M',
    14: 'N',
    15: 'O',
    16: 'P',
    17: 'Q',
    18: 'R',
    19: 'S',
    20: 'T',
    21: 'U',
    22: 'V',
    23: 'W',
    24: 'X',
    25: 'Y',
    26: 'Z',
    27: 'a',
    28: 'b',
    29: 'c',
    30: 'd',
    31: 'e',
    32: 'f',
    33: 'g',
    34: 'h',
    35: 'i',
    36: 'j',
    37: 'k',
    38: 'l',
    39: 'm',
    40: 'n',
    41: 'o',
    42: 'p',
    43: 'q',
    44: 'r',
    45: 's',
    46: 't',
    47: 'u',
    48: 'v',
    49: 'w',
    50: 'x',
    51: 'y',
    52: 'z',
    53: '0',
    54: '1',
    55: '2',
    56: '3',
    57: '4',
    58: '5',
    59: '6',
    60: '7',
    61: '8',
    62: '9',
    63: '+',
    64: '/',
}

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
    "GPS Latitude": "gps_latitude",
    "GPS Latitude Direction": "gps_latitude_ref",
    "GPS Longitude": "gps_longitude",
    "GPS Longitude Direction": "gps_longitude_ref",
    "GPS Timestamp": "gps_timestamp",
    "GPS Speed": "gps_speed",
    "GPS Altitude": "gps_altitude",
    "Exposure Time": "exposure_time",
    "Exposure Program": "exposure_program",
    "OS Version": "software",
    "Color": "color_space",
    "F Number": "f_number",
    "X Resolution":"pixel_x_dimension",
    "Y Resolution": "pixel_y_dimension",
}

def encrypt(plaintext, key):
    """
    This function takes in two parameters: a plaintext  
    string and a key. The plaintext is encrypted using 
    one-time pad style encryption. 
    """

    # Convert plaintext and key from string to list
    list1 = list(plaintext)
    list2 = list(key)

    # Convert each character in plaintext to a number
    for count, i in enumerate(plaintext):
        list1[count] = convert_to_nums.get(i)

    # Convert each character in key to a number
    for count, i in enumerate(key):
        list2[count] = convert_to_nums.get(i)

    # Add plaintext and key and store result in temp list 
    temp = []
    
    for j in range(len(plaintext)):
        sum = list1[j] + list2[j]
        if (sum > 64):
            sum = sum % 64
            if (sum <= 0):
                sum = sum + 64
        temp.append(sum)

    # Convert numbers back to characters
    for count, i in enumerate(temp):
        temp[count] = convert_to_chars.get(i)

    # Change last character in string to a "=" for padding
    temp[len(temp) - 1] = '='

    # Convert list to string and return
    encrypted_data = ''.join([elem for elem in temp])
    return encrypted_data


def decrypt(encrypted_word, key):
    """
    This function takes in two parameters: an encrypted string 
    and a key. The string is decrypted with the key using  
    one-time pad style encryption. 
    """

    # Convert encrypted word and key from string to list
    list1 = list(encrypted_word)
    list2 = list(key)

    # Convert each character in encrypted word to a number
    for count, i in enumerate(encrypted_word):
        list1[count] = convert_to_nums.get(i)

    # Convert each character in key to a number
    for count, i in enumerate(key):
        list2[count] = convert_to_nums.get(i)

    # Subtract key from encrypted_word and store result in temp list
    temp = []
    for j in range(len(encrypted_word)):
        sub = list1[j] - list2[j]
        while (sub <= 0):
            sub = sub + 64   
        temp.append(sub)

    # Convert numbers back to characters
    for count, i in enumerate(temp):
        temp[count] = convert_to_chars.get(i)

    # Change last character in string to a "=" for padding
    temp[len(temp) - 1] = '='

    # Convert list to string and return
    decrypted_data = ''.join([elem for elem in temp])
    return decrypted_data


def save_new_image(imgpath, str, type):
    """
    This function saves a new image file.
    """

    # Create new image name to save in same directory as encrypted image
    extension = os.path.splitext(os.path.basename(imgpath))
    directory = os.path.dirname(imgpath)
    new_name = type + extension[1]
    new_path = directory + "/" + new_name

    # Write string to new image
    with open(new_path, 'wb') as updated_image:
        updated_image.write(base64.b64decode((str)))
        updated_image.close()

def adjust_password(str, key):
    """
    This function adjusts password length to match image string length
    """
    
    difference = len(str)/len(key)
    difference = math.floor(difference)
    key = key * difference
    padding = len(str) - len(key)
    key += ("=" * padding)
    return key

def password_generator_microservice():
    """
    This function runs the password generator microservice.
    """
    # Compile and run microservice in separate process
    subprocess.run('g++ -std=c++11 password_generator.cpp -o password_generator.exe')
    process = subprocess.Popen('password_generator.exe', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
    # Read microservice prompts into program dialog
    output = process.stdout.read(92)
    process.stdout.flush()
    password_length = sg.popup_get_text(output)
    process.stdin.write(password_length + '\n')
    process.stdin.flush()

    # Validate input if invalid size entered
    while (int(password_length) < 8 or int(password_length) > 30):
        password_length = sg.popup_get_text(process.stdout.read(103))
        process.stdout.flush()
        process.stdin.write(password_length + '\n')
        process.stdin.flush()

    # Terminate subprocess
    process.terminate()
    time.sleep(1)


def sort_alphabetical_microservice():
    """
    This function runs the alphabetical sorting microservice.
    """
    # Run the alphabetical sorting microservice as a separate process
    process = subprocess.Popen('py alphabetical_sorting.py', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Read microservice output 
    output = process.stdout.read()
    process.stdout.flush()
    process.terminate()

    # Remove all brackets and quotes from stringified list to convert back to list
    str = re.sub(r"[\['\]]", "", output)
    str = str.split(', ')

    # Create new nested list so that attributes and values are paired together
    sorted_data = []
    tag = 0
    val = 1
    length = len(str)/2

    for elem in range(int(length)):
        sorted_data.append([str[tag], str[val]])
        tag = tag + 2
        val = val + 2

    return sorted_data


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
            info = current_image.get(val, 'No Data')
            data.append([key, info])
       
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

                sorted_data = sort_alphabetical_microservice()  
                window['-TABLE-'].update(values=sorted_data)
        
            if event == "Close" or event == sg.WIN_CLOSED:
                break
        
        window.close()

    else:
        sg.popup('Image does not contain any EXIF data.')
        
  
def encrypt_window(imgpath):
    """
    This function opens the Encrypt window to allow user
    to create a password and encrypt the whole image.
    """
    
    # Window layout
    layout = [
        [sg.Text("Image Name: " + os.path.basename(imgpath), pad=(5,15))],
        [sg.Text("*** Warning ***", text_color='yellow', font='bold')],
        [sg.Text(" Once encrypted, image can only be decrypted with this password.", text_color='yellow')],
        [sg.Text(" Store password somewhere safe.\n", text_color='yellow')],
        [sg.Text("1. Create a password:")],
        [sg.Input(size=(30, 1), key="-PASSWORD-", pad=(10,10)), sg.Text(" OR "), sg.Button("Generate random password")],
        [sg.Text(" 2. Choose how to save encrypted image:", pad=(0,15))],
        [sg.Radio("Overwrite original image", "RAD", default=False, key="-ORIGINAL-")],
        [sg.Radio("Save as new image", "RAD", default=False, key="-NEW-", pad=(5,10))],
        [sg.Text(" 3. Click 'Encrypt' button below to continue:", pad=(0,15))], 
        [sg.Button("Encrypt", pad=(20,0))],
        [sg.VPush()],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Encrypt Metadata", layout, size=(475,500))

    try:
        # Open image file
        with open(imgpath, "rb") as img_file:
            current_image = exif.Image(img_file)
    except:
        sg.popup("Unable to read image.")
        window.close()

    while True:
        event, values = window.read()

        # Make sure password.txt file is clear
        file = open('password.txt','w')
        file.close()

        if event == "Generate random password":

            password_generator_microservice()

            # Open text file, read generated password, fill in text box
            file = open('password.txt','r')
            random_password = file.readline()
            file.close()
            window["-PASSWORD-"].update(value=random_password)

        if event == "Encrypt":

            # Get values entered by user
            key = values["-PASSWORD-"]
            radio1 = values["-ORIGINAL-"]
            radio2 = values["-NEW-"]

            if (len(key) < 8 or len(key) > 30):
                sg.popup("Error: Password must be between 8 and 30 characters long. Try again.")
                break

            if (len(key) == 0):
                sg.popup("Error: No password entered. Please try again.")
                break
            
            if (radio1 == False and radio2 == False):
                sg.popup("Error: No selection made in Step 2. Please try again.")
                break

            try:
                # Convert image to string
                with open(imgpath, "rb") as imgfile:
                    str = base64.b64encode(imgfile.read())
                    str = str.decode('utf-8')
                        
                # Encrypt the string
                key = adjust_password(str, key)
                str = encrypt(str, key)

                if (radio1 == True):
                    # Write encrypted string to original image
                    file = open(imgpath, 'wb')
                    file.write(base64.b64decode((str)))
                    file.close()

                elif (radio2 == True):
                    save_new_image(imgpath, str, "encrypted")
  
                # Display completion message
                sg.popup('Encryption completed.')
                break
            
            except:
                sg.popup('Encryption failed.')
            
        if event == "Close" or event == sg.WIN_CLOSED:
            break    

    window.close()


def decrypt_window(imgpath):
    """
    This function opens the Decrypt window to allow user
    to enter a password to decrypt the image. Decrypted 
    image is saved as a new file.
    """

    # Window layout
    layout = [
        [sg.Text("Image Name: " + os.path.basename(imgpath), pad=(5,15))],
        [sg.Text("Enter the password to decrypt this image:")],
        [sg.Input(size=(25, 1), key="-KEY-", pad=(5,25)), sg.Button("Decrypt", pad=(10,0))],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Decrypt Metadata", layout)

    
    # Close window if image opens correctly since it is not encrypted.
    try:
        with open(imgpath, "rb") as img_file:
            current_image = exif.Image(img_file)
            
        sg.popup("This image is not encrypted. Unable to decrypt.")
        window.close()
    
    except:
        pass  
    
    while True:
        event, values = window.read()
        
        if event == "Decrypt":

            # Get password from text box
            key = values["-KEY-"]

            if (len(key) == 0):
                sg.popup("Error: No password entered. Please try again.")
                break

            try:
                # Convert image to string
                with open(imgpath, "rb") as imgfile:
                    str = base64.b64encode(imgfile.read())
                    str = str.decode('utf-8')
                    
                # Decrypt the string
                key = adjust_password(str, key)
                str = decrypt(str, key)
                
                # Save image
                save_new_image(imgpath, str, "decrypted")

                # Display completion message
                sg.popup('Decryption completed. Check file to verify.')
                break
            
            except:
                sg.popup("Decryption failed.")
                break
                
        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()


def delete_window(imgpath):
    """
    This function opens the Delete Metadata window to allow user
    to delete image EXIF data.
    """

    # Window layout
    layout = [
        [sg.Text("Image Name: " + os.path.basename(imgpath), pad=(5,15))],
        [sg.Text("*** Warning ***", text_color='yellow', font='bold')],
        [sg.Text("This action will remove all metadata for this image and cannot be undone.", text_color='yellow')],
        [sg.Text("Click 'YES' to confirm or 'NO' to return to the main menu.")],
        [sg.Column([[sg.Button("Yes", pad=(10,25)), sg.Button("No", pad=(10,25))]], element_justification='center', expand_x=True)],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Delete Metadata", layout)

    try:
        # Open image file
        with open(imgpath, "rb") as img_file:
            current_image = exif.Image(img_file)
        
        if (current_image.has_exif):

            while True:
                event, values = window.read()

                if event == "No":
                    break
                
                if event == "Yes":

                    # Delete EXIF tag data
                    for key, val in tags.items():
                        try:
                            current_image.delete(val)
                        except:
                            continue

                    # Save changes
                    with open(imgpath, 'wb') as updated_image:
                        updated_image.write(current_image.get_file())
                    
                    sg.popup('All metadata deleted.')
                    break

                if event == "Close" or event == sg.WIN_CLOSED:
                    break
        else:
            sg.popup('Image does not contain any EXIF data to delete.')
    
    except:
        sg.popup("Unable to read image.")
        window.close()

    window.close()


def help_window():
    """
    This function displays a user guide
    """

    # Read text file containing user guide
    file = open('readme.txt','r')
    guide = file.read()
    file.close()

    # Window layout
    layout = [
        [sg.Column([[sg.Text(guide)]], scrollable=True, vertical_scroll_only=True)],
        [sg.Column([[sg.Button("Close")]], element_justification='center', expand_x=True)],
    ]

    window = sg.Window("User Guide", layout, size=(550,400))

    while True:
        event, values = window.read()

        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()


# Main screen layout

column1 = [
    [sg.Text("Select an image:")],
    [
        sg.Input(size=(25, 1), enable_events=True, key="-FILE-", tooltip="You can enter the file path here"),
        sg.FileBrowse(tooltip="Click here to browse and select an image"),
    ],
]

column2 = [
    [sg.Image(key="-IMAGE-")],
    [sg.Text("Error: Unable to display image", visible=False, key="-ERRORMSG-")], 
    [sg.pin(sg.Button("View Metadata", key="-VIEW-", tooltip="View EXIF data for this image", visible=False)),
    sg.pin(sg.Button("Delete Metadata", key="-DELETE-", tooltip="Delete the EXIF data for this image", visible=False)), 
    sg.pin(sg.Button("Encrypt Image", key="-ENCRYPT-", tooltip="Encrypt the EXIF data for this image", visible=False)), 
    sg.pin(sg.Button("Decrypt Image", key="-DECRYPT-", tooltip="Decrypt the EXIF data for this image", visible=False))],
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

# Display selected image and options to user
while True:
    event, values = window.read()

    # Used the following website examples as reference to convert and display jpg images in GUI:
    # https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-convert_to_bytes-function-pil-image-viewer    
    if event == "-FILE-":

        filename = values["-FILE-"]
        if os.path.exists(filename):

            try:
                img = Image.open(values["-FILE-"])
                img.thumbnail((400, 400))
                pic = io.BytesIO()
                img.save(pic, format="PNG")
                window["-IMAGE-"].update(pic.getvalue())
                window["-IMAGE-"].update(visible=True)
                window["-ERRORMSG-"].update(visible=False)
                window["-VIEW-"].update(visible=True)
                window["-ENCRYPT-"].update(visible=True)
                window["-DECRYPT-"].update(visible=True)
                window["-DELETE-"].update(visible=True)
                img.close()

            except:
                window["-IMAGE-"].update(visible=False)
                window["-ERRORMSG-"].update(visible=True)
                window["-VIEW-"].update(visible=True)
                window["-ENCRYPT-"].update(visible=True)
                window["-DECRYPT-"].update(visible=True)
                window["-DELETE-"].update(visible=True)
     
    image_path = values["-FILE-"]

    if event == "-VIEW-":
        try:
            view_window(image_path)
        except:
            sg.popup("Unable to read image.")

    if event == "-ENCRYPT-":
        encrypt_window(image_path)
        
    if event == "-DECRYPT-":
        decrypt_window(image_path)
    
    if event == "-DELETE-":
        delete_window(image_path)
        
    if event == "-HELP-":
        help_window()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
