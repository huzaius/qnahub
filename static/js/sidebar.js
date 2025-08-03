
// Handle active state for sidebar navigation
document.addEventListener('DOMContentLoaded', function () {
    const sidebarLinks = document.querySelectorAll('#sidebar-nav .list-group-item-action');
    const currentPath = window.location.pathname;

    sidebarLinks.forEach(link => {
        // The link's href attribute contains the full URL. We need to compare pathnames.
        const linkPath = new URL(link.href).pathname;

        if (linkPath === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
    
});

