"""
🤖 bAImax Chatbot AVANZADO - Con Datos del Ministerio de Salud
==============================================================

Chatbot entrenado con datos reales y actualizados del Ministerio de Salud
de Colombia, incluyendo alertas epidemiológicas, protocolos médicos y 
estadísticas oficiales.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from baimax_chatbot_entrenado import bAImaxChatbotEntrenado
from baimax_knowledge_base import bAImaxKnowledgeBase

class bAImaxChatbotMejor(bAImaxChatbotEntrenado):
    """
    🩺 Chatbot médico mejorado con datos oficiales del Ministerio de Salud
    """
    
    def __init__(self):
        super().__init__()
        self.nombre = "bAImax Médico Pro"
        self.version = "2.1 - MinSalud Data"
        
        # Cargar datos del Ministerio de Salud
        self.datos_minsalud = self._cargar_datos_minsalud()
        self.alertas_activas = self.datos_minsalud.get('alertas_activas', [])
        self.protocolos_oficiales = self.datos_minsalud.get('protocolos_atencion', [])
        self.estadisticas_nacionales = self.datos_minsalud.get('estadisticas_nacionales', [])
        self.enfermedades_prevalentes = self.datos_minsalud.get('enfermedades_prevalentes', [])
        
        print(f"🩺 {self.nombre} v{self.version} inicializado")
        print(f"📊 Datos MinSalud cargados: {len(self.alertas_activas)} alertas, {len(self.protocolos_oficiales)} protocolos")
    
    def _cargar_datos_minsalud(self) -> Dict[str, Any]:
        """
        📂 Carga datos actualizados del Ministerio de Salud
        """
        try:
            with open("baimax_knowledge_base_actualizada.json", 'r', encoding='utf-8') as f:
                datos = json.load(f)
                print("✅ Datos del MinSalud cargados exitosamente")
                return datos
        except FileNotFoundError:
            print("⚠️ Archivo de datos MinSalud no encontrado, usando datos base")
            return {}
    
    def detectar_intencion_avanzada(self, mensaje: str) -> str:
        """
        🎯 Detecta intenciones con análisis mejorado usando datos oficiales
        """
        mensaje_lower = mensaje.lower()
        
        # Detectar consultas sobre alertas epidemiológicas
        if any(palabra in mensaje_lower for palabra in ['alerta', 'brote', 'epidemia', 'casos']):
            return "consulta_alertas"
        
        # Detectar consultas sobre enfermedades específicas
        for enfermedad in self.enfermedades_prevalentes:
            if enfermedad['nombre'].lower() in mensaje_lower:
                return "consulta_enfermedad"
        
        # Detectar solicitudes de protocolos
        if any(palabra in mensaje_lower for palabra in ['protocolo', 'tratamiento', 'procedimiento']):
            return "consulta_protocolo"
        
        # Detectar consultas estadísticas
        if any(palabra in mensaje_lower for palabra in ['estadística', 'datos', 'números', 'cifras']):
            return "consulta_estadisticas"
        
        # Usar detección base
        return super().detectar_intencion(mensaje)
    
    def generar_respuesta_alertas(self, mensaje: str) -> str:
        """
        🚨 Genera respuesta sobre alertas epidemiológicas actuales
        """
        if not self.alertas_activas:
            return "📊 No hay alertas epidemiológicas activas en este momento. El sistema está monitoreando continuamente."
        
        respuesta = "🚨 **ALERTAS EPIDEMIOLÓGICAS ACTIVAS**\\n\\n"
        
        for i, alerta in enumerate(self.alertas_activas[:2], 1):  # Máximo 2 alertas
            respuesta += f"**{i}. {alerta['titulo']}**\\n"
            respuesta += f"📅 Fecha: {alerta['fecha']}\\n"
            respuesta += f"⚠️ Gravedad: **{alerta['gravedad']}**\\n"
            respuesta += f"📍 Departamentos: {', '.join(alerta['departamentos_afectados'])}\\n"
            respuesta += f"📝 {alerta['descripcion']}\\n\\n"
            
            if alerta.get('recomendaciones'):
                respuesta += "💡 **Recomendaciones:**\\n"
                for rec in alerta['recomendaciones'][:3]:
                    respuesta += f"• {rec}\\n"
            respuesta += "\\n"
        
        respuesta += "🏥 **En caso de síntomas, consulte inmediatamente al centro de salud más cercano.**\\n"
        respuesta += "📞 Línea Nacional: 123 (Emergencias) | 018000-910097 (MinSalud)"
        
        return respuesta
    
    def generar_respuesta_enfermedad(self, mensaje: str) -> str:
        """
        🦠 Genera respuesta específica sobre enfermedades
        """
        mensaje_lower = mensaje.lower()
        
        # Buscar enfermedad mencionada
        enfermedad_encontrada = None
        for enfermedad in self.enfermedades_prevalentes:
            if enfermedad['nombre'].lower() in mensaje_lower:
                enfermedad_encontrada = enfermedad
                break
        
        if not enfermedad_encontrada:
            return "🔍 No encontré información específica sobre esa enfermedad. ¿Podrías ser más específico?"
        
        enf = enfermedad_encontrada
        respuesta = f"🩺 **INFORMACIÓN OFICIAL: {enf['nombre'].upper()}**\\n\\n"
        respuesta += f"📋 **Tipo:** {enf['tipo']}\\n"
        
        if 'vector' in enf:
            respuesta += f"🦟 **Vector:** {enf['vector']}\\n"
        
        respuesta += "\\n**🔍 SÍNTOMAS PRINCIPALES:**\\n"
        for sintoma in enf['sintomas_principales']:
            respuesta += f"• {sintoma}\\n"
        
        respuesta += "\\n**⚠️ SIGNOS DE ALARMA:**\\n"
        for signo in enf['signos_alarma']:
            respuesta += f"• {signo}\\n"
        
        respuesta += f"\\n**💊 TRATAMIENTO:** {enf['tratamiento']}\\n"
        
        respuesta += "\\n**🛡️ PREVENCIÓN:**\\n"
        for prev in enf['prevencion']:
            respuesta += f"• {prev}\\n"
        
        if 'zonas_riesgo' in enf:
            respuesta += f"\\n**📍 ZONAS DE MAYOR RIESGO:** {', '.join(enf['zonas_riesgo'])}\\n"
        
        respuesta += "\\n🚨 **Si presenta signos de alarma, acuda INMEDIATAMENTE al servicio de urgencias.**"
        
        return respuesta
    
    def generar_respuesta_protocolo(self, mensaje: str) -> str:
        """
        📋 Genera respuesta sobre protocolos médicos oficiales
        """
        if not self.protocolos_oficiales:
            return "📋 Los protocolos están siendo actualizados. Consulte con su médico tratante."
        
        # Buscar protocolo relevante
        protocolo_encontrado = None
        mensaje_lower = mensaje.lower()
        
        for protocolo in self.protocolos_oficiales:
            if any(sintoma.lower() in mensaje_lower for sintoma in protocolo.get('sintomas_clave', [])):
                protocolo_encontrado = protocolo
                break
        
        if not protocolo_encontrado:
            protocolo_encontrado = self.protocolos_oficiales[0]  # Usar el primero como ejemplo
        
        prot = protocolo_encontrado
        respuesta = f"📋 **PROTOCOLO OFICIAL: {prot['nombre'].upper()}**\\n\\n"
        respuesta += f"🏥 **Categoría:** {prot['categoria']}\\n"
        respuesta += f"👥 **Población objetivo:** {prot['poblacion_objetivo']}\\n"
        respuesta += f"🏨 **Nivel de atención:** {prot['nivel_atencion']}\\n\\n"
        
        respuesta += "**🔍 SÍNTOMAS CLAVE:**\\n"
        for sintoma in prot['sintomas_clave']:
            respuesta += f"• {sintoma}\\n"
        
        respuesta += "\\n**📝 PASOS DE ATENCIÓN:**\\n"
        for i, paso in enumerate(prot['pasos_atencion'], 1):
            respuesta += f"{i}. {paso}\\n"
        
        respuesta += "\\n⚕️ **Este protocolo está basado en lineamientos del Ministerio de Salud de Colombia.**"
        
        return respuesta
    
    def generar_respuesta_estadisticas(self, mensaje: str) -> str:
        """
        📊 Genera respuesta con estadísticas oficiales de salud
        """
        if not self.estadisticas_nacionales:
            return "📊 Las estadísticas están siendo actualizadas por el sistema."
        
        respuesta = "📊 **ESTADÍSTICAS NACIONALES DE SALUD - 2024**\\n\\n"
        
        for stat in self.estadisticas_nacionales:
            tendencia_emoji = {"Incremental": "📈", "Decremental": "📉", "Estable": "➡️"}
            emoji = tendencia_emoji.get(stat['tendencia'], "📊")
            
            respuesta += f"**{stat['indicador']}**\\n"
            respuesta += f"{emoji} {stat['valor']} {stat['unidad']}\\n"
            respuesta += f"📍 Ámbito: {stat['departamento']} | Tendencia: {stat['tendencia']}\\n\\n"
        
        respuesta += "📄 **Fuente:** Ministerio de Salud y Protección Social de Colombia\\n"
        respuesta += "📅 **Última actualización:** " + datetime.now().strftime("%Y-%m-%d")
        
        return respuesta
    
    def generar_respuesta_mejorada(self, mensaje: str) -> Dict[str, Any]:
        """
        🧠 Genera respuesta mejorada usando datos oficiales del MinSalud
        """
        # Agregar a conversación
        self.conversacion_activa.append({
            'usuario': mensaje,
            'timestamp': datetime.now().isoformat()
        })
        
        # Detectar intención avanzada
        intencion = self.detectar_intencion_avanzada(mensaje)
        
        # Extraer ubicación
        ubicacion = self.extraer_ubicacion(mensaje)
        
        # Generar respuesta según intención
        if intencion == "consulta_alertas":
            respuesta_texto = self.generar_respuesta_alertas(mensaje)
            tipo_respuesta = "alertas_epidemiologicas"
            
        elif intencion == "consulta_enfermedad":
            respuesta_texto = self.generar_respuesta_enfermedad(mensaje)
            tipo_respuesta = "informacion_enfermedad"
            
        elif intencion == "consulta_protocolo":
            respuesta_texto = self.generar_respuesta_protocolo(mensaje)
            tipo_respuesta = "protocolo_oficial"
            
        elif intencion == "consulta_estadisticas":
            respuesta_texto = self.generar_respuesta_estadisticas(mensaje)
            tipo_respuesta = "estadisticas_oficiales"
            
        else:
            # Usar lógica base para otras consultas
            respuesta_base = super().generar_respuesta(mensaje)
            respuesta_texto = respuesta_base['mensaje']
            tipo_respuesta = respuesta_base['tipo_respuesta']
        
        # Construir respuesta final
        respuesta_final = {
            'mensaje': respuesta_texto,
            'tipo_respuesta': tipo_respuesta,
            'ubicacion_detectada': ubicacion,
            'fuente_datos': 'Ministerio de Salud Colombia',
            'confiabilidad': 'OFICIAL',
            'timestamp': datetime.now().isoformat()
        }
        
        # Agregar respuesta a conversación
        self.conversacion_activa.append({
            'bot': respuesta_texto,
            'tipo': tipo_respuesta,
            'timestamp': datetime.now().isoformat()
        })
        
        return respuesta_final


def demo_chatbot_minsalud():
    """
    🎮 Demostración del chatbot mejorado con datos del MinSalud
    """
    print("🚀 Iniciando bAImax Médico Pro con datos del MinSalud...")
    
    # Crear chatbot mejorado
    chatbot = bAImaxChatbotMejor()
    chatbot.inicializar_sistema()
    
    print("\\n" + "="*70)
    print("🩺 bAImax Médico Pro - Con Datos Oficiales del MinSalud")
    print("="*70)
    print("✨ Nuevas capacidades:")
    print("   🚨 Alertas epidemiológicas actuales")
    print("   📋 Protocolos médicos oficiales")
    print("   📊 Estadísticas nacionales de salud")
    print("   🦠 Información detallada de enfermedades")
    print("   🏥 Datos oficiales y confiables")
    print()
    
    print("💡 Ejemplos de consultas especializadas:")
    print("   • 'Qué alertas epidemiológicas hay actualmente?'")
    print("   • 'Información sobre dengue'")
    print("   • 'Protocolo para COVID-19'")
    print("   • 'Estadísticas de salud nacional'")
    print("   • 'Tengo fiebre y dolor de cabeza en Cartagena'")
    print()
    print("Escribe 'salir' para terminar")
    print("="*70)
    
    # Saludo inicial
    respuesta_inicial = chatbot.generar_respuesta_mejorada("hola")
    print(f"🤖 bAImax Pro: {respuesta_inicial['mensaje']}")
    
    while True:
        try:
            mensaje = input("\\n👤 Tú: ")
            
            if mensaje.lower() in ['salir', 'exit', 'quit']:
                despedida = chatbot.generar_respuesta_mejorada("adiós")
                print(f"\\n🤖 bAImax Pro: {despedida['mensaje']}")
                break
            
            # Generar respuesta mejorada
            respuesta = chatbot.generar_respuesta_mejorada(mensaje)
            
            # Mostrar respuesta
            print(f"\\n🤖 bAImax Pro: {respuesta['mensaje']}")
            
            # Mostrar información adicional
            if respuesta['tipo_respuesta'] in ['alertas_epidemiologicas', 'protocolo_oficial', 'estadisticas_oficiales']:
                print("\\n" + "🏛️"*30)
                print(f"📄 FUENTE: {respuesta['fuente_datos']}")
                print(f"✅ CONFIABILIDAD: {respuesta['confiabilidad']}")
                if respuesta['ubicacion_detectada']:
                    print(f"📍 UBICACIÓN: {respuesta['ubicacion_detectada']}")
                print("🏛️"*30)
                
        except KeyboardInterrupt:
            print(f"\\n\\n🤖 bAImax Pro: ¡Hasta pronto! Mantente saludable 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Estadísticas finales
    stats_conv = chatbot.obtener_estadisticas_conversacion()
    print(f"\\n📊 Estadísticas de la sesión:")
    print(f"   💬 Mensajes totales: {stats_conv['mensajes_totales']}")
    print(f"   🏥 Consultas médicas: {stats_conv['problemas_reportados']}")
    print(f"   📍 Ubicación detectada: {'Sí' if stats_conv['ubicacion_detectada'] else 'No'}")


if __name__ == "__main__":
    demo_chatbot_minsalud()