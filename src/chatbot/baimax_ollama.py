#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 bAImax OLLAMA Integration - Chatbot Inteligente Local
========================================================

PROPÓSITO: Integra Ollama (Llama2 local) con el chatbot bAImax para 
proporcionar respuestas médicas más naturales y precisas sin depender 
de APIs externas ni costos adicionales.

JUSTIFICACIÓN EN EL PROYECTO:
- Chatbot completamente gratuito y sin límites de uso
- Respuestas médicas contextualizadas y profesionales  
- Funciona sin conexión a internet una vez configurado
- Privacidad total - datos médicos no salen del equipo
- Diferenciador clave para SENASOFT 2025

ARQUITECTURA:
🏗️ DISEÑO:
1. Cliente Ollama local ejecutando Llama2
2. API REST local en puerto 11434
3. Integración con sistema bAImax existente
4. Fallback al chatbot básico si Ollama no disponible
5. Prompts especializados en contexto médico colombiano

CASOS DE USO:
👩‍⚕️ CONSULTAS MÉDICAS: Respuestas naturales sobre síntomas
🚨 EMERGENCIAS: Orientación inmediata y profesional  
📊 ANÁLISIS: Interpretación de datos epidemiológicos
🏛️ INSTITUCIONAL: Comunicación con ciudadanos

Desarrollado para IBM SENASOFT 2025 - Innovación en IA Local
"""

import requests
import json
import time
from typing import Dict, Any, Optional
import logging

class bAImaxOllama:
    """
    🤖 Motor de IA conversacional local para bAImax usando Ollama
    """
    
    def __init__(self, modelo: str = "llama2"):
        """
        Inicializa la conexión con Ollama
        
        Args:
            modelo: Nombre del modelo a usar (llama2, mistral, etc.)
        """
        self.modelo = modelo
        self.url_base = "http://localhost:11434"
        self.disponible = False
        self.timeout = 30  # segundos
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Verificar disponibilidad
        self._verificar_conexion()
        
    def _verificar_conexion(self) -> bool:
        """
        Verifica si Ollama está ejecutándose y el modelo disponible
        
        Returns:
            bool: True si Ollama está disponible
        """
        try:
            # Verificar si Ollama está corriendo
            response = requests.get(f"{self.url_base}/api/tags", timeout=5)
            
            if response.status_code == 200:
                modelos = response.json()
                modelos_disponibles = [m['name'] for m in modelos.get('models', [])]
                
                if self.modelo in modelos_disponibles or any(self.modelo in m for m in modelos_disponibles):
                    self.disponible = True
                    self.logger.info(f"✅ Ollama conectado - Modelo {self.modelo} disponible")
                    return True
                else:
                    self.logger.warning(f"⚠️ Modelo {self.modelo} no encontrado. Disponibles: {modelos_disponibles}")
                    return False
            else:
                self.logger.warning("⚠️ Ollama ejecutándose pero no responde correctamente")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"⚠️ Ollama no disponible: {e}")
            return False
    
    def _crear_prompt_medico(self, mensaje_usuario: str, contexto: Dict[str, Any] = None) -> str:
        """
        Crea un prompt especializado para consultas médicas
        
        Args:
            mensaje_usuario: Mensaje del usuario
            contexto: Información adicional (ciudad, edad, etc.)
            
        Returns:
            str: Prompt optimizado para respuestas médicas
        """
        
        prompt_sistema = """Eres un asistente médico inteligente llamado bAImax, especializado en el sistema de salud colombiano. 

INSTRUCCIONES IMPORTANTES:
- Proporciona información médica general y orientación
- NUNCA hagas diagnósticos definitivos
- Siempre recomienda consultar un profesional de salud
- Usa terminología comprensible para ciudadanos colombianos
- Si es una emergencia, recomienda llamar al 123 o acudir a urgencias
- Sé empático y profesional
- Respuestas concisas de máximo 150 palabras
- Incluye emojis médicos apropiados

CONTEXTO DEL SISTEMA:
- Eres parte de bAImax 2.0, sistema de IBM SENASOFT 2025
- Ayudas a clasificar gravedad de casos médicos
- Trabajas con datos del Ministerio de Salud de Colombia"""

        if contexto:
            info_contexto = f"\nCONTEXTO ADICIONAL:\n"
            if 'ciudad' in contexto:
                info_contexto += f"- Ciudad: {contexto['ciudad']}\n"
            if 'edad' in contexto:
                info_contexto += f"- Edad: {contexto['edad']} años\n"
            if 'gravedad_detectada' in contexto:
                info_contexto += f"- Gravedad detectada por IA: {contexto['gravedad_detectada']}\n"
        else:
            info_contexto = ""
            
        prompt_completo = f"{prompt_sistema}{info_contexto}\n\nCONSULTA DEL USUARIO: {mensaje_usuario}\n\nRESPUESTA MÉDICA:"
        
        return prompt_completo
    
    def generar_respuesta(self, mensaje: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Genera una respuesta usando Ollama
        
        Args:
            mensaje: Mensaje del usuario
            contexto: Contexto adicional opcional
            
        Returns:
            Dict con la respuesta y metadatos
        """
        
        if not self.disponible:
            return {
                'respuesta': "🤖 El asistente IA avanzado no está disponible. Usando modo básico.",
                'exito': False,
                'tiempo_ms': 0,
                'modelo_usado': 'basic'
            }
        
        try:
            inicio = time.time()
            
            # Crear prompt especializado
            prompt = self._crear_prompt_medico(mensaje, contexto)
            
            # Configurar request para Ollama
            payload = {
                "model": self.modelo,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 200,
                    "stop": ["\n\nCONSULTA DEL USUARIO:", "RESPUESTA MÉDICA:"]
                }
            }
            
            # Hacer request a Ollama
            response = requests.post(
                f"{self.url_base}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                resultado = response.json()
                respuesta_texto = resultado.get('response', '').strip()
                
                # Limpiar respuesta
                respuesta_limpia = self._limpiar_respuesta(respuesta_texto)
                
                tiempo_total = int((time.time() - inicio) * 1000)
                
                self.logger.info(f"✅ Respuesta generada en {tiempo_total}ms")
                
                return {
                    'respuesta': respuesta_limpia,
                    'exito': True,
                    'tiempo_ms': tiempo_total,
                    'modelo_usado': self.modelo,
                    'tokens_usados': len(respuesta_texto.split())
                }
            else:
                self.logger.error(f"❌ Error de Ollama: {response.status_code}")
                return {
                    'respuesta': "🤖 Error temporal del asistente IA. Intente nuevamente.",
                    'exito': False,
                    'tiempo_ms': int((time.time() - inicio) * 1000),
                    'modelo_usado': 'error'
                }
                
        except requests.exceptions.Timeout:
            self.logger.error("❌ Timeout en respuesta de Ollama")
            return {
                'respuesta': "🤖 El asistente está procesando. Intente con una consulta más específica.",
                'exito': False,
                'tiempo_ms': self.timeout * 1000,
                'modelo_usado': 'timeout'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error inesperado: {e}")
            return {
                'respuesta': "🤖 Error del sistema. Por favor, contacte soporte técnico.",
                'exito': False,
                'tiempo_ms': 0,
                'modelo_usado': 'error'
            }
    
    def _limpiar_respuesta(self, respuesta: str) -> str:
        """
        Limpia y formatea la respuesta de Ollama
        
        Args:
            respuesta: Texto crudo de Ollama
            
        Returns:
            str: Respuesta limpia y formateada
        """
        
        # Eliminar texto del sistema que pueda haberse colado
        limpiadores = [
            "RESPUESTA MÉDICA:",
            "CONSULTA DEL USUARIO:",
            "INSTRUCCIONES IMPORTANTES:",
            "CONTEXTO DEL SISTEMA:"
        ]
        
        respuesta_limpia = respuesta
        for limpiador in limpiadores:
            respuesta_limpia = respuesta_limpia.replace(limpiador, "").strip()
        
        # Asegurar que empiece con emoji si no lo tiene
        if respuesta_limpia and not any(emoji in respuesta_limpia[:5] for emoji in ['🏥', '🤖', '⚠️', '🚨', '💊', '🔬']):
            respuesta_limpia = f"🏥 {respuesta_limpia}"
        
        # Limitar longitud
        if len(respuesta_limpia) > 400:
            respuesta_limpia = respuesta_limpia[:397] + "..."
        
        return respuesta_limpia
    
    def verificar_modelo_disponible(self) -> bool:
        """
        Reververifica si el modelo está disponible
        
        Returns:
            bool: Estado actual de disponibilidad
        """
        return self._verificar_conexion()
    
    def obtener_info_sistema(self) -> Dict[str, Any]:
        """
        Obtiene información del sistema Ollama
        
        Returns:
            Dict con información del sistema
        """
        
        if not self.disponible:
            return {
                'estado': 'No disponible',
                'modelo': self.modelo,
                'url': self.url_base
            }
        
        try:
            response = requests.get(f"{self.url_base}/api/tags", timeout=5)
            if response.status_code == 200:
                info = response.json()
                return {
                    'estado': 'Conectado',
                    'modelo': self.modelo,
                    'url': self.url_base,
                    'modelos_disponibles': [m['name'] for m in info.get('models', [])],
                    'version_ollama': 'Ejecutándose'
                }
        except Exception as e:
            return {
                'estado': f'Error: {e}',
                'modelo': self.modelo,
                'url': self.url_base
            }

# =============================================================================
# FUNCIONES DE UTILIDAD PARA INTEGRACIÓN
# =============================================================================

def probar_ollama() -> None:
    """
    Función de prueba para verificar Ollama
    """
    print("🤖 Probando conexión con Ollama...")
    
    ollama = bAImaxOllama()
    info = ollama.obtener_info_sistema()
    
    print(f"📊 Estado: {info['estado']}")
    if 'modelos_disponibles' in info:
        print(f"📚 Modelos: {', '.join(info['modelos_disponibles'])}")
    
    if ollama.disponible:
        print("\n🧪 Probando respuesta...")
        respuesta = ollama.generar_respuesta(
            "Hola, tengo dolor de cabeza leve",
            contexto={'ciudad': 'Bogotá', 'edad': 30}
        )
        
        print(f"✅ Respuesta ({respuesta['tiempo_ms']}ms): {respuesta['respuesta']}")
    else:
        print("❌ Ollama no disponible. Verifique instalación.")

if __name__ == "__main__":
    probar_ollama()