import psycopg
from config import setting

async def get_connection():
    connection =await  psycopg.AsyncConnection.connect(
         host = setting.db_host,
        dbname = setting.db_name,
        user = setting.db_user,
        password = setting.db_password,
        port = setting.db_port    
    )

    return connection
