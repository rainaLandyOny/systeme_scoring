document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('clientModal');
    const openModalButton = document.getElementById('addClientButton');
    const closeModal = document.querySelector('.close');

    openModalButton.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});