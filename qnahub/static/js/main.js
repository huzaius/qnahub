document.addEventListener('DOMContentLoaded', function () {
    // Navbar Toggler
    const navToggler = document.getElementById('nav-toggler');
    const navCollapse = document.getElementById('navbarNav');

    if (navToggler && navCollapse) {
        navToggler.addEventListener('click', () => {
            navCollapse.classList.toggle('hidden');
        });
    }

    // User Dropdown
    const dropdownToggle = document.getElementById('navbarDropdown');
    const dropdownMenu = document.getElementById('dropdown-menu');

    if (dropdownToggle && dropdownMenu) {
        dropdownToggle.addEventListener('click', (event) => {
            event.preventDefault();
            dropdownMenu.classList.toggle('hidden');
        });

        // Optional: Close dropdown when clicking outside
        document.addEventListener('click', (event) => {
            if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.add('hidden');
            }
        });
    }

    // Sort Dropdown on index page
    const sortDropdownToggle = document.getElementById('sort-dropdown-toggle');
    const sortDropdownMenu = document.getElementById('sort-dropdown-menu');

    if (sortDropdownToggle && sortDropdownMenu) {
        sortDropdownToggle.addEventListener('click', (event) => {
            event.preventDefault();
            sortDropdownMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', (event) => {
            if (!sortDropdownToggle.contains(event.target) && !sortDropdownMenu.contains(event.target)) {
                sortDropdownMenu.classList.add('hidden');
            }
        });
    }
});