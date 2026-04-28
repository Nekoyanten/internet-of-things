import serial
import time
import sqlite3
from datetime import datetime

# ===== CONFIGURACIÓN =====
PUERTO = 'COM4'
BAUDRATE = 9600
DB_FILE = 'sensores.db'
# =========================

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lecturas (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha     TEXT NOT NULL,
            temp_lm35 REAL,
            temp_dht  REAL,
            humedad   REAL
        )
    ''')
    conn.commit()
    return conn

def guardar(conn, temp_lm35, temp_dht, humedad):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO lecturas (fecha, temp_lm35, temp_dht, humedad)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), temp_lm35, temp_dht, humedad))
    conn.commit()

def parsear(linea):
    try:
        # Formato: "LM35: 24.4 C | DHT11: 25.8 C | Humedad: 61.0%"
        partes = linea.split('|')
        temp_lm35 = float(partes[0].replace('LM35:', '').replace('C', '').strip())
        temp_dht  = float(partes[1].replace('DHT11:', '').replace('C', '').strip())
        humedad   = float(partes[2].replace('Humedad:', '').replace('%', '').strip())
        return temp_lm35, temp_dht, humedad
    except:
        return None

def leer_serial():
    conn = init_db()
    print(f"Base de datos: {DB_FILE}")

    try:
        arduino = serial.Serial(PUERTO, BAUDRATE, timeout=2)
        time.sleep(2)
        print(f"Conectado a {PUERTO}")
        print("=============================")

        while True:
            linea = arduino.readline().decode('utf-8', errors='ignore').strip()

            if not linea:
                continue

            if 'ALERTA' in linea or 'ESTADO' in linea:
                print(f"  → {linea}")

            elif 'LM35:' in linea and 'DHT11:' in linea:
                print(linea)
                datos = parsear(linea)
                if datos:
                    guardar(conn, *datos)
                    print(f"  ✓ Guardado en {DB_FILE}")

    except serial.SerialException as e:
        print(f"Error de conexión: {e}")

    except KeyboardInterrupt:
        print("\nLectura detenida")
        arduino.close()
        conn.close()

if __name__ == '__main__':
    leer_serial()