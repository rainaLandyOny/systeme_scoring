// Récupérer les données JSON à partir du script
const scores = JSON.parse(document.getElementById('scores-data').textContent);

// Couleurs pour les catégories
const categoryColors = {
    "bon": "green",
    "moyen": "orange",
    "mauvais": "red"
};

// Conteneur des scores
const container = document.getElementById("scores-container");

// Génération des cercles pour chaque score
Object.keys(scores).forEach((key, index) => {
    const score = scores[key];
    const isNumber = typeof score === "number";

    // Créer un conteneur pour le score
    const scoreItem = document.createElement("div");
    scoreItem.classList.add("score-item");

    // Ajouter un canevas pour le graphique
    const canvas = document.createElement("canvas");
    canvas.id = `score-chart-${index}`;
    canvas.width = 150;
    canvas.height = 150;

    // Ajouter le titre du score
    const label = document.createElement("div");
    label.classList.add("score-label");
    label.textContent = `${key}: ${score}`;

    // Ajouter le canevas et le label au conteneur
    scoreItem.appendChild(canvas);
    scoreItem.appendChild(label);
    container.appendChild(scoreItem);

    // Configurer le cercle
    const ctx = canvas.getContext("2d");
    if (isNumber) {
        // Si le score est une note
        new Chart(ctx, {
            type: "doughnut",
            data: {
                datasets: [{
                    data: [score, 100 - score],
                    backgroundColor: ["#e50005", "#e3e4e6"],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                cutout: "80%",
                plugins: {
                    tooltip: { enabled: false },
                    legend: { display: false }
                }
            }
        });
    } else {
        // Si le score est une catégorie
        label.style.color = categoryColors[score.toLowerCase()] || "black";
    }
});