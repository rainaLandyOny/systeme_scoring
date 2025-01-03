import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Charger les données
data = pd.read_csv("../data/data_capacite_remboursement.csv")

# Encoder la cible catégorique
encoder = LabelEncoder()
data["capacite_remboursement"] = encoder.fit_transform(data["capacite_remboursement"])

# Séparer les caractéristiques et la cible
X = data[["revenu_mensuel", "depenses_mensuelles", "dettes_existantes", "montant_credit", "taux_mensuel"]]
y = data["capacite_remboursement"]

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialisation des modèles
models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "Support Vector Classifier": SVC(kernel='rbf', probability=True),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

# Entraînement des modèles et calcul des métriques
model_results = {}
print("\nEntraînement des modèles :")
for name, model in models.items():
    print(f"-> {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calcul des métriques
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    # Enregistrer les résultats
    model_results[name] = {
        "Accuracy": acc,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "R²": r2,
        "MSE": mse
    }

    print(f"{name} - Accuracy: {acc:.2f}, Precision: {precision:.2f}, Recall: {recall:.2f}, F1 Score: {f1:.2f}, R²: {r2:.2f}, MSE: {mse:.2f}")

# Affichage des résultats sous forme de tableau
results_df = pd.DataFrame(model_results).T
print("\nRésultats des modèles :")
print(results_df)

# Sélection du meilleur modèle basé sur l'accuracy
best_model_name = max(model_results, key=lambda name: model_results[name]["Accuracy"])
best_model = models[best_model_name]
print(f"\nMeilleur modèle : {best_model_name}")

# Rapport de classification pour le meilleur modèle
y_pred_best = best_model.predict(X_test)
print("\nRapport de classification pour le meilleur modèle :")
print(classification_report(y_test, y_pred_best, target_names=encoder.classes_))

# Matrice de confusion
conf_matrix = confusion_matrix(y_test, y_pred_best)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="Blues", xticklabels=encoder.classes_, yticklabels=encoder.classes_)
plt.title(f"Matrice de confusion ({best_model_name})")
plt.xlabel("Prédictions")
plt.ylabel("Valeurs réelles")
plt.show()

# Importance des caractéristiques (pour Random Forest ou Gradient Boosting)
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

# Validation croisée
print("\nValidation croisée (5-fold) pour chaque modèle :")
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    print(f"{name} - Accuracy moyen (CV): {scores.mean():.2f}, Écart-type: {scores.std():.2f}")

# Sauvegarde du meilleur modèle avec les métriques et de l'encodeur
best_model.metrics_ = model_results[best_model_name]  # Ajouter les métriques au modèle
joblib.dump(best_model, "modele_capacite_remboursement.pkl")
joblib.dump(encoder, "encodeur_capacite_remboursement.pkl")
print("Meilleur modèle et encodeur sauvegardés avec succès.")
