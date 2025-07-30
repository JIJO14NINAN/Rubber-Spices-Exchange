// My_Staff.js
function openModal() {
    document.getElementById('popup-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('popup-modal').style.display = 'none';
}

function editStaff() {
    // Implement edit staff functionality
    closeModal();
}

function viewProfile() {
    // Implement view full profile functionality
    closeModal();
}

function removeStaff() {
    // Implement remove staff functionality
    closeModal();
}

function openMenu(event, staffId) {
    // Close any open menus
    const allMenus = document.querySelectorAll('.popup-menu');
    allMenus.forEach(menu => {
        menu.style.display = 'none';
    });

    // Show the specific menu for the clicked staff member
    const menu = document.getElementById(`popup-menu-${staffId}`);
    menu.style.display = 'block';

    // Position the menu near the button
    const button = event.currentTarget;
    const rect = button.getBoundingClientRect();
    menu.style.top = `${rect.bottom + window.scrollY}px`; // Position below the button
    menu.style.left = `${rect.left}px`; // Align with the button
}

// Close the menu when clicking outside
window.onclick = function(event) {
    const allMenus = document.querySelectorAll('.popup-menu');
    const button = document.querySelectorAll('.action-button');

    // Check if the click was outside any menu and any button
    if (![...button].some(btn => btn.contains(event.target)) && ![...allMenus].some(menu => menu.contains(event.target))) {
        allMenus.forEach(menu => {
            menu.style.display = 'none';
        });
    }
};

// Optional: Close the menu when the escape key is pressed
window.onkeydown = function(event) {
    if (event.key === "Escape") {
        const allMenus = document.querySelectorAll('.popup-menu');
        allMenus.forEach(menu => {
            menu.style.display = 'none';
        });
    }
};
