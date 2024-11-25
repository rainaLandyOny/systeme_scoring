document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#searchInput');
    const clientsTableBody = document.querySelector('#clientsTableBody');

    searchInput.addEventListener('input', function() {
        const searchQuery = searchInput.value.trim();

        if (searchQuery.length > 0) {
            fetch(searchInput.dataset.url + '?search=' + encodeURIComponent(searchQuery))
                .then(response => response.json())
                .then(data => {
                    clientsTableBody.innerHTML = '';

                    if (data.clients && data.clients.length > 0) {
                        data.clients.forEach(client => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${client.nom}</td>
                                <td>${client.prenom}</td>
                                <td>${client.email || 'N/A'}</td>
                                <td>${client.telephone}</td>
                            `;
                            clientsTableBody.appendChild(row);
                        });
                    } else {
                        const noResultRow = document.createElement('tr');
                        noResultRow.innerHTML = '<td colspan="4">Aucun résultat trouvé</td>';
                        clientsTableBody.appendChild(noResultRow);
                    }
                })
                .catch(error => console.error('Erreur lors de la recherche:', error));
        } else {
            clientsTableBody.innerHTML = '';
        }
    });
});