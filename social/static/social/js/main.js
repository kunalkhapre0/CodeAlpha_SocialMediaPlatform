document.addEventListener('DOMContentLoaded', () => {
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {
        // Add a click event on each of them
        $navbarBurgers.forEach( el => {
            el.addEventListener('click', () => {
                // Get the target from the "data-target" attribute (if you had one, not strictly needed for this simple toggle)
                // const target = el.dataset.target;
                // const $target = document.getElementById(target);

                // For this example, we'll toggle the burger itself and the menu
                const $targetMenu = document.getElementById('navbarMenu'); // Get the menu by ID

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                if ($targetMenu) {
                    $targetMenu.classList.toggle('is-active');
                }
            });
        });
    }
});