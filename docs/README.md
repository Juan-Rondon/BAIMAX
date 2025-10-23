# 🧽🤖 bAImax - Sistema Híbrido de Análisis de Salud Pública

[![SENASOFT 2025](https://img.shields.io/badge/SENASOFT-2025-blue.svg)](https://github.com/naobw85/SenaSoft_2025)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-green.svg)](https://python.org)
[![ML Ready](https://img.shields.io/badge/ML-Ready-red.svg)](https://scikit-learn.org)

> **Sistema Híbrido de Análisis Inteligente desarrollado para SENASOFT 2025**  
> Combina 🧽 SpongeBob (baby) + 🤖 Inteligencia Artificial + ⚡ Optimización (max)

## 🎯 **Descripción del Proyecto**

## 🏆 **Características Principales**

### 🤖 **Clasificación con IA**
- Modelo de Machine Learning (Ensemble de 3 Algoritmos)
- Clasificación automática: **GRAVE** vs **MODERADO**
- Precisión del modelo: **55%** con validación cruzada
- Procesamiento de texto en español

### 🗺️ **Mapas Interactivos**
- **3 tipos de visualización:** Completo, Clusters, Mapa de Calor
- **10 ciudades colombianas** con coordenadas precisas
- Marcadores dinámicos por gravedad y frecuencia
- Tecnología **Folium** con capas intercambiables

### 📊 **Dashboard Analítico**
- **7 gráficas interactivas** con Plotly
- Análisis demográfico, temporal y geográfico
- Correlaciones y patrones de datos
- Exportación de visualizaciones

### 🎯 **Sistema de Recomendaciones**
- **25+ entidades de salud** registradas
- Algoritmo de matching semántico
- Cobertura en **5 ciudades principales**
- Recomendaciones contextuales por problema

### 🌐 **Interfaz Web Completa**
- Aplicación web integrada y responsive
- Navegación fluida entre componentes
- Diseño profesional y atractivo
- Compatible con todos los navegadores

## 🔧 **Tecnologías Utilizadas**

| Categoría | Tecnología | Uso |
|-----------|------------|-----|
| 🤖 **Machine Learning** | scikit-learn | Clasificación Ensemble de 3 Algoritmos |
| 🗺️ **Mapas** | Folium | Mapas interactivos con marcadores y capas |
| 📊 **Gráficas** | Plotly | Visualizaciones interactivas y dashboards |
| 🐍 **Backend** | Python 3.14 | Procesamiento de datos y lógica de negocio |
| 🌐 **Frontend** | HTML/CSS/JS | Interfaz web responsive y moderna |
| 📁 **Datos** | Pandas/NumPy | Manipulación y análisis de datasets |

## 📁 **Estructura del Proyecto**

```
bAImax/
├── 📊 Dataset y Datos
│   ├── dataset_salud_final_optimizado.csv    # Dataset principal (100 registros)
│   └── dataset_comunidades_senasoft.csv     # Dataset original
├── 🤖 Módulos Principales
│   ├── baimax_core.py                       # Clasificador IA y análisis
│   ├── baimax_mapas.py                      # Sistema de mapas interactivos
│   ├── baimax_graficas.py                   # Dashboard y visualizaciones
│   └── baimax_recomendaciones.py            # Motor de recomendaciones
├── 🌐 Aplicación Web
│   ├── baimax_app.py                        # Aplicación principal
│   └── baimax_app.html                      # Interfaz web completa
├── 🗺️ Mapas Generados
│   ├── baimax_mapa_completo.html            # Mapa general
│   ├── baimax_mapa_clusters.html            # Mapa por clusters
│   └── baimax_mapa_calor.html               # Mapa de intensidad
├── 📈 Gráficas Interactivas
│   ├── baimax_distribucion_gravedad.html    # Distribución circular
│   ├── baimax_problemas_ciudad.html         # Problemas por ciudad
│   ├── baimax_evolucion_temporal.html       # Evolución en el tiempo
│   ├── baimax_top_problemas.html            # Ranking de problemas
│   ├── baimax_demografica.html              # Análisis demográfico
│   ├── baimax_heatmap.html                  # Matriz ciudad-problema
│   └── baimax_correlaciones.html            # Correlaciones variables
├── 🤖 Modelo Entrenado
│   └── baimax_modelo.pkl                    # Modelo ML serializado
└── 📚 Documentación
    ├── demo_final.py                        # Demostración completa
    └── README.md                            # Este archivo
```

## 🚀 **Instalación y Configuración**

### **Prerequisitos**
- Python 3.14+
- Git instalado
- Navegador web moderno

### **1. Clonar el Repositorio**
```bash
git clone https://github.com/naobw85/SenaSoft_2025.git
cd SenaSoft_2025
```

### **2. Instalar Dependencias**
```bash
pip install pandas numpy scikit-learn plotly folium matplotlib seaborn
```

### **3. Ejecutar bAImax**
```bash
python baimax_app.py
```

El sistema se iniciará automáticamente y abrirá `baimax_app.html` en tu navegador.

## 🎮 **Uso del Sistema**

### **🌐 Interfaz Principal**
1. **Inicio:** Estadísticas generales del sistema
2. **Clasificador IA:** Demostración del modelo ML
3. **Mapas:** Visualización geográfica interactiva
4. **Gráficas:** Dashboard de análisis completo
5. **Recomendaciones:** Sistema de matching inteligente
6. **Dataset:** Información del corpus de datos

### **🤖 Clasificación de Problemas**
```python
from baimax_core import bAImaxClassifier

# Inicializar clasificador
clasificador = bAImaxClassifier()
clasificador.cargar_modelo()  # o entrenar() para nuevo modelo

# Clasificar problema
resultado = clasificador.predecir("faltan médicos en el centro de salud")
print(f"Gravedad: {resultado['gravedad']}")
print(f"Confianza: {resultado['confianza']:.1%}")
```

### **🗺️ Generar Mapas**
```python
from baimax_mapas import bAImaxMapa

# Crear sistema de mapas
mapa_sistema = bAImaxMapa()

# Generar mapa completo
mapa = mapa_sistema.crear_mapa_completo()
mapa_sistema.guardar_mapa(mapa, 'mi_mapa.html')
```

### **🎯 Obtener Recomendaciones**
```python
from baimax_recomendaciones import bAImaxRecomendaciones

# Sistema de recomendaciones
recomendador = bAImaxRecomendaciones()

# Buscar puntos de atención
resultado = recomendador.recomendar_puntos_atencion(
    "problemas de agua potable", 
    "Bogotá"
)
print(f"Recomendaciones: {len(resultado['recomendaciones'])}")
```

## � **Dataset y Datos**

### **Características del Dataset**
- **📋 100 registros únicos** sin duplicados
- **🏙️ 10 ciudades** colombianas principales
- **🏥 10 tipos** de problemas de salud pública
- **⚖️ Balance:** 60% GRAVE / 40% MODERADO
- **✅ Calidad:** 0% valores nulos, 100% validado

### **Variables Principales**
- `Comentario`: Descripción del problema reportado
- `Nivel_gravedad`: GRAVE o MODERADO (target ML)
- `Ciudad`: Ubicación geográfica del reporte
- `Edad`, `Genero`: Información demográfica
- `Zona_rural`: Ubicación urbana/rural
- `Fecha_reporte`: Timestamp del reporte

## 📈 **Métricas y Rendimiento**

### **🤖 Modelo de Machine Learning**
- **Algoritmo:** TF-IDF Vectorizer + Logistic Regression
- **Precisión:** 55.0% en conjunto de prueba
- **Validación Cruzada:** 52.8% (5-fold)
- **Clases:** Binaria (GRAVE/MODERADO)
- **Features:** Texto vectorizado + metadatos

### **📊 Estadísticas del Sistema**
- **Entidades de Salud:** 25+ registradas
- **Cobertura Geográfica:** 5 ciudades principales
- **Tipos de Problemas:** 13 categorías mapeadas
- **Tiempo de Respuesta:** <2 segundos por consulta
- **Visualizaciones:** 17 archivos HTML generados

## 🎯 **Casos de Uso**

### **🏛️ Para Autoridades Públicas**
- Monitoreo en tiempo real de problemas de salud
- Priorización automática según gravedad
- Identificación de patrones geográficos y temporales
- Optimización de recursos y respuesta

### **👥 Para Ciudadanos**
- Reporte fácil de problemas de salud
- Recomendaciones automáticas de puntos de atención
- Visualización del estado de su zona
- Seguimiento de resolución de problemas

### **🏥 Para Entidades de Salud**
- Dashboard de problemas en su área de cobertura
- Análisis predictivo de demanda
- Coordinación entre instituciones
- Métricas de impacto y efectividad

## 🚀 **Roadmap Futuro**

### **� Mejoras de IA (Fase 2)**
- [ ] Implementar modelos de deep learning (LSTM/BERT)
- [ ] Análisis de sentimientos en comentarios
- [ ] Predicción de tendencias futuras
- [ ] Clustering automático de problemas similares

### **🌍 Expansión Geográfica (Fase 3)**
- [ ] Incluir municipios rurales
- [ ] Mapeo de corregimientos y veredas
- [ ] Coordinación con entidades territoriales
- [ ] Cobertura nacional completa

### **📱 Plataforma Digital (Fase 4)**
- [ ] Aplicación móvil para reportes ciudadanos
- [ ] API REST para integración externa
- [ ] Dashboard en tiempo real
- [ ] Sistema de notificaciones automáticas

### **🏥 Integración Institucional (Fase 5)**
- [ ] Conectar con SISPRO-MSPS
- [ ] API con alcaldías municipales
- [ ] Dashboard para autoridades de salud
- [ ] Reportes automatizados y alertas

## � **Equipo de Desarrollo**

**🏆 SENASOFT 2025**
- **Desarrollador Principal:** Sistema bAImax
- **Institución:** Competencia Nacional SENASOFT
- **Fecha:** Octubre 2025
- **Tecnologías:** Python, ML, Folium, Plotly

## 📄 **Licencia**

Este proyecto fue desarrollado para **SENASOFT 2025** como demostración de capacidades en:
- Inteligencia Artificial y Machine Learning
- Análisis de Datos y Visualización
- Desarrollo de Sistemas Web
- Soluciones de Salud Pública Digital

## 🤝 **Contribuciones**

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## � **Contacto y Soporte**

- **Proyecto:** [SenaSoft_2025](https://github.com/naobw85/SenaSoft_2025)
- **Issues:** [GitHub Issues](https://github.com/naobw85/SenaSoft_2025/issues)
- **Documentación:** Ver archivos del proyecto

## 🎉 **Agradecimientos**

- **SENASOFT 2025** por la oportunidad de desarrollo
- **Comunidad Python** por las excelentes librerías
- **OpenStreetMap** por los datos geográficos
- **Colombia** por ser el contexto de aplicación

---

<div align="center">

**🧽🤖 bAImax - Donde la Inteligencia Artificial se encuentra con la Salud Pública 🇨🇴**

[![GitHub Stars](https://img.shields.io/github/stars/naobw85/SenaSoft_2025?style=social)](https://github.com/naobw85/SenaSoft_2025/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/naobw85/SenaSoft_2025?style=social)](https://github.com/naobw85/SenaSoft_2025/network/members)

**Hecho con ❤️ para SENASOFT 2025**

</div>

---

**¡Dataset listo para entrenar tu próximo modelo de IA! 🚀**