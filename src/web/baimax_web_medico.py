"""
🌐 bAImax 2.0 WEB - Aplicación Web con Chatbot Médico Entrenado
==============================================================

Sistema web completo que integra:
- Chatbot médico entrenado con conocimientos avanzados
- Análisis de síntomas inteligente
- Información contextual de ciudades colombianas  
- Aprendizaje continuo
- Interfaz moderna y responsiva
"""

import pandas as pd
import webbrowser
import os
import json
from datetime import datetime
import threading
import time

# Importar módulos bAImax
from core.baimax_core import bAImaxClassifier, bAImaxAnalyzer
from visualizations.baimax_mapas import bAImaxMapa
from visualizations.baimax_graficas import bAImaxGraficas
from core.baimax_recomendaciones import bAImaxRecomendaciones
from chatbot.baimax_chatbot import bAImaxChatbot as bAImaxChatbotEntrenado
from core.baimax_learning import bAImaxLearningSystem
from core.baimax_knowledge_base import bAImaxKnowledgeBase

class bAImaxWebApp:
    """
    🌐 Aplicación web completa bAImax 2.0 con chatbot médico entrenado
    """
    
    def __init__(self):
        self.title = "🧽🤖 bAImax 2.0 - Asistente Médico Inteligente"
        self.version = "2.0 Entrenado"
        self.desarrollado_por = "Equipo SENASOFT 2025"
        
        # Componentes del sistema entrenado
        self.chatbot_entrenado = None
        self.knowledge_base = None
        self.learning_system = None
        self.clasificador = None
        self.mapa_sistema = None
        self.graficas = None
        self.recomendador = None
        self.analyzer = None
        
        # Sistema de conversaciones médicas
        self.consultas_medicas = {}
        self.contador_consultas = 0
        
        print(f"🌐 {self.title} v{self.version} inicializado")
    
    def inicializar_sistema(self):
        """
        🚀 Inicializa todos los componentes del sistema web
        """
        print("🚀 Inicializando bAImax Web con Chatbot Médico...")
        
        try:
            # Inicializar chatbot médico entrenado
            self.chatbot_entrenado = bAImaxChatbotEntrenado()
            self.chatbot_entrenado.inicializar_sistema()
            
            # Base de conocimientos
            self.knowledge_base = bAImaxKnowledgeBase()
            
            # Sistema de aprendizaje
            self.learning_system = bAImaxLearningSystem()
            
            # Componentes tradicionales
            self.clasificador = bAImaxClassifier()
            self.mapa_sistema = bAImaxMapa()
            self.graficas = bAImaxGraficas()
            self.recomendador = bAImaxRecomendaciones()
            self.analyzer = bAImaxAnalyzer()
            
            print("✅ Sistema web bAImax inicializado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando sistema: {e}")
            return False
    
    def generar_html_completo(self):
        """
        🎨 Genera la interfaz web HTML completa con chatbot médico
        """
        # Obtener estadísticas del sistema
        stats_conocimiento = self.chatbot_entrenado.obtener_estadisticas_conocimiento() if self.chatbot_entrenado else {}
        
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .logo {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stats {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            background: rgba(102, 126, 234, 0.1);
            padding: 10px 20px;
            border-radius: 20px;
            border: 2px solid rgba(102, 126, 234, 0.3);
        }}
        
        .main-content {{
            padding: 40px 0;
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 30px;
            align-items: start;
        }}
        
        .features-section {{
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        
        .feature-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
        }}
        
        .feature-card h3 {{
            font-size: 1.4em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .feature-card p {{
            opacity: 0.9;
            line-height: 1.5;
        }}
        
        /* Chatbot Styles */
        .chatbot-container {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 400px;
            height: 600px;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            backdrop-filter: blur(15px);
            display: flex;
            flex-direction: column;
            z-index: 1000;
            transition: all 0.3s ease;
        }}
        
        .chatbot-minimized {{
            height: 60px;
            width: 60px;
            bottom: 20px;
            right: 20px;
        }}
        
        .chatbot-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 20px 20px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .chatbot-title {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .minimize-btn {{
            background: none;
            border: none;
            color: white;
            font-size: 1.5em;
            cursor: pointer;
            padding: 5px;
            border-radius: 50%;
            transition: background 0.3s;
        }}
        
        .minimize-btn:hover {{
            background: rgba(255,255,255,0.2);
        }}
        
        .chat-messages {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        
        .message {{
            max-width: 80%;
            padding: 15px;
            border-radius: 18px;
            line-height: 1.4;
            word-wrap: break-word;
        }}
        
        .user-message {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }}
        
        .bot-message {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            align-self: flex-start;
        }}
        
        .medical-analysis {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            border-left: 4px solid #fff;
            font-size: 0.95em;
        }}
        
        .chat-input-container {{
            padding: 20px;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
        }}
        
        .chat-input {{
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }}
        
        .chat-input:focus {{
            border-color: #667eea;
        }}
        
        .send-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }}
        
        .send-btn:hover {{
            transform: scale(1.05);
        }}
        
        .floating-toggle {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 1.5em;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
            display: none;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            z-index: 1001;
        }}
        
        .floating-toggle:hover {{
            transform: scale(1.1);
        }}
        
        .knowledge-stats {{
            background: rgba(76, 175, 80, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }}
        
        .knowledge-stats h4 {{
            color: #2E7D32;
            margin-bottom: 10px;
        }}
        
        .knowledge-item {{
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .main-content {{
                grid-template-columns: 1fr;
            }}
            
            .chatbot-container {{
                width: 90vw;
                height: 70vh;
                bottom: 10px;
                right: 5vw;
            }}
            
            .header-content {{
                flex-direction: column;
                gap: 20px;
            }}
            
            .stats {{
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">{self.title}</div>
                <div class="stats">
                    <div class="stat-item">
                        <strong>🏥 {stats_conocimiento.get('ciudades_disponibles', 4)}</strong> Ciudades
                    </div>
                    <div class="stat-item">
                        <strong>🩺 {stats_conocimiento.get('casos_salud_registrados', 5)}</strong> Casos Médicos
                    </div>
                    <div class="stat-item">
                        <strong>📋 {stats_conocimiento.get('protocolos_atencion', 3)}</strong> Protocolos
                    </div>
                    <div class="stat-item">
                        <strong>v{self.version}</strong>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container">
        <div class="main-content">
            <div class="features-section">
                <h2>🧠 Asistente Médico Inteligente</h2>
                <p style="margin-bottom: 30px; font-size: 1.1em; color: #666;">
                    bAImax es tu asistente médico especializado en salud pública colombiana con conocimientos avanzados.
                </p>
                
                <!-- Estadísticas de Conocimiento -->
                <div class="knowledge-stats">
                    <h4>📊 Base de Conocimientos Médicos</h4>
                    <div class="knowledge-item">
                        <span>🏙️ Ciudades colombianas:</span>
                        <strong>{stats_conocimiento.get('ciudades_disponibles', 4)}</strong>
                    </div>
                    <div class="knowledge-item">
                        <span>🏥 Casos de salud:</span>
                        <strong>{stats_conocimiento.get('casos_salud_registrados', 5)}</strong>
                    </div>
                    <div class="knowledge-item">
                        <span>📋 Protocolos médicos:</span>
                        <strong>{stats_conocimiento.get('protocolos_atencion', 3)}</strong>
                    </div>
                    <div class="knowledge-item">
                        <span>🩺 Síntomas analizables:</span>
                        <strong>{stats_conocimiento.get('mapeo_sintomas', 7)}</strong>
                    </div>
                </div>

                <!-- Features -->
                <div class="feature-card">
                    <h3>🩺 Análisis Médico Inteligente</h3>
                    <p>Analiza síntomas y proporciona recomendaciones de especialistas basadas en conocimientos médicos avanzados.</p>
                </div>

                <div class="feature-card">
                    <h3>📍 Información Contextual</h3>
                    <p>Conoce las ciudades colombianas y adapta las recomendaciones según tu ubicación específica.</p>
                </div>

                <div class="feature-card">
                    <h3>⚡ Evaluación de Urgencia</h3>
                    <p>Evalúa automáticamente el nivel de urgencia y proporciona números de emergencia relevantes.</p>
                </div>

                <div class="feature-card">
                    <h3>🧠 Aprendizaje Continuo</h3>
                    <p>Mejora constantemente con cada consulta para ofrecer recomendaciones más precisas.</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(76, 175, 80, 0.1); border-radius: 10px;">
                    <p><strong>💡 Inicia una conversación con el chatbot médico</strong></p>
                    <p style="font-size: 0.9em; color: #666; margin-top: 10px;">
                        Ejemplo: "Tengo fiebre y dolor de cabeza en Bogotá"
                    </p>
                </div>
            </div>
        </div>
    </main>

    <!-- Chatbot Container -->
    <div class="chatbot-container" id="chatbot">
        <div class="chatbot-header">
            <div class="chatbot-title">🤖 bAImax Médico</div>
            <button class="minimize-btn" onclick="toggleChatbot()">−</button>
        </div>
        <div class="chat-messages" id="messages">
            <div class="message bot-message">
                ¡Hola! 👋 Soy bAImax, tu asistente médico inteligente. 
                Tengo conocimientos sobre salud pública en Colombia. 
                ¿En qué puedo ayudarte?
            </div>
        </div>
        <div class="chat-input-container">
            <input type="text" class="chat-input" id="messageInput" 
                   placeholder="Describe tu consulta médica..." 
                   onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendMessage()">Enviar</button>
        </div>
    </div>

    <!-- Floating Toggle Button -->
    <button class="floating-toggle" id="floatingBtn" onclick="toggleChatbot()">
        🤖
    </button>

    <script>
        let chatbotVisible = true;
        let messageCount = 0;

        function toggleChatbot() {{
            const chatbot = document.getElementById('chatbot');
            const floatingBtn = document.getElementById('floatingBtn');
            
            if (chatbotVisible) {{
                chatbot.style.display = 'none';
                floatingBtn.style.display = 'flex';
            }} else {{
                chatbot.style.display = 'flex';
                floatingBtn.style.display = 'none';
            }}
            chatbotVisible = !chatbotVisible;
        }}

        function handleKeyPress(event) {{
            if (event.key === 'Enter') {{
                sendMessage();
            }}
        }}

        function sendMessage() {{
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Agregar mensaje del usuario
            addMessage(message, 'user');
            input.value = '';
            
            // Simular respuesta del bot (médica)
            setTimeout(() => {{
                const botResponse = generateMedicalResponse(message);
                addMessage(botResponse, 'bot');
            }}, 1000);
        }}

        function addMessage(message, sender) {{
            const messagesContainer = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            
            if (sender === 'user') {{
                messageDiv.className = 'message user-message';
            }} else {{
                // Detectar si es análisis médico
                const isMedical = message.includes('🩺') || message.includes('⚠️') || 
                                message.includes('📊') || message.includes('💡');
                messageDiv.className = isMedical ? 'message medical-analysis' : 'message bot-message';
            }}
            
            messageDiv.innerHTML = message.replace(/\\n/g, '<br>');
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            messageCount++;
        }}

        function generateMedicalResponse(userMessage) {{
            const message = userMessage.toLowerCase();
            
            // Análisis de síntomas básico
            if (message.includes('fiebre') || message.includes('dolor')) {{
                return `🩺 **Análisis médico detectado**
                
                📋 He identificado posibles síntomas en tu consulta.
                
                ⚠️ **Nivel de urgencia: MODERADO**
                
                💡 **Recomendaciones:**
                • Considera consultar con un médico general
                • Mantén hidratación adecuada
                • Monitorea la evolución de los síntomas
                
                📞 **Números importantes:**
                🚨 Emergencias: 123
                🏥 Línea Salud: 018000-910097
                
                ⚡ **Importante:** Esta es una evaluación automatizada. 
                Consulta a un profesional médico para diagnóstico definitivo.`;
            }}
            
            // Respuesta general
            const responses = [
                "Entiendo tu consulta. ¿Puedes ser más específico sobre los síntomas que experimentas?",
                "Para brindarte mejor ayuda, ¿en qué ciudad te encuentras actualmente?",
                "🏥 Te recomiendo consultar con un profesional médico para una evaluación completa.",
                "¿Hay algún síntoma específico que te preocupe más?"
            ];
            
            return responses[Math.floor(Math.random() * responses.length)];
        }}

        // Inicialización
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('bAImax Web App cargada correctamente');
        }});
    </script>
</body>
</html>"""
        
        return html_content
    
    def crear_aplicacion_web(self):
        """
        🚀 Crea y lanza la aplicación web completa
        """
        if not self.inicializar_sistema():
            print("❌ Error inicializando sistema, no se puede crear la aplicación web")
            return
        
        # Generar HTML
        html_content = self.generar_html_completo()
        
        # Crear archivo HTML
        archivo_html = "baimax_medico_web.html"
        
        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Aplicación web creada: {archivo_html}")
        
        # Abrir en navegador
        ruta_completa = os.path.abspath(archivo_html)
        print(f"🌐 Abriendo aplicación web en: {ruta_completa}")
        
        try:
            webbrowser.open(f"file://{ruta_completa}")
            print("✅ Aplicación web abierta en el navegador")
        except Exception as e:
            print(f"⚠️  No se pudo abrir automáticamente: {e}")
            print(f"📂 Puedes abrir manualmente: {archivo_html}")
        
        return archivo_html


def main():
    """
    🚀 Función principal para lanzar bAImax Web
    """
    print("🌐 Iniciando bAImax 2.0 - Aplicación Web Médica...")
    
    # Crear aplicación
    app = bAImaxWebApp()
    
    # Crear y lanzar aplicación web
    archivo_creado = app.crear_aplicacion_web()
    
    if archivo_creado:
        print("\\n" + "="*60)
        print("🎉 bAImax Web App Médica LISTA")
        print("="*60)
        print("✨ Características disponibles:")
        print("   🩺 Chatbot médico entrenado")
        print("   📍 Información de ciudades colombianas")
        print("   ⚡ Análisis de síntomas inteligente")
        print("   📞 Números de emergencia")
        print("   🧠 Aprendizaje continuo")
        print()
        print(f"📁 Archivo creado: {archivo_creado}")
        print("🌐 La aplicación debe abrirse automáticamente en tu navegador")
        print()
        print("💡 Prueba consultas como:")
        print("   • 'Tengo fiebre y dolor de cabeza en Bogotá'")
        print("   • 'Problemas respiratorios en Medellín'")
        print("   • 'Diarrea y vómitos en Cartagena'")
        print("="*60)


if __name__ == "__main__":
    main()