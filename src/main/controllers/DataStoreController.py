from src.main.utils.DBOUtil import *
from src.main.constants.constants import *
from src.main.models.responseModel import responseModel
from pathlib import Path

from flask import Flask, request, Response

#Create flask application
app = Flask(__name__)
conn = None

@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def routeHandler(path):
    if request.method == 'GET':
        return retrieveResource(path)
    elif request.method == 'POST':
        return createResource(path)
    elif request.method == 'DELETE':
        return deleteResource(path)
    else:
        return Response(request.environ.get('SERVER_PROTOCOL') + " 405 " + "Method Not Allowed", status=405)

'''
    Function to create a resource
'''
def createResource(path):
    try:
        # Working directory variable
        workingDirectory = Path(__file__).parents[3]

        # HEADERS
        mimeType = request.headers['Content-Type']
        contentLength = request.headers['Content-Length']
        requestBody = request.get_data()
        filePath = request.path[1:]

        # Local file name
        fileName = filePath.split('/')[-1]
        fileName += guess_extension(mimeType)
        fileName = str(workingDirectory) + RELATIVE_STAGING_PATH + fileName

        # Create local file
        writeTofile(requestBody, fileName)

        # Call DBO insert
        insertFile(conn, filePath, mimeType, fileName)

        # Remove local file
        removeFile(fileName)
    except:
        return Response(request.environ.get('SERVER_PROTOCOL') + " 403 " + "Failed to create resource", status=403)
    else:
        return Response(request.environ.get('SERVER_PROTOCOL') + " 200 " + "OK", status=200)

'''
    Function to retrieve a resource
'''
def retrieveResource(path):
    try:
        # Working directory variable
        workingDirectory = Path(__file__).parents[3]

        # HEADERS
        filePath = request.path[1:]

        # Retrieve from DBO and create outbound file
        temp = retrieveFile(conn, filePath, str(workingDirectory))
    except:
        return Response(request.environ.get('SERVER_PROTOCOL') + " 404 " + "Resource does not exist", status=404)
    else:
        response = Response(temp[1], mimetype=temp[0], status=200)

        responseString = responseModel(request.environ.get('SERVER_PROTOCOL'), response.status, response.headers, response.data)

        return str(responseString)

'''
    Function to delete a resource
'''
def deleteResource(path):
    try:
        # Working directory variable
        workingDirectory = Path(__file__).parents[3]

        # HEADERS
        filePath = request.path[1:]

        # Retrieve from DBO and create outbound file
        deleteFile(conn, filePath, str(workingDirectory))
    except:
        return Response(request.environ.get('SERVER_PROTOCOL') + " 404 " + "Failed to delete resource", status=403)
    else:
        return Response(request.environ.get('SERVER_PROTOCOL') + " 200 " + "OK", status=200)

if __name__ == '__main__':
    workingDirectory = Path(__file__).parents[3]
    connectionPath = str(workingDirectory) + RELATIVE_DATABASE_PATH + DATABASE_NAME

    try:
        conn = sqliteConnect(connectionPath)
        createTables(conn)
    except sqlite3.Error as error:
        print(error)
    else:
        app.run()