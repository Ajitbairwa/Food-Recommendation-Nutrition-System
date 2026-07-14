import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("Food_Nutrition_Dataset.csv")

df["iron"] = df["iron"].fillna(df["iron"].median())

df["vitamin_c"] = df["vitamin_c"].fillna(df["vitamin_c"].median())

recommendation_features = [
    "calories",
    "protein",
    "carbs",
    "fat",
    "iron",
    "vitamin_c"
]

features = df[recommendation_features]

scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)

similarity = cosine_similarity(scaled_features)
