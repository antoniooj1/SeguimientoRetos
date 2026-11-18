"""Verifica la conexión sin mostrar ni escribir credenciales en la consola."""
from pathlib import Path
import os
import sys
import struct
import django
import MySQLdb
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name('.env'))
print('Python:', sys.version.split()[0], '| Bits:', struct.calcsize('P') * 8)
print('Entorno:', sys.executable)
print('Django:', django.get_version())
conexion = MySQLdb.connect(
    host=os.environ['DB_HOST'], port=int(os.environ['DB_PORT']),
    user=os.environ['DB_USER'], passwd=os.environ['DB_PASSWORD'],
    db=os.environ['DB_NAME'], charset='utf8mb4',
)
with conexion.cursor() as cursor:
    cursor.execute('SELECT VERSION(), @@port, DATABASE(), CURRENT_USER()')
    print('Servidor, puerto, base y usuario:', cursor.fetchone())
    cursor.execute('SHOW TABLES')
    print('Tablas:', len(cursor.fetchall()))
conexion.close()
print('OK: conexión Python–MySQL')
