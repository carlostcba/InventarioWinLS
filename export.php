<?php

// Datos de conexión a la base de datos
$servername = "localhost";
$username = "inventario";
$password = "LaSalle2599";
$dbname = "inventoryDB";

// Crear conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Consulta SQL para obtener el contenido de la tabla inventoryLS agrupado por hostname y seleccionado el más reciente según la fecha
$sql = "SELECT * FROM inventoryLS WHERE (hostname, date) IN (SELECT hostname, MAX(date) FROM inventoryLS GROUP BY hostname)";
$result = $conn->query($sql);

// Verificar si se obtuvieron resultados
if ($result->num_rows > 0) {
    // Nombre del archivo CSV
    $filename = "inventory_data_" . date('Ymd') . ".csv";

    // Enviar cabeceras para forzar descarga
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="' . $filename . '"');

    // Abrir salida estándar para escribir el archivo CSV
    $output = fopen('php://output', 'w');

    // Obtener el primer registro y extraer las cabeceras excluyendo la columna 'id'
    $row = $result->fetch_assoc();
    $headers = array_keys($row);
    if(($key = array_search('id', $headers)) !== false) {
        unset($headers[$key]);
    }
    fputcsv($output, $headers);

    // Resetear el puntero del resultado y escribir datos excluyendo la columna 'id'
    $result->data_seek(0);
    while ($row = $result->fetch_assoc()) {
        unset($row['id']);
        fputcsv($output, $row);
    }

    // Cerrar el archivo
    fclose($output);
    exit();
} else {
    echo "0 resultados";
}

// Cerrar conexión
$conn->close();

?>
