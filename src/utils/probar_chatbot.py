#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from baimax_chatbot_minsalud import bAImaxChatbotMejor

def probar_chatbot():
    """
    Prueba el chatbot con consultas específicas para verificar funcionamiento
    """
    print("🚀 PROBANDO CHATBOT bAImax 2.0 CON DATOS ACTUALIZADOS")
    print("=" * 60)
    
    # Crear instancia del chatbot
    try:
        chatbot = bAImaxChatbotMejor()
        print("✅ Chatbot inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando chatbot: {e}")
        return
    
    # Consultas de prueba
    consultas_prueba = [
        "Tengo fiebre alta y dolor de cabeza en Cartagena, ¿qué debo hacer?",
        "Dolor abdominal intenso en Bogotá",
        "¿Hay alguna alerta de dengue activa?",
        "Síntomas de infección respiratoria en Medellín"
    ]
    
    for i, consulta in enumerate(consultas_prueba, 1):
        print(f"\n{'-'*50}")
        print(f"🔍 PRUEBA {i}/4:")
        print(f"👤 Consulta: {consulta}")
        print(f"🤖 Respuesta bAImax:")
        
        try:
            respuesta = chatbot.generar_respuesta_mejorada(consulta)
            print(respuesta['mensaje'])
            
            # Mostrar información adicional
            if respuesta.get('tipo_respuesta') in ['alertas_epidemiologicas', 'protocolo_oficial', 'estadisticas_oficiales']:
                print(f"📄 FUENTE: {respuesta['fuente_datos']}")
                print(f"✅ CONFIABILIDAD: {respuesta['confiabilidad']}")
        except Exception as e:
            print(f"❌ Error procesando consulta: {e}")
    
    print(f"\n" + "=" * 60)
    print("✅ PRUEBAS DEL CHATBOT COMPLETADAS")

if __name__ == "__main__":
    probar_chatbot()