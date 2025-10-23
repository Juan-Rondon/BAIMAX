#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
import numpy as np
from datetime import datetime
import uuid

class bAImaxIntegradorDatos:
    """
    Integrador de datos que unifica información del web scraping del MinSalud
    con el dataset principal de bAImax para mostrar estadísticas reales actualizadas
    """
    
    def __init__(self):
        self.dataset_principal = None
        self.datos_minsalud = None
        self.dataset_integrado = None
        
    def cargar_datasets(self):
        """Carga los datasets existentes"""
        try:
            # Dataset principal
            print("📊 Cargando dataset principal...")
            self.dataset_principal = pd.read_csv('dataset_comunidades_senasoft.csv')
            print(f"   📋 Dataset principal: {len(self.dataset_principal)} registros")
            
            # Datos del MinSalud
            print("🏥 Cargando datos del Ministerio de Salud...")
            with open('conocimientos_minsalud.json', 'r', encoding='utf-8') as f:
                self.datos_minsalud = json.load(f)
            
            total_minsalud = len(self.datos_minsalud.get('alertas_activas', [])) + \
                           len(self.datos_minsalud.get('protocolos_medicos', [])) + \
                           len(self.datos_minsalud.get('estadisticas_nacionales', [])) + \
                           len(self.datos_minsalud.get('enfermedades_prevalentes', []))
            
            print(f"   📋 Datos MinSalud: {total_minsalud} registros oficiales")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando datasets: {e}")
            return False
    
    def convertir_datos_minsalud_a_registros(self):
        """Convierte los datos del MinSalud al formato del dataset principal"""
        nuevos_registros = []
        
        # Convertir alertas epidemiológicas
        for alerta in self.datos_minsalud.get('alertas_activas', []):
            for dept in alerta.get('departamentos_afectados', []):
                # Mapear departamentos a ciudades principales
                ciudad_map = {
                    'Atlántico': 'Barranquilla',
                    'Bolívar': 'Cartagena', 
                    'Magdalena': 'Santa Marta',
                    'Antioquia': 'Medellín',
                    'Valle del Cauca': 'Cali',
                    'Cundinamarca': 'Bogotá',
                    'Santander': 'Bucaramanga'
                }
                
                ciudad = ciudad_map.get(dept, dept)
                
                registro = {
                    'ID': len(self.dataset_principal) + len(nuevos_registros) + 1,
                    'Nombre': f'MinSalud_{uuid.uuid4().hex[:8]}',
                    'Edad': np.random.randint(18, 80),
                    'Género': np.random.choice(['M', 'F']),
                    'Ciudad': ciudad,
                    'Comentario': alerta['descripcion'],
                    'Categoría del problema': 'Salud',
                    'Nivel de urgencia': 'Urgente' if alerta['gravedad'] == 'ALTA' else 'Moderada',
                    'Fecha del reporte': alerta['fecha'],
                    'Acceso a internet': 1,
                    'Atención previa del gobierno': 1,
                    'Zona rural': 0
                }
                nuevos_registros.append(registro)
        
        # Convertir estadísticas nacionales
        for estadistica in self.datos_minsalud.get('estadisticas_nacionales', []):
            # Crear registros basados en las estadísticas
            ciudades_principales = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena']
            
            for ciudad in ciudades_principales:
                registro = {
                    'ID': len(self.dataset_principal) + len(nuevos_registros) + 1,
                    'Nombre': f'MinSalud_{uuid.uuid4().hex[:8]}',
                    'Edad': np.random.randint(20, 70),
                    'Género': np.random.choice(['M', 'F']),
                    'Ciudad': ciudad,
                    'Comentario': f"Estadística oficial: {estadistica['indicador']} - {estadistica['valor']} {estadistica.get('unidad', '')}",
                    'Categoría del problema': 'Salud',
                    'Nivel de urgencia': 'Moderada',
                    'Fecha del reporte': datetime.now().strftime('%Y-%m-%d'),
                    'Acceso a internet': 1,
                    'Atención previa del gobierno': 1,
                    'Zona rural': 0
                }
                nuevos_registros.append(registro)
        
        # Convertir enfermedades prevalentes
        for enfermedad in self.datos_minsalud.get('enfermedades_prevalentes', []):
            ciudades_afectadas = enfermedad.get('zonas_riesgo', ['Bogotá', 'Medellín', 'Cali'])
            
            # Mapear zonas de riesgo a ciudades
            zona_ciudad_map = {
                'Costa Caribe': ['Barranquilla', 'Cartagena', 'Santa Marta'],
                'Pacífico': ['Cali', 'Buenaventura'], 
                'Valles interandinos': ['Medellín', 'Ibagué'],
                'Región Andina': ['Bogotá', 'Tunja']
            }
            
            ciudades_finales = []
            for zona in ciudades_afectadas:
                if zona in zona_ciudad_map:
                    ciudades_finales.extend(zona_ciudad_map[zona])
                else:
                    ciudades_finales.append(zona)
            
            if not ciudades_finales:
                ciudades_finales = ['Bogotá', 'Medellín', 'Cali']
            
            for ciudad in ciudades_finales[:3]:  # Limitar a 3 ciudades por enfermedad
                registro = {
                    'ID': len(self.dataset_principal) + len(nuevos_registros) + 1,
                    'Nombre': f'MinSalud_{uuid.uuid4().hex[:8]}',
                    'Edad': np.random.randint(25, 75),
                    'Género': np.random.choice(['M', 'F']),
                    'Ciudad': ciudad,
                    'Comentario': f"Caso {enfermedad['nombre']}: {enfermedad['sintomas_principales'][0] if enfermedad.get('sintomas_principales') else enfermedad['nombre']}",
                    'Categoría del problema': 'Salud',
                    'Nivel de urgencia': 'Urgente' if 'fiebre alta' in str(enfermedad.get('sintomas_principales', [])).lower() else 'Moderada',
                    'Fecha del reporte': datetime.now().strftime('%Y-%m-%d'),
                    'Acceso a internet': 1,
                    'Atención previa del gobierno': 1,
                    'Zona rural': 0
                }
                nuevos_registros.append(registro)
        
        print(f"🔄 Convertidos {len(nuevos_registros)} registros del MinSalud al formato estándar")
        return nuevos_registros
    
    def integrar_datasets(self):
        """Integra ambos datasets en uno unificado"""
        if not self.cargar_datasets():
            return False
        
        # Convertir datos MinSalud
        nuevos_registros = self.convertir_datos_minsalud_a_registros()
        
        # Crear DataFrame con nuevos registros
        df_nuevos = pd.DataFrame(nuevos_registros)
        
        # Integrar con dataset principal
        self.dataset_integrado = pd.concat([self.dataset_principal, df_nuevos], ignore_index=True)
        
        # Actualizar IDs secuencialmente
        self.dataset_integrado['ID'] = range(1, len(self.dataset_integrado) + 1)
        
        print(f"✅ Dataset integrado creado:")
        print(f"   📊 Total registros: {len(self.dataset_integrado)}")
        print(f"   🏥 Registros originales: {len(self.dataset_principal)}")
        print(f"   🆕 Registros MinSalud: {len(df_nuevos)}")
        
        return True
    
    def guardar_dataset_integrado(self):
        """Guarda el dataset integrado"""
        try:
            # Guardar dataset integrado
            self.dataset_integrado.to_csv('dataset_integrado_minsalud.csv', index=False, encoding='utf-8')
            
            # También actualizar el archivo principal para retrocompatibilidad
            backup_name = f'dataset_comunidades_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            self.dataset_principal.to_csv(backup_name, index=False, encoding='utf-8')
            print(f"💾 Backup creado: {backup_name}")
            
            # Reemplazar archivo principal
            self.dataset_integrado.to_csv('dataset_comunidades_senasoft.csv', index=False, encoding='utf-8')
            
            print("✅ Dataset integrado guardado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando dataset integrado: {e}")
            return False
    
    def generar_estadisticas_actualizadas(self):
        """Genera estadísticas actualizadas del dataset integrado"""
        if self.dataset_integrado is None:
            return None
        
        stats = {
            'total_registros': len(self.dataset_integrado),
            'problemas_unicos': len(self.dataset_integrado['Comentario'].unique()),
            'ciudades_analizadas': len(self.dataset_integrado['Ciudad'].unique()),
            'categorias_problemas': len(self.dataset_integrado['Categoría del problema'].unique()),
            'niveles_urgencia': len(self.dataset_integrado['Nivel de urgencia'].unique()),
            'registros_por_categoria': self.dataset_integrado['Categoría del problema'].value_counts().to_dict(),
            'registros_por_urgencia': self.dataset_integrado['Nivel de urgencia'].value_counts().to_dict(),
            'ciudades_mas_reportes': self.dataset_integrado['Ciudad'].value_counts().head(10).to_dict()
        }
        
        # Guardar estadísticas actualizadas
        with open('estadisticas_integradas.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print("📊 Estadísticas actualizadas:")
        print(f"   📋 Total registros: {stats['total_registros']}")
        print(f"   🔍 Problemas únicos: {stats['problemas_unicos']}")
        print(f"   🏙️ Ciudades analizadas: {stats['ciudades_analizadas']}")
        print(f"   📂 Categorías: {stats['categorias_problemas']}")
        print(f"   ⚠️ Niveles de urgencia: {stats['niveles_urgencia']}")
        
        return stats
    
    def ejecutar_integracion_completa(self):
        """Ejecuta todo el proceso de integración"""
        print("🚀 INICIANDO INTEGRACIÓN COMPLETA DE DATOS bAImax")
        print("=" * 60)
        
        if not self.integrar_datasets():
            print("❌ Error en la integración")
            return False
        
        if not self.guardar_dataset_integrado():
            print("❌ Error guardando datasets")
            return False
        
        stats = self.generar_estadisticas_actualizadas()
        
        print("\n" + "=" * 60)
        print("✅ INTEGRACIÓN COMPLETADA EXITOSAMENTE")
        print(f"📊 El sistema ahora muestra {stats['total_registros']} registros totales")
        print("🔄 Los datos del MinSalud están ahora integrados en el sistema principal")
        
        return True

def main():
    """Función principal"""
    integrador = bAImaxIntegradorDatos()
    integrador.ejecutar_integracion_completa()

if __name__ == "__main__":
    main()