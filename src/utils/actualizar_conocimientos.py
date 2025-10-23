"""
Script para actualizar la base de conocimientos de bAImax
"""
from core.baimax_knowledge_base import bAImaxKnowledgeBase
import json

def actualizar_base_conocimientos():
    # Crear instancia de la base de conocimientos
    kb = bAImaxKnowledgeBase()
    
    # Cargar nuevos conocimientos
    with open('src/data/baimax_knowledge_base_actualizada.json', 'r', encoding='utf-8') as f:
        nuevos_conocimientos = json.load(f)
    
    # Actualizar la base de conocimientos
    if 'ciudades_colombia' in nuevos_conocimientos:
        kb.ciudades_colombia = nuevos_conocimientos['ciudades_colombia']
    
    # Agregar nuevos patrones de respuesta
    kb.patrones_respuesta = {
        "saludo": [
            "¡Hola! Soy bAImax, tu asistente médico virtual. ¿En qué puedo ayudarte hoy?",
            "Saludos, soy bAImax. Estoy aquí para asistirte con información y orientación médica. ¿Qué necesitas?",
            "¡Bienvenido! Soy bAImax, tu guía en el sistema de salud. ¿Cómo puedo ayudarte?"
        ],
        "despedida": [
            "Gracias por consultar con bAImax. ¡Que tengas un excelente día! No dudes en volver si necesitas más ayuda.",
            "Ha sido un placer ayudarte. Recuerda que estoy disponible 24/7 para cualquier consulta.",
            "¡Cuídate mucho! Si necesitas más información, no dudes en preguntarme."
        ],
        "falta_medicos": [
            "Se ha detectado un déficit de médicos en esa zona. Las especialidades más afectadas son cardiología, pediatría y neurología. Se están implementando programas de telemedicina y rotación de especialistas.",
            "La escasez de médicos está siendo abordada mediante convenios con universidades y hospitales. Se proyecta incorporar 150 nuevos profesionales en los próximos meses.",
            "Se está trabajando en un plan de incentivos para atraer más especialistas a la zona. El déficit actual afecta principalmente a especialidades críticas."
        ],
        "tiempos_espera": [
            "Los tiempos de espera actuales son: Urgencias: 2-4 horas, Consulta especializada: 15-30 días. Se recomienda agendar citas con anticipación.",
            "Se ha implementado un sistema de triaje mejorado para reducir los tiempos de espera. La espera promedio se ha reducido en un 25%.",
            "Para reducir la espera, se habilitaron nuevos consultorios. También puede usar nuestra plataforma de telemedicina."
        ]
    }
    
    # Agregar palabras clave para mejor reconocimiento
    kb.keywords = {
        "urgencias": ["urgencia", "emergencia", "ambulancia", "crítico", "grave", "inmediato"],
        "consultas": ["cita", "consulta", "médico", "especialista", "doctor"],
        "medicamentos": ["medicina", "medicamento", "pastilla", "tratamiento", "receta"],
        "eps": ["eps", "seguro", "afiliación", "carnet", "cobertura"],
        "hospitales": ["hospital", "clínica", "centro médico", "sanatorio", "institución"],
        "sintomas": ["dolor", "fiebre", "malestar", "síntoma", "molestia"],
        "especialidades": ["cardiólogo", "pediatra", "ginecólogo", "ortopedista", "psiquiatra"]
    }
    
    # Guardar la base de conocimientos actualizada
    kb.guardar_conocimientos('src/data/baimax_knowledge_base.json')
    print("✅ Base de conocimientos actualizada exitosamente")

if __name__ == '__main__':
    actualizar_base_conocimientos()