document.addEventListener("DOMContentLoaded", function() {
    // Récupération des éléments HTML et des valeurs transmises par Django
    const container = document.querySelector(".container");
    const incomeRange = document.getElementById("monthlyIncome");
    const loanRange = document.getElementById("loanAmount");
    const termRange = document.getElementById("loanTerm");

    const incomeValue = document.getElementById("incomeValue");
    const loanValue = document.getElementById("loanValue");
    const termValue = document.getElementById("termValue");
    const monthlyPayment = document.getElementById("monthlyPayment");
    const errorMessage = document.createElement("p");

    // Ajout du message d'erreur dans la section de résultats
    errorMessage.style.color = "red";
    errorMessage.style.fontWeight = "bold";
    errorMessage.style.display = "none";
    document.querySelector(".simulation-result").appendChild(errorMessage);

    // Récupération des données depuis les attributs `data-*`
    const interestRate = parseFloat(container.getAttribute("data-interest-rate")) / 100;
    const minTerm = parseInt(container.getAttribute("data-min-term"));
    const maxTerm = parseInt(container.getAttribute("data-max-term"));
    const minAmount = parseFloat(container.getAttribute("data-min-amount"));
    const maxAmount = parseFloat(container.getAttribute("data-max-amount"));

    // Fonction de mise à jour de la simulation
    function updateSimulation() {
        const loanAmount = parseFloat(loanRange.value);
        const loanTerm = parseInt(termRange.value);
        const monthlyIncome = parseFloat(incomeRange.value);

        // Calcul de la mensualité
        const monthlyInterest = interestRate / 12;
        const monthlyPaymentAmount = (loanAmount * (monthlyInterest / (1 - Math.pow(1 + monthlyInterest, -loanTerm)))).toFixed(2);
        const maxAllowedPayment = (monthlyIncome * 0.4).toFixed(2);

        // Mise à jour des valeurs affichées dans les spans
        incomeValue.textContent = `${monthlyIncome.toLocaleString()} MGA`;
        loanValue.textContent = `${loanAmount.toLocaleString()} MGA`;
        termValue.textContent = `${loanTerm} Mois`;
        monthlyPayment.textContent = `${monthlyPaymentAmount} MGA / mois`;

        // Vérification si la mensualité dépasse 40% du revenu mensuel
        if (parseFloat(monthlyPaymentAmount) > parseFloat(maxAllowedPayment)) {
            // Calcul du montant maximum autorisé pour le prêt en fonction de la mensualité maximale
            const maxLoanAmount = ((maxAllowedPayment * (1 - Math.pow(1 + monthlyInterest, -loanTerm))) / monthlyInterest).toFixed(2);

            // Calcul du nombre de mois nécessaires pour respecter la limite de 40% du revenu
            let maxLoanTerm = maxTerm;
            for (let term = minTerm; term <= maxTerm; term++) {
                const paymentForTerm = (loanAmount * (monthlyInterest / (1 - Math.pow(1 + monthlyInterest, -term)))).toFixed(2);
                if (parseFloat(paymentForTerm) <= parseFloat(maxAllowedPayment)) {
                    maxLoanTerm = term;
                    break;
                }
            }

            // Ajustement du montant du prêt
            loanRange.value = maxLoanAmount; // Ajuste le montant du prêt à la valeur maximale possible
            loanValue.textContent = `${parseFloat(maxLoanAmount).toLocaleString()} MGA`;

            errorMessage.textContent = `Le montant de la mensualité dépasse 40% de votre revenu mensuel. Veuillez ajuster le montant emprunté.
                Montant maximum possible à emprunter : ${parseFloat(maxLoanAmount).toLocaleString()} MGA.
                Durée maximale pour ce prêt : ${maxLoanTerm} Mois.`;
            errorMessage.style.display = "block";
        } else {
            errorMessage.style.display = "none";
        }
    }

    // Écouteurs d'événements pour mettre à jour la simulation
    incomeRange.addEventListener("input", updateSimulation);
    loanRange.addEventListener("input", updateSimulation);
    termRange.addEventListener("input", updateSimulation);

    // Mise à jour initiale
    updateSimulation();
});