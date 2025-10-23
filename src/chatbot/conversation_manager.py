"""
🤖 Módulo de procesamiento de conversación mejorado para bAImax
"""
import re
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

class ConversationManager:
    def __init__(self, knowledge_base_path: str = "src/data/baimax_knowledge_base_actualizada.json"):
        self.knowledge_base_path = knowledge_base_path
        self.conversation_history = []
        self.current_context = {}
        self.load_knowledge_base()
        self.first_interaction = True
        print("🧠 Cargando base de conocimientos actualizada...")
        
    def load_knowledge_base(self):
        """Carga la base de conocimientos desde el archivo JSON"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        except Exception as e:
            print(f"Error cargando base de conocimientos: {e}")
            self.knowledge_base = {}

    def get_city_info(self, city_name: str) -> Dict[str, Any]:
        """Obtiene información detallada de una ciudad"""
        city_name = city_name.lower()
        return self.knowledge_base.get("ciudades_colombia", {}).get(city_name, {})

    def get_health_recommendations(self, problem_type: str, city_data: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones específicas basadas en el problema y la ciudad"""
        recommendations = []
        if problem_type == "médicos" or problem_type == "salud":
            hospitals = city_data.get("hospitales_principales", [])
            eps = city_data.get("eps_principales", [])
            if hospitals:
                recommendations.append(f"Los principales centros médicos en la zona son: {', '.join(hospitals[:3])}")
            if eps:
                recommendations.append(f"Puede contactar a las siguientes EPS: {', '.join(eps[:3])}")
        elif problem_type == "agua":
            recommendations.extend([
                "Contacte inmediatamente a la empresa de servicios públicos local",
                "Reporte el problema en la línea de atención ciudadana",
                "Mientras se resuelve, hierva el agua por al menos 3 minutos antes de consumirla"
            ])
        return recommendations

    def __init__(self, knowledge_base_path: str = "src/data/baimax_knowledge_base_actualizada.json"):
        self.knowledge_base_path = knowledge_base_path
        self.conversation_history = []
        self.current_context = {
            'asking_for': None,  # 'city' o 'problem'
            'identified_city': None,
            'identified_problem': None,
            'consecutive_questions': 0
        }
        self.load_knowledge_base()
        self.first_interaction = True
        print("🧠 Cargando base de conocimientos actualizada...")

    def reset_context(self):
        """Reinicia el contexto de la conversación"""
        self.current_context = {
            'asking_for': None,
            'identified_city': None,
            'identified_problem': None,
            'consecutive_questions': 0
        }

    def process_message(self, message: str) -> Dict[str, Any]:
        """Procesa un mensaje y genera una respuesta contextual"""
        response = {
            'message': '',
            'type': 'general',
            'suggestions': [],
            'context': {}
        }

        # Primera interacción
        if self.first_interaction:
            hora = datetime.now().hour
            saludo = "¡Buenos días!" if 5 <= hora < 12 else "¡Buenas tardes!" if 12 <= hora < 18 else "¡Buenas noches!"
            response['message'] = (f"{saludo} Soy bAImax, especialista en salud pública. "
                                 "Puedo ayudarte con información sobre servicios médicos, problemas de salud "
                                 "y recomendaciones específicas para tu ciudad.")
            self.first_interaction = False
            return response

        # Procesar el mensaje actual
        message_lower = message.lower()
        
        # Detectar la ciudad y el problema en el mensaje actual
        city_mentioned = None
        problem_type = None
        
        # Buscar menciones de ciudades
        for city in self.knowledge_base.get("ciudades_colombia", {}):
            if city in message_lower or self.knowledge_base["ciudades_colombia"][city]["nombre"].lower() in message_lower:
                city_mentioned = city
                self.current_context['identified_city'] = city
                break
        
        # Detectar tipo de problema
        problem_keywords = {
            'médicos': ["médico", "doctor", "hospital", "salud", "eps", "clínica"],
            'agua': ["agua", "potable", "acueducto", "hidratación"],
            'basura': ["basura", "residuos", "desechos", "reciclaje"],
            'seguridad': ["seguridad", "violencia", "delincuencia", "robos"]
        }
        
        for prob_type, keywords in problem_keywords.items():
            if any(word in message_lower for word in keywords):
                problem_type = prob_type
                self.current_context['identified_problem'] = prob_type
                break
        
        # Si tenemos información guardada en el contexto, usarla
        if not city_mentioned and self.current_context['identified_city']:
            city_mentioned = self.current_context['identified_city']
        if not problem_type and self.current_context['identified_problem']:
            problem_type = self.current_context['identified_problem']

        # Generar respuesta basada en la información disponible
        if city_mentioned and problem_type:
            # Tenemos toda la información necesaria
            city_data = self.get_city_info(city_mentioned)
            city_name = city_data.get("nombre", city_mentioned.title())
            
            response['type'] = 'problema_especifico'
            recommendations = self.get_health_recommendations(problem_type, city_data)
            
            response['message'] = f"Entiendo que hay un problema de {problem_type} en {city_name}. "
            
            if problem_type == "médicos":
                problemas_salud = city_data.get("problemas_comunes", [])
                if problemas_salud:
                    response['message'] += f"En esta ciudad son comunes: {', '.join(problemas_salud[:2])}. "
            
            if recommendations:
                response['message'] += "\n\nRecomendaciones específicas:\n- " + "\n- ".join(recommendations)
            
            # Reiniciar el contexto después de dar una respuesta completa
            self.reset_context()
            
        elif city_mentioned:
            # Solo tenemos la ciudad, preguntar por el problema
            self.current_context['asking_for'] = 'problem'
            response['message'] = (f"En {city_mentioned.title()}, ¿qué tipo de problema necesitas resolver?\n"
                                 "• Atención médica o servicios de salud\n"
                                 "• Problemas con el agua potable\n"
                                 "• Manejo de residuos\n"
                                 "• Seguridad sanitaria")
        elif problem_type:
            # Solo tenemos el problema, preguntar por la ciudad
            self.current_context['asking_for'] = 'city'
            response['message'] = f"¿En qué ciudad estás experimentando este problema de {problem_type}?"
        else:
            # No tenemos ni ciudad ni problema
            if self.current_context['consecutive_questions'] > 2:
                # Si hemos preguntado demasiadas veces, dar una respuesta diferente
                response['message'] = ("Permíteme ayudarte de otra manera. Por favor, describe tu situación en una sola frase, "
                                     "incluyendo el problema y la ciudad. Por ejemplo: 'No hay agua en Bogotá' o 'Faltan médicos en Medellín'.")
                self.reset_context()
            else:
                self.current_context['consecutive_questions'] += 1
                response['message'] = ("Para ayudarte mejor, necesito saber:\n"
                                     "1. La ciudad donde te encuentras\n"
                                     "2. El tipo de problema que enfrentas (salud, agua, etc.)")
        
        # Actualizar el historial
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'response': response,
            'context': self.current_context.copy()
        })

        # Actualizar el historial de conversación
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'response': response
        })

        return response

    def detect_topic(self, message: str) -> str:
        """Detecta el tema principal del mensaje"""
        message = message.lower()
        
        for topic, data in self.knowledge_base.get('respuestas_tematicas', {}).items():
            for pattern in data.get('patrones', []):
                if re.search(pattern, message):
                    return topic
        
        return 'general'

    def extract_keywords(self, message: str) -> List[str]:
        """Extrae palabras clave del mensaje"""
        message = message.lower()
        keywords = []
        
        for category, words in self.knowledge_base.get('palabras_clave', {}).items():
            for word in words:
                if word in message:
                    keywords.append((category, word))
        
        return keywords

    def get_context_variables(self, topic: str) -> Dict[str, str]:
        """Obtiene variables de contexto para un tema específico"""
        context = {}
        
        if topic == 'falta_medicos':
            city = self.current_context.get('city', 'Bogotá')
            context = {
                'ciudad': city,
                'numero': '20-30',
                'especialidades': 'Cardiología, Pediatría, Neurología',
                'especialidad': 'Medicina General'
            }
        elif topic == 'tiempo_espera':
            hospital = self.current_context.get('hospital', 'Hospital General')
            context = {
                'hospital': hospital,
                'tiempo_general': '3-5 días',
                'tiempo_especialista': '15-20 días',
                'tiempo_urgencias': '2-4 horas',
                'recomendacion': 'Agenda tus citas con anticipación'
            }
        
        return context

    def fill_template(self, template: str, variables: Dict[str, str]) -> str:
        """Rellena una plantilla con variables de contexto"""
        for key, value in variables.items():
            template = template.replace(f"{{{key}}}", value)
        return template

    def generate_suggestions(self, topic: str) -> List[str]:
        """Genera sugerencias basadas en el tema actual"""
        suggestions = []
        
        if topic == 'falta_medicos':
            suggestions = [
                "Ver hospitales cercanos",
                "Consultar especialistas disponibles",
                "Opciones de telemedicina"
            ]
        elif topic == 'tiempo_espera':
            suggestions = [
                "Buscar otros centros médicos",
                "Agendar cita",
                "Ver horarios de atención"
            ]
        
        return suggestions

    def generate_contextual_response(self, keywords: List[tuple]) -> str:
        """Genera una respuesta contextual basada en palabras clave"""
        if not keywords:
            return "¿Podrías ser más específico sobre lo que necesitas?"
            
        category, keyword = keywords[0]  # Usar la primera palabra clave encontrada
        
        if category == 'urgencias':
            return "🚨 Para emergencias, te recomiendo acudir al centro médico más cercano. ¿Necesitas que te indique las opciones disponibles?"
        elif category == 'especialidades':
            return f"👨‍⚕️ Puedo ayudarte a encontrar especialistas en {keyword}. ¿En qué zona estás buscando?"
        elif category == 'sintomas':
            return "Para brindarte una mejor orientación, ¿podrías describir más detalladamente tus síntomas?"
        elif category == 'servicios':
            return "Te puedo informar sobre los servicios disponibles. ¿Buscas algún centro médico en particular?"
            
        return "Entiendo tu consulta. ¿Podrías darme más detalles para ayudarte mejor?"