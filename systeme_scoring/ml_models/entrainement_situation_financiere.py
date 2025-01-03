import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVR

# Charger le fichier CSV contenant les données
df = pd.read_csv('../data/data_situation_financiere.csv')

# Affichage des premières lignes pour vérifier les données
print("Aperçu des données :")
print(df.head())

# Prétraitement des données

# 1. Encoder la colonne 'situation_bancaire' car elle est catégorique
ordinal_mapping = [['excellent', 'bon', 'moyen', 'faible', 'mauvais']]
ordinal_encoder = OrdinalEncoder(categories=ordinal_mapping)
df['situation_bancaire'] = ordinal_encoder.fit_transform(df[['situation_bancaire']])

# 2. Séparation des caractéristiques (features) et de la cible (label)
X = df.drop(columns=['note_financiere'])  # Caractéristiques
y = df['note_financiere']  # Cible

# 3. Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Normalisation des données (mise à l'échelle)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialisation des modèles
models = {
    "Régression Linéaire": LinearRegression(),
    "Random Forest": RandomForestRegressor(random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "SVR": SVR(kernel='rbf'),
    "KNN": KNeighborsRegressor(n_neighbors=5)
}

# Test des modèles
model_results = {}
print("\nEntraînement des modèles :")
for name, model in models.items():
    print(f"-> {name}")
    model.fit(X_train_scaled, y_train)  # Utilisation des données normalisées
    y_pred = model.predict(X_test_scaled)  # Utilisation des données normalisées

    # Calcul des métriques
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    model_results[name] = {
        "R²": r2,
        "MSE": mse,
        "MAE": mae
    }

    print(f"{name} - R² : {r2:.2f}, MSE : {mse:.2f}, MAE : {mae:.2f}")

# Affichage des résultats sous forme de tableau
results_df = pd.DataFrame(model_results).T  # Transpose pour faciliter la lecture
print("\nRésultats des modèles :")
print(results_df)

# Sélection du meilleur modèle basé sur R²
best_model_name = max(model_results, key=lambda name: model_results[name]["R²"])
best_model = models[best_model_name]
print(f"\nMeilleur modèle : {best_model_name}")

# Comparaison des valeurs réelles et prédites pour le meilleur modèle
y_pred = best_model.predict(X_test_scaled)  # Prédictions finales
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
    plt.title('Importance des caractéristiques pour prédire la note financière')
    plt.xlabel('Importance')
    plt.ylabel('Caractéristiques')
    plt.show()
else:
    print(f"Le modèle {best_model_name} ne supporte pas l'importance des caractéristiques.")

# Validation croisée (optionnelle)
print("\nValidation croisée (5-fold) pour chaque modèle :")
for name, model in models.items():
    scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')  # R² par validation croisée
    print(f"{name} - R² moyen (CV): {scores.mean():.2f}, Écart-type: {scores.std():.2f}")

# Sauvegarder le modèle
best_model.metrics_ = model_results[best_model_name]  # Ajouter les métriques au modèle
model_filepath = "modele_situation_financiere.pkl"
joblib.dump(best_model, model_filepath)
encoders_file = "encoders_situation_bancaire.pkl"
joblib.dump(ordinal_encoder, encoders_file)

print(f"Modèle sauvegardé à {model_filepath}")
print(f"Encoder sauvegardé à {encoders_file}")
