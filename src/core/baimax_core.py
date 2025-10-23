"""
🧽🤖 bAImax - Sistema Híbrido de Análisis Inteligente de Salud Pública
=====================================================================

Desarrollado para SENASOFT 2025
Autor: Proyecto bAImax
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
import pickle
import warnings
warnings.filterwarnings('ignore')

class bAImaxClassifier:
    """
    🧠 Clasificador inteligente de gravedad de problemas de salud
    
    Utiliza TF-IDF + Machine Learning para clasificar automáticamente
    la gravedad de reportes ciudadanos como GRAVE o MODERADO
    """
    
    def __init__(self, modelo_tipo='logistic'):
        self.modelo_tipo = modelo_tipo
        self.pipeline = None
        self.metricas = {}
        self.esta_entrenado = False
        
    def entrenar(self, dataset_path='src/data/dataset_normalizado.csv'):
        """
        🎯 Entrena el modelo con nuestro dataset optimizado
        """
        print("🧽 bAImax iniciando entrenamiento...")
        
        # Cargar dataset
        df = pd.read_csv(dataset_path)
        print(f"📊 Dataset cargado: {len(df)} registros")
        
        # Preparar datos
        X = df['Comentario'].fillna('')
        y = df['Nivel_gravedad']
        
        print(f"🎯 Distribución de clases:")
        print(f"   GRAVE: {sum(y == 'GRAVE')} registros")
        print(f"   MODERADO: {sum(y == 'MODERADO')} registros")
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Crear pipeline según tipo de modelo
        if self.modelo_tipo == 'logistic':
            modelo = LogisticRegression(random_state=42, max_iter=1000)
        else:
            modelo = RandomForestClassifier(random_state=42, n_estimators=100)
            
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),
                stop_words=None  # Mantenemos palabras en español
            )),
            ('modelo', modelo)
        ])
        
        # Entrenar
        print("🤖 Entrenando modelo...")
        self.pipeline.fit(X_train, y_train)
        
        # Evaluar
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(self.pipeline, X, y, cv=5, scoring='accuracy')
        
        self.metricas = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'clasificacion': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
        
        self.esta_entrenado = True
        
        print(f"✅ Modelo entrenado exitosamente!")
        print(f"   Precisión: {accuracy:.3f}")
        print(f"   CV Score: {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")
        
        return self
    
    def predecir(self, comentario):
        """
        🔮 Predice la gravedad de un comentario
        """
        if not self.esta_entrenado:
            raise ValueError("El modelo debe ser entrenado primero")
            
        # Predicción
        prediccion = self.pipeline.predict([comentario])[0]
        probabilidades = self.pipeline.predict_proba([comentario])[0]
        
        # Mapear probabilidades a clases
        clases = self.pipeline.classes_
        prob_dict = dict(zip(clases, probabilidades))
        
        return {
            'gravedad': prediccion,
            'confianza': max(probabilidades),
            'probabilidades': prob_dict
        }
    
    def predecir_lote(self, comentarios):
        """
        📦 Predice múltiples comentarios a la vez
        """
        if not self.esta_entrenado:
            raise ValueError("El modelo debe ser entrenado primero")
            
        predicciones = self.pipeline.predict(comentarios)
        probabilidades = self.pipeline.predict_proba(comentarios)
        
        resultados = []
        for i, comentario in enumerate(comentarios):
            prob_dict = dict(zip(self.pipeline.classes_, probabilidades[i]))
            resultados.append({
                'comentario': comentario,
                'gravedad': predicciones[i],
                'confianza': max(probabilidades[i]),
                'probabilidades': prob_dict
            })
            
        return resultados
    
    def obtener_metricas(self):
        """
        📊 Retorna métricas de evaluación del modelo
        """
        if not self.esta_entrenado:
            return "Modelo no entrenado"
            
        return self.metricas
    
    def guardar_modelo(self, path='src/data/baimax_modelo.pkl'):
        """
        💾 Guarda el modelo entrenado
        """
        if not self.esta_entrenado:
            raise ValueError("El modelo debe ser entrenado primero")
            
        with open(path, 'wb') as f:
            pickle.dump(self.pipeline, f)
        print(f"💾 Modelo guardado en: {path}")
    
    def cargar_modelo(self, path='src/data/baimax_modelo.pkl'):
        """
        📁 Carga un modelo previamente entrenado
        """
        try:
            with open(path, 'rb') as f:
                self.pipeline = pickle.load(f)
            self.esta_entrenado = True
            print(f"📁 Modelo cargado desde: {path}")
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {path}")

class bAImaxAnalyzer:
    """
    📊 Analizador de datos para generar insights y estadísticas
    """
    
    def __init__(self, dataset_path='src/data/dataset_normalizado.csv'):
        self.df = pd.read_csv(dataset_path)
        print(f"📊 Dataset cargado para análisis: {len(self.df)} registros")
    
    def estadisticas_generales(self):
        """
        📈 Genera estadísticas generales del dataset
        """
        stats = {
            'total_registros': len(self.df),
            'problemas_unicos': self.df['Comentario'].nunique(),
            'ciudades': self.df['Ciudad'].nunique(),
            'personas_unicas': self.df['Nombre'].nunique(),
            'distribucion_gravedad': self.df['Nivel_gravedad'].value_counts().to_dict(),
            'distribucion_ciudades': self.df['Ciudad'].value_counts().head(10).to_dict(),
            'distribucion_temporal': self.df['Fecha del reporte'].str[:4].value_counts().to_dict(),
            'zona_rural_urbana': {
                'Rural': (self.df['Zona rural'] == 1).sum(),
                'Urbana': (self.df['Zona rural'] == 0).sum()
            }
        }
        return stats
    
    def top_problemas(self, top_n=10):
        """
        🔝 Obtiene los problemas más reportados
        """
        problemas = self.df.groupby('Comentario').agg({
            'Frecuencia_similar': 'first',
            'Personas_afectadas': 'first',
            'Nivel_gravedad': 'first',
            'Ciudad': lambda x: list(x.unique())
        }).sort_values('Frecuencia_similar', ascending=False).head(top_n)
        
        return problemas.to_dict('index')
    
    def analisis_por_ciudad(self):
        """
        🏙️ Análisis detallado por ciudad
        """
        ciudad_stats = self.df.groupby('Ciudad').agg({
            'Comentario': 'count',
            'Nivel_gravedad': lambda x: (x == 'GRAVE').sum(),
            'Zona rural': 'mean',
            'Acceso a internet': 'mean',
            'Atención previa del gobierno': 'mean'
        }).round(2)
        
        ciudad_stats.columns = ['Total_reportes', 'Reportes_graves', 'Pct_rural', 'Pct_internet', 'Pct_atencion_previa']
        return ciudad_stats.to_dict('index')

# Función de demostración
def demo_baimax():
    """
    🎭 Demostración del sistema bAImax
    """
    print("🧽🤖 DEMO DEL SISTEMA bAImax")
    print("=" * 50)
    
    # Crear y entrenar clasificador
    clasificador = bAImaxClassifier(modelo_tipo='logistic')
    clasificador.entrenar()
    
    # Ejemplos de predicción
    ejemplos = [
        "faltan médicos en el centro de salud",
        "falta agua potable en varias casas",
        "las calles están muy oscuras y peligrosas",
        "necesitamos más bibliotecas públicas"
    ]
    
    print("\n🔮 Predicciones de ejemplo:")
    print("-" * 30)
    
    for ejemplo in ejemplos:
        resultado = clasificador.predecir(ejemplo)
        print(f"📝 '{ejemplo}'")
        print(f"   🎯 Gravedad: {resultado['gravedad']}")
        print(f"   🎪 Confianza: {resultado['confianza']:.3f}")
        print()
    
    # Métricas del modelo
    print("📊 Métricas del modelo:")
    metricas = clasificador.obtener_metricas()
    print(f"   Precisión: {metricas['accuracy']:.3f}")
    print(f"   CV Score: {metricas['cv_mean']:.3f}")
    
    # Análisis estadístico
    print("\n📈 Análisis estadístico:")
    analyzer = bAImaxAnalyzer()
    stats = analyzer.estadisticas_generales()
    print(f"   Total registros: {stats['total_registros']}")
    print(f"   Problemas únicos: {stats['problemas_unicos']}")
    print(f"   Ciudades: {stats['ciudades']}")
    
    # Guardar modelo
    clasificador.guardar_modelo()
    
    print("\n✨ ¡Demo completada exitosamente! ✨")
    return clasificador, analyzer

if __name__ == "__main__":
    demo_baimax()