document.addEventListener("DOMContentLoaded", function() {
    const sidebarToggle = document.getElementById('sidebarToggle'); // Suponiendo que tienes un elemento sidebarToggle
    const sidebar = document.getElementById('sidebar'); // Suponiendo que tienes un elemento sidebar
    const citasTableBody = document.querySelector('#citasTable tbody');
    const addRowButton = document.getElementById('addRow');
    let nextId = 2; // El ID comienza en 2, ya que el ID 1 ya está en la fila de ejemplo

    // --- Funcionalidad de la Barra Lateral (Sidebar) ---
    if (sidebarToggle && sidebar) { // Verifica si los elementos del sidebar existen antes de añadir listeners
        // Función para alternar la barra lateral
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            const isCollapsed = sidebar.classList.contains('collapsed');

            document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header').forEach(el => {
                el.style.opacity = isCollapsed ? '0' : '1';
            });

            document.querySelectorAll('#sidebar .nav-item:not(.has-submenu)').forEach(el => {
                el.style.height = isCollapsed ? '0' : 'auto';
                el.style.overflow = isCollapsed ? 'hidden' : 'visible';
                el.style.margin = isCollapsed ? '0' : 'auto';
                el.style.padding = isCollapsed ? '0' : 'auto';
            });

            if (isCollapsed) {
                document.querySelectorAll('.submenu.show').forEach(submenu => {
                    // Asegúrate de que 'bootstrap' esté disponible globalmente
                    const bsCollapse = new bootstrap.Collapse(submenu, {
                        toggle: false
                    });
                    bsCollapse.hide();
                });
            }
        });

        // Cierra otros submenús cuando se hace clic en un elemento principal del menú
        document.querySelectorAll('#sidebar .nav-item.has-submenu > .nav-link').forEach(link => {
            link.addEventListener('click', function(event) {
                const targetSubmenuId = this.dataset.bsTarget; // Suponiendo que se usa data-bs-target para el ID del submenú

                document.querySelectorAll('.submenu.show').forEach(openSubmenu => {
                    if ('#' + openSubmenu.id !== targetSubmenuId) {
                        const bsCollapse = new bootstrap.Collapse(openSubmenu, {
                            toggle: false
                        });
                        bsCollapse.hide();
                    }
                });
            });
        });

        // Función para ajustar el diseño al cargar y redimensionar
        function adjustLayout() {
            if (window.innerWidth < 768) {
                sidebar.classList.add('collapsed');
                document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header').forEach(el => {
                    el.style.opacity = '0';
                    el.style.height = '0';
                    el.style.padding = '0';
                    el.style.margin = '0';
                });
                document.querySelectorAll('.submenu').forEach(submenu => {
                    const bsCollapse = new bootstrap.Collapse(submenu, {
                        toggle: false
                    });
                    bsCollapse.hide();
                });
            } else {
                sidebar.classList.remove('collapsed');
                document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header').forEach(el => {
                    el.style.opacity = '1';
                    el.style.height = 'auto';
                    el.style.padding = 'auto';
                    el.style.margin = 'auto';
                });
            }
        }

        // Llama al ajuste de diseño al cargar y redimensionar
        adjustLayout();
        window.addEventListener('resize', adjustLayout);
    }
    // --- Fin de la Funcionalidad de la Barra Lateral ---


    // --- Funcionalidad de la Tabla ---

    // Función para añadir una nueva fila
    addRowButton.addEventListener('click', function() {
        const newRow = citasTableBody.insertRow();
        newRow.setAttribute('data-id', nextId);
        newRow.innerHTML = `
            <td class="editable-cell"><input type="text" value=""></td>
            <td class="editable-cell"><input type="text" value=""></td>
            <td class="editable-cell"><input type="text" value=""></td>
            <td class="editable-cell"><input type="text" value=""></td>
            <td><span class="status-activo">Activo</span></td>
            <td class="action-buttons">
                <button class="btn-save d-none"><i class="bi bi-save"></i></button>
                <button class="btn-edit d-none"><i class="bi bi-pencil"></i></button>
                <button class="btn-delete"><i class="bi bi-trash"></i></button>
            </td>
        `;
        nextId++;
        // Habilita la edición para la fila recién añadida
        enableRowEditing(newRow);
    });

    // Delegación de eventos para las acciones de la tabla (editar, guardar, eliminar)
    citasTableBody.addEventListener('click', function(event) {
        const target = event.target;
        const row = target.closest('tr'); // Obtiene el elemento de fila más cercano

        if (!row) return; // Si no se encuentra ninguna fila, sale

        if (target.closest('.btn-edit')) {
            enableRowEditing(row);
        } else if (target.closest('.btn-save')) {
            saveRowEditing(row);
        } else if (target.closest('.btn-delete')) {
            deleteRow(row);
        }
    });

    // Función para habilitar la edición de una fila
    function enableRowEditing(row) {
        // Solo apunta a los primeros cuatro elementos td (Fecha, Médico, Diagnóstico, Observaciones)
        Array.from(row.querySelectorAll('td.editable-cell')).slice(0, 4).forEach(cell => {
            const originalText = cell.textContent.trim();
            // Evita añadir múltiples inputs
            if (!cell.querySelector('input')) {
                cell.innerHTML = `<input type="text" value="${originalText}">`;
            }
        });

        // Muestra el botón de guardar, oculta el botón de editar
        row.querySelector('.btn-save').classList.remove('d-none');
        row.querySelector('.btn-edit').classList.add('d-none');
    }

    // Función para guardar la edición de la fila
    function saveRowEditing(row) {
        // Solo apunta a los primeros cuatro elementos td (Fecha, Médico, Diagnóstico, Observaciones)
        Array.from(row.querySelectorAll('td.editable-cell')).slice(0, 4).forEach(cell => {
            const input = cell.querySelector('input');
            if (input) {
                cell.textContent = input.value;
            }
        });

        // Muestra el botón de editar, oculta el botón de guardar
        row.querySelector('.btn-save').classList.add('d-none');
        row.querySelector('.btn-edit').classList.remove('d-none');
    }

    // Función para eliminar una fila
    function deleteRow(row) {
        if (confirm('¿Estás seguro de que quieres eliminar esta fila?')) {
            row.remove();
        }
    }
});