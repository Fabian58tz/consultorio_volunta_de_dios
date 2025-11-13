document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    // Función para alternar la clase 'collapsed' del sidebar
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
                const bsCollapse = new bootstrap.Collapse(submenu, { toggle: false });
                bsCollapse.hide();
            });
        }
    });

    // Lógica para inicializar el estado del sidebar y el toggler en función del tamaño de la pantalla
    function adjustLayout() {
        if (window.innerWidth <= 768) {
            // En móviles, el sidebar debe estar colapsado (por defecto)
            sidebar.classList.add('collapsed');
            // Ocultamos los contenidos del sidebar para que no haya desbordamiento
            document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header, #sidebar .nav-item:not(.has-submenu)').forEach(el => {
                el.style.opacity = '0';
                el.style.height = '0';
                el.style.padding = '0';
                el.style.margin = '0';
            });
            // Colapsar todos los submenús en vista móvil inicialmente
            document.querySelectorAll('.submenu').forEach(submenu => {
                const bsCollapse = new bootstrap.Collapse(submenu, { toggle: false });
                bsCollapse.hide();
            });

        } else {
            // En escritorio, el sidebar debe estar expandido (por defecto)
            sidebar.classList.remove('collapsed');
            // Restablecer la visibilidad de los elementos del sidebar
            document.querySelectorAll('#sidebar .nav-link span, #sidebar .menu-title, #sidebar .footer-quote, #sidebar .sidebar-header, #sidebar .nav-item').forEach(el => {
                el.style.opacity = '1';
                el.style.height = ''; 
                el.style.padding = '';
                el.style.margin = '';
            });
        }
    
    }
    
    // Cerrar otros submenús cuando se hace clic en un elemento del menú principal
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

    // Llamar a la función de ajuste de diseño al cargar y al cambiar el tamaño de la ventana
    adjustLayout();
    window.addEventListener('resize', adjustLayout);
});