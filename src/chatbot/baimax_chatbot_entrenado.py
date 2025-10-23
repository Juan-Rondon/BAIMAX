"""
🤖 bAImax Chatbot ENTRENADO - Motor de Conversación Inteligente Avanzado
========================================================================

Sistema de chatbot integrado para bAImax 2.0 que permite:
- Conversación natural en español
- Clasificación automática de problemas  
- Análisis avanzado de síntomas
- Conocimientos específicos de ciudades colombianas
- Protocolos de atención médica
- Recomendaciones contextuales inteligentes
- Aprendizaje de nuevos reportes
"""

import pandas as pd
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

# Importar módulos bAImax existentes
from baimax_core import bAImaxClassifier, bAImaxAnalyzer
from baimax_recomendaciones import bAImaxRecomendaciones
from baimax_knowledge_base import bAImaxKnowledgeBase

class bAImaxChatbotEntrenado:
    """
    🧠 Motor de chatbot inteligente entrenado para bAImax 2.0
    """
    
    def __init__(self):
        self.nombre = "bAImax Assistant Entrenado"
        self.version = "2.0 - Conocimientos Avanzados"
        self.personalidad = "asistente médico inteligente especializado en salud pública colombiana"
        
        # Inicializar componentes de bAImax
        self.clasificador = None
        self.recomendador = None
        self.analyzer = None
        
        # Nueva base de conocimientos avanzada
        self.knowledge_base = bAImaxKnowledgeBase()
        
        # Sistema de conversación
        self.conversacion_activa = []
        self.contexto_usuario = {}
        self.ultimo_problema_reportado = None
        
        # Patrones de conversación mejorados
        self.patrones_saludo = [
            r"hola|hi|hello|buenos días|buenas tardes|buenas noches|saludos",
            r"hey|que tal|como estas|que hay|buen día"
        ]
        
        self.patrones_despedida = [
            r"adiós|bye|hasta luego|nos vemos|gracias|chao|hasta pronto",
            r"eso es todo|ya termine|no necesito más ayuda|me voy"
        ]
        
        self.patrones_problema = [
            r"tengo|hay|necesito|problema|urgente|ayuda|dolor|enfermo",
            r"me duele|siento|malestar|síntoma|fiebre|tos|diarrea"
        ]
        
        self.patrones_ubicacion = [
            r"en (.+?)(?:\s|$)",
            r"desde (.+?)(?:\s|$)", 
            r"vivo en (.+?)(?:\s|$)",
            r"estoy en (.+?)(?:\s|$)"
        ]
        
        print(f"🧠 {self.nombre} v{self.version} inicializado")
        print(f"📚 Base de conocimientos: {len(self.knowledge_base.ciudades_colombia)} ciudades, {len(self.knowledge_base.casos_salud)} casos de salud")
    
    def inicializar_sistema(self):
        """
        🚀 Inicializa todos los componentes de bAImax
        """
        try:
            print("🤖 Inicializando bAImax Chatbot Entrenado...")
            
            # Inicializar clasificador
            self.clasificador = bAImaxClassifier()
            
            # Inicializar recomendador 
            self.recomendador = bAImaxRecomendaciones()
            
            # Inicializar analyzer
            self.analyzer = bAImaxAnalyzer()
            
            print("✅ bAImax Chatbot Entrenado inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando chatbot: {e}")
    
    def detectar_intencion(self, mensaje: str) -> str:
        """
        🎯 Detecta la intención del mensaje del usuario (mejorado)
        """
        mensaje_lower = mensaje.lower()
        
        # Detectar saludo
        for patron in self.patrones_saludo:
            if re.search(patron, mensaje_lower):
                return "saludo"
        
        # Detectar despedida
        for patron in self.patrones_despedida:
            if re.search(patron, mensaje_lower):
                return "despedida"
        
        # Detectar problema de salud (análisis avanzado)
        for patron in self.patrones_problema:
            if re.search(patron, mensaje_lower):
                return "problema_salud"
        
        # Detectar solicitud de ubicación
        for patron in self.patrones_ubicacion:
            if re.search(patron, mensaje_lower):
                return "ubicacion"
        
        # Análisis de síntomas específicos
        sintomas_medicos = ["fiebre", "tos", "dolor", "mareos", "fatiga", "diarrea", "vomito", "nauseas"]
        if any(sintoma in mensaje_lower for sintoma in sintomas_medicos):
            return "sintomas"
        
        # Si contiene palabras relacionadas con salud pública
        palabras_salud = ["médico", "hospital", "agua", "basura", "luz", "internet", "seguridad", "educación"]
        if any(palabra in mensaje_lower for palabra in palabras_salud):
            return "problema_publico"
        
        return "conversacion_general"
    
    def extraer_ubicacion(self, mensaje: str) -> Optional[str]:
        """
        📍 Extrae la ubicación del mensaje del usuario (mejorado)
        """
        mensaje_lower = mensaje.lower()
        
        # Buscar en base de conocimientos de ciudades
        for ciudad_key in self.knowledge_base.ciudades_colombia.keys():
            ciudad_clean = ciudad_key.replace('_', ' ')
            if ciudad_clean in mensaje_lower or ciudad_key in mensaje_lower:
                return self.knowledge_base.ciudades_colombia[ciudad_key]['nombre']
        
        # Patrones con regex
        for patron in self.patrones_ubicacion:
            match = re.search(patron, mensaje_lower)
            if match:
                ubicacion_extraida = match.group(1).strip()
                # Buscar coincidencias en las ciudades conocidas
                for ciudad_key in self.knowledge_base.ciudades_colombia.keys():
                    if ciudad_key in ubicacion_extraida:
                        return self.knowledge_base.ciudades_colombia[ciudad_key]['nombre']
        
        return None
    
    def analizar_sintomas_usuario(self, mensaje: str) -> Dict[str, Any]:
        """
        🩺 Análisis avanzado de síntomas usando la base de conocimientos
        """
        # Extraer posibles síntomas del mensaje
        sintomas_detectados = []
        sintomas_posibles = ["fiebre", "tos", "dolor cabeza", "mareos", "fatiga", "diarrea", "vomito", "dolor pecho", "nauseas"]
        
        mensaje_lower = mensaje.lower()
        for sintoma in sintomas_posibles:
            if sintoma in mensaje_lower:
                sintomas_detectados.append(sintoma.replace(' ', '_'))
        
        if sintomas_detectados:
            # Usar base de conocimientos para analizar
            enfermedades_posibles = self.knowledge_base.analizar_sintomas(sintomas_detectados)
            return {
                'sintomas_detectados': sintomas_detectados,
                'enfermedades_posibles': enfermedades_posibles,
                'tiene_sintomas': True
            }
        
        return {'tiene_sintomas': False}
    
    def generar_respuesta_contextual_avanzada(self, mensaje: str, ubicacion: Optional[str] = None) -> str:
        """
        🧠 Generar respuesta usando la base de conocimientos avanzada
        """
        # Análisis contextual con knowledge base
        respuesta_contextual = self.knowledge_base.generar_respuesta_contextual(mensaje, ubicacion)
        
        # Análisis de síntomas
        analisis_sintomas = self.analizar_sintomas_usuario(mensaje)
        
        # Construir respuesta inteligente
        respuesta_parts = []
        
        if analisis_sintomas['tiene_sintomas']:
            respuesta_parts.append("🩺 **He detectado posibles síntomas en tu mensaje.**")
            
            sintomas = analisis_sintomas['sintomas_detectados']
            respuesta_parts.append(f"📋 Síntomas identificados: {', '.join(sintomas).replace('_', ' ')}")
            
            enfermedades = analisis_sintomas['enfermedades_posibles']
            if enfermedades:
                respuesta_parts.append("\\n🔍 **Posibles condiciones a considerar:**")
                for enfermedad in enfermedades[:2]:  # Máximo 2
                    info = enfermedad['info']
                    nombre_enfermedad = enfermedad['enfermedad'].replace('_', ' ').title()
                    respuesta_parts.append(f"   • **{nombre_enfermedad}**")
                    respuesta_parts.append(f"     📊 Gravedad: {info['gravedad']}")
                    respuesta_parts.append(f"     👨‍⚕️ Especialista: {info['especialista']}")
        
        # Información de la ciudad si está disponible
        if ubicacion:
            info_ciudad = self.knowledge_base.buscar_informacion_ciudad(ubicacion)
            if info_ciudad:
                respuesta_parts.append(f"\\n📍 **Información de {info_ciudad['nombre']}:**")
                respuesta_parts.append(f"   👥 Población: {info_ciudad['poblacion']:,} habitantes")
                respuesta_parts.append(f"   🌡️ Clima: {info_ciudad['clima']}")
                if 'problemas_comunes' in info_ciudad:
                    respuesta_parts.append("   🏥 Problemas de salud comunes:")
                    for problema in info_ciudad['problemas_comunes'][:2]:
                        respuesta_parts.append(f"     • {problema}")
        
        # Nivel de urgencia
        respuesta_parts.append(f"\\n⚠️ **Nivel de urgencia estimado: {respuesta_contextual['nivel_urgencia']}**")
        
        # Recomendaciones específicas
        if respuesta_contextual['recomendaciones']:
            respuesta_parts.append("\\n💡 **Recomendaciones específicas:**")
            for rec in respuesta_contextual['recomendaciones']:
                respuesta_parts.append(f"   {rec}")
        
        # Números de emergencia relevantes
        respuesta_parts.append("\\n📞 **Números importantes:**")
        respuesta_parts.append("   🚨 Emergencias: 123")
        respuesta_parts.append("   🏥 Línea Salud: 018000-910097") 
        respuesta_parts.append("   🧠 Salud Mental: 106")
        
        respuesta_parts.append("\\n⚡ **Importante:** Esta es una evaluación automatizada. Consulta a un profesional médico para diagnóstico definitivo.")
        
        return '\\n'.join(respuesta_parts)
    
    def procesar_problema(self, mensaje: str, ubicacion: Optional[str] = None) -> Dict[str, Any]:
        """
        🔍 Procesa un problema reportado por el usuario (mejorado)
        """
        try:
            # Clasificar el problema si hay clasificador disponible
            resultado_clasificacion = None
            if self.clasificador:
                resultado_clasificacion = self.clasificador.predecir(mensaje)
            
            # Obtener recomendaciones si tenemos ubicación
            recomendaciones = []
            if ubicacion and self.recomendador:
                resultado_rec = self.recomendador.recomendar_puntos_atencion(mensaje, ubicacion)
                recomendaciones = resultado_rec.get('recomendaciones', [])
            
            # Guardar en contexto
            self.ultimo_problema_reportado = {
                'mensaje': mensaje,
                'ubicacion': ubicacion,
                'clasificacion': resultado_clasificacion,
                'recomendaciones': recomendaciones,
                'timestamp': datetime.now().isoformat()
            }
            
            return {
                'exito': True,
                'clasificacion': resultado_clasificacion,
                'recomendaciones': recomendaciones,
                'ubicacion': ubicacion
            }
            
        except Exception as e:
            print(f"❌ Error procesando problema: {e}")
            return {'exito': False, 'error': str(e)}
    
    def generar_respuesta(self, mensaje: str) -> Dict[str, Any]:
        """
        💭 Genera respuesta inteligente basada en el mensaje del usuario con conocimientos avanzados
        """
        # Agregar a conversación
        self.conversacion_activa.append({
            'usuario': mensaje,
            'timestamp': datetime.now().isoformat()
        })
        
        # Detectar intención
        intencion = self.detectar_intencion(mensaje)
        
        # Extraer ubicación si está presente
        ubicacion = self.extraer_ubicacion(mensaje)
        
        # Generar respuesta según intención
        respuesta_texto = ""
        acciones_sugeridas = []
        tipo_respuesta = intencion
        
        if intencion == "saludo":
            respuesta_texto = "¡Hola! 👋 Soy bAImax, tu asistente médico inteligente. Tengo conocimientos sobre salud pública en Colombia. ¿En qué puedo ayudarte?"
            
        elif intencion == "despedida":
            respuesta_texto = "¡Nos vemos! 🤖 bAImax siempre está aquí para ayudarte con tu salud. ¡Cuídate!"
            
        elif intencion == "sintomas" or intencion == "problema_salud":
            # Usar análisis avanzado para problemas de salud
            respuesta_texto = self.generar_respuesta_contextual_avanzada(mensaje, ubicacion)
            tipo_respuesta = "analisis_medico"
            
            # Procesar como problema para el sistema
            if self.clasificador:
                self.procesar_problema(mensaje, ubicacion)
            
        elif intencion == "problema_publico":
            # Procesar problema de salud pública tradicional
            resultado_proceso = self.procesar_problema(mensaje, ubicacion)
            
            if resultado_proceso['exito']:
                respuesta_texto = self._construir_respuesta_problema(resultado_proceso, mensaje)
            else:
                respuesta_texto = "He detectado que tienes un problema de salud pública. Para ayudarte mejor, ¿puedes ser más específico sobre tu ubicación?"
                
        else:
            # Conversación general
            respuesta_texto = "Estoy aquí para ayudarte con temas de salud pública. ¿Tienes algún problema médico o de salud que quieras consultarme?"
        
        # Construir respuesta final
        respuesta_final = {
            'mensaje': respuesta_texto,
            'tipo_respuesta': tipo_respuesta,
            'ubicacion_detectada': ubicacion,
            'acciones_sugeridas': acciones_sugeridas,
            'timestamp': datetime.now().isoformat()
        }
        
        # Agregar respuesta a conversación
        self.conversacion_activa.append({
            'bot': respuesta_texto,
            'tipo': tipo_respuesta,
            'timestamp': datetime.now().isoformat()
        })
        
        return respuesta_final
    
    def _construir_respuesta_problema(self, resultado: Dict, mensaje: str) -> str:
        """
        🏗️ Construir respuesta para problemas de salud pública
        """
        respuesta_parts = ["🤖 **Análisis de tu reporte:**", ""]
        
        # Clasificación
        if resultado['clasificacion']:
            clasificacion = resultado['clasificacion']
            if isinstance(clasificacion, dict):
                gravedad = clasificacion.get('prediccion', 'MODERADO')
                confianza = clasificacion.get('confianza', 0) * 100
                respuesta_parts.append(f"🔴 **Clasificación:** {gravedad}")
                respuesta_parts.append(f"📊 **Confianza:** {confianza:.1f}%")
        
        # Ubicación
        if resultado['ubicacion']:
            respuesta_parts.append(f"📍 **Ubicación:** {resultado['ubicacion']}")
        
        respuesta_parts.append(f'**📋 Problema analizado:** "{mensaje}"')
        respuesta_parts.append("")
        
        # Recomendaciones
        if resultado['recomendaciones']:
            respuesta_parts.append("🎯 **Puntos de atención recomendados:**")
            respuesta_parts.append("")
            
            for i, rec in enumerate(resultado['recomendaciones'][:2], 1):
                respuesta_parts.append(f"**{i}. {rec.get('tipo', 'Entidad')}: {rec.get('nombre', 'No disponible')}**")
                if rec.get('telefono'):
                    respuesta_parts.append(f"📞 {rec['telefono']}")
                if rec.get('direccion'):
                    respuesta_parts.append(f"📍 {rec['direccion']}")
                if rec.get('web'):
                    respuesta_parts.append(f"🌐 {rec['web']}")
                respuesta_parts.append("")
        
        respuesta_parts.append("✅ **Tu reporte ha sido registrado** y contribuirá a mejorar nuestro sistema.")
        respuesta_parts.append("")
        respuesta_parts.append("¿Te fue útil esta información? ¿Necesitas algo más?")
        
        return '\\n'.join(respuesta_parts)
    
    def obtener_estadisticas_conversacion(self) -> Dict[str, Any]:
        """
        📊 Obtiene estadísticas de la conversación actual
        """
        mensajes_usuario = [msg for msg in self.conversacion_activa if 'usuario' in msg]
        mensajes_bot = [msg for msg in self.conversacion_activa if 'bot' in msg]
        
        return {
            'mensajes_totales': len(self.conversacion_activa),
            'mensajes_usuario': len(mensajes_usuario),
            'mensajes_bot': len(mensajes_bot),
            'problemas_reportados': 1 if self.ultimo_problema_reportado else 0,
            'ubicacion_detectada': bool(self.ultimo_problema_reportado and self.ultimo_problema_reportado.get('ubicacion'))
        }
    
    def obtener_estadisticas_conocimiento(self) -> Dict[str, Any]:
        """
        📊 Obtener estadísticas de la base de conocimientos
        """
        return {
            'ciudades_disponibles': len(self.knowledge_base.ciudades_colombia),
            'casos_salud_registrados': len(self.knowledge_base.casos_salud),
            'protocolos_atencion': len(self.knowledge_base.protocolos_atencion),
            'mapeo_sintomas': len(self.knowledge_base.sintomas_enfermedades),
            'version_knowledge': self.knowledge_base.version
        }


def demo_chatbot_entrenado():
    """
    🎮 Demostración del chatbot con capacidades avanzadas de conocimiento
    """
    print("🚀 Iniciando bAImax 2.0 con Conocimientos Avanzados...")
    
    # Inicializar chatbot entrenado
    chatbot = bAImaxChatbotEntrenado()
    chatbot.inicializar_sistema()
    
    print("\\n" + "="*70)
    print("🧠 bAImax 2.0 - Chatbot Médico Inteligente")
    print("="*70)
    print("✨ Capacidades avanzadas:")
    print("   🏥 Conocimientos de ciudades colombianas")
    print("   🩺 Análisis avanzado de síntomas")
    print("   📋 Protocolos de atención médica")
    print("   🎯 Recomendaciones contextuales inteligentes")
    print("   🇨🇴 Especializado en salud pública de Colombia")
    print()
    
    # Mostrar estadísticas de conocimiento
    stats_know = chatbot.obtener_estadisticas_conocimiento()
    print("📊 Base de conocimientos cargada:")
    for key, value in stats_know.items():
        key_es = key.replace('_', ' ').title()
        print(f"   {key_es}: {value}")
    
    print("\\nEscribe 'salir' para terminar")
    print("💡 Ejemplos de consultas avanzadas:")
    print("   • 'Tengo fiebre y dolor de cabeza en Bogotá'")
    print("   • 'Hay diarrea y vómitos en Barranquilla'")
    print("   • 'Problemas de agua potable en Medellín'")
    print("   • 'Me siento muy triste y sin energía en Cali'")
    print()
    
    # Mensaje inicial
    respuesta_inicial = chatbot.generar_respuesta("hola")
    print(f"🤖 bAImax: {respuesta_inicial['mensaje']}")
    
    while True:
        try:
            mensaje = input("\\n👤 Tú: ")
            
            if mensaje.lower() in ['salir', 'exit', 'quit']:
                despedida = chatbot.generar_respuesta("adiós")
                print(f"\\n🤖 bAImax: {despedida['mensaje']}")
                break
            
            # Generar respuesta
            respuesta = chatbot.generar_respuesta(mensaje)
            print(f"\\n🤖 bAImax: {respuesta['mensaje']}")
            
            # Mostrar información adicional si es análisis médico
            if respuesta['tipo_respuesta'] == 'analisis_medico':
                print("\\n" + "="*50)
                print("💊 Este fue un análisis médico automatizado")
                print("⚡ Basado en conocimientos de salud colombiana")
                if respuesta['ubicacion_detectada']:
                    print(f"📍 Ubicación detectada: {respuesta['ubicacion_detectada']}")
                print("="*50)
                
        except KeyboardInterrupt:
            print(f"\\n\\n🤖 bAImax: ¡Hasta pronto! Cuida tu salud. 👋")
            break
        except Exception as e:
            print(f"\\n❌ Error: {e}")
    
    # Estadísticas finales
    stats = chatbot.obtener_estadisticas_conversacion()
    print(f"\\n📊 Estadísticas de la conversación:")
    print(f"   💬 Mensajes totales: {stats['mensajes_totales']}")
    print(f"   🏥 Problemas médicos reportados: {stats['problemas_reportados']}")
    print(f"   📍 Ubicación detectada: {'Sí' if stats['ubicacion_detectada'] else 'No'}")


if __name__ == "__main__":
    # Ejecutar entrenamiento de conocimientos primero
    print("🎓 Cargando base de conocimientos médicos avanzados...")
    
    try:
        # Entrenar conocimientos
        from baimax_knowledge_base import entrenar_chatbot_con_conocimientos
        entrenar_chatbot_con_conocimientos()
        
        print("\\n" + "="*60)
        print("🚀 bAImax 2.0 - Chatbot Médico Entrenado")
        print("="*60)
        
        # Ejecutar demo
        demo_chatbot_entrenado()
        
    except Exception as e:
        print(f"❌ Error ejecutando sistema: {e}")
        print("📚 Asegúrate de que todos los módulos estén disponibles")