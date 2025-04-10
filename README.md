# BG3-Icon-Formatter
This app is designed to automate the process for batch formatting of Action/Skill/Spell/Passive/Status icons for Baldur's Gate 3.

It is not optimized for Class, Subclass, or Race icons. 

How it works:
     -Creates 3 copies of the image(s) in the selected input folder

     -Resizes all images  to 144x144, 380x380, and 64x64 sizes 

     -Creates 3 folders in the selected output folder corresponding to the resolutions
      E.g.(Icons/64x64,Icons/144x144, Icons/380x380)
 
     -Places resized images into the created folders within the selected output folder.

     -Applies a gradual bottom up fade to only the 380x380 images to mimic the fade effect on the vanilla tooltip icons.
      Note: The fade effect directly overwrites the resized 380x380 images in the 380x380 folder.

     -Opens output folder when process has finished.

 File Prefix: inserts the input text string before each ouput image file name. Random button will generate a random character string followed by underscore. 
      Example Input File name: Spell_Spellname
      Example Output File name: ABC_Spell_Spellname
Using a prefix is best practice to avoid conflict with other mods. I prefer to use one consistent prefix for all files in a mod.


Installation:
# For Non-Devs
1. Download the latest release
2. Run `BG3_icon_formatter.exe`

# For Developers
```bash
# Install dependencies
pip install -r requirements.txt

# run directly from source
python src/main.py

# build EXE (requires PyInstaller)
./build/build.sh