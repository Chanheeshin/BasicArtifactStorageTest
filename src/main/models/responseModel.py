from src.main.utils.FileOperationsUtil import isBinary

class responseModel:

    def __init__(self, protocol, status, headers, body):
        self.protocol = protocol
        self.status = status
        self.headers = headers
        self.body = body

    def __str__(self):
        responseString = self.protocol + " " + self.status + "\n"
        responseString += self.headers[0][0] + ": " + self.headers[0][1].split(';')[0] + "\n"
        responseString += self.headers[1][0] + ": " + self.headers[1][1] + "\n\n"

        if isBinary(self.headers[0][1].split(';')[0].split('/')[0], self.headers[0][1].split(';')[0].split('/')[1]):
            responseString += "Downloading Binary File"
        else:
            responseString += self.body.decode("utf-8")

        return responseString