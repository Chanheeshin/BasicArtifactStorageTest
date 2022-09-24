import json
from flask import Flask, request

#Create flask application
app = Flask(__name__)

'''

'''
@app.route('/<path:path>', methods=['POST'])
def createResource(path):

    return json.dumps("Resource path is " + path)

'''
GET Route mapped to retrieving resources.

Use path argument to retrieve this specific resource

'''
@app.route('/<path:path>', methods=['GET'])
def createResource(path):

    return json.dumps("Resource path is " + path)



if __name__ == '__main__':
   app.run()