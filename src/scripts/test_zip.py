from zipfile import ZipFile
from os.path import basename
import os
import time

# zip metrics files
# create a ZipFile object
with ZipFile('test_{}.zip'.format(str(time.time_ns())), 'w') as zipObj:
    # Iterate over all the files in directory
    for folderName, subfolders, filenames in os.walk("config"):
        for filename in filenames:
            #create complete filepath of file in directory
            filePath = os.path.join(folderName, filename)
            # Add file to zip
            zipObj.write(filePath, basename(filePath))