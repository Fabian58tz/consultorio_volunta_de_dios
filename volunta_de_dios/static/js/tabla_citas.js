
document.addEventListener('DOMContentLoaded', function() {
    // Obteniendo referencias a los elementos del DOM
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const citasTableBody = document.querySelector('#citasTable tbody');
    const addRowButton = document.getElementById('addRow');
    let nextId = 2; // El ID comienza en 2 porque el ejemplo ya tiene un ID 1

    // Función para alternar la barra lateral (sidebar)
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed'); // Alterna la clase 'collapsed'
        const isCollapsed = sidebar.classList.contains('collapsed'); // Verifica si está colapsada

        // Ajusta la opacidad de los elementos de texto en la barra lateral
        document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header').forEach(el => {
            el.style.opacity = isCollapsed ? '0' : '1';
        });

        // Ajusta la altura, desbordamiento, margen y relleno de los elementos de navegación sin submenú
        document.querySelectorAll('#sidebar .nav-item:not(.has-submenu)').forEach(el => {
            el.style.height = isCollapsed ? '0' : '';
            el.style.overflow = isCollapsed ? 'hidden' : '';
            el.style.margin = isCollapsed ? '0' : '';
            el.style.padding = isCollapsed ? '0' : '';
        });

        // Si la barra lateral está colapsada, oculta cualquier submenú abierto
        if (isCollapsed) {
            document.querySelectorAll('.submenu.show').forEach(submenu => {
                const bsCollapse = new bootstrap.Collapse(submenu, { toggle: false });
                bsCollapse.hide();
            });
        }
    });

    // Function to adjust layout on resize and initial load
    function adjustLayout() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header, #sidebar .nav-item:not(.has-submenu)').forEach(el => {
                el.style.opacity = '0';
                el.style.height = '0';
                el.style.padding = '0';
                el.style.margin = '0';
            });
            document.querySelectorAll('.submenu').forEach(submenu => {
                const bsCollapse = new bootstrap.Collapse(submenu, { toggle: false });
                bsCollapse.hide();
            });
        } else {
            sidebar.classList.remove('collapsed');
            document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header, #sidebar .nav-item').forEach(el => {
                el.style.opacity = '1';
                el.style.height = '';
                el.style.padding = '';
                el.style.margin = '';
            });
        }
    }

    // Close other submenus when a main menu item is clicked
    document.querySelectorAll('#sidebar .nav-item.has-submenu > .nav-link').forEach(link => {
        link.addEventListener('click', function(event) {
            const targetSubmenuId = this.dataset.bsTarget;
            document.querySelectorAll('.submenu.show').forEach(openSubmenu => {
                if ('#' + openSubmenu.id !== targetSubmenuId) {
                    const bsCollapse = new bootstrap.Collapse(openSubmenu, { toggle: false });
                    bsCollapse.hide();
                }
            });
        });
    });

    // Call layout adjustment on load and resize
    adjustLayout();
    window.addEventListener('resize', adjustLayout);


    // --- Table Functionality ---

    // Function to add a new row
    addRowButton.addEventListener('click', function() {
        const newRow = citasTableBody.insertRow();
        newRow.setAttribute('data-id', nextId);
        newRow.innerHTML = `
            <td>${nextId}</td> <td class="editable-cell"><input type="text" value=""></td> <td class="editable-cell"><input type="text" value=""></td> <td class="editable-cell"><input type="text" value=""></td> <td class="editable-cell"><input type="text" value=""></td> <td class="editable-cell"><input type="text" value=""></td> <td><span class="status-activo">Activo</span></td>
            <td class="action-buttons">
                <button class="btn-save"><i class="bi bi-save"></i></button>
                <button class="btn-edit d-none"><i class="bi bi-pencil"></i></button>
                <button class="btn-delete"><i class="bi bi-trash"></i></button>
            </td>
        `;
        // Habilitar edición para las celdas de la nueva fila (excluyendo el ID)
        enableRowEditing(newRow);
        nextId++; // Incrementa el ID para la próxima fila
    });

    // Event delegation for table actions (edit, save, delete)
    citasTableBody.addEventListener('click', function(event) {
        const target = event.target;
        const row = target.closest('tr'); // Get the closest row element

        if (!row) return; // If no row is found, exit

        if (target.closest('.btn-edit')) {
            enableRowEditing(row);
        } else if (target.closest('.btn-save')) {
            saveRowEditing(row);
        } else if (target.closest('.btn-delete')) {
            deleteRow(row);
        }
    });

    // Function to enable editing for a row
    function enableRowEditing(row) {
        // Selecciona solo las celdas con la clase 'editable-cell' para habilitar la edición
        row.querySelectorAll('.editable-cell').forEach(cell => {
            const originalText = cell.textContent.trim();
            if (!cell.querySelector('input')) { // Prevent adding multiple inputs
                cell.innerHTML = `<input type="text" value="${originalText}">`;
            }
        });

        // Show save button, hide edit button
        row.querySelector('.btn-save').classList.remove('d-none');
        row.querySelector('.btn-edit').classList.add('d-none');
    }

    // Function to save row editing
    function saveRowEditing(row) {
        row.querySelectorAll('.editable-cell').forEach(cell => {
            const input = cell.querySelector('input');
            if (input) {
                cell.textContent = input.value;
            }
        });

        // Show edit button, hide save button
        row.querySelector('.btn-save').classList.add('d-none');
        row.querySelector('.btn-edit').classList.remove('d-none');
    }

    // Function to delete a row
    function deleteRow(row) {
        if (confirm('¿Estás seguro de que quieres eliminar esta fila?')) {
            row.remove();
        }
    }
});