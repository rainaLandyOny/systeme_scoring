import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
data = pd.read_csv("../data/data_situation_professionnelle.csv")

# Prétraitement des données
data['is_unemployed'] = (data['situation_professionnelle'] == 'sans_emploi').astype(int)
data.loc[data['situation_professionnelle'] == 'sans_emploi', 'duree_emploie'] = 0
data.loc[data['situation_professionnelle'] == 'sans_emploi', 'revenu_mensuel'] = 0
data.loc[data['situation_professionnelle'] == 'sans_emploi', 'secteur_activite'] = 'aucun'
data.loc[data['situation_professionnelle'] == 'sans_emploi', 'type_contrat'] = 'aucun'

# Encoder les variables catégoriques
ordinal_mapping_situation_professionnelle = [['sans_emploi', 'etudiant', 'retraite', 'employe', 'independant']]
ordinal_encoder_situation_professionnelle = OrdinalEncoder(categories=ordinal_mapping_situation_professionnelle)
data['situation_professionnelle'] = ordinal_encoder_situation_professionnelle.fit_transform(
    data[['situation_professionnelle']]
)

ordinal_mapping_type_contrat = [['aucun', 'stage', 'temporaire', 'freelance', 'cdi', 'cdd']]
ordinal_encoder_type_contrat = OrdinalEncoder(categories=ordinal_mapping_type_contrat)
data['type_contrat'] = ordinal_encoder_type_contrat.fit_transform(data[['type_contrat']])

label_encoder_secteur = LabelEncoder()
data['secteur_activite'] = label_encoder_secteur.fit_transform(data['secteur_activite'].astype(str))

# Séparer les features et la target
X = data[['situation_professionnelle', 'duree_emploie', 'revenu_mensuel', 'secteur_activite', 'type_contrat']]
y = data['score_professionnelle']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modèles à tester
models = {
    "Régression Linéaire": LinearRegression(),
    "Random Forest": RandomForestRegressor(random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "SVR": SVR(kernel='rbf'),
    "KNN": KNeighborsRegressor(n_neighbors=5)
}

model_results = {}

print("\n### Entraînement et évaluation des modèles ###")
for name, model in models.items():
    print(f"Entraînement du modèle : {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calcul des métriques
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    # Validation croisée
    cross_val_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    mean_cv_score = cross_val_scores.mean()
    std_cv_score = cross_val_scores.std()

    # Enregistrer les résultats
    model_results[name] = {
        "R²": r2,
        "MSE": mse,
        "R² (CV moyen)": mean_cv_score,
        "Écart-type (CV)": std_cv_score
    }

    print(
        f"{name} - R² : {r2:.2f}, MSE : {mse:.2f}, R² (CV moyen) : {mean_cv_score:.2f}, Écart-type (CV) : {std_cv_score:.2f}"
    )

# Sélection du meilleur modèle basé sur le R² moyen en validation croisée
best_model_name = max(model_results, key=lambda name: model_results[name]["R² (CV moyen)"])
best_model = models[best_model_name]

print(f"\n### Résumé des performances ###")
for name, results in model_results.items():
    print(
        f"{name} - R² : {results['R²']:.2f}, MSE : {results['MSE']:.2f}, R² (CV moyen) : {results['R² (CV moyen)']:.2f}"
    )

print(f"\nLe modèle sélectionné est : {best_model_name}")

# Comparaison des valeurs réelles et prédites pour le meilleur modèle
y_pred = best_model.predict(X_test)
plt.figure(figsize=(10, 6))
sns.regplot(x=y_test, y=y_pred, line_kws={'color': 'red'}, scatter_kws={'s': 10})
plt.xlabel('Valeurs réelles')
plt.ylabel('Valeurs prédites')
plt.title(f'Comparaison des valeurs réelles et prédites ({best_model_name})')
plt.show()

# Importance des caractéristiques (si disponible)
if hasattr(best_model, 'feature_importances_'):
    feature_importances = best_model.feature_importances_
    features = X.columns

    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importances, y=features)
    plt.title('Importance des caractéristiques')
    plt.xlabel('Importance')
    plt.ylabel('Caractéristiques')
    plt.show()
else:
    print(f"Le modèle {best_model_name} ne supporte pas l'importance des caractéristiques.")

# Sauvegarder le meilleur modèle et les encodeurs
best_model.metrics_ = model_results[best_model_name]  # Ajouter les métriques au modèle

joblib.dump(best_model, 'modele_situation_professionnelle.pkl')
joblib.dump(label_encoder_secteur, 'label_encoder_secteur.pkl')
joblib.dump(ordinal_encoder_situation_professionnelle, 'encoder_situation_professionnelle.pkl')
joblib.dump(ordinal_encoder_type_contrat, 'encoder_type_contrat.pkl')

print("Modèle et encodeurs sauvegardés avec succès !")

