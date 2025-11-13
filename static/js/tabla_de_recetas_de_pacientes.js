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

    // Función para ajustar el diseño en el cambio de tamaño de la ventana y en la carga inicial
    function adjustLayout() {
        if (window.innerWidth < 768) { // Si el ancho de la ventana es menor a 768px (típicamente móvil)
            sidebar.classList.add('collapsed'); // Colapsa la barra lateral
            // Oculta los elementos de texto y ajusta las propiedades para los elementos de navegación
            document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header, #sidebar .nav-item:not(.has-submenu)').forEach(el => {
                el.style.opacity = '0';
                el.style.height = '0';
                el.style.padding = '0';
                el.style.margin = '0';
            });
            // Oculta todos los submenús
            document.querySelectorAll('.submenu').forEach(submenu => {
                const bsCollapse = new bootstrap.Collapse(submenu, { toggle: false });
                bsCollapse.hide();
            });
        } else { // Si el ancho de la ventana es mayor o igual a 768px (típicamente escritorio)
            sidebar.classList.remove('collapsed'); // Descolapsa la barra lateral
            // Restaura la visibilidad y propiedades de los elementos de texto y navegación
            document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header, #sidebar .nav-item:not(.has-submenu)').forEach(el => {
                el.style.opacity = '1';
                el.style.height = ''; // Restaura a la altura por defecto
                el.style.padding = ''; // Restaura el padding por defecto
                el.style.margin = ''; // Restaura el margin por defecto
            });
        }
    }

    // Cierra otros submenús cuando se hace clic en un elemento del menú principal con submenú
    document.querySelectorAll('#sidebar .nav-item.has-submenu > .nav-link').forEach(link => {
        link.addEventListener('click', function(event) {
            const targetSubmenuId = this.dataset.bsTarget; // Obtiene el ID del submenú objetivo
            document.querySelectorAll('.submenu.show').forEach(openSubmenu => {
                // Si el submenú abierto no es el submenú objetivo, lo cierra
                if ('#' + openSubmenu.id !== targetSubmenuId) {
                    const bsCollapse = new bootstrap.Collapse(openSubmenu, { toggle: false });
                    bsCollapse.hide();
                }
            });
        });
    });

    // Llama a la función de ajuste de diseño en la carga inicial y en el evento de redimensionamiento de la ventana
    adjustLayout();
    window.addEventListener('resize', adjustLayout);


    // --- Funcionalidad de la Tabla ---

    // Función para agregar una nueva fila
    addRowButton.addEventListener('click', function() {
        const newRow = citasTableBody.insertRow(); // Inserta una nueva fila en el tbody
        newRow.setAttribute('data-id', nextId); // Asigna un ID de datos a la nueva fila
        newRow.innerHTML = `
            <td class="editable-cell"><input type="text" value="${nextId}"></td> 
            <td class="editable-cell"><input type="text" value=""></td> 
            <td class="editable-cell"><input type="text" value=""></td>
             <td class="editable-cell"><input type="text" value=""></td>
              <td class="editable-cell"><input type="text" value=""></td> 
              <td><span class="status-activo">Activo</span></td>
            <td class="action-buttons">
                <button class="btn-save"><i class="bi bi-save"></i></button>
                <button class="btn-edit d-none"><i class="bi bi-pencil"></i></button>
                <button class="btn-delete"><i class="bi bi-trash"></i></button>
            </td>
        `;
        enableRowEditing(newRow); // Habilita la edición para la fila recién añadida
        nextId++; // Incrementa el ID para la próxima fila
    });

    // Delegación de eventos para las acciones de la tabla (editar, guardar, eliminar)
    citasTableBody.addEventListener('click', function(event) {
        const target = event.target; // El elemento en el que se hizo clic
        const row = target.closest('tr'); // Obtiene el elemento de fila más cercano

        if (!row) return; // Si no se encuentra una fila, sale de la función

        if (target.closest('.btn-edit')) { // Si se hizo clic en el botón de editar
            enableRowEditing(row);
        } else if (target.closest('.btn-save')) { // Si se hizo clic en el botón de guardar
            saveRowEditing(row);
        } else if (target.closest('.btn-delete')) { // Si se hizo clic en el botón de eliminar
            deleteRow(row);
        }
    });

    // Función para habilitar la edición de una fila
    function enableRowEditing(row) {
        row.querySelectorAll('.editable-cell').forEach(cell => {
            // Evita agregar múltiples inputs si ya existe uno
            if (!cell.querySelector('input')) {
                const originalText = cell.textContent.trim(); // Obtiene el texto original de la celda
                cell.innerHTML = `<input type="text" value="${originalText}">`; // Reemplaza el texto con un input
            }
        });

        // Muestra el botón de guardar y oculta el botón de editar en la fila actual
        row.querySelector('.btn-save').classList.remove('d-none');
        row.querySelector('.btn-edit').classList.add('d-none');
    }

    // Función para guardar la edición de una fila
    function saveRowEditing(row) {
        row.querySelectorAll('.editable-cell').forEach(cell => {
            const input = cell.querySelector('input'); // Obtiene el input dentro de la celda
            if (input) {
                cell.textContent = input.value; // Actualiza el texto de la celda con el valor del input
            }
        });

        // Muestra el botón de editar y oculta el botón de guardar en la fila actual
        row.querySelector('.btn-save').classList.add('d-none');
        row.querySelector('.btn-edit').classList.remove('d-none');
    }

    // Función para eliminar una fila
    function deleteRow(row) {
        if (confirm('¿Estás seguro de que quieres eliminar esta fila?')) { // Pide confirmación al usuario
            row.remove(); // Elimina la fila del DOM
        }
    }
});