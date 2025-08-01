
// Handle active state for sidebar navigation
document.addEventListener('DOMContentLoaded', function () {
    const sidebarLinks = document.querySelectorAll('#sidebar-nav .list-group-item-action');

    sidebarLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            // Prevent default link behavior
            event.preventDefault();

            // Remove 'active' class from all sidebar links
            sidebarLinks.forEach(l => l.classList.remove('active'));

            // Add 'active' class to the clicked link
            this.classList.add('active');
        });
    });
});
