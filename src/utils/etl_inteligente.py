"""
ETL Script Inteligente para procesamiento de datos de comunidades SENASOFT
Filtra datos de categoría "Salud", elimina spam por persona y calcula niveles de gravedad
basado en la frecuencia de comentarios similares entre diferentes personas
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import logging
from typing import List, Tuple, Dict
from collections import defaultdict, Counter
import warnings
warnings.filterwarnings('ignore')

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ETLSaludInteligente:
    """
    Procesador ETL inteligente que:
    1. Filtra datos de salud
    2. Elimina spam por persona (mismo comentario de la misma persona)
    3. Calcula niveles de gravedad basado en frecuencia entre personas diferentes
    4. Mantiene diversidad con información de importancia
    """
    
    def __init__(self, input_file: str, output_file: str, similarity_threshold: float = 0.80):
        self.input_file = input_file
        self.output_file = output_file
        self.similarity_threshold = similarity_threshold
        self.df_original = None
        self.df_salud = None
        self.df_processed = None
        
    def extract(self) -> pd.DataFrame:
        """
        EXTRACT: Cargar datos del archivo CSV
        """
        logger.info(f"Iniciando extracción de datos desde: {self.input_file}")
        
        try:
            self.df_original = pd.read_csv(self.input_file, encoding='utf-8')
            logger.info(f"Datos extraídos exitosamente. Forma: {self.df_original.shape}")
            
            # Mostrar estadísticas básicas
            categorias = self.df_original['Categoría del problema'].value_counts()
            logger.info(f"Distribución de categorías:\n{categorias}")
            
            return self.df_original
            
        except Exception as e:
            logger.error(f"Error en extracción: {str(e)}")
            raise
    
    def transform(self) -> pd.DataFrame:
        """
        TRANSFORM: Aplicar transformaciones inteligentes
        """
        logger.info("Iniciando transformación inteligente de datos")
        
        # 1. Filtrar solo registros de categoría "Salud"
        self.df_salud = self._filter_health_category()
        
        # 2. Eliminar spam por persona
        df_no_spam = self._remove_person_spam()
        
        # 3. Calcular frecuencias y niveles de gravedad
        df_with_gravity = self._calculate_gravity_levels(df_no_spam)
        
        # 4. Limpiar y estructurar datos finales
        self.df_processed = self._finalize_dataset(df_with_gravity)
        
        logger.info(f"Transformación completada. Registros finales: {len(self.df_processed)}")
        return self.df_processed
    
    def _filter_health_category(self) -> pd.DataFrame:
        """
        Filtrar solo registros de categoría "Salud"
        """
        logger.info("Filtrando registros de categoría 'Salud'")
        
        df_salud = self.df_original[self.df_original['Categoría del problema'] == 'Salud'].copy()
        
        # Eliminar registros con comentarios vacíos
        initial_count = len(df_salud)
        df_salud = df_salud.dropna(subset=['Comentario'])
        df_salud = df_salud[df_salud['Comentario'].str.strip() != '']
        
        removed = initial_count - len(df_salud)
        logger.info(f"Registros de salud válidos: {len(df_salud)} (eliminados {removed} con comentarios vacíos)")
        
        return df_salud
    
    def _remove_person_spam(self) -> pd.DataFrame:
        """
        Eliminar spam: mismo comentario de la misma persona múltiples veces
        """
        logger.info("Eliminando spam por persona (duplicados de la misma persona)")
        
        # Normalizar comentarios para comparación
        df_work = self.df_salud.copy()
        df_work['Comentario_normalizado'] = df_work['Comentario'].apply(self._normalize_text)
        
        initial_count = len(df_work)
        
        # Eliminar duplicados por persona (mismo nombre + mismo comentario normalizado)
        df_no_spam = df_work.drop_duplicates(subset=['Nombre', 'Comentario_normalizado'])
        
        removed_spam = initial_count - len(df_no_spam)
        logger.info(f"Eliminados {removed_spam} registros de spam (mismo comentario por misma persona)")
        
        return df_no_spam
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalizar texto para comparación
        """
        if pd.isna(text) or text == '':
            return ''
        
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def _calculate_gravity_levels(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcular niveles de gravedad basado en frecuencia de comentarios similares
        entre diferentes personas
        """
        logger.info("Calculando niveles de gravedad basado en frecuencia entre personas")
        
        df_result = df.copy()
        
        # Obtener comentarios únicos
        comentarios_unicos = df_result['Comentario_normalizado'].unique()
        
        if len(comentarios_unicos) < 2:
            logger.warning("Muy pocos comentarios para análisis de similitud")
            df_result['Nivel_gravedad'] = 'MODERADO'
            df_result['Frecuencia_similar'] = 1
            df_result['Personas_afectadas'] = 1
            return df_result
        
        # Crear vectores TF-IDF
        vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(comentarios_unicos)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Agrupar comentarios similares
            grupos_similares = self._group_similar_comments(
                comentarios_unicos, similarity_matrix
            )
            
            # Calcular estadísticas por grupo
            df_result = self._assign_gravity_levels(df_result, grupos_similares)
            
        except Exception as e:
            logger.error(f"Error en cálculo de similitud: {str(e)}")
            df_result['Nivel_gravedad'] = 'MODERADO'
            df_result['Frecuencia_similar'] = 1
            df_result['Personas_afectadas'] = 1
        
        return df_result
    
    def _group_similar_comments(self, comentarios: np.ndarray, similarity_matrix: np.ndarray) -> Dict[int, List[int]]:
        """
        Agrupar comentarios similares basado en umbral de similitud
        """
        n_comments = len(comentarios)
        grupos = {}
        procesados = set()
        grupo_id = 0
        
        for i in range(n_comments):
            if i in procesados:
                continue
            
            # Encontrar comentarios similares
            similares = []
            for j in range(n_comments):
                if similarity_matrix[i][j] >= self.similarity_threshold:
                    similares.append(j)
                    procesados.add(j)
            
            if similares:
                grupos[grupo_id] = similares
                grupo_id += 1
        
        logger.info(f"Identificados {len(grupos)} grupos de comentarios similares")
        return grupos
    
    def _assign_gravity_levels(self, df: pd.DataFrame, grupos: Dict[int, List[int]]) -> pd.DataFrame:
        """
        Asignar niveles de gravedad basado en frecuencia de cada grupo
        """
        df_result = df.copy()
        comentarios_unicos = df_result['Comentario_normalizado'].unique()
        
        # Mapear comentarios a grupos
        comment_to_group = {}
        for grupo_id, indices in grupos.items():
            for idx in indices:
                comment_to_group[comentarios_unicos[idx]] = grupo_id
        
        # Calcular frecuencias por grupo
        grupo_frecuencias = defaultdict(int)
        grupo_personas = defaultdict(set)
        
        for _, row in df_result.iterrows():
            comentario_norm = row['Comentario_normalizado']
            if comentario_norm in comment_to_group:
                grupo_id = comment_to_group[comentario_norm]
                grupo_frecuencias[grupo_id] += 1
                grupo_personas[grupo_id].add(row['Nombre'])
        
        # Asignar niveles de gravedad basado en múltiples criterios
        frecuencias = list(grupo_frecuencias.values())
        personas_counts = [len(personas) for personas in grupo_personas.values()]
        
        if len(frecuencias) > 0:
            # Usar percentiles combinados de frecuencia y personas afectadas
            freq_p50 = np.percentile(frecuencias, 50)
            freq_p80 = np.percentile(frecuencias, 80)
            
            personas_p50 = np.percentile(personas_counts, 50) if personas_counts else 1
            personas_p80 = np.percentile(personas_counts, 80) if personas_counts else 1
        else:
            freq_p50 = freq_p80 = 1
            personas_p50 = personas_p80 = 1
        
        # Asignar valores a cada registro
        for idx, row in df_result.iterrows():
            comentario_norm = row['Comentario_normalizado']
            
            if comentario_norm in comment_to_group:
                grupo_id = comment_to_group[comentario_norm]
                frecuencia = grupo_frecuencias[grupo_id]
                personas_count = len(grupo_personas[grupo_id])
                
                # Determinar nivel de gravedad basado en múltiples criterios
                if frecuencia >= freq_p80 and personas_count >= personas_p80:
                    nivel = 'GRAVE'
                elif frecuencia >= freq_p50 or personas_count >= personas_p50:
                    nivel = 'MODERADO'
                else:
                    nivel = 'LEVE'
                
                df_result.loc[idx, 'Nivel_gravedad'] = nivel
                df_result.loc[idx, 'Frecuencia_similar'] = frecuencia
                df_result.loc[idx, 'Personas_afectadas'] = personas_count
            else:
                df_result.loc[idx, 'Nivel_gravedad'] = 'MODERADO'
                df_result.loc[idx, 'Frecuencia_similar'] = 1
                df_result.loc[idx, 'Personas_afectadas'] = 1
        
        # Log estadísticas
        niveles = df_result['Nivel_gravedad'].value_counts()
        logger.info(f"Distribución de niveles de gravedad:\n{niveles}")
        
        return df_result
    
    def _finalize_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Finalizar y limpiar dataset para entrenamiento de IA
        """
        logger.info("Finalizando dataset para entrenamiento de IA")
        
        # Seleccionar y ordenar columnas importantes
        columns_final = [
            'ID', 'Nombre', 'Edad', 'Género', 'Ciudad',
            'Comentario', 'Nivel_gravedad', 'Frecuencia_similar', 'Personas_afectadas',
            'Categoría del problema', 'Nivel de urgencia', 'Fecha del reporte',
            'Acceso a internet', 'Atención previa del gobierno', 'Zona rural'
        ]
        
        df_final = df[columns_final].copy()
        
        # Ordenar por nivel de gravedad y frecuencia
        orden_gravedad = {'GRAVE': 3, 'MODERADO': 2, 'LEVE': 1}
        df_final['_orden'] = df_final['Nivel_gravedad'].map(orden_gravedad)
        df_final = df_final.sort_values(['_orden', 'Frecuencia_similar'], ascending=[False, False])
        df_final = df_final.drop('_orden', axis=1)
        
        # Reset index
        df_final = df_final.reset_index(drop=True)
        
        logger.info(f"Dataset final: {len(df_final)} registros únicos sin spam")
        
        return df_final
    
    def load(self) -> bool:
        """
        LOAD: Guardar datos procesados
        """
        logger.info(f"Guardando dataset inteligente en: {self.output_file}")
        
        try:
            self.df_processed.to_csv(self.output_file, index=False, encoding='utf-8')
            logger.info("Dataset guardado exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error al guardar: {str(e)}")
            return False
    
    def run_etl(self) -> bool:
        """
        Ejecutar proceso ETL completo
        """
        try:
            logger.info("=== INICIANDO PROCESO ETL INTELIGENTE ===")
            
            # Extract
            self.extract()
            
            # Transform
            self.transform()
            
            # Load
            success = self.load()
            
            if success:
                self._generate_report()
                logger.info("=== PROCESO ETL COMPLETADO EXITOSAMENTE ===")
            
            return success
            
        except Exception as e:
            logger.error(f"Error en proceso ETL: {str(e)}")
            return False
    
    def _generate_report(self):
        """
        Generar reporte de procesamiento
        """
        if self.df_processed is None:
            return
        
        report = f"""
=== REPORTE ETL INTELIGENTE ===

ARCHIVO ENTRADA: {self.input_file}
ARCHIVO SALIDA: {self.output_file}

ESTADÍSTICAS:
- Registros originales: {len(self.df_original)}
- Registros de salud iniciales: {len(self.df_salud)}
- Registros finales (sin spam): {len(self.df_processed)}

DISTRIBUCIÓN DE GRAVEDAD:
{self.df_processed['Nivel_gravedad'].value_counts().to_string()}

ESTADÍSTICAS DE FRECUENCIA:
- Frecuencia promedio: {self.df_processed['Frecuencia_similar'].mean():.1f}
- Frecuencia máxima: {self.df_processed['Frecuencia_similar'].max()}
- Personas promedio por problema: {self.df_processed['Personas_afectadas'].mean():.1f}

TOP 5 PROBLEMAS MÁS FRECUENTES:
{self.df_processed.nlargest(5, 'Frecuencia_similar')[['Comentario', 'Nivel_gravedad', 'Frecuencia_similar']].to_string(index=False)}

DISTRIBUCIÓN GEOGRÁFICA:
{self.df_processed['Ciudad'].value_counts().head(10).to_string()}

Este dataset está optimizado para entrenamiento de IA con información de gravedad.
        """
        
        print(report)
        
        # Guardar reporte
        report_file = self.output_file.replace('.csv', '_report.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Reporte guardado en: {report_file}")


def main():
    """
    Función principal
    """
    input_file = "dataset_comunidades_senasoft.csv"
    output_file = "dataset_salud_inteligente.csv"
    
    processor = ETLSaludInteligente(
        input_file=input_file,
        output_file=output_file,
        similarity_threshold=0.80
    )
    
    success = processor.run_etl()
    
    if success:
        print(f"\n✅ ETL Inteligente completado!")
        print(f"📄 Dataset generado: {output_file}")
    else:
        print("\n❌ Error en el proceso ETL")


if __name__ == "__main__":
    main()