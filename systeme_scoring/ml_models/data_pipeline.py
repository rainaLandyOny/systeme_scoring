import pandas as pd
from cemapp.models_classes.training_data import TrainingData

def load_training_data(model_key):
    """Charge les données depuis PostgreSQL"""
    session = TrainingData.get_session()
    try:
        query = session.query(
            TrainingData.features, 
            TrainingData.true_score
        ).filter(
            TrainingData.model_key == model_key,
            TrainingData.is_used == False
        )
        
        df = pd.read_sql(query.statement, session.bind)
        return pd.json_normalize(df['features']), df['true_score']
    finally:
        session.close()

def mark_data_as_used(model_key):
    """Marque les données comme utilisées"""
    session = TrainingData.get_session()
    try:
        session.query(TrainingData).filter(
            TrainingData.model_key == model_key,
            TrainingData.is_used == False
        ).update({'is_used': True})
        session.commit()
    finally:
        session.close()