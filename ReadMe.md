
# About

Final project for CS 361 - Software Engineering I 

The purpose of this program is to serve as a tool to handle 
image metadata. Available options include: viewing metadata,
deleting metadata, encrypting an image, or decrypting an image.

Demo video: https://media.oregonstate.edu/media/t/1_r7xcrqhv


# Getting Started


1. On the left hand-side of the main screen, click on the "Browse" 
   button to search for and select an image. 

2. Search for and select your desired image. Once selected, click "OK".

3. You will see your image appear on the right-hand side of the main screen.

4. Select an option located under the image. Options include: 
   "View Metadata", "Delete Metadata", "Encrypt Image", "Decrypt Image"


# FAQ's

## Viewing Images

* How do I choose an image?

On the left-hand side of the main screen, click on the "Browse" 
  button to search for and select an image file. You can also paste
  the path to the file in the text field.


* What kind of image formats are supported?

- This program can display JPEG, PNG, GIF, TIFF, and BMP files.
  However, it can only encrypt/decrypt JPEG and PNG files at this time.


* How do I choose another image?

- You can click on the "Browse" button to select another image file 
  and it will update on the main screen.



## Deleting Metadata

* What does the "Delete Metadata" button do?

- This button will open a window to allow you to remove the selected image's EXIF data.


* Will my image be ovewritten if I delete the metadata?

- Yes, the original image will be overwritten. 


* Can I retrieve the EXIF data once it has been deleted?

- No, once the data has been deleted, it cannot be recovered. It is highly recommended 
  to save a copy of your image prior to deleting the metadata for this reason.



## Encrypting Images

* What does the "Encrypt Image" button do?

- This button will encrypt the entire image using one-time pad style encryption.


* Will my image be ovewritten if I encrypt?

- Yes, the selected image will be ovewritten if you select "Overwrite original".
  You can choose "Save as new image" to save the encrypted image as a new file
  so that you can keep your original.

* How long does my password need to be? 

- Password must be between 8 and 30 characters.


* What does the "Generate Random Password" button do?

- This optional button generates a password for you. It will first
  ask for your desired password length. After clicking "OK", the
  generated password will appear in the text box.


* Why did I get an "Encryption Failed" message?

- This message appears when the encryption algorithm encountered an 
  error that prevents it from succesfully completing the action. If
  you receive this message, your image has not been encrypted and 
  you can try again if you wish.



## Decrypting Images

* What does the "Decrypt Image" button do?

- This button will decrypt an image using one-time pad style encryption. It will 
  need the password that was originally used to encrypt the image. Without the 
  correct password, the image cannot be correctly decrypted.

* Will my image be ovewritten if I decrypt?

- No. The decrypted image will save as a new file in the same directory that
  the encrypted image is located at.


* How do I know if my image was successfully decrypted?

- When the decryption action has completed, you can navigate to and open the new 
  file that has been created. If the file opens and you are able to see the 
  original image, then the decryption was successful. 


* Why is the decrypted image file not opening?

- If the decrypted file does not open, it means the image was decrypted with the
  incorrect password. Retry the process again with the correct password.
