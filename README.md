# BG3-Icon-Formatter
This app is designed to automate the formatting process for batch formatting of Action/Skill/Spell/Passive/Status icons for Baldur's Gate 3.

It is not optimized for Class, Subclass, or Race icons. 

How it works:

     -Creates 3 copies of the image(s) in the selected input folder

     -Resizes all images  to 144x144, 380x380, and 64x64 sizes 

     -Creates 3 folders in the selected output folder corresponding to the resolutions
      E.g.(Icons/64x64,Icons/144x144, Icons/380x380)
 
     -Places resized images into the created folders within the selected output folder.

Note:
      Applies a gradual bottom up fade to only the 380x380 images to match the fade effect on the vanilla tooltip icons.

The fade effect directly overwrites the resized 380x380 images in the 380x380 folder.
