import sqlite3
from src.main.constants.constants import DATABASE_METADATA_TABLE
from src.main.constants.constants import DATABASE_FILE_TABLE
from src.main.constants.constants import RELATIVE_OUTBOUND_PATH
from mimetypes import guess_extension

from src.main.utils.FileOperationsUtil import convertToBinaryData
from src.main.utils.FileOperationsUtil import writeTofile
from src.main.utils.FileOperationsUtil import removeFile


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
    except sqlite3.Error as error:
        print(f"Error connecting to the database '{connectionString}'")
        return error
    else:
        return conn

'''
    Function to initialize tables in SQLite3 database
'''
def createTables(connectionObject):
    try:
        connection = connectionObject

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

        return 0

    except sqlite3.Error as error:
        print("Failed to create tables in database:")
        print(error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")

'''
    Function to insert files into the database 
    
    :params
        - filePath : literal file path
        - mimeType : actual file type
        - fileData : data that is in the file
    :returns
        - 0 : ALL GOOD
'''
def insertFile(connectionString, filePath, mimeType, inboundFileName):
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

        binaryData = convertToBinaryData(inboundFileName)

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
def retrieveFile(connectionString, filePath, workingDirectory):
    try:
        connection = sqliteConnect(connectionString)
        print("Connected to database")

        cursor = connection.cursor()

        sqlFileTypeSearchQuery = f"""SELECT * FROM {DATABASE_METADATA_TABLE} WHERE file_path=?"""
        sqlFileDataSearchQuery = f"""SELECT * FROM {DATABASE_FILE_TABLE} WHERE file_path=?"""

        result = cursor.execute(sqlFileTypeSearchQuery, (filePath,))
        mimeType = cursor.fetchone()[1]

        result = cursor.execute(sqlFileDataSearchQuery, (filePath,))
        fileData = cursor.fetchone()[1]

        # Create outbound file name
        outboundFileName = workingDirectory + RELATIVE_OUTBOUND_PATH + filePath.split("/")[-1] + guess_extension(mimeType)

        writeTofile(fileData, outboundFileName)

        return(mimeType, fileData)

    except sqlite3.Error as error:
        print("Failure while retrieving file from database:")
        print(error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")

'''
    Function to delete files from the database
'''
def deleteFile(connectionString, filePath, workingDirectory):
    try:
        connection = sqliteConnect(connectionString)
        cursor = connection.cursor()

        sqlDeleteMetadataFileQuery = f"""DELETE FROM {DATABASE_METADATA_TABLE} WHERE file_path=?"""
        sqlDeleteDataFileQuery = f"""DELETE FROM {DATABASE_FILE_TABLE} WHERE file_path=?"""
        sqlFileTypeSearchQuery = f"""SELECT * FROM {DATABASE_METADATA_TABLE} WHERE file_path=?"""

        result = cursor.execute(sqlFileTypeSearchQuery, (filePath,))
        mimeType = cursor.fetchone()[1]

        outboundFileName = workingDirectory + RELATIVE_OUTBOUND_PATH + filePath.split("/")[-1] + guess_extension(mimeType)

        removeFile(outboundFileName)

        cursor.execute(sqlDeleteMetadataFileQuery, (filePath,))
        cursor.execute(sqlDeleteDataFileQuery, (filePath,))

        connection.commit()

        return

    except sqlite3.Error as error:
        print("Failure to delete file")
        print(error)
    finally:
        if connection:
            connection.close()
            print("Connection closed")