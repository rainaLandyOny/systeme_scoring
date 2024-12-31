document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#searchInput');
    const clientsTableBody = document.querySelector('#clientList');

    searchInput.addEventListener('input', function() {
        const searchQuery = searchInput.value.trim();

        if (searchQuery.length > 0) {
            fetch(searchInput.dataset.url + '?search=' + encodeURIComponent(searchQuery), {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erreur réseau ou serveur');
                    }
                    return response.json();
                })
                .then(data => {
                    clientsTableBody.innerHTML = '';

                    if (data.clients && data.clients.length > 0) {
                        data.clients.forEach(client => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${client.nom}</td>
                                <td>${client.prenom}</td>
                                <td>${client.date_naissance}</td>
                                <td>${client.n_cin}</td>
                                <td>${client.email || 'N/A'}</td>
                            `;
                            row.style.cursor = 'pointer';
                            row.addEventListener('click', () => {
                                window.location.href = `/gestionnairedemande/modifie_client/${client.id}/`;
                            });
                            clientsTableBody.appendChild(row);
                        });
                    } else {
                        const noResultRow = document.createElement('tr');
                        noResultRow.innerHTML = '<td colspan="5">Aucun résultat trouvé</td>';
                        clientsTableBody.appendChild(noResultRow);
                    }
                })
                .catch(error => console.error('Erreur lors de la recherche:', error));
        } else {
            clientsTableBody.innerHTML = '';
        }
    });
});