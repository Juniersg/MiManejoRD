from decouple import config
import pymysql

def get_connection():
    try:
        return pymysql.connect(
            HOST = config("MYSQL_HOST"),
            USER = config("MYSQL_USER"),
            PASSWORD = config("MYSQL_PASSWORD"),
            DB = config("MYSQL_MYSQL_DB")
          )
    except Exception as ex:
        print("Error al conextar con la base de datos: ", ex)


print(get_connection)