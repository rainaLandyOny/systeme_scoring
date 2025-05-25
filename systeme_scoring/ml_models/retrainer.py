import joblib
from .model_manager import ModelManager
from .data_pipeline import load_training_data, mark_data_as_used

def retrain_model(model_key, user):
    manager = ModelManager()
    
    # 1. Chargement des données
    X_train, X_test, y_train, y_test = load_training_data(model_key)
    
    # 2. Chargement du modèle et encodeur
    model = manager.load_model(model_key, user)
    encoder = manager.load_encoder(f"{model_key}_encoder")
    
    # 3. Préparation des données
    X_train_encoded = encoder.transform(X_train)
    X_test_encoded = encoder.transform(X_test)
    
    # 4. Réentraînement
    model.fit(X_train_encoded, y_train)
    
    # 5. Évaluation
    score = model.score(X_test_encoded, y_test)
    print(f"New accuracy for {model_key}: {score:.2f}")
    
    # 6. Sauvegarde
    joblib.dump(model, manager.models[model_key])
    manager.update_model_cache(user.id, model_key, model)
    
    # 7. Nettoyage
    mark_data_as_used(model_key)
    
    return model