import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OrdinalEncoder
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Chargement des données
data = pd.read_csv('../data/data_situation_familiale.csv', encoding='latin1')

# Calcul de l'âge à partir de la date de naissance
def calculate_age(birth_date):
    today = pd.Timestamp.today()
    birth_date = pd.to_datetime(birth_date, format='%Y-%m-%d', errors='coerce')
    age = today.year - birth_date.dt.year - (
        (today.month < birth_date.dt.month) | 
        ((today.month == birth_date.dt.month) & (today.day < birth_date.dt.day))
    )
    return age

data['age'] = calculate_age(data['date_naissance'])
data = data.drop(columns=['date_naissance'])

# Encodage ordinal pour 'statut_familial'
ordinal_mapping = [['Divorcé(e)', 'Célibataire', 'Veuf/Veuve', 'Marié(e)']]
ordinal_encoder = OrdinalEncoder(categories=ordinal_mapping)
data['statut_familial'] = ordinal_encoder.fit_transform(data[['statut_familial']])

# Préparation des données
X = data.drop(columns=['score_familial'])
y = data['score_familial']

# Division en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialisation des modèles
models = {
    "Régression Linéaire": LinearRegression(),
    "Random Forest": RandomForestRegressor(random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "SVR": SVR(kernel='rbf'),
    "KNN": KNeighborsRegressor(n_neighbors=5)
}

# Entraînement des modèles et calcul des métriques
model_results = {}
print("\nEntraînement des modèles :")
for name, model in models.items():
    print(f"-> {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calcul des métriques
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)  # Calcul du RMSE
    mae = np.mean(np.abs(y_test - y_pred))  # Mean Absolute Error

    # Validation croisée (5-fold)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()

    # Enregistrer les résultats
    model_results[name] = {
        "R²": r2,
        "MSE": mse,
        "RMSE": rmse,
        "MAE": mae,
        "CV Mean R²": cv_mean,
        "CV Std R²": cv_std
    }

    print(f"{name} - R²: {r2:.2f}, MSE: {mse:.2f}, RMSE: {rmse:.2f}, MAE: {mae:.2f}, CV Mean R²: {cv_mean:.2f}, CV Std R²: {cv_std:.2f}")

# Affichage des résultats sous forme de tableau
results_df = pd.DataFrame(model_results).T
print("\n### Résultats des modèles ###")
print(results_df)

# Sélection du meilleur modèle basé sur R²
best_model_name = max(model_results, key=lambda name: model_results[name]["R²"])
best_model = models[best_model_name]
print(f"\nMeilleur modèle : {best_model_name}")

# Comparaison des valeurs réelles et prédites pour le meilleur modèle
y_pred_best = best_model.predict(X_test)
plt.figure(figsize=(10, 6))
sns.regplot(x=y_test, y=y_pred_best, line_kws={'color': 'red'}, scatter_kws={'s': 10})
plt.xlabel('Valeurs réelles')
plt.ylabel('Valeurs prédites')
plt.title(f'Comparaison des valeurs réelles et prédites ({best_model_name})')
plt.show()

# Importance des caractéristiques (si applicable)
if hasattr(best_model, 'feature_importances_'):
    feature_importances = best_model.feature_importances_
    features = X.columns
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importances, y=features)
    plt.title('Importance des caractéristiques pour prédire le score familial')
    plt.xlabel('Importance')
    plt.ylabel('Caractéristiques')
    plt.show()
else:
    print(f"Le modèle {best_model_name} ne supporte pas l'importance des caractéristiques.")

# Sauvegarde du meilleur modèle et des encodages
best_model.metrics_ = model_results[best_model_name]  # Ajouter les métriques au modèle
model_file = "modele_situation_familiale.pkl"
joblib.dump(best_model, model_file)

encoders_file = "encoders_situation_familiale.pkl"
joblib.dump(ordinal_encoder, encoders_file)

print(f"\nModèle sauvegardé sous le fichier : {model_file}")
print(f"Encodages sauvegardés sous le fichier : {encoders_file}")
