 document.addEventListener('DOMContentLoaded', function() {
            // --- Lógica existente del Sidebar ---
            const sidebarToggle = document.getElementById('sidebarToggle');
            const sidebar = document.getElementById('sidebar');

            // Función para alternar la clase 'collapsed' del sidebar
            if (sidebarToggle && sidebar) { // Verificación para asegurar que los elementos existen
                sidebarToggle.addEventListener('click', function() {
                    sidebar.classList.toggle('collapsed');
                    const isCollapsed = sidebar.classList.contains('collapsed');

                    // Ajustar visibilidad de los elementos dentro del sidebar para la transición
                    document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header').forEach(el => {
                        el.style.opacity = isCollapsed ? '0' : '1';
                    });

                    document.querySelectorAll('#sidebar .nav-item:not(.has-submenu)').forEach(el => {
                        el.style.height = isCollapsed ? '0' : '';
                        el.style.overflow = isCollapsed ? 'hidden' : '';
                        el.style.margin = isCollapsed ? '0' : '';
                        el.style.padding = isCollapsed ? '0' : '';
                    });

                    // Si el sidebar se colapsa, ocultar submenús activos
                    if (isCollapsed) {
                        document.querySelectorAll('.submenu.show').forEach(submenu => {
                            if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                                const bsCollapse = new bootstrap.Collapse(submenu, { toggle: false });
                                bsCollapse.hide();
                            }
                        });
                    }
                });
            } else {
                console.warn("Sidebar toggle or sidebar element not found. Sidebar functionality might be affected.");
            }

            // Lógica para inicializar el estado del sidebar y el toggler en función del tamaño de la pantalla
            function adjustLayout() {
                if (window.innerWidth <= 768) {
                    if (sidebar) {
                        sidebar.classList.add('collapsed');
                        document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header, #sidebar .nav-item:not(.has-submenu)').forEach(el => {
                            el.style.opacity = '0';
                            el.style.height = '0';
                            el.style.padding = '0';
                            el.style.margin = '0';
                        });
                        document.querySelectorAll('.submenu').forEach(submenu => {
                            if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                                const bsCollapse = new bootstrap.Collapse(submenu, { toggle: false });
                                bsCollapse.hide();
                            }
                        });
                    }

                } else {
                    if (sidebar) {
                        sidebar.classList.remove('collapsed');
                        document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header, #sidebar .nav-item').forEach(el => {
                            el.style.opacity = '1';
                            el.style.height = ''; 
                            el.style.padding = '';
                            el.style.margin = '';
                        });
                    }
                }
            }
            
            // Cerrar otros submenús cuando se hace clic en un elemento del menú principal
            document.querySelectorAll('#sidebar .nav-item.has-submenu > .nav-link').forEach(link => {
                link.addEventListener('click', function(event) {
                    const targetSubmenuId = this.dataset.bsTarget;
                    document.querySelectorAll('.submenu.show').forEach(openSubmenu => {
                        if ('#' + openSubmenu.id !== targetSubmenuId) {
                            if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                                const bsCollapse = new bootstrap.Collapse(openSubmenu, { toggle: false });
                                bsCollapse.hide();
                            }
                        }
                    });
                });
            });

            // Llamar a la función de ajuste de diseño al cargar y al cambiar el tamaño de la ventana
            adjustLayout();
            window.addEventListener('resize', adjustLayout);


            // --- Nueva Lógica para los Botones de Historial ---
            // CORRECCIÓN: Los IDs de los botones en el HTML son 'guardarHistorialBtn' y 'eliminarHistorialBtn'
            const fechaCreacionInput = document.getElementById('fechaCreacion');
            const nombrePacienteInput = document.getElementById('nombrePaciente');
            const otrosDatosTextarea = document.getElementById('otrosDatos');
            const guardarBtn = document.getElementById('guardarHistorialBtn'); // ID CORREGIDO
            const eliminarBtn = document.getElementById('eliminarHistorialBtn'); // ID CORREGIDO

            // Verificación crítica: Asegúrate de que todos los elementos existen antes de añadir event listeners
            const formElementsExist = fechaCreacionInput && nombrePacienteInput && otrosDatosTextarea && guardarBtn && eliminarBtn;

            if (!formElementsExist) {
                console.error('Error: Uno o más elementos del formulario de historial no fueron encontrados. Revisa los IDs en tu HTML.');
                console.log('Estado de elementos:');
                console.log('fechaCreacionInput:', fechaCreacionInput);
                console.log('nombrePacienteInput:', nombrePacienteInput);
                console.log('otrosDatosTextarea:', otrosDatosTextarea);
                console.log('guardarBtn (esperaba #guardarHistorialBtn):', guardarBtn);
                console.log('eliminarBtn (esperaba #eliminarHistorialBtn):', eliminarBtn);
                return; // Detener la ejecución de la lógica del formulario si faltan elementos
            }

            function areAllFieldsFilled() {
                const fechaLlena = fechaCreacionInput.value.trim() !== '';
                const nombreLlena = nombrePacienteInput.value.trim() !== '';
                const otrosDatosLlenos = otrosDatosTextarea.value.trim() !== '';
                return fechaLlena && nombreLlena && otrosDatosLlenos;
            }

            // Funcionalidad para el botón GUARDAR
            guardarBtn.addEventListener('click', function() {
                console.log('Botón Guardar clickeado.');
                if (areAllFieldsFilled()) {
                    const datosAguardar = {
                        fecha: fechaCreacionInput.value.trim(),
                        nombre: nombrePacienteInput.value.trim(),
                        otros: otrosDatosTextarea.value.trim()
                    };
                    console.log('Datos a guardar:', datosAguardar);
                    alert('Datos guardados exitosamente!');
                    // Aquí deberías integrar tu lógica de backend para guardar los datos
                    // Por ejemplo: fetch('/api/guardarHistorial', { method: 'POST', body: JSON.stringify(datosAguardar) })
                } else {
                    alert('Por favor, complete todos los campos antes de guardar.');
                }
            });

            // Funcionalidad para el botón ELIMINAR
            eliminarBtn.addEventListener('click', function() {
                console.log('Botón Eliminar clickeado.');
                if (areAllFieldsFilled()) {
                    if (confirm('¿Está seguro de que desea eliminar los datos de estos campos?')) {
                        // Aquí deberías integrar tu lógica de backend para eliminar datos
                        // Por ejemplo: fetch('/api/eliminarHistorial', { method: 'DELETE', body: JSON.stringify({ nombre: nombrePacienteInput.value.trim() }) })
                        
                        // Limpiar los campos después de la "eliminación"
                        fechaCreacionInput.value = '';
                        nombrePacienteInput.value = '';
                        otrosDatosTextarea.value = '';

                        console.log('Campos eliminados.');
                        alert('Datos eliminados exitosamente.');
                        updateButtonStates(); // Actualiza el estado de los botones
                    }
                } else {
                    alert('Todos los campos deben estar llenos para poder proceder con la eliminación (o no hay datos que eliminar).');
                }
            });

            // Opcional: Validación en tiempo real (habilitar/deshabilitar botones)
            const fields = [fechaCreacionInput, nombrePacienteInput, otrosDatosTextarea];

            function updateButtonStates() {
                const fieldsFilled = areAllFieldsFilled();
                // Asegúrate de que los botones existan antes de intentar deshabilitarlos
                if (guardarBtn) guardarBtn.disabled = !fieldsFilled;
                if (eliminarBtn) eliminarBtn.disabled = !fieldsFilled;
            }

            fields.forEach(field => {
                if (field) { // Asegúrate de que el campo exista antes de añadir el event listener
                    field.addEventListener('input', updateButtonStates);
                }
            });

            // Llamar una vez al cargar la página para establecer el estado inicial de los botones
            updateButtonStates();
        });