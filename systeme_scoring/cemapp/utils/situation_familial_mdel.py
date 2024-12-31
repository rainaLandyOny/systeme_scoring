import os
import pickle
import numpy as np

# Charger le modèle depuis le dossier `ml_models`
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../ml_models/family_model.pkl')

class FamilyModel:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)

    def predict(self, data):
        """
        Prédire un score basé sur les données fournies.
        :param data: Dictionnaire contenant les valeurs nécessaires.
        :return: Score prédictif.
        """
        input_data = np.array([[data['statut_familial'], data['nbr_dependant'], data['age']]])
        return self.model.predict(input_data)[0]
