"""
🗺️ bAImax - Sistema de Mapas Interactivos
=========================================

Módulo para visualización geográfica de problemas de salud pública
"""

import pandas as pd
import folium
from folium import plugins
import numpy as np

class bAImaxMapa:
    """
    🗺️ Generador de mapas interactivos para el sistema bAImax
    """
    
    def __init__(self, dataset_path='src/data/dataset_normalizado.csv'):
        self.df = pd.read_csv(dataset_path)
        
        # Coordenadas aproximadas de ciudades colombianas
        self.coordenadas = {
            'Bogotá': [4.7110, -74.0721],
            'Medellín': [6.2442, -75.5812],
            'Cali': [3.4516, -76.5320],
            'Barranquilla': [10.9685, -74.7813],
            'Cartagena': [10.3910, -75.4794],
            'Cúcuta': [7.8890, -72.4967],
            'Bucaramanga': [7.1190, -73.1198],
            'Pereira': [4.8133, -75.6961],
            'Santa Marta': [11.2408, -74.2099],
            'Manizales': [5.0700, -75.5138]
        }
        
        # Colores para diferentes niveles de gravedad
        self.colores = {
            'GRAVE': '#FF0000',      # Rojo
            'MODERADO': '#FFA500',   # Naranja
            'LEVE': '#FFFF00'        # Amarillo
        }
        
    def crear_mapa_base(self, centro=[4.5709, -74.2973], zoom=6):
        """
        🏗️ Crea mapa base de Colombia
        """
        mapa = folium.Map(
            location=centro,
            zoom_start=zoom,
            tiles='OpenStreetMap'
        )
        return mapa
    
    def agregar_problemas_por_ciudad(self, mapa):
        """
        📍 Agrega marcadores de problemas por ciudad
        """
        # Agrupar por ciudad y gravedad
        ciudad_problemas = self.df.groupby(['Ciudad', 'Nivel_gravedad']).agg({
            'Comentario': 'count',
            'Frecuencia_similar': 'sum',
            'Personas_afectadas': 'sum'
        }).reset_index()
        
        for _, row in ciudad_problemas.iterrows():
            ciudad = row['Ciudad']
            gravedad = row['Nivel_gravedad']
            count = row['Comentario']
            
            if ciudad in self.coordenadas:
                lat, lon = self.coordenadas[ciudad]
                
                # Información del popup
                popup_info = f"""
                <div style='width: 250px'>
                    <h4>🏙️ {ciudad}</h4>
                    <p><strong>Nivel:</strong> {gravedad}</p>
                    <p><strong>Reportes:</strong> {count}</p>
                    <p><strong>Personas afectadas:</strong> {row['Personas_afectadas']}</p>
                    <p><strong>Frecuencia:</strong> {row['Frecuencia_similar']}</p>
                </div>
                """
                
                # Tamaño del marcador basado en la cantidad de reportes
                radio = max(5, min(20, count * 2))
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=radio,
                    popup=folium.Popup(popup_info, max_width=300),
                    color='black',
                    fillColor=self.colores.get(gravedad, '#808080'),
                    fillOpacity=0.7,
                    weight=2
                ).add_to(mapa)
        
        return mapa
    
    def crear_mapa_calor(self, mapa=None):
        """
        🔥 Crea mapa de calor de problemas
        """
        if mapa is None:
            mapa = self.crear_mapa_base()
        
        # Datos para el mapa de calor
        heat_data = []
        
        for _, row in self.df.iterrows():
            ciudad = row['Ciudad']
            if ciudad in self.coordenadas:
                lat, lon = self.coordenadas[ciudad]
                
                # Peso basado en gravedad y frecuencia
                peso = row['Frecuencia_similar']
                if row['Nivel_gravedad'] == 'GRAVE':
                    peso *= 2
                
                heat_data.append([lat, lon, peso])
        
        # Agregar capa de calor
        plugins.HeatMap(heat_data, radius=15, blur=10).add_to(mapa)
        
        return mapa
    
    def crear_mapa_clusters(self, mapa=None):
        """
        🌟 Crea mapa con clusters de problemas
        """
        if mapa is None:
            mapa = self.crear_mapa_base()
        
        # Crear cluster
        marker_cluster = plugins.MarkerCluster().add_to(mapa)
        
        # Agrupar problemas por ciudad
        for ciudad, grupo in self.df.groupby('Ciudad'):
            if ciudad in self.coordenadas:
                lat, lon = self.coordenadas[ciudad]
                
                # Contar problemas por gravedad
                graves = (grupo['Nivel_gravedad'] == 'GRAVE').sum()
                moderados = (grupo['Nivel_gravedad'] == 'MODERADO').sum()
                total = len(grupo)
                
                # Información detallada
                problemas_detalle = grupo['Comentario'].value_counts().head(5)
                problemas_html = "<br>".join([f"• {prob}: {count}" for prob, count in problemas_detalle.items()])
                
                popup_info = f"""
                <div style='width: 300px'>
                    <h3>🏙️ {ciudad}</h3>
                    <hr>
                    <p><strong>📊 Resumen:</strong></p>
                    <p>🔴 Graves: {graves}</p>
                    <p>🟠 Moderados: {moderados}</p>
                    <p>📈 Total: {total}</p>
                    <hr>
                    <p><strong>🔝 Principales problemas:</strong></p>
                    {problemas_html}
                </div>
                """
                
                # Icono según predominancia
                icono = '🔴' if graves > moderados else '🟠'
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_info, max_width=350),
                    tooltip=f"{icono} {ciudad} ({total} reportes)",
                    icon=folium.Icon(
                        color='red' if graves > moderados else 'orange',
                        icon='exclamation-sign'
                    )
                ).add_to(marker_cluster)
        
        return mapa
    
    def crear_mapa_completo(self):
        """
        🎨 Crea mapa completo con todas las visualizaciones
        """
        # Mapa base
        mapa = self.crear_mapa_base()
        
        # Capa 1: Marcadores por ciudad
        self.agregar_problemas_por_ciudad(mapa)
        
        # Capa 2: Mapa de calor
        heat_data = []
        for _, row in self.df.iterrows():
            ciudad = row['Ciudad']
            if ciudad in self.coordenadas:
                lat, lon = self.coordenadas[ciudad]
                peso = row['Frecuencia_similar'] * (2 if row['Nivel_gravedad'] == 'GRAVE' else 1)
                heat_data.append([lat, lon, peso])
        
        heat_layer = plugins.HeatMap(
            heat_data, 
            radius=15, 
            blur=10, 
            name='Mapa de Calor'
        )
        
        # Crear grupos de capas
        feature_group = folium.FeatureGroup(name='Problemas por Ciudad')
        mapa.add_child(feature_group)
        mapa.add_child(heat_layer)
        
        # Control de capas
        folium.LayerControl().add_to(mapa)
        
        # Leyenda
        leyenda_html = """
        <div style='position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px'>
        <h4>🧽 bAImax - Leyenda</h4>
        <p><span style='color:#FF0000'>●</span> Problemas GRAVES</p>
        <p><span style='color:#FFA500'>●</span> Problemas MODERADOS</p>
        <p>Tamaño = Número de reportes</p>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(leyenda_html))
        
        return mapa
    
    def guardar_mapa(self, mapa, filename='baimax_mapa.html'):
        """
        💾 Guarda el mapa como archivo HTML
        """
        mapa.save(filename)
        print(f"🗺️ Mapa guardado como: {filename}")
        return filename

# Función de demostración
def demo_mapa():
    """
    🎭 Demostración del sistema de mapas bAImax
    """
    print("🗺️ DEMO DEL SISTEMA DE MAPAS bAImax")
    print("=" * 50)
    
    # Crear instancia del mapa
    mapa_sistema = bAImaxMapa()
    
    # Crear diferentes tipos de mapas
    print("🏗️ Creando mapa completo...")
    mapa_completo = mapa_sistema.crear_mapa_completo()
    
    print("🌟 Creando mapa con clusters...")
    mapa_clusters = mapa_sistema.crear_mapa_clusters()
    
    print("🔥 Creando mapa de calor...")
    mapa_calor = mapa_sistema.crear_mapa_calor()
    
    # Guardar mapas
    mapa_sistema.guardar_mapa(mapa_completo, 'baimax_mapa_completo.html')
    mapa_sistema.guardar_mapa(mapa_clusters, 'baimax_mapa_clusters.html')
    mapa_sistema.guardar_mapa(mapa_calor, 'baimax_mapa_calor.html')
    
    print("\n✨ ¡Mapas creados exitosamente! ✨")
    print("📁 Archivos generados:")
    print("   • baimax_mapa_completo.html")
    print("   • baimax_mapa_clusters.html") 
    print("   • baimax_mapa_calor.html")
    
    return mapa_sistema

if __name__ == "__main__":
    demo_mapa()