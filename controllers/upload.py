import os
from flask_restful import abort
import shutil

UPLOAD_FOLDER='./uploadedfiles'

# Set contains allowed file extensions to be stored
ALLOWED_EXTENSIONS=set(["pptx","docx","xlsl"])

# Check whether file format is supported for storage
def isallowed(f_name):
    return f_name.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

# Method to store files in /uploadedfiles folder
def uploadfile(file,id):
    if isallowed(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER,f"{id}"+file.filename))
        return "File uploded successfully..(./uploadedfiles)"
    else:
        return ("File should be (pptx,docs,xlsl)")

# lists all the files available for download
def list_():
    entries = os.listdir(UPLOAD_FOLDER)
    if entries:
        all_files=""
        for i in entries:
            all_files+=i+"\n"
        return all_files
    else:
        return "Empty : No files to display.."

# method to download the files available in /uploadedfiles folder in system /download   
def move(filename):
    source="./uploadedfiles/"+filename
    dest=os.path.join(os.path.expanduser('~'), 'downloads')+f"/{filename}" #get location of your system download folder
    shutil.copyfile(source, dest)


