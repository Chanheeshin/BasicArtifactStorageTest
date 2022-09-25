'''
if __name__ == '__main__':
    testDBPath = "../resources/database/resource.db"

    testPath = "test/path/jsonTest2"
    testMIME = "application/json"
    testData = '{ "name":"John", "age":30, "city":"New York"}'

    createFile(testPath, testMIME, testData)

    sqliteConnect(testDBPath)
    createTables(testDBPath)

    insertFile(testDBPath, testPath, testMIME, "jsonTest2.json")

    removeFile(RELATIVE_STAGING_PATH + "jsonTest2.json")

    temp = retrieveFile(testDBPath, testPath, "jsonTest2.json")

    print(temp)

'''