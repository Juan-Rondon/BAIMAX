"""
🤖 Script para probar el chatbot bAImax de forma interactiva
"""
from src.chatbot.baimax_chatbot import bAImaxChatbot

def main():
    print("\n🏥 Bienvenido al probador interactivo de bAImax!")
    print("================================================")
    print("Escribe 'salir' para terminar la conversación\n")
    
    # Inicializar el chatbot
    chatbot = bAImaxChatbot()
    
    while True:
        # Obtener entrada del usuario
        mensaje = input("\n👤 Tú: ")
        
        if mensaje.lower() == 'salir':
            print("\n🤖 bAImax: ¡Hasta pronto! Gracias por usar nuestro servicio.")
            break
            
        try:
            # Obtener respuesta del chatbot
            respuesta = chatbot.generar_respuesta(mensaje)
            
            # Mostrar la respuesta principal
            print(f"\n🤖 bAImax: {respuesta['mensaje']}")
            
            # Mostrar sugerencias si existen
            if 'datos_extra' in respuesta and respuesta['datos_extra'].get('sugerencias'):
                print("\n💡 Sugerencias:")
                for sugerencia in respuesta['datos_extra']['sugerencias']:
                    print(f"  • {sugerencia}")
                    
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()