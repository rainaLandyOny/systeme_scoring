import joblib
import os
from threading import Lock
from model_manager import ModelManager

from sklearn.metrics import classification_report

# Verrou pour gérer un accès concurrent
model_lock = Lock()

# Cache utilisateur spécifique
user_model_cache = {}


class ModelManager:
    def __init__(self):
        # Chemins des fichiers des modèles
        self.models = {
            "situation_familiale": "ml_models/modele_situation_familiale.pkl",
            "situation_professionnelle": "ml_models/modele_situation_professionnelle.pkl",
            "situation_financiere": "ml_models/modele_situation_financiere.pkl",
            "capacite_remboursement": "ml_models/modele_capacite_remboursement.pkl",
            "inspection_environnement": "ml_models/modele_inspection_environnement.pkl"
        }

        # Chemins des fichiers des encodeurs
        self.encoders = {
            "situation_familiale": "ml_models/encoders_situation_familiale.pkl",
            "secteur_activite": "ml_models/label_situation_professionnelle_encoders.pkl",
            "type_contrat": "ml_models/encoder_type_contrat.pkl",
            "situation_bancaire": "ml_models/encoders_situation_bancaire.pkl",
            "capacite_remboursement": "ml_models/encodeur_capacite_remboursement.pkl",
            "situation_professionnelle": "ml_models/encoder_situation_professionnelle.pkl",
            "statut_juridique": "ml_models/encoder_statut_juridique.pkl",
            "inspection_environnement": "ml_models/ordinal_encoder_inspection_environnement.pkl",
        }

    def load_model(self, model_key, user):
        """
        Charge un modèle spécifique au cache utilisateur connecté.

        Args:
            model_key (str): La clé du modèle.
            user (CustomUser): L'utilisateur connecté.

        Returns:
            object: Le modèle chargé.
        """
        user_id = user.id

        with model_lock:
            # Vérifier le cache utilisateur
            if user_id in user_model_cache and model_key in user_model_cache[user_id]:
                return user_model_cache[user_id][model_key]

            # Charger le modèle depuis le disque
            if model_key in self.models:
                model_path = self.models[model_key]
                if os.path.exists(model_path):
                    model = joblib.load(model_path)

                    # Ajouter au cache utilisateur
                    if user_id not in user_model_cache:
                        user_model_cache[user_id] = {}
                    user_model_cache[user_id][model_key] = model

                    return model
                else:
                    raise FileNotFoundError(f"Model file not found: {model_path}")
            else:
                raise ValueError(f"Invalid model key: {model_key}")

    def load_encoder(self, encoder_key):
        """
        Charge un encodeur à partir du fichier.

        Args:
            encoder_key (str): La clé de l'encodeur à charger.

        Returns:
            object: L'encodeur chargé.

        Raises:
            FileNotFoundError: Si le fichier de l'encodeur est introuvable.
            ValueError: Si la clé de l'encodeur est invalide.
        """
        if encoder_key in self.encoders:
            encoder_path = self.encoders[encoder_key]
            if os.path.exists(encoder_path):
                return joblib.load(encoder_path)
            else:
                raise FileNotFoundError(f"Encoder file not found: {encoder_path}")
        else:
            raise ValueError(f"Invalid encoder key: {encoder_key}")

    def update_model_cache(self, user_id, model_key, updated_model):
        """
        Met à jour le cache utilisateur avec un modèle modifié.

        Args:
            user_id (str): L'ID utilisateur.
            model_key (str): La clé du modèle à mettre à jour.
            updated_model (object): Le modèle mis à jour.

        Raises:
            ValueError: Si la clé du modèle est invalide.
        """
        with model_lock:
            if model_key not in self.models:
                raise ValueError(f"Invalid model key: {model_key}")

            if user_id not in user_model_cache:
                user_model_cache[user_id] = {}
            user_model_cache[user_id][model_key] = updated_model

    def clear_user_cache(self, user_id):
        """
        Supprime le cache pour un utilisateur spécifique.

        Args:
            user_id (str): L'ID utilisateur.
        """
        with model_lock:
            if user_id in user_model_cache:
                del user_model_cache[user_id]

    def clear_all_caches(self):
        """
        Supprime tous les caches utilisateurs.
        """
        with model_lock:
            user_model_cache.clear()
            
    def get_model_metrics(self, model_key, X_test, y_test):
        """
        Calcule les métriques d'un modèle sur un jeu de test.

        Args:
            model_key (str): La clé du modèle.
            X_test (array-like): Les caractéristiques du jeu de test.
            y_test (array-like): Les vraies étiquettes du jeu de test.

        Returns:
            dict: Les métriques sous forme de dictionnaire.
        """
        with model_lock:
            if model_key not in self.models:
                raise ValueError(f"Invalid model key: {model_key}")

            model = joblib.load(self.models[model_key])
            y_pred = model.predict(X_test)

            # Générer les métriques
            metrics = classification_report(y_test, y_pred, output_dict=True)
            return metrics
        
    def train_model_situation_familiale():
        model = ModelManager.load_model()
        pass
    
    def train_model_situation_professionnelle():
        pass
    
    def train_model_situation_financiere():
        pass
    
    def train_model_capacite_remboursement():
        pass
    
    def train_model_inspection_environnement():
        pass
