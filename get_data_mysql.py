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

# Obtener memoria física instalada (RAM)
for cs in c.Win32_ComputerSystem():
    MemoriaRAM = round(int(cs.TotalPhysicalMemory) / (1024**3), 2)

# Obtener información de cada banco de memoria
bancos_memoria = []
for memoria in c.Win32_PhysicalMemory():
    tamaño = round(int(memoria.Capacity) / (1024**3), 2)  # Convertir bytes a GB
    if tamaño > 0:
        bancos_memoria.append((memoria.DeviceLocator, tamaño))

# Completar hasta 4 bancos de memoria con valores nulos si es necesario
while len(bancos_memoria) < 4:
    bancos_memoria.append((None, None))

# Obtener unidades de disco
discos = []
for disk in c.Win32_DiskDrive():
    modelo = disk.Model
    if disk.Size is not None:
        tamaño = round(int(disk.Size) / (1024**3), 2)
    else:
        tamaño = 0  # Si el tamaño es desconocido, se establece en 0 para excluirlo
    if tamaño > 0:
        discos.append((modelo, tamaño))

# Completar hasta 4 discos con valores nulos si es necesario
while len(discos) < 4:
    discos.append((None, None))

# Conectar a la base de datos MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='tu_usuario',
    password='tu_contraseña',
    database='inventoryDB'  # Asegúrate de usar el nombre correcto de la base de datos
)
cursor = conn.cursor()

# Insertar los datos en la tabla
query = """
INSERT INTO inventoryLS (
    nameOS, tipoOS, hostname, motherboard, totalRAM, 
    bank1_name, bank1_capacity, bank2_name, bank2_capacity, 
    bank3_name, bank3_capacity, bank4_name, bank4_capacity, 
    disk1_model, disk1_capacity, disk2_model, disk2_capacity, 
    disk3_model, disk3_capacity, disk4_model, disk4_capacity, date)
VALUES (
    %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, 
    %s, %s, %s, %s, 
    %s, %s, %s, %s, 
    %s, %s, %s
)
"""
values = (
    NombreSO,
    TipoSistema,
    NombreSistema,
    ProductoPlacaBase,
    MemoriaRAM,
    bancos_memoria[0][0], bancos_memoria[0][1],
    bancos_memoria[1][0], bancos_memoria[1][1],
    bancos_memoria[2][0], bancos_memoria[2][1],
    bancos_memoria[3][0], bancos_memoria[3][1],
    discos[0][0], discos[0][1],
    discos[1][0], discos[1][1],
    discos[2][0], discos[2][1],
    discos[3][0], discos[3][1],
    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
)

cursor.execute(query, values)
conn.commit()

cursor.close()
conn.close()

print("Los datos se han guardado en la base de datos MySQL")
