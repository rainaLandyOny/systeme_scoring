import pandas as pd
import random

statut_juridique_choices = ['individuelle', 'sarl', 'sa', 'autres']
etat_locaux_choices = ["excellent", "bon", "moyen", "mediocre"]
systeme_gestion_choices = ["informatise", "manuel"]
niveau_concurrence_choices = ["faible", "moyen", "fort"]

def calculate_score(row):
    # Pondérations mises à jour
    pondérations = {
        "statut_juridique": {"individuelle": 20, "sarl": 20, "sa": 20, "autres": 20},
        "etat_locaux": {"excellent": 10, "bon": 8, "moyen": 5, "mediocre": 2},
        "systeme_gestion": {"informatise": 10, "manuel": 5},
        "niveau_concurrence": {"faible": 10, "moyen": 5, "fort": 2},
    }

    score = (
        pondérations["statut_juridique"][row["statut_juridique"]] +
        pondérations["etat_locaux"][row["etat_locaux"]] +
        pondérations["systeme_gestion"][row["systeme_gestion"]] +
        pondérations["niveau_concurrence"][row["niveau_concurrence"]]
    )

    if 10000000 <= row["revenu_moyen_mensuel"] <= 20000000:
        score += 15
    elif row["revenu_moyen_mensuel"] > 20000000:
        score += 10

    if row["rentabilite_estimee"] >= 0.7:
        score += 15
    elif 0.4 <= row["rentabilite_estimee"] < 0.7:
        score += 10

    return max(50, min(100, score))


def generate_random_data(num_samples):
    data = {
        "statut_juridique": random.choices(statut_juridique_choices, k=num_samples),
        "annee_creation": [random.randint(1970, 2023) for _ in range(num_samples)],
        "etat_locaux": random.choices(etat_locaux_choices, k=num_samples),
        "nombre_employes": [random.randint(1, 500) for _ in range(num_samples)],
        "revenu_moyen_mensuel": [round(random.uniform(5000000, 25000000), 2) for _ in range(num_samples)],
        "depenses_moyennes_mensuelles": [round(random.uniform(2500000, 20000000), 2) for _ in range(num_samples)],
        "rentabilite_estimee": [round(random.uniform(0.1, 0.9), 2) for _ in range(num_samples)],
        "systeme_gestion": random.choices(systeme_gestion_choices, k=num_samples),
        "nombre_clients_reguliers": [random.randint(1, 500) for _ in range(num_samples)],
        "niveau_concurrence": random.choices(niveau_concurrence_choices, k=num_samples)
    }

    df = pd.DataFrame(data)

    # Calculer les scores
    df["score_inspection"] = df.apply(calculate_score, axis=1)
    return df

num_samples = 100000
data = generate_random_data(num_samples)

file_path = "donnees_inspection_environnement_score.csv"
data.to_csv(file_path, index=False)
print(f"Les données ont été sauvegardées dans {file_path}")
print(data["score_inspection"].describe())

