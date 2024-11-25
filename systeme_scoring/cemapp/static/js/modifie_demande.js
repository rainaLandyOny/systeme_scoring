document.addEventListener("DOMContentLoaded", () => {
    const typeCreditSelect = document.getElementById("type_credit");
    const sousTypeCreditSelect = document.getElementById("sous_type_credit");
    const creditLimits = document.getElementById("credit_limits");

    // Fonction pour charger les sous-types de crédit
    const updateSousTypes = (typeCreditId) => {
        sousTypeCreditSelect.innerHTML = '<option value="" selected disabled>-- Sélectionner un sous-type de crédit --</option>';
        sousTypeCreditSelect.disabled = true;
        creditLimits.textContent = "";

        if (!typeCreditId) return;

        fetch(`/api/sous-types-credit/${typeCreditId}/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Erreur lors du chargement des sous-types de crédit.");
                }
                return response.json();
            })
            .then((data) => {
                if (data.error) {
                    creditLimits.textContent = data.error;
                } else {
                    sousTypeCreditSelect.disabled = false;
                    data.forEach((sousType) => {
                        const option = document.createElement("option");
                        option.value = sousType.id;
                        option.textContent = sousType.nom;

                        // Ajouter des données optionnelles si disponibles
                        if (sousType.montant_min) option.dataset.min = sousType.montant_min;
                        if (sousType.montant_max) option.dataset.max = sousType.montant_max;

                        sousTypeCreditSelect.appendChild(option);
                    });
                }
            })
            .catch((error) => {
                console.error(error);
                creditLimits.textContent = "Une erreur s'est produite lors du chargement des sous-types de crédit.";
            });
    };

    // Fonction pour afficher les limites du crédit
    const updateLimits = (sousTypeId) => {
        const selectedOption = sousTypeCreditSelect.querySelector(`option[value="${sousTypeId}"]`);
        if (!selectedOption) {
            creditLimits.textContent = "";
            return;
        }

        const montantMin = selectedOption.dataset.min || "N/A";
        const montantMax = selectedOption.dataset.max || "N/A";
        creditLimits.textContent = `Montant minimum: ${montantMin}, Montant maximum: ${montantMax}`;
    };

    // Événement pour charger les sous-types lorsque le type de crédit change
    typeCreditSelect.addEventListener("change", (event) => {
        const typeCreditId = event.target.value;
        updateSousTypes(typeCreditId);
    });

    // Événement pour mettre à jour les limites lorsque le sous-type change
    sousTypeCreditSelect.addEventListener("change", (event) => {
        const sousTypeId = event.target.value;
        updateLimits(sousTypeId);
    });

    // Chargement initial : si un type de crédit est déjà sélectionné, charger ses sous-types
    const initialTypeCreditId = typeCreditSelect.value;
    if (initialTypeCreditId) {
        updateSousTypes(initialTypeCreditId);
    }
});