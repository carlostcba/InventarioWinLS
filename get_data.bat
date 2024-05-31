# Obtiene los datos del sistema operativo Windows y los guarda en un archivo de texto

# Obtener nombre del SO
$NombreSO = (Get-WmiObject -Class Win32_OperatingSystem).Caption

# Obtener tipo de sistema
$TipoSistema = (Get-WmiObject -Class Win32_ComputerSystem).SystemType

# Obtener nombre del sistema
$NombreSistema = (Get-WmiObject -Class Win32_ComputerSystem).Name

# Obtener modelo del sistema
$ModeloSistema = (Get-WmiObject -Class Win32_ComputerSystem).Model

# Obtener producto de la placa base
$ProductoPlacaBase = (Get-WmiObject -Class Win32_BaseBoard).Product

# Obtener información del procesador
$Procesador = (Get-WmiObject -Class Win32_Processor).Name

# Obtener memoria física instalada (RAM)
$MemoriaRAM = (Get-WmiObject -Class Win32_ComputerSystem).TotalPhysicalMemory / 1GB
$MemoriaRAM = [math]::Round($MemoriaRAM, 2)

# Obtener unidades de disco
$UnidadesDisco = Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, VolumeName, Size, FreeSpace | Format-Table -AutoSize | Out-String

# Obtener modelo de pantalla
$Pantalla = (Get-WmiObject -Namespace root\wmi -Class WmiMonitorBasicDisplayParams).MonitorName

# Crear el contenido del archivo de texto
$ContenidoArchivo = @"
Nombre de SO: $NombreSO
Tipo de sistema: $TipoSistema
Nombre del sistema: $NombreSistema
Modelo del sistema: $ModeloSistema
Producto de la placa base: $ProductoPlacaBase
Procesador: $Procesador
Memoria física instalada (RAM): $MemoriaRAM GB
Unidades de disco:
$UnidadesDisco
Pantalla (Modelo): $Pantalla
"@

# Ruta del archivo de texto
$RutaArchivo = "C:\Ruta\archivo.txt"

# Guardar los datos en el archivo de texto
$ContenidoArchivo | Out-File -FilePath $RutaArchivo -Encoding utf8

Write-Host "Los datos se han guardado en $RutaArchivo"