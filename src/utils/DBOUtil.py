import sqlite3
from src.constants.constants import DATABASE_METADATA_TABLE
from src.constants.constants import DATABASE_FILE_TABLE

'''
    Create Database Operations utility class which 
    covers all database operations:
        CREATE
        UPDATE
        DELETE
    
    DBO scripts will be pulled from the ./scripts 
    folder where SQL scripts are stored and ready to 
    be executed as needed.
'''

'''
    Function to actually connect to the database.

    :params
        - none
    :return
        - conn (connection type object)
'''
def sqliteConnect(connectionString):
    try:
        conn = sqlite3.connect(connectionString)


    except sqlite3.Error:
        print(f"Error connecting to the database '{connectionString}'")
    finally:
        return conn



def createTables(connectionString):
    try:
        connection = sqliteConnect(connectionString)

        sqlCreateMetadataTableQuery = f""" CREATE TABLE IF NOT EXISTS {DATABASE_METADATA_TABLE} (
                                                file_path VARCHAR(100) PRIMARY KEY,
                                                mime_type VARCHAR(100)
                                            ); """

        sqlCreateFileTableQuery = f""" CREATE TABLE IF NOT EXISTS {DATABASE_FILE_TABLE} (
                                                file_path VARCHAR(100) PRIMARY KEY,
                                                file_data BLOB
                                            ); """

        cursor = connection.cursor()

        cursor.execute(sqlCreateMetadataTableQuery)
        cursor.execute(sqlCreateFileTableQuery)

    except sqlite3.Error as error:
        print("Failed to create tables in database:")
        print(error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")

        # return 0 to signify everything was successful
        return 0


'''
    Function to insert files into the database 
    
    :params
        - filePath : literal file path
        - mimeType : actual file type
        - fileData : data that is in the file
    :returns
        - 0 : ALL GOOD
'''
def insertFile(connectionString, filePath, mimeType, fileData):
    try:
        connection = sqliteConnect(connectionString)
        print("Connected to database")

        cursor = connection.cursor()

        sqlMetadataInsertQuery = f"""
                                    INSERT OR REPLACE INTO {DATABASE_METADATA_TABLE} (file_path, mime_type) VALUES (?, ?)
                                    """

        sqlFileInsertQuery = f"""
                                INSERT OR REPLACE INTO {DATABASE_FILE_TABLE} (file_path, file_data) VALUES (?, ?)  
                                """

        binaryData = ''.join(format(ord(i), '08b') for i in fileData)

        cursor.execute(sqlMetadataInsertQuery, (filePath, mimeType))
        cursor.execute(sqlFileInsertQuery, (filePath, binaryData))

        connection.commit()
        print("Successfully inserted file into database as BLOB")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into database:")
        print(error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")

        #return 0 to signify everything was successful
        return 0


'''
    Function to retrieve files from the database 

    :params
        - filePath : literal file path
    :returns
        - (mimeType, fileData) : Successful completion
        - 1 : failure to find file in metadata table
        - 2 : failure to find file in data table
'''
def retrieveFile(connectionString, filePath):
    try:
        mimeType = None
        fileData = None
        connection = sqliteConnect(connectionString)
        print("Connected to database")

        cursor = connection.cursor()

        sqlFileTypeSearchQuery = f"""SELECT * FROM {DATABASE_METADATA_TABLE} WHERE file_path=?"""

        sqlFileDataSearchQuery = f"""SELECT * FROM {DATABASE_FILE_TABLE} WHERE file_path=?"""

        # As we know the database is made up of two tables as expressed in the design doc we don't need much more logic
        # than this I believe. Simple enough to grab check that it grabbed 1 and return it. This checks the file exists.
        result = cursor.execute(sqlFileTypeSearchQuery, (filePath,))

        if cursor.fetchone()[1] is not NoneType:
            mimeType = cursor.fetchone()[1]
        else:
            # return 1 for now to indicate that the file does not exist
            return 1

        result = cursor.execute(sqlFileDataSearchQuery, (filePath,))

        if cursor.fetchone()[1] is not None:
            temp = cursor.fetchone()[1]
            fileData = ''.join(format(ord(i), '08b') for i in temp)

        else:
            # return 2 for now to indicate that the file for some reason exists but it's data was not stored.
            return 2

        return((mimeType, fileData))

    except sqlite3.Error as error:
        print("Failure while retrieving file from database:")
        print(error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")
