from ml_models.alchemy_db import Base, SessionLocal
from sqlalchemy import Column, Integer, String, JSON, Float, Boolean, DateTime
from datetime import datetime

class TrainingData(Base):
    __tablename__ = 'training_data'

    id = Column(Integer, primary_key=True)
    model_key = Column(String(50), nullable=False)  # 'situation_familiale', etc.
    features = Column(JSON, nullable=False)        # Dictionnaire des features
    true_score = Column(Float, nullable=False)     # Score corrigé
    created_at = Column(DateTime, default=datetime.utcnow)
    is_used = Column(Boolean, default=False)

    @classmethod
    def get_session(cls):
        return SessionLocal()

# Crée les tables au besoin
Base.metadata.create_all(bind=SessionLocal().bind)