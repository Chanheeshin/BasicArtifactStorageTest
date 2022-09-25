import os

def removeFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
    else:
        print("The file does not exist")

def convertToBinaryData(fileName):
    # Convert digital data to binary format
    with open(fileName, 'rb') as file:
        blobData = file.read()
    return blobData

def writeTofile(data, fileName):
    # Convert binary data to proper format and write it on Hard Disk
    with open(fileName, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", fileName, "\n")

def isBinary(mimeType, subtype):
    if mimeType == "text":
        return False
    if mimeType != "application":
        return True
    return subtype not in ["json", "ld+json", "x-httpd-php", "x-sh", "x-csh", "xhtml+xml", "xml"]