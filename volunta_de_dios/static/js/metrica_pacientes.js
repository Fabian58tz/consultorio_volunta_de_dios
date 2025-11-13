document.addEventListener('DOMContentLoaded', function() {
    const saveMetricBtn = document.getElementById('saveMetricBtn');
    const deleteMetricBtn = document.getElementById('deleteMetricBtn');
    const fechaMedicionInput = document.getElementById('fechaMedicion');
    const tallaInput = document.getElementById('talla');
    const pesoInput = document.getElementById('peso');
    const otrosDatosTextarea = document.getElementById('otrosDatos');
    const messageArea = document.getElementById('messageArea');

    // Función para mostrar mensajes
    function displayMessage(message, type) {
        messageArea.textContent = message;
        messageArea.className = 'message-area'; // Restablecer clases
        if (type === 'success') {
            messageArea.classList.add('alert', 'alert-success');
        } else if (type === 'error') {
            messageArea.classList.add('alert', 'alert-danger');
        }
        messageArea.style.display = 'block';
    }

    // Función para limpiar mensajes
    function clearMessage() {
        messageArea.textContent = '';
        messageArea.className = 'message-area';
        messageArea.style.display = 'none';
    }

    // Función para limpiar todos los campos del formulario
    function clearFormFields() {
        fechaMedicionInput.value = '';
        tallaInput.value = '';
        pesoInput.value = '';
        otrosDatosTextarea.value = '';
        clearMessage(); // Limpiar también los mensajes al limpiar los campos
    }

    // Evento de clic para el botón Guardar
    saveMetricBtn.addEventListener('click', function() {
        clearMessage(); // Limpiar mensajes anteriores

        const fechaMedicion = fechaMedicionInput.value.trim(); // .trim() para eliminar espacios en blanco
        const talla = tallaInput.value.trim();
        const peso = pesoInput.value.trim();
        const otrosDatos = otrosDatosTextarea.value.trim();

        // Validaciones individuales para cada campo requerido
        if (!fechaMedicion) {
            displayMessage('Por favor, llene el campo **Fecha de Medición**.', 'error');
            fechaMedicionInput.focus();
            return;
        }
        if (!talla) {
            displayMessage('Por favor, llene el campo **Talla**.', 'error');
            tallaInput.focus();
            return;
        }
        if (!peso) {
            displayMessage('Por favor, llene el campo **Peso**.', 'error');
            pesoInput.focus();
            return;
        }

        // Validación de tipo de dato y valor para Talla y Peso
        const parsedTalla = parseFloat(talla);
        const parsedPeso = parseFloat(peso);

        if (isNaN(parsedTalla) || parsedTalla <= 0) {
            displayMessage('La **Talla** debe ser un número válido mayor que cero.', 'error');
            tallaInput.focus();
            return;
        }
        if (isNaN(parsedPeso) || parsedPeso <= 0) {
            displayMessage('El **Peso** debe ser un número válido mayor que cero.', 'error');
            pesoInput.focus();
            return;
        }

        // --- Simulación de guardado funcional ---
        // En una aplicación real, aquí es donde enviarías los datos a tu servidor.
        // Por ahora, solo los mostraremos en la consola y simularemos una respuesta.
        console.log('Datos a guardar:');
        console.log({
            fechaMedicion: fechaMedicion,
            talla: parsedTalla,
            peso: parsedPeso,
            otrosDatos: otrosDatos
        });

        // Simular una llamada a una API que siempre tiene éxito por ahora
        setTimeout(() => { // Usamos setTimeout para simular una operación asíncrona
            displayMessage('¡Métrica guardada exitosamente!', 'success');
            clearFormFields(); // Limpiar los campos después de un guardado exitoso
        }, 500); // Retraso de 500ms para simular la respuesta del servidor

        /*
        // Ejemplo de cómo harías una solicitud real con fetch (descomenta para usar)
        fetch('/api/save-metric', { // Reemplaza '/api/save-metric' con la URL de tu API
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 'Authorization': 'Bearer TU_TOKEN_DE_AUTENTICACION' // Si usas tokens
            },
            body: JSON.stringify({
                fechaMedicion: fechaMedicion,
                talla: parsedTalla,
                peso: parsedPeso,
                otrosDatos: otrosDatos
            }),
        })
        .then(response => {
            if (!response.ok) {
                // Manejar errores HTTP (ej. 400, 500)
                throw new Error('Error en la red o en el servidor: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) { // Asumiendo que tu API devuelve { success: true }
                displayMessage('¡Métrica guardada exitosamente!', 'success');
                clearFormFields();
            } else {
                displayMessage('Error al guardar la métrica: ' + (data.message || 'Error desconocido'), 'error');
            }
        })
        .catch((error) => {
            console.error('Error al guardar la métrica:', error);
            displayMessage('Error de conexión o problema al guardar la métrica.', 'error');
        });
        */
    });

    // Evento de clic para el botón Eliminar
    deleteMetricBtn.addEventListener('click', function() {
        clearFormFields();
        displayMessage('Los campos han sido limpiados.', 'success');
    });
});