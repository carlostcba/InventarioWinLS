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

# Obtener información del procesador
for processor in c.Win32_Processor():
    Procesador = processor.Name

# Obtener producto de la placa base
for bb in c.Win32_BaseBoard():
    ProductoPlacaBase = bb.Product

# Obtener información de cada banco de memoria y calcular la RAM total
bancos_memoria = []
MemoriaRAM_total = 0
for memoria in c.Win32_PhysicalMemory():
    tamaño = round(int(memoria.Capacity) / (1024**3), 2)  # Convertir bytes a GB
    if tamaño > 0:
        bancos_memoria.append(f"{tamaño} GB")
        MemoriaRAM_total += tamaño

# Completar hasta 4 bancos de memoria con valores nulos si es necesario
while len(bancos_memoria) < 4:
    bancos_memoria.append(None)

# Formatear MemoriaRAM_total con unidad de medida
if MemoriaRAM_total >= 1024:  # Si la memoria es mayor o igual a 1 TB
    MemoriaRAM_total = round(MemoriaRAM_total / 1024, 2)
    unidad_medida = "TB"
else:
    unidad_medida = "GB"
MemoriaRAM_total = f"{MemoriaRAM_total} {unidad_medida}"

# Obtener unidades de disco y excluir aquellos con capacidad 0
discos = []
for disk in c.Win32_DiskDrive():
    modelo = disk.Model
    if disk.Size is not None:
        tamaño_gb = round(int(disk.Size) / (1024**3), 2)
        if tamaño_gb > 0:
            capacidad = f"{tamaño_gb} GB"
            discos.append((modelo, capacidad))

# Completar hasta 4 discos con valores nulos si es necesario
while len(discos) < 4:
    discos.append((None, None))

# Obtener direcciones MAC e IP de las interfaces de red físicas
mac_addresses = []
ip_addresses = []
for nic in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
    if nic.MACAddress is not None and "Virtual" not in nic.Description:
        mac_addresses.append(nic.MACAddress)
        if nic.IPAddress:
            ip_addresses.extend(nic.IPAddress)

# Seleccionar la IP de la interfaz de red principal (si está disponible)
ip_principal = None
for ip in ip_addresses:
    if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
        ip_principal = ip
        break

# Completar hasta 4 direcciones MAC con valores nulos si es necesario
while len(mac_addresses) < 4:
    mac_addresses.append(None)

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
INSERT INTO inventoryLS (nameOS, tipoOS, hostname, processor, motherboard, totalRAM, bank1, bank2, bank3, bank4, disk1_model, disk1_capacity, disk2_model, disk2_capacity, disk3_model, disk3_capacity, disk4_model, disk4_capacity, mac1, mac2, mac3, mac4, ip_principal, date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
values = (
    NombreSO,
    TipoSistema,
    NombreSistema,
    Procesador,
    ProductoPlacaBase,
    MemoriaRAM_total,
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
    mac_addresses[0],
    mac_addresses[1],
    mac_addresses[2],
    mac_addresses[3],
    ip_principal,
    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
)

cursor.execute(query, values)
conn.commit()

cursor.close()
conn.close()

print("Los datos se han guardado en la base de datos MySQL")
