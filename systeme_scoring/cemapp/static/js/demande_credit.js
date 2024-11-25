let montantMin = 0,
    montantMax = 0,
    tauxInteret = 0;

// Recherche dynamique pour les clients
document.getElementById('clientSearch').addEventListener('input', function() {
    const searchQuery = this.value.toLowerCase();
    const clientOptions = document.getElementById('client').options;

    for (let i = 0; i < clientOptions.length; i++) {
        const option = clientOptions[i];
        const text = option.textContent.toLowerCase();
        option.style.display = text.includes(searchQuery) ? '' : 'none';
    }
});

// Charger les sous-types de crédit
document.getElementById('type_credit').addEventListener('change', function() {
    const typeCreditId = this.value;
    const sousTypeSelect = document.getElementById('sous_type_credit');

    // Réinitialiser le champ des sous-types
    sousTypeSelect.innerHTML = '<option value="" selected disabled>Chargement...</option>';
    sousTypeSelect.disabled = true;

    fetch(`/api/sous-types-credit/${typeCreditId}/`)
        .then(response => response.json())
        .then(data => {
            sousTypeSelect.innerHTML = '<option value="" selected disabled>-- Sélectionner un sous-type de crédit --</option>';
            data.forEach(sousType => {
                sousTypeSelect.innerHTML += `<option value="${sousType.id}" data-min="${sousType.montant_min}" data-max="${sousType.montant_max}" data-taux="${sousType.taux_interet}">${sousType.nom}</option>`;
            });
            sousTypeSelect.disabled = false;
        });
});

// Mettre à jour les limites de montant
document.getElementById('sous_type_credit').addEventListener('change', function() {
    const selectedOption = this.options[this.selectedIndex];
    montantMin = parseFloat(selectedOption.dataset.min);
    montantMax = parseFloat(selectedOption.dataset.max);
    tauxInteret = parseFloat(selectedOption.dataset.taux);
    document.getElementById('credit_limits').textContent = `Montant min: ${montantMin} - Montant max: ${montantMax}`;
});

// Validation du montant total uniquement
document.getElementById('montant_total').addEventListener('input', function() {
    const montantTotal = parseFloat(this.value);

    if (montantTotal < montantMin || montantTotal > montantMax) {
        this.setCustomValidity(`Le montant doit être entre ${montantMin} et ${montantMax}`);
    } else {
        this.setCustomValidity('');
    }
});

// Suppression de la logique de calcul pour le montant mensuel
document.getElementById('duree').addEventListener('input', function() {
    // L'entrée de durée est laissée intacte pour envoyer les données au backend si nécessaire.
});