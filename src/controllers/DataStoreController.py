from src.utils.DBOUtil import *
from src.utils.FileOperationsUtil import *
from src.constants.constants import *
from pathlib import Path

import json
from flask import Flask, request

#Create flask application
app = Flask(__name__)

'''

'''
@app.route('/<path:path>', methods=['POST'])
def createResource(path):

    # Working directory variable
    workingDirectory = Path(__file__).parents[2]

    # HEADERS
    mimeType = request.headers['Content-Type']
    contentLength = request.headers['Content-Length']
    requestBody = request.get_data()
    filePath = request.path[1:]

    # Local file name
    fileName = filePath.split('/')[-1]
    fileName += guess_extension(mimeType)
    fileName = str(workingDirectory) + RELATIVE_STAGING_PATH + fileName

    # Local Database path
    connectionPath = str(workingDirectory) + RELATIVE_DATABASE_PATH + DATABASE_NAME

    # Create local file
    writeTofile(requestBody, fileName)

    # Call DBO insert
    insertFile(connectionPath, filePath, mimeType, fileName)

    # Remove local file
    removeFile(fileName)

    return json.dumps("Resource path is " + path)

'''
GET Route mapped to retrieving resources.

Use path argument to retrieve this specific resource

'''
@app.route('/<path:path>', methods=['GET'])
def retrieveResource(path):
    # Working directory variable
    workingDirectory = Path(__file__).parents[2]

    # HEADERS
    filePath = request.path[1:]

    # Local Database path
    connectionPath = str(workingDirectory) + RELATIVE_DATABASE_PATH + DATABASE_NAME

    # Retrieve from DBO and create outbound file
    temp = retrieveFile(connectionPath, filePath, str(workingDirectory))

    return json.dumps("Resource path is " + path)


if __name__ == '__main__':
    workingDirectory = Path(__file__).parents[2]
    connectionPath = str(workingDirectory) + RELATIVE_DATABASE_PATH + DATABASE_NAME

    sqliteConnect(connectionPath)
    createTables(connectionPath)

    app.run()