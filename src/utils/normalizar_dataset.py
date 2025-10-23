#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def normalizar_dataset():
    """
    Normaliza el dataset para compatibilidad con los componentes bAImax
    """
    print("🔄 Normalizando dataset para compatibilidad...")
    
    # Cargar dataset
    df = pd.read_csv('dataset_comunidades_senasoft.csv')
    print(f"📊 Dataset cargado: {len(df)} registros")
    
    # Mapear columnas para compatibilidad
    df_norm = df.copy()
    
    # Crear columna Nivel_gravedad mapeando desde "Nivel de urgencia"
    urgencia_map = {
        'Urgente': 'GRAVE',
        'Moderada': 'MODERADO',
        'No urgente': 'LEVE'
    }
    df_norm['Nivel_gravedad'] = df['Nivel de urgencia'].map(urgencia_map)
    
    # Crear columna Categoria mapeando desde "Categoría del problema"
    df_norm['Categoria'] = df['Categoría del problema']
    
    # Limpiar y normalizar ciudades
    ciudades_normalizadas = []
    for ciudad in df['Ciudad'].values:
        if pd.isna(ciudad):
            ciudades_normalizadas.append('Bogotá')  # Default
        else:
            ciudad_clean = str(ciudad).strip()
            # Normalizar nombres de ciudades conocidas
            if 'bogota' in ciudad_clean.lower() or 'bogotá' in ciudad_clean.lower():
                ciudades_normalizadas.append('Bogotá')
            elif 'medellin' in ciudad_clean.lower() or 'medellín' in ciudad_clean.lower():
                ciudades_normalizadas.append('Medellín')
            elif 'cali' in ciudad_clean.lower():
                ciudades_normalizadas.append('Cali')
            elif 'cartagena' in ciudad_clean.lower():
                ciudades_normalizadas.append('Cartagena')
            elif 'barranquilla' in ciudad_clean.lower():
                ciudades_normalizadas.append('Barranquilla')
            else:
                ciudades_normalizadas.append(ciudad_clean)
    
    df_norm['Ciudad'] = ciudades_normalizadas
    
    # Agregar columnas adicionales requeridas por los componentes
    df_norm['Frecuencia_similar'] = 1  # Cada registro cuenta como 1
    df_norm['Personas_afectadas'] = 1  # Cada registro representa 1 persona
    
    # Agregar columna de fecha normalizada
    if 'Fecha del reporte' in df_norm.columns:
        df_norm['Fecha'] = df_norm['Fecha del reporte']
    else:
        df_norm['Fecha'] = '2024-01-01'  # Fecha default
    
    print("✅ Mapeos creados:")
    print(f"   📊 Nivel_gravedad: {df_norm['Nivel_gravedad'].value_counts().to_dict()}")
    print(f"   🏙️ Ciudades principales: {df_norm['Ciudad'].value_counts().head().to_dict()}")
    print(f"   📈 Columnas adicionales: Frecuencia_similar, Personas_afectadas, Fecha")
    
    # Guardar dataset normalizado
    df_norm.to_csv('src/data/dataset_normalizado.csv', index=False, encoding='utf-8')
    print("💾 Dataset normalizado guardado como: src/data/dataset_normalizado.csv")
    
    return df_norm

if __name__ == "__main__":
    normalizar_dataset()