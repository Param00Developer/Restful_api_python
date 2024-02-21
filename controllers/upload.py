import os
from flask_restful import abort
import shutil


UPLOAD_FOLDER='./uploadedfiles'
ALLOWED_EXTENSIONS=set(["pptx","docs","xlsl"])
def isallowed(f_name):
    return f_name.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS
def uploadfile(file,id):
    if isallowed(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER,f"{id}"+file.filename))
        return "File uploded successfully..(./uploadedfiles)"
    else:
        return ("File should be (pptx,docs,xlsl)")
def list_():
    entries = os.listdir(UPLOAD_FOLDER)
    if entries:
        all_files=""
        for i in entries:
            all_files+=i+"\n"
        return all_files
    else:
        return "Empty : No files to display.."
def move(filename):
    # copy the contents of the demo.py file to  a new file called demo1.py
    source="./uploadedfiles/"+filename
    dest=os.path.join(os.path.expanduser('~'), 'downloads')+f"/{filename}"
    shutil.copyfile(source, dest)


