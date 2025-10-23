"""
🤖 bAImax 2.0 - Sistema de Aprendizaje Continuo
===============================================

Sistema que permite agregar nuevos reportes al dataset 
y re-entrenar el modelo automáticamente
"""

import pandas as pd
import os
import pickle
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

# Importar módulos bAImax
from .baimax_core import bAImaxClassifier, bAImaxAnalyzer
from chatbot.baimax_chatbot import bAImaxChatbot

class bAImaxLearningSystem:
    """
    🧠 Sistema de aprendizaje continuo para bAImax
    """
    
    def __init__(self, dataset_path: str = "src/data/dataset_normalizado.csv"):
        self.dataset_path = dataset_path
        self.dataset_backup_path = f"{dataset_path}.backup"
        self.nuevos_reportes_path = "src/data/nuevos_reportes_baimax.csv"
        self.metricas_path = "src/data/metricas_aprendizaje.json"
        
        # Componentes del sistema
        self.clasificador = None
        self.analyzer = None
        self.chatbot = None
        
        # Métricas de aprendizaje
        self.metricas = {
            'reportes_iniciales': 0,
            'reportes_nuevos': 0,
            'precision_inicial': 0.0,
            'precision_actual': 0.0,
            'entrenamientos_realizados': 0,
            'ultimo_entrenamiento': None,
            'historial_precision': []
        }
        
        # Umbral de reentrenamiento
        self.umbral_nuevos_reportes = 5  # Reentrenar cada 5 nuevos reportes
        self.mejora_minima_precision = 0.01  # 1% mejora mínima
        
    def inicializar_sistema(self) -> bool:
        """
        🚀 Inicializa el sistema de aprendizaje continuo
        """
        try:
            print("🧠 Inicializando Sistema de Aprendizaje Continuo bAImax...")
            
            # Cargar componentes
            self.clasificador = bAImaxClassifier()
            self.analyzer = bAImaxAnalyzer()
            self.chatbot = bAImaxChatbot()
            
            # Inicializar chatbot
            self.chatbot.inicializar_sistema()
            
            # Cargar métricas existentes
            self.cargar_metricas()
            
            # Verificar dataset principal
            if not os.path.exists(self.dataset_path):
                print(f"❌ Dataset principal no encontrado: {self.dataset_path}")
                return False
            
            # Crear archivos de control si no existen
            self.crear_archivos_control()
            
            # Cargar modelo existente o entrenar nuevo
            if os.path.exists('src/data/baimax_modelo.pkl'):
                self.clasificador.cargar_modelo()
                print("📁 Modelo existente cargado")
            else:
                print("🔄 Entrenando modelo inicial...")
                self.clasificador.entrenar()
                self.metricas['entrenamientos_realizados'] = 1
                self.metricas['ultimo_entrenamiento'] = datetime.now().isoformat()
            
            # Actualizar métricas iniciales
            self.actualizar_metricas_iniciales()
            
            print("✅ Sistema de aprendizaje continuo inicializado")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando sistema: {e}")
            return False
    
    def crear_archivos_control(self):
        """
        📁 Crea archivos de control necesarios
        """
        # Crear archivo de nuevos reportes si no existe
        if not os.path.exists(self.nuevos_reportes_path):
            columnas = [
                'Comentario', 'Ciudad', 'Nivel_gravedad', 'Fecha_reporte',
                'Fuente', 'Confianza_IA', 'Timestamp', 'Validado'
            ]
            df_nuevo = pd.DataFrame(columns=columnas)
            df_nuevo.to_csv(self.nuevos_reportes_path, index=False)
            print(f"📋 Creado archivo de nuevos reportes: {self.nuevos_reportes_path}")
        
        # Crear backup del dataset original si no existe
        if not os.path.exists(self.dataset_backup_path):
            df_original = pd.read_csv(self.dataset_path)
            df_original.to_csv(self.dataset_backup_path, index=False)
            print(f"💾 Backup del dataset original creado: {self.dataset_backup_path}")
    
    def cargar_metricas(self):
        """
        📊 Carga métricas existentes del sistema
        """
        if os.path.exists(self.metricas_path):
            with open(self.metricas_path, 'r', encoding='utf-8') as f:
                self.metricas.update(json.load(f))
            print("📊 Métricas existentes cargadas")
    
    def guardar_metricas(self):
        """
        💾 Guarda las métricas actuales
        """
        with open(self.metricas_path, 'w', encoding='utf-8') as f:
            json.dump(self.metricas, f, indent=2, ensure_ascii=False)
    
    def actualizar_metricas_iniciales(self):
        """
        📈 Actualiza las métricas iniciales del sistema
        """
        try:
            # Contar reportes en dataset principal
            df_principal = pd.read_csv(self.dataset_path)
            self.metricas['reportes_iniciales'] = len(df_principal)
            
            # Contar nuevos reportes
            if os.path.exists(self.nuevos_reportes_path):
                df_nuevos = pd.read_csv(self.nuevos_reportes_path)
                self.metricas['reportes_nuevos'] = len(df_nuevos[df_nuevos['Validado'] == True]) if 'Validado' in df_nuevos.columns else 0
            
            # Obtener precisión actual del modelo
            if hasattr(self.clasificador, 'obtener_metricas'):
                metricas_modelo = self.clasificador.obtener_metricas()
                if 'accuracy' in metricas_modelo:
                    precision_actual = metricas_modelo['accuracy']
                    self.metricas['precision_actual'] = precision_actual
                    
                    if self.metricas['precision_inicial'] == 0.0:
                        self.metricas['precision_inicial'] = precision_actual
            
            self.guardar_metricas()
            
        except Exception as e:
            print(f"❌ Error actualizando métricas: {e}")
    
    def agregar_nuevo_reporte(self, reporte: Dict[str, Any]) -> bool:
        """
        ➕ Agrega un nuevo reporte al sistema
        """
        try:
            # Validar reporte
            campos_requeridos = ['Comentario', 'Ciudad', 'Nivel_gravedad']
            for campo in campos_requeridos:
                if campo not in reporte:
                    print(f"❌ Campo requerido faltante: {campo}")
                    return False
            
            # Preparar datos del reporte
            nuevo_reporte = {
                'Comentario': reporte['Comentario'],
                'Ciudad': reporte['Ciudad'],
                'Nivel_gravedad': reporte['Nivel_gravedad'],
                'Fecha_reporte': reporte.get('Fecha_reporte', datetime.now().strftime('%Y-%m-%d')),
                'Fuente': reporte.get('Fuente', 'bAImax_2.0_User'),
                'Confianza_IA': reporte.get('Confianza_IA', 0.0),
                'Timestamp': reporte.get('Timestamp', datetime.now().isoformat()),
                'Validado': False  # Por defecto no validado hasta revisión
            }
            
            # Cargar archivo de nuevos reportes
            df_nuevos = pd.read_csv(self.nuevos_reportes_path)
            
            # Agregar el nuevo reporte
            df_nuevos = pd.concat([df_nuevos, pd.DataFrame([nuevo_reporte])], ignore_index=True)
            
            # Guardar archivo actualizado
            df_nuevos.to_csv(self.nuevos_reportes_path, index=False)
            
            # Actualizar métricas
            self.metricas['reportes_nuevos'] = len(df_nuevos)
            self.guardar_metricas()
            
            print(f"✅ Nuevo reporte agregado. Total reportes nuevos: {self.metricas['reportes_nuevos']}")
            
            # Verificar si es necesario reentrenar
            self.verificar_reentrenamiento()
            
            return True
            
        except Exception as e:
            print(f"❌ Error agregando reporte: {e}")
            return False
    
    def validar_reporte(self, indice: int, es_valido: bool) -> bool:
        """
        ✅ Valida o rechaza un reporte específico
        """
        try:
            df_nuevos = pd.read_csv(self.nuevos_reportes_path)
            
            if indice >= len(df_nuevos):
                print(f"❌ Índice fuera de rango: {indice}")
                return False
            
            # Marcar como validado o rechazado
            df_nuevos.loc[indice, 'Validado'] = es_valido
            
            # Guardar cambios
            df_nuevos.to_csv(self.nuevos_reportes_path, index=False)
            
            estado = "validado" if es_valido else "rechazado"
            print(f"✅ Reporte {indice} {estado}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error validando reporte: {e}")
            return False
    
    def obtener_reportes_pendientes(self) -> List[Dict[str, Any]]:
        """
        📋 Obtiene reportes pendientes de validación
        """
        try:
            df_nuevos = pd.read_csv(self.nuevos_reportes_path)
            
            # Filtrar reportes no validados
            pendientes = df_nuevos[df_nuevos['Validado'] == False]
            
            return pendientes.to_dict('records')
            
        except Exception as e:
            print(f"❌ Error obteniendo reportes pendientes: {e}")
            return []
    
    def verificar_reentrenamiento(self) -> bool:
        """
        🔄 Verifica si es necesario reentrenar el modelo
        """
        try:
            # Contar reportes validados
            df_nuevos = pd.read_csv(self.nuevos_reportes_path)
            reportes_validados = len(df_nuevos[df_nuevos['Validado'] == True])
            
            # Verificar umbral
            if reportes_validados >= self.umbral_nuevos_reportes:
                print(f"🔄 Umbral alcanzado ({reportes_validados} reportes). Iniciando reentrenamiento...")
                return self.reentrenar_modelo()
            
            return False
            
        except Exception as e:
            print(f"❌ Error verificando reentrenamiento: {e}")
            return False
    
    def reentrenar_modelo(self) -> bool:
        """
        🔄 Reentrena el modelo con los nuevos datos
        """
        try:
            print("🔄 Iniciando reentrenamiento del modelo...")
            
            # Crear dataset combinado
            dataset_combinado = self.crear_dataset_combinado()
            
            if dataset_combinado is None:
                print("❌ Error creando dataset combinado")
                return False
            
            # Guardar precisión anterior
            precision_anterior = self.metricas['precision_actual']
            
            # Reentrenar clasificador con datos combinados
            self.clasificador.dataset_path = 'dataset_temporal_entrenamiento.csv'
            dataset_combinado.to_csv(self.clasificador.dataset_path, index=False)
            
            # Entrenar
            resultado = self.clasificador.entrenar()
            
            if resultado:
                # Obtener nueva precisión
                metricas_nuevo = self.clasificador.obtener_metricas()
                precision_nueva = metricas_nuevo.get('accuracy', 0.0)
                
                # Verificar mejora
                mejora = precision_nueva - precision_anterior
                
                if mejora >= self.mejora_minima_precision or precision_nueva > precision_anterior:
                    # Aceptar nuevo modelo
                    self.metricas['precision_actual'] = precision_nueva
                    self.metricas['entrenamientos_realizados'] += 1
                    self.metricas['ultimo_entrenamiento'] = datetime.now().isoformat()
                    self.metricas['historial_precision'].append({
                        'fecha': datetime.now().isoformat(),
                        'precision': precision_nueva,
                        'mejora': mejora
                    })
                    
                    # Integrar reportes validados al dataset principal
                    self.integrar_reportes_validados()
                    
                    print(f"✅ Modelo reentrenado exitosamente")
                    print(f"📈 Precisión: {precision_anterior:.1%} → {precision_nueva:.1%} (+{mejora:.1%})")
                    
                else:
                    print(f"⚠️ Nueva precisión ({precision_nueva:.1%}) no mejora lo suficiente")
                    print("🔄 Manteniendo modelo anterior")
                
                # Limpiar archivo temporal
                if os.path.exists('dataset_temporal_entrenamiento.csv'):
                    os.remove('dataset_temporal_entrenamiento.csv')
                
                self.guardar_metricas()
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error reentrenando modelo: {e}")
            return False
    
    def crear_dataset_combinado(self) -> Optional[pd.DataFrame]:
        """
        🔗 Crea un dataset combinado con datos originales y nuevos validados
        """
        try:
            # Cargar dataset original
            df_original = pd.read_csv(self.dataset_path)
            
            # Cargar nuevos reportes validados
            df_nuevos = pd.read_csv(self.nuevos_reportes_path)
            df_validados = df_nuevos[df_nuevos['Validado'] == True].copy()
            
            if len(df_validados) == 0:
                print("⚠️ No hay reportes validados para integrar")
                return df_original
            
            # Asegurar columnas compatibles
            columnas_necesarias = ['Comentario', 'Ciudad', 'Nivel_gravedad', 'Fecha_reporte']
            
            for col in columnas_necesarias:
                if col not in df_validados.columns:
                    if col == 'Fecha_reporte':
                        df_validados[col] = datetime.now().strftime('%Y-%m-%d')
                    else:
                        print(f"❌ Columna faltante en nuevos reportes: {col}")
                        return None
            
            # Seleccionar solo columnas comunes
            columnas_comunes = list(set(df_original.columns) & set(df_validados.columns))
            
            df_original_filtrado = df_original[columnas_comunes]
            df_validados_filtrado = df_validados[columnas_comunes]
            
            # Combinar datasets
            df_combinado = pd.concat([df_original_filtrado, df_validados_filtrado], ignore_index=True)
            
            print(f"🔗 Dataset combinado creado: {len(df_original)} originales + {len(df_validados)} nuevos = {len(df_combinado)} total")
            
            return df_combinado
            
        except Exception as e:
            print(f"❌ Error creando dataset combinado: {e}")
            return None
    
    def integrar_reportes_validados(self):
        """
        🔗 Integra reportes validados al dataset principal
        """
        try:
            df_nuevos = pd.read_csv(self.nuevos_reportes_path)
            df_validados = df_nuevos[df_nuevos['Validado'] == True].copy()
            
            if len(df_validados) == 0:
                return
            
            # Cargar dataset principal
            df_principal = pd.read_csv(self.dataset_path)
            
            # Agregar columnas faltantes si es necesario
            columnas_necesarias = df_principal.columns.tolist()
            for col in columnas_necesarias:
                if col not in df_validados.columns:
                    if col == 'Edad':
                        df_validados[col] = 30  # Valor por defecto
                    elif col == 'Genero':
                        df_validados[col] = 'No especificado'
                    elif col == 'Zona_rural':
                        df_validados[col] = 0
                    elif col == 'Acceso_internet':
                        df_validados[col] = 1
                    elif col == 'Atencion_previa':
                        df_validados[col] = 0
                    elif col == 'Nivel_urgencia':
                        df_validados[col] = 'Moderada'
                    else:
                        df_validados[col] = ''
            
            # Seleccionar solo columnas del dataset principal
            df_validados_integrar = df_validados[columnas_necesarias]
            
            # Combinar con dataset principal
            df_actualizado = pd.concat([df_principal, df_validados_integrar], ignore_index=True)
            
            # Guardar dataset actualizado
            df_actualizado.to_csv(self.dataset_path, index=False)
            
            # Limpiar reportes integrados
            df_nuevos_limpio = df_nuevos[df_nuevos['Validado'] == False]
            df_nuevos_limpio.to_csv(self.nuevos_reportes_path, index=False)
            
            print(f"🔗 {len(df_validados)} reportes integrados al dataset principal")
            
        except Exception as e:
            print(f"❌ Error integrando reportes: {e}")
    
    def obtener_estadisticas_aprendizaje(self) -> Dict[str, Any]:
        """
        📊 Obtiene estadísticas completas del sistema de aprendizaje
        """
        self.actualizar_metricas_iniciales()
        
        return {
            'reportes': {
                'iniciales': self.metricas['reportes_iniciales'],
                'nuevos_total': self.metricas['reportes_nuevos'],
                'pendientes_validacion': len(self.obtener_reportes_pendientes()),
                'umbral_reentrenamiento': self.umbral_nuevos_reportes
            },
            'modelo': {
                'precision_inicial': self.metricas['precision_inicial'],
                'precision_actual': self.metricas['precision_actual'],
                'mejora_total': self.metricas['precision_actual'] - self.metricas['precision_inicial'],
                'entrenamientos_realizados': self.metricas['entrenamientos_realizados'],
                'ultimo_entrenamiento': self.metricas['ultimo_entrenamiento']
            },
            'historial': self.metricas['historial_precision']
        }

# Demostración del sistema de aprendizaje
def demo_aprendizaje_continuo():
    """
    🎭 Demostración del sistema de aprendizaje continuo
    """
    print("🧠 DEMO: Sistema de Aprendizaje Continuo bAImax 2.0")
    print("="*60)
    
    # Inicializar sistema
    learning_system = bAImaxLearningSystem()
    
    if not learning_system.inicializar_sistema():
        print("❌ Error inicializando sistema")
        return
    
    # Mostrar estadísticas iniciales
    stats = learning_system.obtener_estadisticas_aprendizaje()
    print(f"\n📊 Estadísticas iniciales:")
    print(f"   Reportes en dataset: {stats['reportes']['iniciales']}")
    print(f"   Precisión del modelo: {stats['modelo']['precision_actual']:.1%}")
    print(f"   Entrenamientos realizados: {stats['modelo']['entrenamientos_realizados']}")
    
    # Simular nuevos reportes
    nuevos_reportes_demo = [
        {
            'Comentario': 'No hay suficientes ambulancias en la zona',
            'Ciudad': 'Medellín',
            'Nivel_gravedad': 'GRAVE',
            'Fuente': 'Demo_Usuario_1'
        },
        {
            'Comentario': 'Falta mantenimiento en el centro de salud',
            'Ciudad': 'Cali',
            'Nivel_gravedad': 'MODERADO',
            'Fuente': 'Demo_Usuario_2'
        }
    ]
    
    print(f"\n➕ Agregando {len(nuevos_reportes_demo)} reportes de demostración...")
    for reporte in nuevos_reportes_demo:
        resultado = learning_system.agregar_nuevo_reporte(reporte)
        if resultado:
            print(f"   ✅ Agregado: {reporte['Comentario'][:50]}...")
    
    # Mostrar reportes pendientes
    pendientes = learning_system.obtener_reportes_pendientes()
    print(f"\n📋 Reportes pendientes de validación: {len(pendientes)}")
    
    # Validar reportes (simulado)
    print(f"\n✅ Validando reportes automáticamente (demo)...")
    for i in range(len(pendientes)):
        learning_system.validar_reporte(i, True)
    
    # Estadísticas finales
    stats_final = learning_system.obtener_estadisticas_aprendizaje()
    print(f"\n📊 Estadísticas finales:")
    print(f"   Reportes nuevos validados: {stats_final['reportes']['nuevos_total']}")
    print(f"   Sistema listo para aprendizaje continuo ✅")

if __name__ == "__main__":
    demo_aprendizaje_continuo()