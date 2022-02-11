# This program allows the user to upload an image and select
# from four options: view, encrypt, decrypt, or delete metadata.

import PySimpleGUI as sg
from PIL import Image
import csv
import operator
import io
import os


# View Metadata Window
def window1(img): 
    
    # Read csv file and fill table with data
    data = []

    with open("test.csv", "r") as infile:
        reader = csv.reader(infile)
        data = list(reader) 
            
    
    # Table layout

    close = [[sg.Button("Close")]]

    layout = [
        [sg.Text("Image Name: " + img, pad=(5,15))],
        [sg.Table(values=data, headings=["TAG", "DATA"], auto_size_columns=True, justification='left', key="-TABLE-")],
        [sg.Button("Sort Alphabetical", pad=(25,25))],
        [sg.Column(close, element_justification='center', expand_x=True)],
    ]

    window = sg.Window("View Metadata", layout, grab_anywhere=False)

    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break
        
        if event == "Sort Alphabetical":

            # read csv file & sort data based on "TAG" column
            data = csv.reader(open('test.csv'), delimiter=',')
            data = sorted(data, key=operator.itemgetter(0))

            # Display updated sorted list    
            window['-TABLE-'].update(values=data)
         
    window.close()

# Encrypt Metadata Window
def window2(img):

    close = [[sg.Button("Close")]]

    layout = [
        [sg.Text("Image Name: " + img, pad=(5,15))],
        [sg.Text("Instructions: First create a password or get a random generated one.\n"
        "Please be aware this password will be required for decrypting.", pad=(5,15))],
        [sg.Text("1. Create a password:")],
        [sg.Input(size=(25, 1), key="-PASSWORD-", pad=(15,0)), sg.Button("Generate random password")],
        [sg.Text("2. Click 'Encrypt' button below to continue:", pad=(0,15))], 
        [sg.Button("Encrypt", pad=(10,0))],
        [sg.VPush()],
        [sg.Column(close, element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Encrypt Metadata", layout, size=(400,300))
    input = window['-PASSWORD-']

    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break
        
        # Auto fill password if random generated password option selected
        if event == "Generate random password":

            # Open text file, read generated password, fill in text box
            file = open('password.txt','r')
            random_password = file.read()
            file.close()

            input = input.update(value=random_password)
        
        if event == "Encrypt":
            sg.popup('Encryption Successful!')

    window.close()

# Decrypt Metadata Window
def window3(img):

    close = [[sg.Button("Close")]]

    layout = [
        [sg.Text("Image Name: " + img, pad=(5,15))],
        [sg.Text("Enter the password to decrypt metadata for this image:")],
        [sg.Input(size=(25, 1), pad=(5,25)), sg.Button("Decrypt", pad=(10,0))],
        [sg.Column(close, element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Decrypt Metadata", layout)

    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break
        
        if event == "Decrypt":
            sg.popup('Decryption Successful!')

    window.close()


# Delete Metadata Window
def window4(img):

    close = [[sg.Button("Close")]]
    choice = [[sg.Button("Yes", pad=(10,25)), sg.Button("No", pad=(10,25))]]

    layout = [
        [sg.Text("Image Name: " + img, pad=(5,15))],
        [sg.Text("*** Warning ***")],
        [sg.Text("This action will remove all metadata for this image and cannot be undone.")],
        [sg.Text("Click 'YES' to confirm or 'NO' to return to the main menu.")],
        [sg.Column(choice, element_justification='center', expand_x=True)],
        [sg.Column(close, element_justification='center', expand_x=True)],
    ]

    window = sg.Window("Delete Metadata", layout)

    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break

        if event == "No":
            break
        
        if event == "Yes":
            sg.popup('All metadata deleted.')

    window.close()

def help_window():

    # Read text file containing user guide
    file = open('guide.txt','r')
    guide = file.read()
    file.close()

    close = [[sg.Button("Close")]]

    layout = [
        [sg.Text(guide)],
        [sg.Column(close, element_justification='center', expand_x=True)],
    ]

    window = sg.Window("User Guide", layout)

    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()


# Main screen columns layout
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
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
        
    if event == "-FILE-":

        filename = values["-FILE-"]

        if os.path.exists(filename):
            
            image = Image.open(values["-FILE-"])
            image.thumbnail((400, 400))
            pic = io.BytesIO()
            image.save(pic, format="PNG")
            window["-IMAGE-"].update(data=pic.getvalue())
            window["-VIEW-"].update(visible=True)
            window["-ENCRYPT-"].update(visible=True)
            window["-DECRYPT-"].update(visible=True)
            window["-DELETE-"].update(visible=True)

    imageName = values["-FILE-"]
    imageName = os.path.basename(imageName)

    if event == "-VIEW-":
        window1(imageName)
    
    if event == "-ENCRYPT-":
        window2(imageName)

    if event == "-DECRYPT-":
        window3(imageName)
    
    if event == "-DELETE-":
        window4(imageName)

    if event == "-HELP-":
        help_window()
        

window.close()
