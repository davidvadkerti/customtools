# -*- coding: UTF-8 -*-

__title__ = 'Import Report'
__doc__ = 'Open interactive HTML file saved from pyRevit script output. Makes element links active.'
__helpurl__ = 'https://youtu.be/0lXwqbIrDiY'
__context__ = 'zero-doc'

from pyrevit import forms
from pyrevit import script, coreutils
import os
from shutil import copyfile
from customOutput import ct_icon
# from os import path

# copy file to correct location for all users of the extension
def copyFile(fileName,pathTo,folderPath):
    # path for common user
    try:
        copyFromPath = homepath + "\AppData\Roaming\pyRevit\Extensions\CustomTools.extension" + pathTo
        copyfile(copyFromPath, folderPath+fileName)
    # path for developer using git clone
    except:
        copyFromPath = homepath + "\OneDrive\Dokumenty\gitrepos\pyRevit Extension\CustomTools.extension" + pathTo
        copyfile(copyFromPath, folderPath+fileName)

# pick source html file to edit
filePath = forms.pick_file(file_ext='html', title='Select HTML report')

if filePath:
    # fixing CSS path in HTML - copying CSS file into path subfolder
    # make folder if it already does not exist
    lastBackslash = filePath.rindex("\\")
    folderPath = filePath[:lastBackslash]+"\\lib\\"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
       
    # make copy of Chart.js and css file
    # getting %HOMEPATH%
    from os.path import expanduser
    homepath = expanduser("~")

    # copy Chart.js file
    copyFile("Chart.min.js.download","\support\outputWindow\Chart.min.js.download",folderPath)

    # copy css file
    copyFile("outputstylesCustom.css","\outputstylesCustom.css",folderPath)


    f = open(filePath, "r+")
    content = f.read()
    # print(content)

    # read the file and find css path
    try:
        start = content.index('<link href="file:///')
        end = content.index('outputstylesCustom.css"')
        changed_content = content[:start]+'<link href="lib/'+content[end:]

        # write changed relative path to css file
        f = open(filePath, "w")
        f.write(changed_content)
        f.close()
    except:
        pass


    # view the HTML file
    output = script.get_output()
    output.set_height(700)
    # changing icon
    ct_icon(output)
    # output.open_url(filePath)
    output.open_page(filePath)