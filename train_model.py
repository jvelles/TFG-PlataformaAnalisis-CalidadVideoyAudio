import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

# Crear dataset simulado (usa datos reales si tienes un conjunto de datos)
data = {
    'resolucion': [480, 720, 1080, 480, 720, 1080, 1080, 720, 480, 720],
    'bitrate': [500, 1500, 3000, 400, 800, 2500, 3500, 1200, 600, 900],
    'framerate': [15, 30, 60, 15, 24, 30, 60, 30, 24, 15],
    'calidad': ['baja', 'media', 'alta', 'baja', 'media', 'alta', 'alta', 'media', 'baja', 'media']
}
df = pd.DataFrame(data)

# Separar características y etiquetas
X = df[['resolucion', 'bitrate', 'framerate']]
y = df['calidad']

# Dividir el dataset en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
print(f"Precisión del modelo: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Guardar el modelo entrenado
joblib.dump(model, 'model_quality_predictor.pkl')
print("Modelo guardado como model_quality_predictor.pkl")
