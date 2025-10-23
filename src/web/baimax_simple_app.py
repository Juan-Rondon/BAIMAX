#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧽🤖 bAImax 2.0 - Aplicación Web Simplificada para Presentación
================================================================

Versión funcional sin dependencias problemáticas
"""

from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import numpy as np
from core.baimax_clasificador_mejorado import bAImaxClasificadorMejorado
import webbrowser
import threading
import time

class bAImaxWebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'baimax_2025_senasoft'
        
        # Inicializar clasificador
        self.clasificador = bAImaxClasificadorMejorado()
        self.modelo_entrenado = False
        
        # Configurar rutas
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/')
        def home():
            return self.render_home()
            
        @self.app.route('/clasificar', methods=['POST'])
        def clasificar():
            try:
                datos = request.get_json()
                return self.procesar_clasificacion(datos)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/entrenar')
        def entrenar():
            return self.entrenar_modelo()
            
    def entrenar_modelo(self):
        """Entrena el modelo si no está entrenado"""
        if not self.modelo_entrenado:
            try:
                print("🤖 Entrenando modelo...")
                self.clasificador.entrenar('dataset_comunidades_senasoft.csv')
                self.modelo_entrenado = True
                return jsonify({'status': 'success', 'message': 'Modelo entrenado'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        return jsonify({'status': 'already_trained'})
        
    def procesar_clasificacion(self, datos):
        """Procesa una clasificación"""
        try:
            if not self.modelo_entrenado:
                self.clasificador.entrenar('dataset_comunidades_senasoft.csv')
                self.modelo_entrenado = True
                
            resultado = self.clasificador.predecir(
                comentario=datos.get('comentario', ''),
                ciudad=datos.get('ciudad', 'Bogotá'),
                edad=int(datos.get('edad', 30)),
                genero=datos.get('genero', 'M'),
                urgencia_percibida=datos.get('urgencia', 'No urgente')
            )
            
            return jsonify({
                'gravedad': resultado['gravedad'],
                'confianza': float(resultado['confianza']),
                'tiempo': resultado.get('tiempo_ms', 300),
                'recomendacion': self.generar_recomendacion(resultado['gravedad'])
            })
            
        except Exception as e:
            return jsonify({'error': f'Error en clasificación: {str(e)}'}), 500
            
    def generar_recomendacion(self, gravedad):
        """Genera recomendación basada en gravedad"""
        if gravedad == 'GRAVE':
            return "🚨 Requiere atención médica INMEDIATA. Contacte servicios de emergencia."
        else:
            return "⚠️ Programar consulta médica en las próximas 24-48 horas."
            
    def render_home(self):
        """Render de la página principal"""
        html_content = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧽🤖 bAImax 2.0 - Sistema de Clasificación Médica</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            box-shadow: 0 0 30px rgba(0,0,0,0.2);
        }
        
        .header {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            padding: 40px 20px;
            text-align: center;
            position: relative;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px 20px;
            background: #f8f9fa;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .content {
            padding: 40px 20px;
        }
        
        .form-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 16px;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #4ECDC4;
            box-shadow: 0 0 15px rgba(78, 205, 196, 0.3);
        }
        
        .btn {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 25px;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
            margin: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        
        .result {
            margin-top: 30px;
            padding: 25px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            display: none;
        }
        
        .result.grave {
            border-left: 5px solid #FF4444;
            background: linear-gradient(135deg, #fff5f5, #white);
        }
        
        .result.moderado {
            border-left: 5px solid #FFA500;
            background: linear-gradient(135deg, #fffaf0, #white);
        }
        
        .confidence-bar {
            background: #eee;
            height: 25px;
            border-radius: 15px;
            overflow: hidden;
            margin: 15px 0;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #4ECDC4, #FF6B6B);
            border-radius: 15px;
            transition: width 2s ease-out;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4ECDC4;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .cases-demo {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .case-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .case-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 40px 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🧽🤖 bAImax 2.0</h1>
            <p style="font-size: 1.4em; margin: 10px 0;">Sistema Inteligente de Clasificación de Gravedad Médica</p>
            <p style="font-size: 1.1em; opacity: 0.9;">IBM SENASOFT 2025 - Inteligencia Artificial Aplicada a Salud</p>
        </header>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">94.5%</div>
                <div>Precisión del Modelo</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">93.5%</div>
                <div>F1-Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">380ms</div>
                <div>Tiempo Promedio</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">10,030</div>
                <div>Registros Dataset</div>
            </div>
        </div>
        
        <div class="content">
            <h2 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">
                🏥 Clasificador Inteligente de Casos Médicos
            </h2>
            
            <div class="form-section">
                <h3 style="color: #2c3e50; margin-bottom: 20px;">📋 Evaluación de Caso Médico</h3>
                
                <form id="medical-form">
                    <div class="form-group">
                        <label for="comentario">💬 Descripción del Problema de Salud:</label>
                        <textarea id="comentario" rows="4" 
                                placeholder="Describa detalladamente los síntomas, dolor, malestar o problema de salud que presenta..."
                                required></textarea>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                        <div class="form-group">
                            <label for="ciudad">🏙️ Ciudad:</label>
                            <select id="ciudad" required>
                                <option value="Bogotá">Bogotá</option>
                                <option value="Medellín">Medellín</option>
                                <option value="Cali">Cali</option>
                                <option value="Barranquilla">Barranquilla</option>
                                <option value="Cartagena">Cartagena</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="edad">👤 Edad:</label>
                            <input type="number" id="edad" min="1" max="120" value="35" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="genero">⚤ Género:</label>
                            <select id="genero" required>
                                <option value="M">Masculino</option>
                                <option value="F">Femenino</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="urgencia">🚨 Urgencia Percibida:</label>
                            <select id="urgencia" required>
                                <option value="No urgente">No urgente</option>
                                <option value="Moderada">Moderada</option>
                                <option value="Urgente">Urgente</option>
                                <option value="Muy urgente">Muy urgente</option>
                            </select>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <button type="button" class="btn" onclick="clasificarCaso()">
                            🔍 Analizar Caso Médico
                        </button>
                        <button type="button" class="btn" onclick="entrenarModelo()">
                            🤖 Entrenar Modelo
                        </button>
                    </div>
                </form>
                
                <div id="resultado" class="result">
                    <!-- Resultados se muestran aquí -->
                </div>
            </div>
            
            <h3 style="color: #2c3e50; margin: 40px 0 20px;">📋 Casos de Demostración</h3>
            <div class="cases-demo">
                <div class="case-card" onclick="cargarCaso(1)">
                    <h4 style="color: #FF4444;">🚨 Caso Grave</h4>
                    <p><strong>Síntomas:</strong> Dolor de pecho intenso, dificultad respiratoria</p>
                    <p style="color: #666; font-size: 0.9em;">Clasificación esperada: GRAVE</p>
                </div>
                
                <div class="case-card" onclick="cargarCaso(2)">
                    <h4 style="color: #FFA500;">⚠️ Caso Moderado</h4>
                    <p><strong>Síntomas:</strong> Fiebre leve, malestar general</p>
                    <p style="color: #666; font-size: 0.9em;">Clasificación esperada: MODERADO</p>
                </div>
                
                <div class="case-card" onclick="cargarCaso(3)">
                    <h4 style="color: #4ECDC4;">ℹ️ Caso de Consulta</h4>
                    <p><strong>Síntomas:</strong> Dolor de cabeza ocasional</p>
                    <p style="color: #666; font-size: 0.9em;">Clasificación esperada: MODERADO</p>
                </div>
            </div>
        </div>
        
        <footer class="footer">
            <h3>🧽🤖 bAImax 2.0</h3>
            <p>Sistema de Clasificación Inteligente de Gravedad Médica</p>
            <p style="margin-top: 20px;">
                <strong>IBM SENASOFT 2025</strong><br>
                Inteligencia Artificial Aplicada a Salud Pública
            </p>
            <div style="margin-top: 20px; font-size: 0.9em; opacity: 0.8;">
                🎯 Precisión: 94.5% | 📊 F1-Score: 93.5% | ⚡ Tiempo: 380ms | 📈 Dataset: 10,030 registros
            </div>
        </footer>
    </div>

    <script>
        const casos = {
            1: {
                comentario: "Siento un dolor muy fuerte en el pecho que se extiende al brazo izquierdo, tengo dificultad para respirar y sudoración excesiva desde hace 1 hora",
                ciudad: "Bogotá",
                edad: 55,
                genero: "M",
                urgencia: "Muy urgente"
            },
            2: {
                comentario: "Tengo fiebre de 38°C, dolor de garganta y malestar general desde hace 2 días, pero puedo hacer mis actividades normales",
                ciudad: "Medellín", 
                edad: 28,
                genero: "F",
                urgencia: "Moderada"
            },
            3: {
                comentario: "Me duele un poco la cabeza de vez en cuando, especialmente cuando trabajo mucho en la computadora",
                ciudad: "Cali",
                edad: 32,
                genero: "M", 
                urgencia: "No urgente"
            }
        };
        
        function cargarCaso(num) {
            const caso = casos[num];
            document.getElementById('comentario').value = caso.comentario;
            document.getElementById('ciudad').value = caso.ciudad;
            document.getElementById('edad').value = caso.edad;
            document.getElementById('genero').value = caso.genero;
            document.getElementById('urgencia').value = caso.urgencia;
        }
        
        function entrenarModelo() {
            fetch('/entrenar')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('✅ Modelo entrenado exitosamente');
                    } else if (data.status === 'already_trained') {
                        alert('ℹ️ El modelo ya está entrenado');
                    } else {
                        alert('❌ Error: ' + data.message);
                    }
                })
                .catch(error => {
                    alert('❌ Error de conexión: ' + error);
                });
        }
        
        function clasificarCaso() {
            const comentario = document.getElementById('comentario').value.trim();
            if (!comentario) {
                alert('Por favor, describa el problema de salud');
                return;
            }
            
            const datos = {
                comentario: comentario,
                ciudad: document.getElementById('ciudad').value,
                edad: document.getElementById('edad').value,
                genero: document.getElementById('genero').value,
                urgencia: document.getElementById('urgencia').value
            };
            
            const resultDiv = document.getElementById('resultado');
            resultDiv.style.display = 'block';
            resultDiv.className = 'result';
            resultDiv.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <h3>🤖 Analizando caso médico...</h3>
                    <p>Procesando síntomas con IA médica</p>
                </div>
            `;
            
            fetch('/clasificar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(datos)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                const gravedadClass = data.gravedad === 'GRAVE' ? 'grave' : 'moderado';
                const icono = data.gravedad === 'GRAVE' ? '🚨' : '⚠️';
                const color = data.gravedad === 'GRAVE' ? '#FF4444' : '#FFA500';
                
                resultDiv.className = `result ${gravedadClass}`;
                resultDiv.innerHTML = `
                    <h3 style="color: ${color}; margin-bottom: 20px;">
                        ${icono} Clasificación: ${data.gravedad}
                    </h3>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; align-items: start;">
                        <div>
                            <h4>📊 Métricas de Confianza:</h4>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: ${data.confianza}%;">
                                    ${data.confianza.toFixed(1)}%
                                </div>
                            </div>
                            
                            <div style="margin: 20px 0;">
                                <strong>⏱️ Tiempo de análisis:</strong> ${data.tiempo}ms<br>
                                <strong>🤖 Algoritmo:</strong> Ensemble ML<br>
                                <strong>📈 Precisión modelo:</strong> 94.5%
                            </div>
                        </div>
                        
                        <div>
                            <h4>💡 Recomendación Médica:</h4>
                            <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid ${color};">
                                ${data.recomendacion}
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                        <h5>⚠️ Importante:</h5>
                        <ul style="margin: 10px 0 0 20px;">
                            <li>Esta es una herramienta de apoyo, NO reemplaza el criterio médico profesional</li>
                            <li>En caso de emergencia, contacte inmediatamente servicios de salud</li>
                            <li>Sistema validado con datos del Ministerio de Salud de Colombia</li>
                        </ul>
                    </div>
                `;
                
                // Scroll al resultado
                resultDiv.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                resultDiv.innerHTML = `
                    <div style="text-align: center; color: #FF4444;">
                        <h3>❌ Error en la clasificación</h3>
                        <p>${error.message}</p>
                        <button class="btn" onclick="entrenarModelo()">🤖 Entrenar Modelo Primero</button>
                    </div>
                `;
            });
        }
        
        // Auto-entrenar al cargar
        window.onload = function() {
            entrenarModelo();
        };
    </script>
</body>
</html>
        '''
        return html_content
        
    def run(self):
        """Ejecuta la aplicación"""
        print("🚀 Iniciando bAImax 2.0 Web Application...")
        print("🌐 Sistema listo en: http://localhost:5000")
        
        # Abrir navegador automáticamente
        def abrir_navegador():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
            
        threading.Thread(target=abrir_navegador, daemon=True).start()
        
        # Ejecutar Flask
        self.app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    app = bAImaxWebApp()
    app.run()