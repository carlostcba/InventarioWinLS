import wmi
import mysql.connector
from datetime import datetime

# Crear instancia de la clase wmi
c = wmi.WMI()

# Obtener nombre del SO
for os in c.Win32_OperatingSystem():
    NombreSO = os.Caption
    if NombreSO.startswith("Microsoft "):
        NombreSO = NombreSO.replace("Microsoft ", "")

# Obtener tipo de sistema
for cs in c.Win32_ComputerSystem():
    TipoSistema = cs.SystemType
    if TipoSistema == "x64-based PC":
        TipoSistema = "64 bits"
    elif TipoSistema == "x86-based PC":
        TipoSistema = "32 bits"

# Obtener nombre del sistema
for cs in c.Win32_ComputerSystem():
    NombreSistema = cs.Name

# Obtener producto de la placa base
for bb in c.Win32_BaseBoard():
    ProductoPlacaBase = bb.Product

# Obtener información del procesador
for processor in c.Win32_Processor():
    Procesador = processor.Name

# Obtener información de cada banco de memoria
bancos_memoria = []
totalRAM = 0  # Inicializar totalRAM
for memoria in c.Win32_PhysicalMemory():
    tamaño = round(int(memoria.Capacity) / (1024**3), 2)  # Convertir bytes a GB
    if tamaño > 0:
        bancos_memoria.append(f"{tamaño} GB")
        totalRAM += tamaño  # Sumar el tamaño al total de RAM

# Completar hasta 4 bancos de memoria con valores nulos si es necesario
while len(bancos_memoria) < 4:
    bancos_memoria.append(None)

# Obtener unidades de disco
discos = []
for disk in c.Win32_DiskDrive():
    modelo = disk.Model
    if disk.Size is not None:
        tamaño_gb = round(int(disk.Size) / (1024**3), 2)
        capacidad = f"{tamaño_gb} GB"  # Agregar la unidad de medida "GB" al valor de capacidad
    else:
        capacidad = "0 GB"  # Si el tamaño es desconocido, se establece en 0 para excluirlo
    discos.append((modelo, capacidad))

# Completar hasta 4 discos con valores nulos si es necesario
while len(discos) < 4:
    discos.append((None, None))

# Conectar a la base de datos MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='inventario',
    password='LaSalle2599',
    database='inventoryDB'
)
cursor = conn.cursor()

# Insertar los datos en la tabla
query = """
INSERT INTO inventoryLS (nameOS, tipoOS, hostname, motherboard, processor, totalRAM, bank1, bank2, bank3, bank4, disk1_model, disk1_capacity, disk2_model, disk2_capacity, disk3_model, disk3_capacity, disk4_model, disk4_capacity, date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
values = (
    NombreSO,
    TipoSistema,
    NombreSistema,
    ProductoPlacaBase,
    Procesador,
    f"{totalRAM} GB",  # Formatear totalRAM con unidad GB
    bancos_memoria[0],
    bancos_memoria[1],
    bancos_memoria[2],
    bancos_memoria[3],
    discos[0][0],
    discos[0][1],
    discos[1][0],
    discos[1][1],
    discos[2][0],
    discos[2][1],
    discos[3][0],
    discos[3][1],
    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
)

cursor.execute(query, values)
conn.commit()

cursor.close()
conn.close()

print("Los datos se han guardado en la base de datos MySQL")
