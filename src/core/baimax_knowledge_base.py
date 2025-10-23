"""
🧠 bAImax Knowledge Base - Base de Conocimientos Inteligente
===========================================================

Sistema de conocimientos avanzado para entrenar el chatbot bAImax con:
- Información detallada de ciudades colombianas
- Casos de salud pública específicos
- Protocolos de atención médica
- Datos epidemiológicos y sanitarios
"""

import pandas as pd
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class bAImaxKnowledgeBase:
    """
    🧠 Base de conocimientos especializada en salud pública colombiana
    """
    
    def __init__(self):
        self.version = "1.0"
        self.ultima_actualizacion = datetime.now()
        
        # Bases de conocimiento
        self.ciudades_colombia = {}
        self.casos_salud = {}
        self.protocolos_atencion = {}
        self.entidades_salud = {}
        self.sintomas_enfermedades = {}
        
        # Inicializar conocimientos
        self._cargar_ciudades_colombia()
        self._cargar_casos_salud()
        self._cargar_protocolos_atencion()
        self._cargar_entidades_salud()
        self._cargar_sintomas_enfermedades()
        
        print("🧠 Base de conocimientos bAImax inicializada")
        print(f"📊 {len(self.ciudades_colombia)} ciudades cargadas")
        print(f"🏥 {len(self.casos_salud)} casos de salud registrados")
        print(f"📋 {len(self.protocolos_atencion)} protocolos de atención")
    
    def _cargar_ciudades_colombia(self):
        """Cargar información detallada de ciudades colombianas"""
        self.ciudades_colombia = {
            "bogota": {
                "nombre": "Bogotá D.C.",
                "poblacion": 7_181_469,
                "departamento": "Cundinamarca",
                "altitud": 2640,
                "clima": "Frío de montaña",
                "problemas_comunes": [
                    "Enfermedades respiratorias por altura",
                    "Contaminación del aire",
                    "Estrés urbano",
                    "Problemas cardiovasculares"
                ],
                "hospitales_principales": [
                    "Hospital Universitario San Ignacio",
                    "Fundación Santa Fe de Bogotá",
                    "Hospital El Tunal",
                    "Hospital de La Misericordia"
                ],
                "eps_principales": [
                    "Compensar EPS",
                    "Sanitas EPS", 
                    "Nueva EPS",
                    "Salud Total EPS"
                ],
                "zonas_criticas": [
                    "Ciudad Bolívar",
                    "Bosa",
                    "Kennedy",
                    "Suba"
                ]
            },
            "medellin": {
                "nombre": "Medellín",
                "poblacion": 2_569_846,
                "departamento": "Antioquia",
                "altitud": 1495,
                "clima": "Templado",
                "problemas_comunes": [
                    "Dengue y enfermedades tropicales",
                    "Violencia urbana",
                    "Drogadicción",
                    "Embarazos adolescentes"
                ],
                "hospitales_principales": [
                    "Hospital Pablo Tobón Uribe",
                    "Clínica Las Vegas",
                    "Hospital General de Medellín",
                    "Clínica CES"
                ],
                "eps_principales": [
                    "Sura EPS",
                    "Coomeva EPS",
                    "Nueva EPS",
                    "Sanitas EPS"
                ],
                "zonas_criticas": [
                    "Comuna 1 - Popular",
                    "Comuna 13 - San Javier",
                    "Comuna 3 - Manrique",
                    "Comuna 8 - Villa Hermosa"
                ]
            },
            "cali": {
                "nombre": "Santiago de Cali",
                "poblacion": 2_252_616,
                "departamento": "Valle del Cauca",
                "altitud": 1018,
                "clima": "Tropical seco",
                "problemas_comunes": [
                    "Enfermedades tropicales",
                    "Deshidratación por calor",
                    "Dengue y chikungunya",
                    "Violencia intrafamiliar"
                ],
                "hospitales_principales": [
                    "Fundación Valle del Lili",
                    "Hospital Universitario del Valle",
                    "Clínica Imbanaco",
                    "Hospital San Juan de Dios"
                ],
                "eps_principales": [
                    "Emssanar EPS",
                    "Sura EPS",
                    "Nueva EPS",
                    "Sanitas EPS"
                ],
                "zonas_criticas": [
                    "Aguablanca",
                    "Ladera",
                    "Siloé",
                    "Terrón Colorado"
                ]
            },
            "barranquilla": {
                "nombre": "Barranquilla",
                "poblacion": 1_274_250,
                "departamento": "Atlántico",
                "altitud": 18,
                "clima": "Tropical cálido",
                "problemas_comunes": [
                    "Enfermedades tropicales",
                    "Deshidratación severa",
                    "Infecciones intestinales",
                    "Problemas dermatológicos"
                ],
                "hospitales_principales": [
                    "Clínica Portoazul",
                    "Hospital Universidad del Norte",
                    "Clínica Bautista",
                    "Hospital Niño Jesús"
                ],
                "eps_principales": [
                    "Coosalud EPS",
                    "Nueva EPS",
                    "Sanitas EPS",
                    "Sura EPS"
                ]
            }
        }
    
    def _cargar_casos_salud(self):
        """Cargar casos específicos de salud pública"""
        self.casos_salud = {
            "enfermedades_respiratorias": {
                "sintomas": ["tos", "fiebre", "dificultad respirar", "dolor pecho"],
                "causas_comunes": ["contaminación", "altura", "clima frío", "virus"],
                "ciudades_afectadas": ["bogota", "tunja", "pasto"],
                "protocolo": "respiratorio_general",
                "gravedad": "MODERADO",
                "especialista": "neumólogo"
            },
            "dengue": {
                "sintomas": ["fiebre alta", "dolor cabeza", "dolor muscular", "manchas rojas"],
                "causas_comunes": ["mosquito aedes", "aguas estancadas", "clima tropical"],
                "ciudades_afectadas": ["cali", "medellin", "barranquilla", "cartagena"],
                "protocolo": "enfermedades_tropicales",
                "gravedad": "GRAVE",
                "especialista": "infectólogo"
            },
            "hipertension": {
                "sintomas": ["dolor cabeza", "mareos", "vision borrosa", "fatiga"],
                "causas_comunes": ["estrés", "mala alimentación", "sedentarismo"],
                "ciudades_afectadas": ["bogota", "medellin", "cali", "bucaramanga"],
                "protocolo": "cardiovascular",
                "gravedad": "GRAVE",
                "especialista": "cardiólogo"
            },
            "gastroenteritis": {
                "sintomas": ["diarrea", "vómito", "dolor abdominal", "deshidratación"],
                "causas_comunes": ["agua contaminada", "alimentos", "virus", "bacterias"],
                "ciudades_afectadas": ["barranquilla", "cartagena", "santa_marta"],
                "protocolo": "gastrointestinal",
                "gravedad": "MODERADO",
                "especialista": "gastroenterólogo"
            },
            "depresion": {
                "sintomas": ["tristeza", "fatiga", "insomnio", "pérdida apetito"],
                "causas_comunes": ["estrés", "problemas sociales", "violencia", "desempleo"],
                "ciudades_afectadas": ["bogota", "medellin", "cali", "cucuta"],
                "protocolo": "salud_mental",
                "gravedad": "GRAVE",
                "especialista": "psiquiatra"
            }
        }
    
    def _cargar_protocolos_atencion(self):
        """Cargar protocolos específicos de atención"""
        self.protocolos_atencion = {
            "respiratorio_general": {
                "pasos": [
                    "1. Evaluar saturación de oxígeno",
                    "2. Verificar temperatura corporal",
                    "3. Escuchar pulmones",
                    "4. Ordenar radiografía si es necesario",
                    "5. Prescribir tratamiento según síntomas"
                ],
                "tiempo_atencion": "30 minutos",
                "nivel_urgencia": "MODERADO"
            },
            "enfermedades_tropicales": {
                "pasos": [
                    "1. Toma de signos vitales urgente",
                    "2. Examen físico completo",
                    "3. Prueba rápida dengue/chikungunya",
                    "4. Hidratación inmediata",
                    "5. Monitoreo 24 horas si es necesario"
                ],
                "tiempo_atencion": "45 minutos",
                "nivel_urgencia": "GRAVE"
            },
            "salud_mental": {
                "pasos": [
                    "1. Evaluación psicológica inicial",
                    "2. Identificar factores de riesgo",
                    "3. Aplicar escalas de depresión/ansiedad",
                    "4. Plan de tratamiento psicoterapéutico",
                    "5. Seguimiento programado"
                ],
                "tiempo_atencion": "60 minutos",
                "nivel_urgencia": "GRAVE"
            }
        }
    
    def _cargar_entidades_salud(self):
        """Cargar entidades de salud por especialidad"""
        self.entidades_salud = {
            "emergencias": {
                "telefono": "123",
                "descripcion": "Número único de emergencias Colombia"
            },
            "linea_salud": {
                "telefono": "018000-910097",
                "descripcion": "Línea gratuita del Ministerio de Salud"
            },
            "salud_mental": {
                "telefono": "106",
                "descripcion": "Línea Nacional de Salud Mental"
            },
            "violencia_intrafamiliar": {
                "telefono": "155",
                "descripcion": "Línea Nacional contra Violencia Intrafamiliar"
            }
        }
    
    def _cargar_sintomas_enfermedades(self):
        """Cargar mapeo de síntomas a posibles enfermedades"""
        self.sintomas_enfermedades = {
            "fiebre": ["dengue", "gripa", "infección", "covid19"],
            "tos": ["enfermedades_respiratorias", "covid19", "bronquitis"],
            "dolor_cabeza": ["hipertension", "dengue", "migraña", "estrés"],
            "diarrea": ["gastroenteritis", "intoxicación", "virus"],
            "mareos": ["hipertension", "anemia", "deshidratación"],
            "fatiga": ["depresion", "anemia", "estrés", "hipertension"],
            "dolor_pecho": ["enfermedades_respiratorias", "problemas_cardiacos", "ansiedad"]
        }
    
    def buscar_informacion_ciudad(self, ciudad: str) -> Dict:
        """Buscar información específica de una ciudad"""
        ciudad_key = ciudad.lower().replace(' ', '_')
        return self.ciudades_colombia.get(ciudad_key, {})
    
    def analizar_sintomas(self, sintomas: List[str]) -> List[Dict]:
        """Analizar síntomas y sugerir posibles enfermedades"""
        posibles_enfermedades = []
        
        for sintoma in sintomas:
            sintoma_clean = sintoma.lower().replace(' ', '_')
            if sintoma_clean in self.sintomas_enfermedades:
                for enfermedad in self.sintomas_enfermedades[sintoma_clean]:
                    if enfermedad in self.casos_salud:
                        posibles_enfermedades.append({
                            "enfermedad": enfermedad,
                            "info": self.casos_salud[enfermedad],
                            "coincidencia_sintomas": sintoma
                        })
        
        return posibles_enfermedades
    
    def obtener_protocolo_atencion(self, tipo_caso: str) -> Dict:
        """Obtener protocolo de atención específico"""
        return self.protocolos_atencion.get(tipo_caso, {})
    
    def generar_respuesta_contextual(self, problema: str, ciudad: Optional[str] = None) -> Dict:
        """Generar respuesta contextual basada en conocimientos"""
        respuesta = {
            "problema_detectado": problema,
            "ciudad": ciudad,
            "recomendaciones": [],
            "informacion_adicional": [],
            "nivel_urgencia": "MODERADO"
        }
        
        # Analizar ciudad si se proporciona
        if ciudad:
            info_ciudad = self.buscar_informacion_ciudad(ciudad)
            if info_ciudad:
                respuesta["informacion_adicional"].append(f"📍 En {info_ciudad['nombre']} es común ver:")
                for problema_comun in info_ciudad.get('problemas_comunes', []):
                    respuesta["informacion_adicional"].append(f"   • {problema_comun}")
        
        # Buscar palabras clave en casos de salud
        for caso_key, caso_info in self.casos_salud.items():
            if any(word in problema.lower() for word in caso_info['sintomas']):
                respuesta["nivel_urgencia"] = caso_info['gravedad']
                respuesta["recomendaciones"].append(f"🏥 Recomiendo consultar con: {caso_info['especialista']}")
                
                protocolo = self.obtener_protocolo_atencion(caso_info['protocolo'])
                if protocolo:
                    respuesta["informacion_adicional"].append("📋 Protocolo de atención:")
                    for paso in protocolo.get('pasos', []):
                        respuesta["informacion_adicional"].append(f"   {paso}")
        
        return respuesta
    
    def guardar_conocimientos(self, archivo: str = "src/data/baimax_knowledge_base.json"):
        """Guardar base de conocimientos en archivo"""
        conocimientos = {
            "version": self.version,
            "ultima_actualizacion": self.ultima_actualizacion.isoformat(),
            "ciudades_colombia": self.ciudades_colombia,
            "casos_salud": self.casos_salud,
            "protocolos_atencion": self.protocolos_atencion,
            "entidades_salud": self.entidades_salud,
            "sintomas_enfermedades": self.sintomas_enfermedades
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(conocimientos, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Base de conocimientos guardada en: {archivo}")
    
    def cargar_conocimientos(self, archivo: str = "src/data/baimax_knowledge_base.json"):
        """Cargar base de conocimientos desde archivo"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                conocimientos = json.load(f)
            
            self.ciudades_colombia = conocimientos.get('ciudades_colombia', {})
            self.casos_salud = conocimientos.get('casos_salud', {})
            self.protocolos_atencion = conocimientos.get('protocolos_atencion', {})
            self.entidades_salud = conocimientos.get('entidades_salud', {})
            self.sintomas_enfermedades = conocimientos.get('sintomas_enfermedades', {})
            
            print(f"📂 Base de conocimientos cargada desde: {archivo}")
            
        except FileNotFoundError:
            print(f"⚠️  Archivo {archivo} no encontrado, usando conocimientos por defecto")


# Funciones de utilidad para el entrenamiento del chatbot
def entrenar_chatbot_con_conocimientos():
    """
    🎓 Función principal para entrenar el chatbot con la base de conocimientos
    """
    print("🎓 Iniciando entrenamiento avanzado del chatbot bAImax...")
    
    # Crear base de conocimientos
    knowledge_base = bAImaxKnowledgeBase()
    
    # Guardar conocimientos
    knowledge_base.guardar_conocimientos()
    
    print("✅ Entrenamiento completado!")
    print("🤖 El chatbot ahora tiene conocimientos sobre:")
    print(f"   📍 {len(knowledge_base.ciudades_colombia)} ciudades colombianas")
    print(f"   🏥 {len(knowledge_base.casos_salud)} casos de salud específicos")
    print(f"   📋 {len(knowledge_base.protocolos_atencion)} protocolos de atención")
    print(f"   🩺 {len(knowledge_base.sintomas_enfermedades)} mapeos síntoma-enfermedad")
    
    return knowledge_base


if __name__ == "__main__":
    # Ejecutar entrenamiento
    knowledge_base = entrenar_chatbot_con_conocimientos()
    
    # Ejemplo de uso
    print("\n" + "="*60)
    print("🧪 DEMOSTRACIÓN DE CONOCIMIENTOS")
    print("="*60)
    
    # Buscar información de ciudad
    info_bogota = knowledge_base.buscar_informacion_ciudad("bogota")
    print(f"\n📍 Información de Bogotá:")
    print(f"   Población: {info_bogota['poblacion']:,}")
    print(f"   Problemas comunes: {', '.join(info_bogota['problemas_comunes'][:2])}")
    
    # Analizar síntomas
    sintomas_ejemplo = ["fiebre", "dolor_cabeza", "tos"]
    enfermedades = knowledge_base.analizar_sintomas(sintomas_ejemplo)
    print(f"\n🩺 Síntomas: {', '.join(sintomas_ejemplo)}")
    print(f"   Posibles enfermedades: {len(enfermedades)} encontradas")
    
    # Generar respuesta contextual
    respuesta = knowledge_base.generar_respuesta_contextual(
        "Tengo fiebre y dolor de cabeza en Bogotá", 
        "bogota"
    )
    print(f"\n🤖 Análisis contextual:")
    print(f"   Nivel urgencia: {respuesta['nivel_urgencia']}")
    print(f"   Recomendaciones: {len(respuesta['recomendaciones'])}")