import wmi

# Crear instancia de la clase wmi
c = wmi.WMI()

# Obtener nombre del SO
for os in c.Win32_OperatingSystem():
    NombreSO = os.Caption

# Obtener tipo de sistema
for cs in c.Win32_ComputerSystem():
    TipoSistema = cs.SystemType

# Obtener nombre del sistema
for cs in c.Win32_ComputerSystem():
    NombreSistema = cs.Name

# Obtener modelo del sistema
for cs in c.Win32_ComputerSystem():
    ModeloSistema = cs.Model

# Obtener producto de la placa base
for bb in c.Win32_BaseBoard():
    ProductoPlacaBase = bb.Product

# Obtener información del procesador
for processor in c.Win32_Processor():
    Procesador = processor.Name

# Obtener memoria física instalada (RAM)
for cs in c.Win32_ComputerSystem():
    MemoriaRAM = round(int(cs.TotalPhysicalMemory) / (1024**3), 2)

# Obtener unidades de disco
UnidadesDisco = ""
for disk in c.Win32_DiskDrive():
    modelo = disk.Model
    if disk.Size is not None:
        tamaño = round(int(disk.Size) / (1024**3), 2)
    else:
        tamaño = "Desconocido"
    UnidadesDisco += f"Modelo: {modelo}, Tamaño: {tamaño} GB\n"


# Crear el contenido del archivo de texto
contenido_archivo = f"""
Nombre de SO: {NombreSO}
Tipo de sistema: {TipoSistema}
Nombre del sistema: {NombreSistema}
Modelo del sistema: {ModeloSistema}
Producto de la placa base: {ProductoPlacaBase}
Procesador: {Procesador}
Memoria física instalada (RAM): {MemoriaRAM} GB
Unidades de disco:
{UnidadesDisco}
"""

# Ruta del archivo de texto
ruta_archivo = "C:\\Ruta\\archivo.txt"

# Guardar los datos en el archivo de texto
with open(ruta_archivo, "w") as archivo:
    archivo.write(contenido_archivo)

print(f"Los datos se han guardado en {ruta_archivo}")