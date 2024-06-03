<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Data</title>
    <style>
        @keyframes blinking {
            0% { background-color: rgba(255, 165, 0, 0.3); }
            50% { background-color: rgba(255, 255, 0, 0.3); }
            100% { background-color: rgba(255, 165, 0, 0.3); }
        }
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            padding: 20px;
        }
        .box {
            border: 2px solid;
            padding: 10px;
            margin: 10px;
            width: 300px;
            border-radius: 8px;
            position: relative;
        }
        .box.red {
            border-color: red;
            background-color: rgba(255, 0, 0, 0.1);
        }
        .box.green {
            border-color: green;
            background-color: rgba(0, 255, 0, 0.1);
        }
        .box.blinking {
            animation: blinking 1s infinite;
            border-color: orange;
        }
        .hostname {
            background-color: #f0f0f0;
            color: #000;
            padding: 5px;
            font-weight: bold;
            text-align: center;
            border-radius: 4px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .data-field {
            padding: 5px;
            margin-bottom: 5px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        .change {
            color: orange;
        }
        .previous {
            color: red;
        }
        .checkbox-container {
            position: right;
        }
    </style>
</head>
<body>

<!-- Formulario de exportación -->
<form method="post" action="export.php">
    <button type="submit">Exportar a CSV</button>
</form>

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

// Consulta SQL para obtener el contenido de la tabla inventoryLS agrupado por hostname y seleccionado el más reciente según la fecha y ordenado por hostname
$sql = "SELECT * FROM inventoryLS WHERE (hostname, date) IN (SELECT hostname, MAX(date) FROM inventoryLS GROUP BY hostname) ORDER BY hostname";
$result = $conn->query($sql);

// Verificar si se obtuvieron resultados
if ($result->num_rows > 0) {
    echo "<div class='container'>";
    
    // Consulta para obtener el registro anterior
    $previousQuery = $conn->prepare("SELECT * FROM inventoryLS WHERE hostname = ? ORDER BY date DESC LIMIT 1,1");
    
    while ($row = $result->fetch_assoc()) {
        // Calcular la diferencia de tiempo entre la fecha actual y la fecha del registro
        $currentDate = new DateTime();
        $recordDate = new DateTime($row['date']);
        $interval = $currentDate->diff($recordDate);

        // Determinar el color del borde según la diferencia de tiempo
        $boxClass = ($interval->days * 24 + $interval->h) > 72 ? 'box red' : 'box green';

        // Obtener el registro anterior para comparar
        $previousQuery->bind_param('s', $row['hostname']);
        $previousQuery->execute();
        $previousResult = $previousQuery->get_result();
        $changes = [];
        $totalRAMChanged = false;
        if ($previousResult->num_rows > 0) {
            $previousRow = $previousResult->fetch_assoc();
            
            // Comparar campos relevantes
            $fieldsToCompare = [
                'processor', 'motherboard', 'totalRAM', 
                'bank1', 'bank2', 'bank3', 'bank4', 
                'disk1_model', 'disk1_capacity', 'disk2_model', 'disk2_capacity', 
                'disk3_model', 'disk3_capacity', 'disk4_model', 'disk4_capacity'
            ];
            $hasChanges = false;
            
            foreach ($fieldsToCompare as $field) {
                if ($row[$field] != $previousRow[$field]) {
                    $hasChanges = true;
                    $changes[$field] = ['previous' => $previousRow[$field], 'current' => $row[$field]];
                    if ($field == 'totalRAM') {
                        $totalRAMChanged = true;
                    }
                }
            }
            
            if ($hasChanges && $totalRAMChanged) {
                $boxClass = 'box blinking';
            } elseif ($hasChanges) {
                $boxClass = 'box green';
            }
        }

        echo "<div class='$boxClass'>";

        // Resaltar y centrar el hostname con el checkbox solo si es blinking o red
        echo "<div class='hostname'>" . $row['hostname'];
        if ($boxClass == 'box blinking' || $boxClass == 'box red') {
            echo "<div class='checkbox-container'><input type='checkbox' onchange='toggleBlinking(this)'></div>";
        }
        echo "</div>";

        // Mostrar nameOS y tipoOS juntos
        if (!is_null($row['nameOS']) && !is_null($row['tipoOS'])) {
            echo "<div class='data-field'>" . $row['nameOS'] . " " . $row['tipoOS'] . "</div>";
        }

        // Mostrar el procesador
        if (!is_null($row['processor'])) {
            echo "<div class='data-field'>" . $row['processor'];
            if (isset($changes['processor'])) {
                echo " <span class='previous'>(antes: " . $changes['processor']['previous'] . ")</span>";
            }
            echo "</div>";
        }

        // Mostrar otros datos no nulos
        foreach ($row as $key => $value) {
            if ($key != 'id' && $key != 'hostname' && $key != 'nameOS' && $key != 'tipoOS' && $key != 'processor' && $key != 'status' && !is_null($value)) {
                // Agregar etiquetas específicas para bancos de memoria y RAM total
                if (strpos($key, 'bank') === 0) {
                    $bankNumber = str_replace('bank', '', $key);
                    echo "<div class='data-field'>Slot $bankNumber: $value";
                    if (isset($changes[$key])) {
                        echo " <span class='previous'>(antes: " . $changes[$key]['previous'] . ")</span>";
                    }
                    echo "</div>";
                } elseif ($key == 'totalRAM') {
                    echo "<div class='data-field'>RAM: $value";
                    if (isset($changes[$key])) {
                        echo " <span class='previous'>(antes: " . $changes[$key]['previous'] . ")</span>";
                    }
                    echo "</div>";
                } else {
                    echo "<div class='data-field'>$value";
                    if (isset($changes[$key])) {
                        echo " <span class='previous'>(antes: " . $changes[$key]['previous'] . ")</span>";
                    }
                    echo "</div>";
                }
            }
        }

        // Mostrar bancos de memoria que han sido removidos
        for ($i = 1; $i <= 4; $i++) {
            $bankKey = "bank$i";
            if (!isset($row[$bankKey]) && isset($previousRow[$bankKey]) && !is_null($previousRow[$bankKey])) {
                echo "<div class='data-field change'>Slot $i: (antes: " . $previousRow[$bankKey] . ")</div>";
            }
        }

        // Mostrar discos que han sido removidos
        for ($i = 1; $i <= 4; $i++) {
            $diskModelKey = "disk{$i}_model";
            $diskCapacityKey = "disk{$i}_capacity";
            if (!isset($row[$diskModelKey]) && isset($previousRow[$diskModelKey]) && !is_null($previousRow[$diskModelKey])) {
                echo "<div class='data-field change'>Disk $i: " . $previousRow[$diskModelKey] . " " . $previousRow[$diskCapacityKey] . " (antes)</div>";
            }
        }

        echo "</div>";
    }
    echo "</div>";
} else {
    echo "0 resultados";
}

// Cerrar conexión
$conn->close();

?>

<!-- Script para cambiar el estado de los cuadros -->
<script>
    function toggleBlinking(checkbox) {
        const box = checkbox.closest('.box');
        if (box.classList.contains('red')) {
            box.style.display = 'none';
        } else if (box.classList.contains('blinking')) {
            box.classList.remove('blinking');
            box.classList.add('green');
            checkbox.parentElement.style.display = 'none'; // Ocultar el checkbox después del cambio
        }
    }
</script>

</body>
</html>
