"""
🎯 bAImax - Sistema de Recomendaciones de Puntos de Atención
============================================================

Módulo para recomendar puntos de atención según el tipo de problema
"""

import pandas as pd
import random
from typing import List, Dict, Any

class bAImaxRecomendaciones:
    """
    🎯 Sistema inteligente de recomendaciones de puntos de atención
    
    Mapea problemas de salud pública a entidades y servicios apropiados
    """
    
    def __init__(self):
        self.puntos_atencion = self._crear_base_puntos_atencion()
        self.mapeo_problemas = self._crear_mapeo_problemas()
        
    def _crear_base_puntos_atencion(self) -> Dict:
        """
        🏥 Crea base de datos sintética de puntos de atención
        """
        return {
            'Bogotá': {
                'hospitales': [
                    {'nombre': 'Hospital San Juan de Dios', 'telefono': '(1) 597-3300', 'direccion': 'Calle 10 #15-20', 'especialidad': 'General'},
                    {'nombre': 'Hospital La Samaritana', 'telefono': '(1) 353-1515', 'direccion': 'Carrera 8 #0-29 Sur', 'especialidad': 'Urgencias'},
                    {'nombre': 'Clínica Marly', 'telefono': '(1) 343-6600', 'direccion': 'Calle 50 #9-67', 'especialidad': 'Especializada'}
                ],
                'centros_salud': [
                    {'nombre': 'Centro de Salud Chapinero', 'telefono': '(1) 594-1000', 'direccion': 'Calle 63 #11-40'},
                    {'nombre': 'Centro de Salud Usaquén', 'telefono': '(1) 671-3000', 'direccion': 'Carrera 7 #116-50'}
                ],
                'acueducto': [
                    {'nombre': 'EAAB - Empresa de Acueducto', 'telefono': '(1) 377-2000', 'web': 'eaab.com.co', 'direccion': 'Diagonal 47A #15-09'}
                ],
                'policia': [
                    {'nombre': 'CAI Centro', 'telefono': '(1) 315-9111', 'direccion': 'Plaza de Bolívar'},
                    {'nombre': 'Policía Nacional - MEBOG', 'telefono': '123', 'direccion': 'Carrera 59 #26-21'}
                ],
                'alcaldia': [
                    {'nombre': 'Alcaldía Mayor de Bogotá', 'telefono': '(1) 381-3000', 'web': 'bogota.gov.co', 'direccion': 'Carrera 8 #10-65'}
                ],
                'secretaria_salud': [
                    {'nombre': 'Secretaría Distrital de Salud', 'telefono': '(1) 364-9000', 'direccion': 'Carrera 32 #12-81'}
                ]
            },
            'Medellín': {
                'hospitales': [
                    {'nombre': 'Hospital San Vicente Fundación', 'telefono': '(4) 444-1333', 'direccion': 'Calle 64 #51A-30', 'especialidad': 'General'},
                    {'nombre': 'Clínica Medellín', 'telefono': '(4) 305-6565', 'direccion': 'Carrera 48 #32-15', 'especialidad': 'Especializada'}
                ],
                'centros_salud': [
                    {'nombre': 'Centro de Salud Belén', 'telefono': '(4) 385-5500', 'direccion': 'Calle 30A #76-55'}
                ],
                'acueducto': [
                    {'nombre': 'EPM', 'telefono': '(4) 380-8000', 'web': 'epm.com.co', 'direccion': 'Carrera 58 #42-125'}
                ],
                'policia': [
                    {'nombre': 'CAI El Poblado', 'telefono': '(4) 385-5555', 'direccion': 'Carrera 43A #5-15'}
                ],
                'alcaldia': [
                    {'nombre': 'Alcaldía de Medellín', 'telefono': '(4) 385-5555', 'web': 'medellin.gov.co', 'direccion': 'Calle 44 #52-165'}
                ]
            },
            'Cali': {
                'hospitales': [
                    {'nombre': 'Hospital Universitario del Valle', 'telefono': '(2) 620-2020', 'direccion': 'Calle 5 #36-08', 'especialidad': 'General'},
                    {'nombre': 'Clínica Imbanaco', 'telefono': '(2) 555-1000', 'direccion': 'Carrera 38A #5A-100', 'especialidad': 'Especializada'}
                ],
                'acueducto': [
                    {'nombre': 'EMCALI', 'telefono': '(2) 620-1010', 'web': 'emcali.com.co', 'direccion': 'Calle 54 #2-50'}
                ],
                'alcaldia': [
                    {'nombre': 'Alcaldía de Cali', 'telefono': '(2) 660-1010', 'web': 'cali.gov.co', 'direccion': 'Avenida 2 Norte #10-70'}
                ]
            },
            'Barranquilla': {
                'hospitales': [
                    {'nombre': 'Hospital Universidad del Norte', 'telefono': '(5) 350-9999', 'direccion': 'Calle 76 #55-133', 'especialidad': 'General'}
                ],
                'acueducto': [
                    {'nombre': 'Triple A', 'telefono': '(5) 360-5555', 'web': 'aaa.com.co', 'direccion': 'Vía 40 #36-135'}
                ],
                'alcaldia': [
                    {'nombre': 'Alcaldía de Barranquilla', 'telefono': '(5) 339-9999', 'web': 'barranquilla.gov.co', 'direccion': 'Carrera 54 #75-44'}
                ]
            },
            'Cartagena': {
                'hospitales': [
                    {'nombre': 'Hospital Naval', 'telefono': '(5) 669-0640', 'direccion': 'Bosque #30B-149', 'especialidad': 'General'}
                ],
                'acueducto': [
                    {'nombre': 'Aguas de Cartagena', 'telefono': '(5) 693-7777', 'web': 'acuacar.com', 'direccion': 'Avenida Pedro de Heredia #31-74'}
                ]
            }
        }
    
    def _crear_mapeo_problemas(self) -> Dict:
        """
        🗺️ Crea mapeo de problemas a tipos de entidades
        """
        return {
            'agua potable': ['acueducto', 'alcaldia', 'secretaria_salud'],
            'médicos': ['hospitales', 'centros_salud', 'secretaria_salud'],
            'centro de salud': ['hospitales', 'centros_salud', 'secretaria_salud'],
            'seguridad': ['policia', 'alcaldia'],
            'calles oscuras': ['policia', 'alcaldia'],
            'presencia policial': ['policia', 'alcaldia'],
            'contaminación': ['alcaldia', 'secretaria_salud'],
            'basura': ['alcaldia'],
            'recolección': ['alcaldia'],
            'internet': ['alcaldia'],
            'escuelas': ['alcaldia'],
            'bibliotecas': ['alcaldia'],
            'centros culturales': ['alcaldia']
        }
    
    def analizar_problema(self, comentario: str) -> List[str]:
        """
        🔍 Analiza el comentario para identificar el tipo de problema
        """
        comentario_lower = comentario.lower()
        tipos_identificados = []
        
        for problema, entidades in self.mapeo_problemas.items():
            if problema in comentario_lower:
                tipos_identificados.extend(entidades)
        
        # Si no se identifica ningún problema específico, retornar opciones generales
        if not tipos_identificados:
            tipos_identificados = ['alcaldia', 'secretaria_salud']
        
        # Eliminar duplicados manteniendo orden
        return list(dict.fromkeys(tipos_identificados))
    
    def recomendar_puntos_atencion(self, comentario: str, ciudad: str, top_n: int = 3) -> Dict[str, Any]:
        """
        🎯 Recomienda puntos de atención basado en el problema y ciudad
        """
        # Analizar el tipo de problema
        tipos_entidades = self.analizar_problema(comentario)
        
        # Verificar si la ciudad existe en nuestra base de datos
        if ciudad not in self.puntos_atencion:
            ciudades_disponibles = list(self.puntos_atencion.keys())
            ciudad_recomendada = random.choice(ciudades_disponibles)
        else:
            ciudad_recomendada = ciudad
        
        recomendaciones = []
        datos_ciudad = self.puntos_atencion[ciudad_recomendada]
        
        # Buscar puntos de atención para cada tipo de entidad
        for tipo_entidad in tipos_entidades:
            if tipo_entidad in datos_ciudad:
                entidades = datos_ciudad[tipo_entidad]
                for entidad in entidades[:top_n]:  # Limitar a top_n por tipo
                    recomendacion = {
                        'tipo': tipo_entidad.replace('_', ' ').title(),
                        'nombre': entidad['nombre'],
                        'telefono': entidad.get('telefono', 'No disponible'),
                        'direccion': entidad.get('direccion', 'No disponible'),
                        'web': entidad.get('web', 'No disponible'),
                        'especialidad': entidad.get('especialidad', 'General'),
                        'ciudad': ciudad_recomendada
                    }
                    recomendaciones.append(recomendacion)
        
        # Calcular puntaje de relevancia
        puntaje_relevancia = len([t for t in tipos_entidades if t in datos_ciudad]) / len(tipos_entidades) if tipos_entidades else 0
        
        return {
            'problema_analizado': comentario,
            'ciudad': ciudad_recomendada,
            'tipos_problema_identificados': tipos_entidades,
            'puntaje_relevancia': round(puntaje_relevancia * 100, 1),
            'recomendaciones': recomendaciones[:top_n],
            'total_opciones': len(recomendaciones)
        }
    
    def buscar_por_tipo(self, tipo_entidad: str, ciudad: str = None) -> List[Dict]:
        """
        🔎 Busca entidades por tipo específico
        """
        resultados = []
        
        ciudades_buscar = [ciudad] if ciudad and ciudad in self.puntos_atencion else self.puntos_atencion.keys()
        
        for c in ciudades_buscar:
            datos_ciudad = self.puntos_atencion[c]
            if tipo_entidad in datos_ciudad:
                for entidad in datos_ciudad[tipo_entidad]:
                    resultado = entidad.copy()
                    resultado['ciudad'] = c
                    resultado['tipo'] = tipo_entidad.replace('_', ' ').title()
                    resultados.append(resultado)
        
        return resultados
    
    def estadisticas_sistema(self) -> Dict:
        """
        📊 Estadísticas del sistema de recomendaciones
        """
        total_entidades = 0
        entidades_por_tipo = {}
        ciudades_cobertura = len(self.puntos_atencion)
        
        for ciudad, datos in self.puntos_atencion.items():
            for tipo, entidades in datos.items():
                if tipo not in entidades_por_tipo:
                    entidades_por_tipo[tipo] = 0
                entidades_por_tipo[tipo] += len(entidades)
                total_entidades += len(entidades)
        
        return {
            'total_entidades': total_entidades,
            'ciudades_cobertura': ciudades_cobertura,
            'entidades_por_tipo': entidades_por_tipo,
            'tipos_problemas': len(self.mapeo_problemas),
            'ciudades_disponibles': list(self.puntos_atencion.keys())
        }

# Función de demostración
def demo_recomendaciones():
    """
    🎭 Demostración del sistema de recomendaciones bAImax
    """
    print("🎯 DEMO DEL SISTEMA DE RECOMENDACIONES bAImax")
    print("=" * 60)
    
    # Crear instancia del sistema
    recomendador = bAImaxRecomendaciones()
    
    # Casos de prueba
    casos_prueba = [
        {'problema': 'faltan médicos en el centro de salud', 'ciudad': 'Bogotá'},
        {'problema': 'falta agua potable en varias casas', 'ciudad': 'Medellín'},
        {'problema': 'las calles están muy oscuras y peligrosas', 'ciudad': 'Cali'},
        {'problema': 'hay problemas con la recolección de basura', 'ciudad': 'Barranquilla'},
        {'problema': 'necesitamos más acceso a internet', 'ciudad': 'Cartagena'}
    ]
    
    print("🔍 Analizando problemas y generando recomendaciones...")
    print()
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"🏥 Caso {i}: {caso['problema']}")
        print(f"📍 Ciudad: {caso['ciudad']}")
        
        resultado = recomendador.recomendar_puntos_atencion(caso['problema'], caso['ciudad'])
        
        print(f"🎯 Relevancia: {resultado['puntaje_relevancia']}%")
        print(f"🔧 Tipos identificados: {', '.join(resultado['tipos_problema_identificados'])}")
        print("📋 Recomendaciones:")
        
        for j, rec in enumerate(resultado['recomendaciones'], 1):
            print(f"   {j}. {rec['tipo']}: {rec['nombre']}")
            print(f"      📞 {rec['telefono']}")
            print(f"      📍 {rec['direccion']}")
            if rec['web'] != 'No disponible':
                print(f"      🌐 {rec['web']}")
        
        print("-" * 50)
    
    # Estadísticas del sistema
    stats = recomendador.estadisticas_sistema()
    print("\n📊 Estadísticas del Sistema:")
    print(f"   • Total entidades: {stats['total_entidades']}")
    print(f"   • Ciudades con cobertura: {stats['ciudades_cobertura']}")
    print(f"   • Tipos de problemas: {stats['tipos_problemas']}")
    print(f"   • Ciudades disponibles: {', '.join(stats['ciudades_disponibles'])}")
    
    print("\n✨ ¡Sistema de recomendaciones funcionando perfectamente! ✨")
    return recomendador

if __name__ == "__main__":
    demo_recomendaciones()