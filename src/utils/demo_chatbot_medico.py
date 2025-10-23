"""
🎮 DEMO INTERACTIVA - bAImax Chatbot Médico Entrenado
====================================================

Demostración simplificada del chatbot entrenado con conocimientos
avanzados de salud colombiana para que puedas probar fácilmente.
"""

from baimax_chatbot_entrenado import bAImaxChatbotEntrenado

def demo_interactiva_simple():
    """
    🎯 Demo interactiva simple del chatbot entrenado
    """
    print("🚀 Inicializando bAImax Médico Entrenado...")
    
    # Crear chatbot entrenado
    chatbot = bAImaxChatbotEntrenado()
    
    print("\n" + "="*60)
    print("🧠 bAImax Médico - Chatbot Entrenado")
    print("="*60)
    print("🩺 Especializado en salud pública colombiana")
    print("📍 Conoce ciudades de toda Colombia")
    print("⚡ Análisis médico inteligente")
    print()
    
    # Mostrar estadísticas
    stats = chatbot.obtener_estadisticas_conocimiento()
    print("📊 Base de conocimientos:")
    print(f"   🏙️  Ciudades: {stats['ciudades_disponibles']}")
    print(f"   🏥 Casos de salud: {stats['casos_salud_registrados']}")
    print(f"   📋 Protocolos: {stats['protocolos_atencion']}")
    print(f"   🩺 Síntomas: {stats['mapeo_sintomas']}")
    print()
    
    print("💡 Ejemplos de consulta:")
    print("   • 'Tengo fiebre y dolor de cabeza en Bogotá'")
    print("   • 'Diarrea y vómitos en Cartagena'")
    print("   • 'Me duele el pecho en Medellín'")
    print("   • 'Problemas respiratorios en Cali'")
    print()
    print("Escribe 'salir' para terminar")
    print("="*60)
    
    # Saludo inicial
    respuesta_inicial = chatbot.generar_respuesta("hola")
    print(f"🤖 bAImax: {respuesta_inicial['mensaje']}")
    
    while True:
        try:
            # Entrada del usuario
            print()
            mensaje = input("👤 Tú: ")
            
            if mensaje.lower() in ['salir', 'exit', 'quit']:
                despedida = chatbot.generar_respuesta("adiós")
                print(f"\n🤖 bAImax: {despedida['mensaje']}")
                break
            
            # Generar respuesta
            respuesta = chatbot.generar_respuesta(mensaje)
            
            # Mostrar respuesta
            print(f"\n🤖 bAImax: {respuesta['mensaje']}")
            
            # Info adicional si es análisis médico
            if respuesta['tipo_respuesta'] == 'analisis_medico':
                print("\n" + "🩺"*30)
                print("⚕️  ANÁLISIS MÉDICO AUTOMATIZADO")
                if respuesta['ubicacion_detectada']:
                    print(f"📍 Ubicación: {respuesta['ubicacion_detectada']}")
                print("⚡ Basado en conocimientos de salud colombiana")
                print("🩺"*30)
            
        except KeyboardInterrupt:
            print(f"\n\n🤖 bAImax: ¡Hasta pronto! Cuida tu salud 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Estadísticas finales
    stats_conv = chatbot.obtener_estadisticas_conversacion()
    print(f"\n📊 Resumen de la sesión:")
    print(f"   💬 Mensajes: {stats_conv['mensajes_totales']}")
    print(f"   🏥 Consultas médicas: {stats_conv['problemas_reportados']}")


if __name__ == "__main__":
    demo_interactiva_simple()