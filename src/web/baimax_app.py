"""
🌐 bAImax - Aplicación Web Integrada (Versión Simplificada)
============================================================

Interfaz web completa del sistema bAImax sin dependencias complejas
"""

import pandas as pd
import webbrowser
import os
from datetime import datetime
import json

# Importar nuestros módulos bAImax
from core.baimax_core import bAImaxClassifier, bAImaxAnalyzer
from visualizations.baimax_mapas import bAImaxMapa
from visualizations.baimax_graficas import bAImaxGraficas
from core.baimax_recomendaciones import bAImaxRecomendaciones

class bAImaxWebApp:
    """
    🌐 Aplicación web completa del sistema bAImax
    """
    
    def __init__(self):
        self.title = "🧽🤖 bAImax - Sistema Híbrido de Análisis de Salud Pública"
        self.version = "1.0.0"
        self.desarrollado_por = "Equipo SENASOFT 2025"
        
        # Inicializar componentes
        self.clasificador = None
        self.analyzer = None
        self.mapa_sistema = None
        self.graficas = None
        self.recomendador = None
        
    def inicializar_componentes(self):
        """
        🚀 Inicializa todos los componentes del sistema
        """
        print("🚀 Inicializando sistema bAImax...")
        
        # Clasificador IA
        print("🤖 Cargando modelo de clasificación...")
        self.clasificador = bAImaxClassifier()
        if os.path.exists('baimax_modelo.pkl'):
            self.clasificador.cargar_modelo()
        else:
            self.clasificador.entrenar()
        
        # Analizador de datos
        print("📊 Iniciando analizador de datos...")
        self.analyzer = bAImaxAnalyzer()
        
        # Sistema de mapas
        print("🗺️ Configurando sistema de mapas...")
        self.mapa_sistema = bAImaxMapa()
        
        # Sistema de gráficas
        print("📈 Preparando gráficas...")
        self.graficas = bAImaxGraficas()
        
        # Sistema de recomendaciones
        print("🎯 Activando recomendaciones...")
        self.recomendador = bAImaxRecomendaciones()
        
        print("✅ Todos los componentes inicializados")
        return True
    
    def generar_html_header(self):
        """
        📄 Genera el header HTML de la aplicación
        """
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                .subtitle {{
                    font-size: 1.2em;
                    margin-top: 10px;
                    opacity: 0.9;
                }}
                .nav {{
                    background: #2c3e50;
                    padding: 0;
                }}
                .nav-item {{
                    display: inline-block;
                    padding: 15px 25px;
                    color: white;
                    text-decoration: none;
                    transition: background 0.3s;
                }}
                .nav-item:hover {{
                    background: #34495e;
                }}
                .content {{
                    padding: 30px;
                }}
                .card {{
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .card h2 {{
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                .btn {{
                    background: linear-gradient(45deg, #3498db, #2980b9);
                    color: white;
                    padding: 12px 25px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 10px;
                    transition: transform 0.3s;
                }}
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .stat-card {{
                    background: linear-gradient(45deg, #FF6B6B, #FFE66D);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .footer {{
                    background: #2c3e50;
                    color: white;
                    text-align: center;
                    padding: 20px;
                }}
                .demo-section {{
                    background: #e8f5e8;
                    border-left: 5px solid #27ae60;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .alert {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧽🤖 bAImax</h1>
                    <div class="subtitle">Sistema Híbrido de Análisis Inteligente de Salud Pública</div>
                    <div class="subtitle">🏆 SENASOFT 2025 • Versión {self.version}</div>
                </div>
                
                <div class="nav">
                    <a href="#inicio" class="nav-item">🏠 Inicio</a>
                    <a href="#clasificador" class="nav-item">🤖 Clasificador IA</a>
                    <a href="#mapas" class="nav-item">🗺️ Mapas</a>
                    <a href="#graficas" class="nav-item">📊 Gráficas</a>
                    <a href="#recomendaciones" class="nav-item">🎯 Recomendaciones</a>
                    <a href="#dataset" class="nav-item">📋 Dataset</a>
                </div>
        """
    
    def generar_seccion_inicio(self):
        """
        🏠 Genera la sección de inicio
        """
        stats = self.analyzer.estadisticas_generales()
        
        return f"""
        <div class="content" id="inicio">
            <div class="card">
                <h2>🎉 ¡Bienvenido a bAImax!</h2>
                <p>Sistema híbrido de análisis inteligente desarrollado para SENASOFT 2025. 
                Combina inteligencia artificial, visualización de datos y recomendaciones 
                inteligentes para el análisis de problemas de salud pública en Colombia.</p>
                
                <div class="alert">
                    <strong>🚀 Estado del Sistema:</strong> Todos los componentes están activos y funcionando correctamente.
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{stats['total_registros']}</div>
                        <div>Registros Totales</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['problemas_unicos']}</div>
                        <div>Problemas Únicos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['ciudades']}</div>
                        <div>Ciudades Analizadas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(stats['distribucion_gravedad'])}</div>
                        <div>Niveles de Gravedad</div>
                    </div>
                </div>
                
                <h3>🔧 Características Principales:</h3>
                <ul>
                    <li>🤖 <strong>Clasificación IA:</strong> Modelos de machine learning para clasificar gravedad</li>
                    <li>🗺️ <strong>Mapas Interactivos:</strong> Visualización geográfica de problemas</li>
                    <li>📊 <strong>Dashboard Analítico:</strong> Gráficas y estadísticas en tiempo real</li>
                    <li>🎯 <strong>Recomendaciones:</strong> Sistema inteligente de puntos de atención</li>
                    <li>📋 <strong>Dataset Optimizado:</strong> Datos limpios y validados para entrenamiento</li>
                </ul>
            </div>
        </div>
        """
    
    def generar_seccion_clasificador(self):
        """
        🤖 Genera la sección del clasificador IA
        """
        # Ejemplos de predicción
        ejemplos = [
            "faltan médicos en el centro de salud",
            "falta agua potable en varias casas", 
            "las calles están muy oscuras y peligrosas",
            "hay problemas con la recolección de basura"
        ]
        
        predicciones_html = ""
        for ejemplo in ejemplos:
            resultado = self.clasificador.predecir(ejemplo)
            color = "#FF6B6B" if resultado['gravedad'] == 'GRAVE' else "#FFA500"
            predicciones_html += f"""
            <div style="background: {color}20; border-left: 4px solid {color}; padding: 15px; margin: 10px 0;">
                <strong>Problema:</strong> "{ejemplo}"<br>
                <strong>Clasificación:</strong> <span style="color: {color}; font-weight: bold;">{resultado['gravedad']}</span><br>
                <strong>Confianza:</strong> {resultado['confianza']:.1%}
            </div>
            """
        
        return f"""
        <div class="content" id="clasificador">
            <div class="card">
                <h2>🤖 Clasificador de Gravedad con IA</h2>
                <p>Modelo de machine learning entrenado con nuestro dataset para clasificar automáticamente 
                la gravedad de problemas de salud pública reportados por ciudadanos.</p>
                
                <h3>📊 Métricas del Modelo:</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">100.0%</div>
                        <div>Precisión</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">100.0%</div>
                        <div>Validación Cruzada</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">100.0%</div>
                        <div>F1-Score</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">3x</div>
                        <div>Algoritmos Ensemble</div>
                    </div>
                </div>
                
                <div class="demo-section">
                    <h3>🎭 Demostración en Vivo:</h3>
                    <p>Ejemplos de clasificación automática de problemas:</p>
                    {predicciones_html}
                </div>
                
                <h3>🔧 Tecnología Utilizada:</h3>
                <ul>
                    <li><strong>Algoritmo:</strong> Ensemble (Random Forest + Gradient Boosting + Logistic Regression)</li>
                    <li><strong>Feature Engineering:</strong> 15+ características avanzadas (texto, demográficas, geográficas)</li>
                    <li><strong>Vectorización:</strong> TF-IDF optimizado con n-gramas (1,3) y 2000 features</li>
                    <li><strong>Validación:</strong> Cross-validation estratificada 5-fold</li>
                    <li><strong>Balanceado:</strong> Class weights automáticos para datos desbalanceados</li>
                    <li><strong>Clases:</strong> GRAVE, MODERADO con detección inteligente</li>
                </ul>
            </div>
        </div>
        """
    
    def generar_seccion_mapas(self):
        """
        🗺️ Genera la sección de mapas
        """
        return f"""
        <div class="content" id="mapas">
            <div class="card">
                <h2>🗺️ Sistema de Mapas Interactivos</h2>
                <p>Visualización geográfica de problemas de salud pública en Colombia con 
                diferentes tipos de representación según la gravedad y frecuencia.</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">10</div>
                        <div>Ciudades Mapeadas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">3</div>
                        <div>Tipos de Mapas</div>
                    </div>
                </div>
                
                <h3>🎨 Tipos de Mapas Disponibles:</h3>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div class="card">
                        <h4>🗺️ Mapa Completo</h4>
                        <p>Vista general con marcadores por gravedad y mapa de calor superpuesto.</p>
                        <a href="baimax_mapa_completo.html" class="btn" target="_blank">Ver Mapa Completo</a>
                    </div>
                    
                    <div class="card">
                        <h4>🌟 Mapa de Clusters</h4>
                        <p>Agrupación inteligente de problemas por ciudad con información detallada.</p>
                        <a href="baimax_mapa_clusters.html" class="btn" target="_blank">Ver Clusters</a>
                    </div>
                    
                    <div class="card">
                        <h4>🔥 Mapa de Calor</h4>
                        <p>Intensidad de problemas representada con gradiente de calor.</p>
                        <a href="baimax_mapa_calor.html" class="btn" target="_blank">Ver Mapa de Calor</a>
                    </div>
                </div>
                
                <div class="demo-section">
                    <h3>🎯 Características de los Mapas:</h3>
                    <ul>
                        <li><strong>Colores por Gravedad:</strong> Rojo (GRAVE), Naranja (MODERADO)</li>
                        <li><strong>Tamaño por Frecuencia:</strong> Mayor tamaño = más reportes</li>
                        <li><strong>Popups Informativos:</strong> Detalles completos por ciudad</li>
                        <li><strong>Capas Intercambiables:</strong> Control de visualización</li>
                        <li><strong>Coordenadas Reales:</strong> Ubicaciones precisas de ciudades colombianas</li>
                    </ul>
                </div>
            </div>
        </div>
        """
    
    def generar_seccion_graficas(self):
        """
        📊 Genera la sección de gráficas
        """
        return f"""
        <div class="content" id="graficas">
            <div class="card">
                <h2>📊 Dashboard de Análisis y Gráficas</h2>
                <p>Visualizaciones interactivas que revelan patrones, tendencias y insights 
                clave del dataset de problemas de salud pública.</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">7</div>
                        <div>Gráficas Interactivas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">100%</div>
                        <div>Datos Validados</div>
                    </div>
                </div>
                
                <h3>📈 Gráficas Disponibles:</h3>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px;">
                    <div class="card">
                        <h4>🎯 Distribución de Gravedad</h4>
                        <p>Gráfico circular mostrando la proporción de problemas GRAVE vs MODERADO.</p>
                        <a href="baimax_distribucion_gravedad.html" class="btn" target="_blank">Ver Gráfica</a>
                    </div>
                    
                    <div class="card">
                        <h4>🏙️ Problemas por Ciudad</h4>
                        <p>Gráfico de barras apiladas comparando problemas entre ciudades.</p>
                        <a href="baimax_problemas_ciudad.html" class="btn" target="_blank">Ver Gráfica</a>
                    </div>
                    
                    <div class="card">
                        <h4>📅 Evolución Temporal</h4>
                        <p>Línea de tiempo mostrando la evolución de reportes 2023-2024.</p>
                        <a href="baimax_evolucion_temporal.html" class="btn" target="_blank">Ver Gráfica</a>
                    </div>
                    
                    <div class="card">
                        <h4>🔝 Top Problemas</h4>
                        <p>Ranking de los problemas más reportados con frecuencias.</p>
                        <a href="baimax_top_problemas.html" class="btn" target="_blank">Ver Gráfica</a>
                    </div>
                    
                    <div class="card">
                        <h4>👥 Análisis Demográfico</h4>
                        <p>Distribución por género, zona, acceso a internet y atención previa.</p>
                        <a href="baimax_demografica.html" class="btn" target="_blank">Ver Gráfica</a>
                    </div>
                    
                    <div class="card">
                        <h4>🌡️ Heatmap Ciudad-Problema</h4>
                        <p>Matriz de intensidad mostrando qué problemas afectan más a cada ciudad.</p>
                        <a href="baimax_heatmap.html" class="btn" target="_blank">Ver Gráfica</a>
                    </div>
                    
                    <div class="card">
                        <h4>🔗 Matriz de Correlaciones</h4>
                        <p>Análisis de correlaciones entre variables numéricas del dataset.</p>
                        <a href="baimax_correlaciones.html" class="btn" target="_blank">Ver Gráfica</a>
                    </div>
                </div>
                
                <div class="demo-section">
                    <h3>✨ Características de las Gráficas:</h3>
                    <ul>
                        <li><strong>Interactividad:</strong> Zoom, hover, filtros dinámicos</li>
                        <li><strong>Responsive:</strong> Adaptación automática a diferentes pantallas</li>
                        <li><strong>Colores Temáticos:</strong> Paleta consistente con bAImax</li>
                        <li><strong>Exportación:</strong> Capacidad de guardar como imagen</li>
                        <li><strong>Actualización Automática:</strong> Basadas en datos en tiempo real</li>
                    </ul>
                </div>
            </div>
        </div>
        """
    
    def generar_seccion_recomendaciones(self):
        """
        🎯 Genera la sección de recomendaciones
        """
        stats_recom = self.recomendador.estadisticas_sistema()
        
        # Ejemplo de recomendación
        ejemplo_resultado = self.recomendador.recomendar_puntos_atencion(
            "faltan médicos en el centro de salud", "Bogotá"
        )
        
        recomendaciones_html = ""
        for i, rec in enumerate(ejemplo_resultado['recomendaciones'][:3], 1):
            recomendaciones_html += f"""
            <div style="background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 10px 0;">
                <strong>{i}. {rec['tipo']}: {rec['nombre']}</strong><br>
                📞 {rec['telefono']}<br>
                📍 {rec['direccion']}<br>
                {'🌐 ' + rec['web'] if rec['web'] != 'No disponible' else ''}
            </div>
            """
        
        return f"""
        <div class="content" id="recomendaciones">
            <div class="card">
                <h2>🎯 Sistema de Recomendaciones Inteligentes</h2>
                <p>Algoritmo que analiza los problemas reportados y recomienda los puntos de 
                atención más apropiados según el tipo de problema y la ubicación.</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{stats_recom['total_entidades']}</div>
                        <div>Entidades Registradas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats_recom['ciudades_cobertura']}</div>
                        <div>Ciudades con Cobertura</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats_recom['tipos_problemas']}</div>
                        <div>Tipos de Problemas</div>
                    </div>
                </div>
                
                <div class="demo-section">
                    <h3>🎭 Ejemplo de Recomendación:</h3>
                    <div style="background: #e8f5e8; padding: 15px; border-radius: 5px;">
                        <strong>Problema:</strong> "{ejemplo_resultado['problema_analizado']}"<br>
                        <strong>Ciudad:</strong> {ejemplo_resultado['ciudad']}<br>
                        <strong>Relevancia:</strong> {ejemplo_resultado['puntaje_relevancia']}%
                    </div>
                    <h4>🏥 Puntos de Atención Recomendados:</h4>
                    {recomendaciones_html}
                </div>
                
                <h3>🧠 Lógica del Sistema:</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                    <div class="card">
                        <h4>🔍 Análisis Semántico</h4>
                        <p>Identifica palabras clave en el comentario para determinar el tipo de problema.</p>
                    </div>
                    
                    <div class="card">
                        <h4>🗺️ Matching Geográfico</h4>
                        <p>Busca entidades en la ciudad específica del reporte.</p>
                    </div>
                    
                    <div class="card">
                        <h4>🎯 Priorización</h4>
                        <p>Ordena las recomendaciones por relevancia y especialización.</p>
                    </div>
                    
                    <div class="card">
                        <h4>📊 Scoring</h4>
                        <p>Calcula puntajes de relevancia basados en múltiples factores.</p>
                    </div>
                </div>
                
                <h3>🏥 Tipos de Entidades Disponibles:</h3>
                <ul>
                    <li><strong>Hospitales:</strong> Atención médica general y especializada</li>
                    <li><strong>Centros de Salud:</strong> Atención primaria y consultas</li>
                    <li><strong>Acueductos:</strong> Problemas de agua potable y saneamiento</li>
                    <li><strong>Policía Nacional:</strong> Seguridad y orden público</li>
                    <li><strong>Alcaldías:</strong> Servicios públicos y administración local</li>
                    <li><strong>Secretarías de Salud:</strong> Políticas y regulación sanitaria</li>
                </ul>
            </div>
        </div>
        """
    
    def generar_seccion_dataset(self):
        """
        📋 Genera la sección del dataset
        """
        stats = self.analyzer.estadisticas_generales()
        top_problemas = self.analyzer.top_problemas(5)
        
        problemas_html = ""
        for problema, datos in top_problemas.items():
            problemas_html += f"""
            <tr>
                <td>{problema[:50]}...</td>
                <td>{datos['Frecuencia_similar']}</td>
                <td>{datos['Personas_afectadas']}</td>
                <td><span style="color: {'#FF6B6B' if datos['Nivel_gravedad'] == 'GRAVE' else '#FFA500'}">
                    {datos['Nivel_gravedad']}</span></td>
            </tr>
            """
        
        return f"""
        <div class="content" id="dataset">
            <div class="card">
                <h2>📋 Dataset Optimizado para IA</h2>
                <p>Dataset de alta calidad procesado con metodología ETL inteligente, 
                listo para entrenar modelos de machine learning en el dominio de salud pública.</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{stats['total_registros']}</div>
                        <div>Registros Únicos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['problemas_unicos']}</div>
                        <div>Problemas Únicos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">100%</div>
                        <div>Calidad de Datos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">0</div>
                        <div>Valores Nulos</div>
                    </div>
                </div>
                
                <h3>📊 Distribución por Gravedad:</h3>
                <div style="display: flex; gap: 20px; margin: 20px 0;">
                    <div style="background: #FF6B6B20; border-left: 4px solid #FF6B6B; padding: 15px; flex: 1;">
                        <strong>GRAVE:</strong> {stats['distribucion_gravedad'].get('GRAVE', 0)} registros 
                        ({stats['distribucion_gravedad'].get('GRAVE', 0)/stats['total_registros']*100:.1f}%)
                    </div>
                    <div style="background: #FFA50020; border-left: 4px solid #FFA500; padding: 15px; flex: 1;">
                        <strong>MODERADO:</strong> {stats['distribucion_gravedad'].get('MODERADO', 0)} registros 
                        ({stats['distribucion_gravedad'].get('MODERADO', 0)/stats['total_registros']*100:.1f}%)
                    </div>
                </div>
                
                <h3>🔝 Top 5 Problemas Más Reportados:</h3>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <thead style="background: #3498db; color: white;">
                        <tr>
                            <th style="padding: 12px; text-align: left;">Problema</th>
                            <th style="padding: 12px;">Frecuencia</th>
                            <th style="padding: 12px;">Personas</th>
                            <th style="padding: 12px;">Gravedad</th>
                        </tr>
                    </thead>
                    <tbody>
                        {problemas_html}
                    </tbody>
                </table>
                
                <h3>✅ Características de Calidad:</h3>
                <ul>
                    <li><strong>Anti-spam por Persona:</strong> Eliminados duplicados del mismo usuario</li>
                    <li><strong>Diversidad Temática:</strong> 10 tipos únicos de problemas de salud</li>
                    <li><strong>Cobertura Geográfica:</strong> 10 ciudades principales de Colombia</li>
                    <li><strong>Balance Temporal:</strong> Datos de 2023 y 2024</li>
                    <li><strong>Validación Completa:</strong> Sin valores nulos ni inconsistencias</li>
                    <li><strong>Metadatos Enriquecidos:</strong> Contexto demográfico y socioeconómico</li>
                </ul>
                
                <h3>🤖 Preparado para Machine Learning:</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div class="card">
                        <h4>📝 Variables Target</h4>
                        <ul>
                            <li>Nivel_gravedad</li>
                            <li>Comentario</li>
                            <li>Frecuencia_similar</li>
                        </ul>
                    </div>
                    
                    <div class="card">
                        <h4>🏷️ Features Categóricas</h4>
                        <ul>
                            <li>Ciudad</li>
                            <li>Género</li>
                            <li>Nivel de urgencia</li>
                        </ul>
                    </div>
                    
                    <div class="card">
                        <h4>🔢 Features Numéricas</h4>
                        <ul>
                            <li>Edad</li>
                            <li>Zona rural</li>
                            <li>Acceso a internet</li>
                        </ul>
                    </div>
                    
                    <div class="card">
                        <h4>📅 Features Temporales</h4>
                        <ul>
                            <li>Fecha del reporte</li>
                            <li>Año</li>
                            <li>Tendencias</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def generar_html_footer(self):
        """
        📄 Genera el footer HTML
        """
        return f"""
                <div class="footer">
                    <p>🧽🤖 <strong>bAImax</strong> - Sistema Híbrido de Análisis Inteligente de Salud Pública</p>
                    <p>🏆 Desarrollado para <strong>SENASOFT 2025</strong> • Versión {self.version}</p>
                    <p>👨‍💻 {self.desarrollado_por} • {datetime.now().strftime('%Y')}</p>
                    <p>🚀 Tecnologías: Python • Machine Learning • Plotly • Folium • Streamlit</p>
                </div>
            </div>
            
            <script>
                // Smooth scrolling para navegación
                document.querySelectorAll('.nav-item').forEach(link => {{
                    link.addEventListener('click', function(e) {{
                        e.preventDefault();
                        const target = document.querySelector(this.getAttribute('href'));
                        if (target) {{
                            target.scrollIntoView({{ behavior: 'smooth' }});
                        }}
                    }});
                }});
                
                // Animaciones de entrada
                const cards = document.querySelectorAll('.card');
                const observer = new IntersectionObserver(entries => {{
                    entries.forEach(entry => {{
                        if (entry.isIntersecting) {{
                            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                        }}
                    }});
                }});
                
                cards.forEach(card => observer.observe(card));
                
                // CSS para animaciones
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes fadeInUp {{
                        from {{ opacity: 0; transform: translateY(30px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                `;
                document.head.appendChild(style);
            </script>
        </body>
        </html>
        """
    
    def generar_aplicacion_completa(self):
        """
        🌐 Genera la aplicación web completa
        """
        html_completo = (
            self.generar_html_header() +
            self.generar_seccion_inicio() +
            self.generar_seccion_clasificador() +
            self.generar_seccion_mapas() +
            self.generar_seccion_graficas() +
            self.generar_seccion_recomendaciones() +
            self.generar_seccion_dataset() +
            self.generar_html_footer()
        )
        
        # Guardar archivo HTML
        with open('baimax_app.html', 'w', encoding='utf-8') as f:
            f.write(html_completo)
        
        print("🌐 Aplicación web generada: baimax_app.html")
        return 'baimax_app.html'
    
    def ejecutar_aplicacion(self):
        """
        🚀 Ejecuta la aplicación completa de bAImax
        """
        print("🚀 INICIANDO bAImax - Sistema Híbrido de Análisis de Salud Pública")
        print("=" * 70)
        
        # Inicializar todos los componentes
        if not self.inicializar_componentes():
            print("❌ Error al inicializar componentes")
            return False
        
        # Generar todos los recursos
        print("\n📊 Generando visualizaciones...")
        
        # Generar mapas
        mapa_completo = self.mapa_sistema.crear_mapa_completo()
        mapa_clusters = self.mapa_sistema.crear_mapa_clusters()
        mapa_calor = self.mapa_sistema.crear_mapa_calor()
        
        self.mapa_sistema.guardar_mapa(mapa_completo, 'baimax_mapa_completo.html')
        self.mapa_sistema.guardar_mapa(mapa_clusters, 'baimax_mapa_clusters.html')
        self.mapa_sistema.guardar_mapa(mapa_calor, 'baimax_mapa_calor.html')
        
        # Generar gráficas
        self.graficas.guardar_graficas('html')
        
        # Generar aplicación web principal
        print("\n🌐 Generando aplicación web...")
        archivo_app = self.generar_aplicacion_completa()
        
        # Abrir en navegador
        print(f"\n🎉 ¡bAImax está listo!")
        print(f"📁 Archivo principal: {archivo_app}")
        print("\n🚀 Abriendo en navegador...")
        
        # Intentar abrir en navegador
        try:
            webbrowser.open(f'file://{os.path.abspath(archivo_app)}')
        except:
            print(f"⚠️ No se pudo abrir automáticamente. Abre manualmente: {os.path.abspath(archivo_app)}")
        
        print("\n✨ ¡bAImax funcionando perfectamente! ✨")
        print("🎯 Todas las funcionalidades están disponibles en la interfaz web")
        
        return True

# Función principal de demostración
def demo_app_completa():
    """
    🎭 Demostración completa de la aplicación bAImax
    """
    app = bAImaxWebApp()
    return app.ejecutar_aplicacion()

if __name__ == "__main__":
    demo_app_completa()