document.addEventListener("DOMContentLoaded", () => {
    const typeField = document.getElementById("type");
    const container = document.getElementById("fields-container");

    typeField.addEventListener("change", () => {
        const type = typeField.value;
        container.innerHTML = ""; // Réinitialiser les champs

        // Ajouter les champs en fonction du type de document sélectionné
        if (["recapitulatif", "echeancier", "avis_remboursement", "attestation_cloture"].includes(type)) {
            container.innerHTML += `
                <div class="form-group">
                    <label for="demande_id">ID de la Demande :</label>
                    <input type="text" name="demande_id" id="demande_id" class="form-control" required>
                </div>
            `;
        } else if (["certificat_solvabilite", "historique_paiements"].includes(type)) {
            container.innerHTML += `
                <div class="form-group">
                    <label for="client_id">ID du Client :</label>
                    <input type="text" name="client_id" id="client_id" class="form-control" required>
                </div>
            `;
        } else if (type === "declaration_fiscale") {
            container.innerHTML += `
                <div class="form-group">
                    <label for="client_id">ID du Client :</label>
                    <input type="text" name="client_id" id="client_id" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="date_debut">Date Début :</label>
                    <input type="date" name="date_debut" id="date_debut" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="date_fin">Date Fin :</label>
                    <input type="date" name="date_fin" id="date_fin" class="form-control" required>
                </div>
            `;
        }
    });
});