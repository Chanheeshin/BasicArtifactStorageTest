from src.utils.DBOUtil import insertFile
from src.utils.DBOUtil import retrieveFile
from src.utils.DBOUtil import sqliteConnect
from src.utils.DBOUtil import createTables


if __name__ == '__main__':
    sqliteConnect("../resources/database/resource.db")
    createTables("../resources/database/resource.db")
    insertFile("../resources/database/resource.db", "test", "text/plain", "this is a test file")
    temp = retrieveFile("../resources/database/resource.db", "test")

    print(temp)