"""
🤖 bAImax Chatbot - Motor de Conversación Inteligente
====================================================

Sistema de chatbot integrado para bAImax 2.0 que permite:
- Conversación natural en español
- Clasificación automática de problemas
- Recomendaciones contextuales en tiempo real
- Aprendizaje de nuevos reportes
"""

import pandas as pd
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

# Importar módulos bAImax existentes
from core.baimax_core import bAImaxClassifier, bAImaxAnalyzer
from core.baimax_recomendaciones import bAImaxRecomendaciones
from core.baimax_knowledge_base import bAImaxKnowledgeBase
from .conversation_manager import ConversationManager

# Importar nuevo motor de IA local
try:
    from baimax_ollama import bAImaxOllama
    OLLAMA_DISPONIBLE = True
except ImportError:
    OLLAMA_DISPONIBLE = False
    print("⚠️ baimax_ollama no disponible - usando modo básico")

class bAImaxChatbot:
    """
    🤖 Motor de chatbot inteligente para bAImax 2.0
    """
    
    def __init__(self):
        self.nombre = "bAImax Assistant"
        self.version = "2.0 - Entrenado"
        self.personalidad = "asistente inteligente especializado en salud pública colombiana"
        
        # Inicializar componentes de bAImax
        self.clasificador = None
        self.recomendador = None
        self.analyzer = None
        
        # Nueva base de conocimientos avanzada
        self.knowledge_base = bAImaxKnowledgeBase()
        
        # Gestor de conversación mejorado
        self.conversation_manager = ConversationManager()
        
        # Motor de IA local avanzada (Ollama)
        self.ollama = None
        if OLLAMA_DISPONIBLE:
            try:
                self.ollama = bAImaxOllama()
                if self.ollama.disponible:
                    print("🤖 Ollama IA conectado - Modo conversacional avanzado activado")
                else:
                    print("⚠️ Ollama instalado pero modelo no disponible")
            except Exception as e:
                print(f"⚠️ Error conectando Ollama: {e}")
        
        # Sistema de conversación
        self.conversacion_activa = []
        self.contexto_usuario = {}
        self.ultimo_problema_reportado = None
        self.esperando_detalles = False
        self.intentos_detalles = 0
        self.max_intentos_detalles = 2  # Máximo número de veces que pedirá detalles
        
        # Patrones de conversación
        self.patrones_saludo = [
            r"hola|hi|hello|buenos días|buenas tardes|buenas noches|saludos",
            r"hey|que tal|como estas|que hay"
        ]
        
        self.patrones_despedida = [
            r"adiós|bye|hasta luego|nos vemos|gracias|chao|hasta pronto",
            r"eso es todo|ya termine|no necesito más ayuda"
        ]
        
        self.patrones_problema = [
            r"tengo un problema|hay un problema|reportar|necesito ayuda",
            r"falta|no hay|está dañado|no funciona|problema con",
            r"médicos|agua|basura|luz|internet|seguridad|educación"
        ]
        
        self.patrones_ubicacion = [
            r"en (.*?)|ciudad de (.*?)|vivo en (.*?)|estoy en (.*?)",
            r"bogotá|medellín|cali|barranquilla|cartagena|cúcuta|bucaramanga|pereira|manizales|santa marta"
        ]
        
        # Respuestas preparadas
        self.respuestas_saludo = [
            "¡Hola! 👋 Soy bAImax, tu asistente de salud pública. ¿En qué puedo ayudarte hoy?",
            "¡Buen día! 🌟 Soy bAImax, aquí para ayudarte con problemas de salud pública. ¿Qué necesitas?",
            "¡Saludos! 🤖 Soy bAImax 2.0. Puedo ayudarte a reportar problemas y encontrar soluciones. ¿Cómo puedo asistirte?"
        ]
        
        self.respuestas_despedida = [
            "¡Hasta pronto! 👋 Gracias por usar bAImax. ¡Que tengas un excelente día!",
            "¡Adiós! 🌟 Recuerda que siempre puedes volver para reportar problemas o buscar ayuda.",
            "¡Nos vemos! 🤖 bAImax siempre está aquí para ayudarte con la salud pública."
        ]
        
    def inicializar_sistema(self):
        """
        🚀 Inicializa todos los componentes del chatbot
        """
        try:
            print("🤖 Inicializando bAImax Chatbot...")
            
            # Cargar clasificador
            self.clasificador = bAImaxClassifier()
            if hasattr(self.clasificador, 'cargar_modelo'):
                self.clasificador.cargar_modelo()
            else:
                self.clasificador.entrenar()
            
            # Cargar sistema de recomendaciones
            self.recomendador = bAImaxRecomendaciones()
            
            # Inicializar analyzer
            self.analyzer = bAImaxAnalyzer()
            
            print("✅ bAImax Chatbot inicializado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando chatbot: {e}")
            return False
    
    def detectar_intencion(self, mensaje: str) -> str:
        """
        🎯 Detecta la intención del usuario en el mensaje
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
        
        # Detectar reporte de problema
        for patron in self.patrones_problema:
            if re.search(patron, mensaje_lower):
                return "problema"
        
        # Detectar pregunta sobre ubicación
        for patron in self.patrones_ubicacion:
            if re.search(patron, mensaje_lower):
                return "ubicacion"
        
        # Si contiene palabras relacionadas con salud
        palabras_salud = ["médico", "hospital", "agua", "basura", "luz", "internet", "seguridad", "educación"]
        if any(palabra in mensaje_lower for palabra in palabras_salud):
            return "problema"
        
        return "conversacion_general"
    
    def extraer_ubicacion(self, mensaje: str) -> str:
        """
        📍 Extrae la ubicación del mensaje del usuario
        """
        mensaje_lower = mensaje.lower()
        
        # Ciudades principales de Colombia
        ciudades = {
            "bogotá": "Bogotá", "bogota": "Bogotá",
            "medellín": "Medellín", "medellin": "Medellín",
            "cali": "Cali", "santiago de cali": "Cali",
            "barranquilla": "Barranquilla",
            "cartagena": "Cartagena",
            "cúcuta": "Cúcuta", "cucuta": "Cúcuta",
            "bucaramanga": "Bucaramanga",
            "pereira": "Pereira",
            "manizales": "Manizales",
            "santa marta": "Santa Marta"
        }
        
        for ciudad_key, ciudad_nombre in ciudades.items():
            if ciudad_key in mensaje_lower:
                return ciudad_nombre
        
        # Patrones con regex
        for patron in self.patrones_ubicacion:
            match = re.search(patron, mensaje_lower)
            if match:
                ubicacion_extraida = match.group(1).strip()
                # Buscar en las ciudades
                for ciudad_key, ciudad_nombre in ciudades.items():
                    if ciudad_key in ubicacion_extraida:
                        return ciudad_nombre
        
        return None
    
    def preguntar_detalles_problema(self) -> Dict[str, str]:
        """
        🤔 Hace preguntas interactivas para obtener detalles del problema
        """
        self.esperando_detalles = True
        self.intentos_detalles += 1
        
        if self.intentos_detalles >= self.max_intentos_detalles:
            self.esperando_detalles = False
            self.intentos_detalles = 0
            return {
                'mensaje': "Entiendo que hay un problema, pero necesito más detalles específicos. " +
                          "Por favor, intenta de nuevo especificando el tipo de problema y la ciudad.",
                'tipo': 'error_detalles'
            }
            
        mensajes_ayuda = [
            "🏥 Para ayudarte mejor con tu reporte, necesito algunos detalles:\n\n" +
            "1. ¿Qué tipo de problema tienes? (médicos, agua, basura, etc.)\n" +
            "2. ¿En qué ciudad te encuentras?\n\n" +
            "Por favor, cuéntame ambos detalles en una frase.\n" +
            "Ejemplo: \"No hay médicos suficientes en Bogotá\"",
            
            "🤔 Necesito un poco más de información:\n" +
            "Por favor, dime el tipo de problema y la ciudad en una sola frase.\n" +
            "Por ejemplo: \"Problemas con el agua en Medellín\""
        ]
        
        return {
            'mensaje': mensajes_ayuda[min(self.intentos_detalles - 1, len(mensajes_ayuda) - 1)],
            'tipo': 'pregunta_detalles',
            'requiere': ['tipo_problema', 'ubicacion']
        }

    def procesar_problema(self, mensaje: str, ubicacion: str = None) -> Dict[str, Any]:
        """
        🔍 Procesa un problema reportado por el usuario
        """
        try:
            # Verificar si tenemos suficiente información
            if not mensaje or len(mensaje.split()) < 3:
                return self.preguntar_detalles_problema()
            
            # Clasificar el problema
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
        💭 Genera respuesta inteligente y conversacional
        """
        try:
            # Detectar si es un reporte de problema
            es_problema = any(re.search(patron, mensaje.lower()) for patron in self.patrones_problema)
            tiene_ubicacion = self.extraer_ubicacion(mensaje) is not None
            tiene_detalles = len(mensaje.split()) >= 3
            
            # Verificar si estábamos esperando detalles y los recibimos
            if self.esperando_detalles and tiene_ubicacion and tiene_detalles:
                self.esperando_detalles = False
                self.intentos_detalles = 0
            
            # Si es un nuevo problema o estamos esperando detalles
            if (es_problema and not tiene_detalles) or (self.esperando_detalles and not tiene_ubicacion):
                return self.preguntar_detalles_problema()
            
            # Procesar el mensaje con el gestor de conversación mejorado
            respuesta_procesada = self.conversation_manager.process_message(mensaje)
            
            # Construir la respuesta
            respuesta = {
                'mensaje': respuesta_procesada['message'],
                'tipo': respuesta_procesada['type'],
                'datos_extra': {
                    'sugerencias': respuesta_procesada['suggestions'],
                    'contexto': respuesta_procesada['context']
                }
            }
            
            # Si es una respuesta general, intentar mejorarla
            if respuesta_procesada['type'] == 'general':
                try:
                    respuesta_avanzada = self.generar_respuesta_contextual_avanzada(mensaje)
                    if respuesta_avanzada and len(respuesta_avanzada) > 20:
                        respuesta['mensaje'] = respuesta_avanzada
                except:
                    pass  # Mantener la respuesta original si falla
                    
            # Agregar a la conversación activa
            self.conversacion_activa.append({
                'usuario': mensaje,
                'respuesta': respuesta['mensaje'],
                'timestamp': datetime.now().isoformat()
            })
            
            return respuesta
            
        except Exception as e:
            print(f"❌ Error generando respuesta: {e}")
            return {
                'mensaje': "Lo siento, tuve un problema procesando tu mensaje. ¿Podrías reformularlo?",
                'tipo': 'error',
                'datos_extra': {}
            }
        respuesta_procesada = self.conversation_manager.process_message(mensaje)
        
        respuesta = {
            'mensaje': respuesta_procesada['message'],
            'tipo': respuesta_procesada['type'],
            'datos_extra': {},
            'acciones_sugeridas': []
        }
        
        if intencion == "saludo":
            import random
            respuesta['mensaje'] = random.choice(self.respuestas_saludo)
            respuesta['acciones_sugeridas'] = [
                "Reportar un problema de salud pública",
                "Ver estadísticas de mi ciudad", 
                "Buscar puntos de atención médica"
            ]
            
        elif intencion == "despedida":
            import random
            respuesta['mensaje'] = random.choice(self.respuestas_despedida)
            
        elif intencion == "problema":
            # Extraer ubicación si está disponible
            ubicacion = self.extraer_ubicacion(mensaje)
            
            if not ubicacion:
                respuesta['mensaje'] = """
🤖 He detectado que tienes un problema de salud pública. Para ayudarte mejor, ¿me puedes decir en qué ciudad te encuentras?

Las ciudades que tengo en mi base de datos son:
📍 Bogotá, Medellín, Cali, Barranquilla, Cartagena, Cúcuta, Bucaramanga, Pereira, Manizales, Santa Marta

Por ejemplo: "Estoy en Bogotá" o "Vivo en Medellín"
                """
                respuesta['tipo'] = 'solicitar_ubicacion'
                return respuesta
            
            # 🤖 USAR OLLAMA SI ESTÁ DISPONIBLE PARA RESPUESTA INTELIGENTE
            if self.ollama and self.ollama.disponible:
                try:
                    # Contexto médico para Ollama
                    contexto_medico = {
                        'ciudad': ubicacion,
                        'sistema': 'bAImax 2.0',
                        'tipo_consulta': 'problema_salud'
                    }
                    
                    # Generar respuesta inteligente
                    resultado_ollama = self.ollama.generar_respuesta(mensaje, contexto_medico)
                    
                    if resultado_ollama['exito']:
                        respuesta['mensaje'] = resultado_ollama['respuesta']
                        respuesta['datos_extra'] = {
                            'ia_avanzada': True,
                            'modelo_usado': resultado_ollama['modelo_usado'],
                            'tiempo_ms': resultado_ollama['tiempo_ms'],
                            'ubicacion': ubicacion
                        }
                        respuesta['acciones_sugeridas'] = [
                            "Ver centros médicos cercanos",
                            "Reportar otro problema", 
                            "Obtener más información"
                        ]
                        
                        # También procesar con sistema básico para estadísticas
                        try:
                            self.procesar_problema(mensaje, ubicacion)
                        except:
                            pass  # No crítico si falla
                        
                        return respuesta
                    
                except Exception as e:
                    print(f"⚠️ Error en Ollama: {e}")
                    # Continúa con procesamiento básico
            
            # Procesar el problema (modo básico)
            resultado = self.procesar_problema(mensaje, ubicacion)
            
            if resultado['exito']:
                clasificacion = resultado['clasificacion']
                recomendaciones = resultado['recomendaciones']
                
                # Generar respuesta personalizada
                emoji_gravedad = "🔴" if clasificacion['gravedad'] == 'GRAVE' else "🟡"
                
                respuesta_texto = f"""
🤖 **Análisis de tu reporte:**

{emoji_gravedad} **Clasificación:** {clasificacion['gravedad']}
📊 **Confianza:** {clasificacion['confianza']:.1%}
📍 **Ubicación:** {ubicacion}

**📋 Problema analizado:** "{mensaje}"

"""
                
                if recomendaciones:
                    respuesta_texto += "🎯 **Puntos de atención recomendados:**\n\n"
                    for i, rec in enumerate(recomendaciones[:3], 1):
                        respuesta_texto += f"""
**{i}. {rec['tipo']}: {rec['nombre']}**
📞 {rec['telefono']}
📍 {rec['direccion']}
{'🌐 ' + rec['web'] if rec['web'] != 'No disponible' else ''}

"""
                
                respuesta_texto += """
✅ **Tu reporte ha sido registrado** y contribuirá a mejorar nuestro sistema.

¿Te fue útil esta información? ¿Necesitas algo más?
                """
                
                respuesta['mensaje'] = respuesta_texto
                respuesta['datos_extra'] = {
                    'clasificacion': clasificacion,
                    'recomendaciones': recomendaciones,
                    'ubicacion': ubicacion
                }
                respuesta['acciones_sugeridas'] = [
                    "Reportar otro problema",
                    "Ver mapa de mi zona",
                    "Obtener más recomendaciones"
                ]
                
            else:
                respuesta['mensaje'] = f"❌ Lo siento, hubo un error procesando tu reporte: {resultado.get('error', 'Error desconocido')}"
        
        elif intencion == "ubicacion":
            ubicacion = self.extraer_ubicacion(mensaje)
            if ubicacion:
                self.contexto_usuario['ubicacion'] = ubicacion
                respuesta['mensaje'] = f"📍 Perfecto, he registrado que estás en **{ubicacion}**. Ahora cuéntame, ¿qué problema de salud pública quieres reportar?"
                respuesta['datos_extra'] = {'ubicacion': ubicacion}
            else:
                respuesta['mensaje'] = "🤔 No pude identificar tu ciudad. ¿Podrías decirme específicamente en cuál de estas ciudades estás?\n\n📍 Bogotá, Medellín, Cali, Barranquilla, Cartagena, Cúcuta, Bucaramanga, Pereira, Manizales, Santa Marta"
        
        else:  # conversacion_general
            # 🤖 INTENTAR RESPUESTA INTELIGENTE CON OLLAMA
            if self.ollama and self.ollama.disponible:
                try:
                    contexto_general = {
                        'sistema': 'bAImax 2.0 - Salud Pública Colombia',
                        'tipo_consulta': 'conversacion_general'
                    }
                    
                    resultado_ollama = self.ollama.generar_respuesta(mensaje, contexto_general)
                    
                    if resultado_ollama['exito']:
                        respuesta['mensaje'] = resultado_ollama['respuesta']
                        respuesta['datos_extra'] = {
                            'ia_avanzada': True,
                            'modelo_usado': resultado_ollama['modelo_usado'],
                            'tiempo_ms': resultado_ollama['tiempo_ms']
                        }
                        respuesta['acciones_sugeridas'] = [
                            "Reportar un problema de salud",
                            "Ver estadísticas", 
                            "Hacer otra consulta"
                        ]
                        return respuesta
                        
                except Exception as e:
                    print(f"⚠️ Error en Ollama conversación: {e}")
                    # Continúa con respuesta básica
            
            # Respuesta básica
            respuesta['mensaje'] = """
🤖 Soy bAImax, especializado en ayudarte con problemas de salud pública en Colombia. 

Puedo ayudarte a:
✅ Reportar problemas (falta de médicos, agua, basura, etc.)
✅ Clasificar la gravedad automáticamente
✅ Encontrar puntos de atención cercanos
✅ Ver estadísticas de tu zona

¿Tienes algún problema de salud pública que reportar?
            """
            respuesta['acciones_sugeridas'] = [
                "Sí, tengo un problema que reportar",
                "Ver estadísticas de mi ciudad",
                "Conocer más sobre bAImax"
            ]
        
        # Agregar respuesta a conversación
        self.conversacion_activa.append({
            'bot': respuesta['mensaje'],
            'tipo': intencion,
            'timestamp': datetime.now().isoformat()
        })
        
        return respuesta
    
    def obtener_estadisticas_conversacion(self) -> Dict[str, Any]:
        """
        📊 Obtiene estadísticas de la conversación actual
        """
        return {
            'mensajes_totales': len(self.conversacion_activa),
            'problemas_reportados': 1 if self.ultimo_problema_reportado else 0,
            'ubicacion_detectada': self.contexto_usuario.get('ubicacion'),
            'ultimo_reporte': self.ultimo_problema_reportado
        }
    
    def reiniciar_conversacion(self):
        """
        🔄 Reinicia la conversación actual
        """
        self.conversacion_activa = []
        self.contexto_usuario = {}
        self.ultimo_problema_reportado = None
        return "🔄 Conversación reiniciada. ¡Hola de nuevo!"
    
    def exportar_reporte(self) -> Dict[str, Any]:
        """
        📋 Exporta el último reporte para guardado en dataset
        """
        if not self.ultimo_problema_reportado:
            return None
        
        # Formato compatible con el dataset existente
        reporte = {
            'Comentario': self.ultimo_problema_reportado['mensaje'],
            'Ciudad': self.ultimo_problema_reportado['ubicacion'],
            'Nivel_gravedad': self.ultimo_problema_reportado['clasificacion']['gravedad'],
            'Fecha_reporte': datetime.now().strftime('%Y-%m-%d'),
            'Fuente': 'bAImax_Chatbot_2.0',
            'Confianza_IA': self.ultimo_problema_reportado['clasificacion']['confianza'],
            'Timestamp': self.ultimo_problema_reportado['timestamp']
        }
        
        return reporte

# Función de demostración del chatbot
def demo_chatbot():
    """
    🎭 Demostración interactiva del chatbot bAImax
    """
    print("🚀 Iniciando bAImax Chatbot 2.0...")
    
    chatbot = bAImaxChatbot()
    
    if not chatbot.inicializar_sistema():
        print("❌ Error inicializando el sistema")
        return
    
    print("\n" + "="*60)
    print("🤖 bAImax Chatbot 2.0 - Sistema de Salud Pública Interactivo")
    print("="*60)
    print("Escribe 'salir' para terminar la conversación")
    print()
    
    # Mensaje inicial del bot
    respuesta_inicial = chatbot.generar_respuesta("hola")
    print(f"🤖 bAImax: {respuesta_inicial['mensaje']}")
    
    while True:
        try:
            # Entrada del usuario
            mensaje_usuario = input("\n👤 Tú: ")
            
            if mensaje_usuario.lower() in ['salir', 'exit', 'quit']:
                despedida = chatbot.generar_respuesta("adiós")
                print(f"\n🤖 bAImax: {despedida['mensaje']}")
                break
            
            # Generar respuesta
            respuesta = chatbot.generar_respuesta(mensaje_usuario)
            print(f"\n🤖 bAImax: {respuesta['mensaje']}")
            
            # Mostrar acciones sugeridas si las hay
            if respuesta['acciones_sugeridas']:
                print("\n💡 Acciones sugeridas:")
                for i, accion in enumerate(respuesta['acciones_sugeridas'], 1):
                    print(f"   {i}. {accion}")
            
        except KeyboardInterrupt:
            print(f"\n\n🤖 bAImax: ¡Hasta pronto! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Mostrar estadísticas finales
    stats = chatbot.obtener_estadisticas_conversacion()
    print(f"\n📊 Estadísticas de la conversación:")
    print(f"   Mensajes intercambiados: {stats['mensajes_totales']}")
    print(f"   Problemas reportados: {stats['problemas_reportados']}")
    print(f"   Ubicación detectada: {stats['ubicacion_detectada']}")

    def analizar_sintomas_usuario(self, mensaje: str) -> Dict[str, Any]:
        """
        🩺 Análisis avanzado de síntomas usando la base de conocimientos
        """
        # Extraer posibles síntomas del mensaje
        sintomas_detectados = []
        sintomas_posibles = ["fiebre", "tos", "dolor cabeza", "mareos", "fatiga", "diarrea", "vomito", "dolor pecho"]
        
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
            respuesta_parts.append(f"📋 Síntomas identificados: {', '.join(sintomas)}")
            
            enfermedades = analisis_sintomas['enfermedades_posibles']
            if enfermedades:
                respuesta_parts.append("\n🔍 **Posibles condiciones a considerar:**")
                for enfermedad in enfermedades[:3]:  # Máximo 3
                    info = enfermedad['info']
                    respuesta_parts.append(f"   • **{enfermedad['enfermedad'].replace('_', ' ').title()}**")
                    respuesta_parts.append(f"     Gravedad: {info['gravedad']}")
                    respuesta_parts.append(f"     Especialista recomendado: {info['especialista']}")
        
        # Información de la ciudad si está disponible
        if ubicacion:
            info_ciudad = self.knowledge_base.buscar_informacion_ciudad(ubicacion)
            if info_ciudad:
                respuesta_parts.append(f"\n📍 **Información de {info_ciudad['nombre']}:**")
                respuesta_parts.append(f"   Población: {info_ciudad['poblacion']:,} habitantes")
                if 'problemas_comunes' in info_ciudad:
                    respuesta_parts.append("   Problemas de salud comunes en la zona:")
                    for problema in info_ciudad['problemas_comunes'][:3]:
                        respuesta_parts.append(f"     • {problema}")
        
        # Recomendaciones generales
        respuesta_parts.append(f"\n⚠️  **Nivel de urgencia estimado: {respuesta_contextual['nivel_urgencia']}**")
        
        if respuesta_contextual['recomendaciones']:
            respuesta_parts.append("\n💡 **Recomendaciones:**")
            for rec in respuesta_contextual['recomendaciones']:
                respuesta_parts.append(f"   {rec}")
        
        respuesta_parts.append("\n🚨 **Importante:** Esta es una evaluación automatizada. Consulta a un profesional médico para diagnóstico definitivo.")
        
        return '\n'.join(respuesta_parts)
    
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


def demo_chatbot_avanzado():
    """
    🎮 Demostración del chatbot con capacidades avanzadas de conocimiento
    """
    print("🚀 Iniciando bAImax 2.0 con Conocimientos Avanzados...")
    
    # Inicializar chatbot entrenado
    chatbot = bAImaxChatbot()
    chatbot.inicializar_sistema()
    
    print("\n" + "="*70)
    print("🧠 bAImax 2.0 - Chatbot Inteligente Entrenado")
    print("="*70)
    print("✨ Nuevas capacidades:")
    print("   🏥 Conocimientos de ciudades colombianas")
    print("   🩺 Análisis avanzado de síntomas")
    print("   📋 Protocolos de atención médica")
    print("   🎯 Recomendaciones contextuales inteligentes")
    print()
    
    # Mostrar estadísticas de conocimiento
    stats_know = chatbot.obtener_estadisticas_conocimiento()
    print("📊 Base de conocimientos cargada:")
    for key, value in stats_know.items():
        print(f"   {key}: {value}")
    
    print("\nEscribe 'salir' para terminar")
    print("Ejemplos de consultas avanzadas:")
    print("   • 'Tengo fiebre y dolor de cabeza en Bogotá'")
    print("   • 'Hay problemas de agua potable en Medellín'")
    print("   • 'Diarrea y vómitos en Barranquilla'")
    print()
    
    # Mensaje inicial
    print("🤖 bAImax: ¡Hola! Soy bAImax 2.0, ahora con conocimientos avanzados sobre salud en Colombia. 🇨🇴")
    
    while True:
        try:
            mensaje = input("\n👤 Tú: ")
            
            if mensaje.lower() in ['salir', 'exit', 'quit']:
                print("\n🤖 bAImax: ¡Hasta pronto! Espero haber sido útil. 👋")
                break
            
            # Generar respuesta con análisis avanzado
            respuesta_basica = chatbot.generar_respuesta(mensaje)
            ubicacion = chatbot.extraer_ubicacion(mensaje)
            
            # Si se detectó problema de salud, usar análisis avanzado
            if respuesta_basica['tipo_respuesta'] == 'problema':
                respuesta_avanzada = chatbot.generar_respuesta_contextual_avanzada(mensaje, ubicacion)
                print(f"\n🤖 bAImax (Análisis Avanzado):\n{respuesta_avanzada}")
            else:
                print(f"\n🤖 bAImax: {respuesta_basica['mensaje']}")
                
        except KeyboardInterrupt:
            print(f"\n\n🤖 bAImax: ¡Hasta pronto! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Ejecutar entrenamiento de conocimientos primero
    print("🎓 Entrenando chatbot con conocimientos avanzados...")
    from core.baimax_knowledge_base import entrenar_chatbot_con_conocimientos
    entrenar_chatbot_con_conocimientos()
    
    print("\n" + "="*50)
    print("Elige modo de demostración:")
    print("1. Chatbot básico")
    print("2. Chatbot avanzado (CON conocimientos)")
    print("="*50)
    
    opcion = input("Opción (1 o 2): ")
    
    if opcion == "2":
        demo_chatbot_avanzado()
    else:
        demo_chatbot()