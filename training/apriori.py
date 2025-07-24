import random
import json
from collections import defaultdict
from itertools import combinations

class AprioriAnalyzer:
    def __init__(self, min_support=0.1, min_confidence=0.6):
        """
        Inicializa el analizador Apriori
        
        Args:
            min_support: Soporte mínimo (porcentaje de transacciones)
            min_confidence: Confianza mínima para reglas de asociación
        """
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.transacciones = []
        self.itemsets_frecuentes = {}
        self.reglas_asociacion = []
    
    def cargar_datos(self, datos_ventas):
        """
        Convierte los datos de ventas en transacciones para Apriori
        
        Args:
            datos_ventas: Lista con estructura [{"id_venta": 1, "producto": {"id_producto": 1}}, ...]
                         o estructura alternativa
        """
        if not datos_ventas:
            print("[X] Error: No se proporcionaron datos de ventas")
            return []
        
        # Agrupar productos por venta
        ventas_productos = defaultdict(set)
        
        # Detectar estructura de datos
        primer_elemento = datos_ventas[0]
        
        if isinstance(primer_elemento, dict):
            if 'id_venta' in primer_elemento and 'producto' in primer_elemento:
                # Estructura esperada: [{"id_venta": 1, "producto": {"id_producto": 1}}, ...]
                print("[OK] Procesando estructura estándar de datos")
                for item in datos_ventas:
                    id_venta = item['id_venta']
                    if isinstance(item['producto'], dict) and 'id_producto' in item['producto']:
                        id_producto = item['producto']['id_producto']
                    else:
                        id_producto = item['producto']  # Si es directo
                    ventas_productos[id_venta].add(id_producto)
                    
            elif 'venta_id' in primer_elemento or 'sale_id' in primer_elemento:
                # Estructura alternativa 1
                print("[OK] Procesando estructura alternativa (venta_id/sale_id)")
                for item in datos_ventas:
                    id_venta = item.get('venta_id') or item.get('sale_id')
                    id_producto = item.get('producto_id') or item.get('product_id') or item.get('id_producto')
                    if id_venta and id_producto:
                        ventas_productos[id_venta].add(id_producto)
                        
            else:
                # Intentar detectar automáticamente las columnas
                print("⚠️  Estructura no reconocida, intentando detección automática...")
                keys = list(primer_elemento.keys())
                print(f"Campos disponibles: {keys}")
                
                # Buscar campos que podrían ser venta
                venta_field = None
                for key in keys:
                    if 'venta' in key.lower() or 'sale' in key.lower() or 'transaction' in key.lower():
                        venta_field = key
                        break
                
                # Buscar campos que podrían ser producto
                producto_field = None
                for key in keys:
                    if 'producto' in key.lower() or 'product' in key.lower() or 'item' in key.lower():
                        producto_field = key
                        break
                
                if venta_field and producto_field:
                    print(f"[OK] Detectados: venta='{venta_field}', producto='{producto_field}'")
                    for item in datos_ventas:
                        id_venta = item[venta_field]
                        id_producto = item[producto_field]
                        ventas_productos[id_venta].add(id_producto)
                else:
                    print("[X] No se pudo detectar la estructura de datos automáticamente")
                    return []
        else:
            print("[X] Formato de datos no soportado")
            return []
        
        # Convertir a lista de transacciones
        self.transacciones = [list(productos) for productos in ventas_productos.values()]
        print(f"[OK] Cargadas {len(self.transacciones)} transacciones")
        
        # Mostrar estadísticas básicas
        if self.transacciones:
            productos_unicos = set()
            total_items = 0
            for transaccion in self.transacciones:
                productos_unicos.update(transaccion)
                total_items += len(transaccion)
            
            promedio_productos = total_items / len(self.transacciones)
            print(f"[OK] Productos únicos: {len(productos_unicos)}")
            print(f"[OK] Promedio de productos por transacción: {promedio_productos:.2f}")
            
            # Mostrar ejemplos de transacciones
            print(f"\nEjemplos de transacciones:")
            for i, transaccion in enumerate(self.transacciones[:3]):
                print(f"  Transacción {i+1}: {sorted(transaccion)}")
        
        return self.transacciones
    
    def calcular_soporte(self, itemset):
        """
        Calcula el soporte de un itemset
        
        Args:
            itemset: Conjunto de productos
            
        Returns:
            float: Soporte (frecuencia relativa)
        """
        if not self.transacciones:
            return 0
        
        contador = 0
        itemset_set = set(itemset)
        
        for transaccion in self.transacciones:
            if itemset_set.issubset(set(transaccion)):
                contador += 1
        
        return contador / len(self.transacciones)
    
    def generar_candidatos(self, itemsets_previos, k):
        """
        Genera candidatos de tamaño k a partir de itemsets de tamaño k-1
        
        Args:
            itemsets_previos: Itemsets frecuentes del nivel anterior
            k: Tamaño de los nuevos candidatos
            
        Returns:
            list: Lista de candidatos
        """
        candidatos = []
        itemsets_list = list(itemsets_previos)
        
        for i in range(len(itemsets_list)):
            for j in range(i + 1, len(itemsets_list)):
                # Unir dos itemsets si difieren en solo un elemento
                itemset1 = sorted(itemsets_list[i])
                itemset2 = sorted(itemsets_list[j])
                
                if itemset1[:-1] == itemset2[:-1]:
                    candidato = tuple(sorted(set(itemset1) | set(itemset2)))
                    if len(candidato) == k:
                        candidatos.append(candidato)
        
        return candidatos
    
    def ejecutar_apriori(self):
        """
        Ejecuta el algoritmo Apriori completo
        
        Returns:
            dict: Itemsets frecuentes por nivel
        """
        if not self.transacciones:
            print("Error: No hay transacciones cargadas")
            return {}
        
        # Obtener todos los productos únicos
        todos_productos = set()
        for transaccion in self.transacciones:
            todos_productos.update(transaccion)
        
        # L1: Itemsets de tamaño 1
        itemsets_1 = []
        soporte_1 = {}
        
        for producto in todos_productos:
            soporte = self.calcular_soporte([producto])
            if soporte >= self.min_support:
                itemsets_1.append((producto,))
                soporte_1[(producto,)] = soporte
        
        self.itemsets_frecuentes[1] = itemsets_1
        print(f"L1: {len(itemsets_1)} itemsets frecuentes de tamaño 1")
        
        # Generar itemsets de mayor tamaño
        k = 2
        itemsets_previos = itemsets_1
        
        while itemsets_previos:
            candidatos = self.generar_candidatos(itemsets_previos, k)
            itemsets_k = []
            
            for candidato in candidatos:
                soporte = self.calcular_soporte(candidato)
                if soporte >= self.min_support:
                    itemsets_k.append(candidato)
            
            if itemsets_k:
                self.itemsets_frecuentes[k] = itemsets_k
                print(f"L{k}: {len(itemsets_k)} itemsets frecuentes de tamaño {k}")
                itemsets_previos = itemsets_k
                k += 1
            else:
                itemsets_previos = []
        
        return self.itemsets_frecuentes
    
    def generar_reglas_asociacion(self):
        """
        Genera reglas de asociación a partir de itemsets frecuentes
        
        Returns:
            list: Lista de reglas de asociación
        """
        self.reglas_asociacion = []
        
        # Para itemsets de tamaño >= 2
        for k in range(2, max(self.itemsets_frecuentes.keys()) + 1):
            for itemset in self.itemsets_frecuentes[k]:
                # Generar todas las posibles divisiones del itemset
                for i in range(1, len(itemset)):
                    for antecedente in combinations(itemset, i):
                        consecuente = tuple(item for item in itemset if item not in antecedente)
                        
                        # Calcular confianza
                        soporte_itemset = self.calcular_soporte(itemset)
                        soporte_antecedente = self.calcular_soporte(antecedente)
                        
                        if soporte_antecedente > 0:
                            confianza = soporte_itemset / soporte_antecedente
                            
                            if confianza >= self.min_confidence:
                                # Calcular lift
                                soporte_consecuente = self.calcular_soporte(consecuente)
                                lift = confianza / soporte_consecuente if soporte_consecuente > 0 else 0
                                
                                regla = {
                                    'antecedente': antecedente,
                                    'consecuente': consecuente,
                                    'soporte': soporte_itemset,
                                    'confianza': confianza,
                                    'lift': lift
                                }
                                self.reglas_asociacion.append(regla)
        
        # Ordenar reglas por confianza
        self.reglas_asociacion.sort(key=lambda x: x['confianza'], reverse=True)
        
        return self.reglas_asociacion
    
    def mostrar_resultados(self):
        """
        Muestra los resultados del análisis Apriori
        """
        print("\n" + "="*60)
        print("RESULTADOS DEL ANÁLISIS APRIORI")
        print("="*60)
        
        print(f"\nParámetros utilizados:")
        print(f"- Soporte mínimo: {self.min_support:.1%}")
        print(f"- Confianza mínima: {self.min_confidence:.1%}")
        print(f"- Total de transacciones: {len(self.transacciones)}")
        
        # Mostrar itemsets frecuentes
        print(f"\nITEMSETS FRECUENTES:")
        for k, itemsets in self.itemsets_frecuentes.items():
            print(f"\nTamaño {k}: {len(itemsets)} itemsets")
            for itemset in itemsets[:10]:  # Mostrar solo los primeros 10
                soporte = self.calcular_soporte(itemset)
                productos_str = f"{{Productos: {', '.join(map(str, itemset))}}}"
                print(f"  {productos_str} -> Soporte: {soporte:.3f} ({soporte:.1%})")
            if len(itemsets) > 10:
                print(f"  ... y {len(itemsets) - 10} más")
        
        # Mostrar reglas de asociación
        print(f"\nREGLAS DE ASOCIACIÓN:")
        print(f"Total de reglas encontradas: {len(self.reglas_asociacion)}")
        
        if self.reglas_asociacion:
            print(f"\nTop 15 reglas por confianza:")
            for i, regla in enumerate(self.reglas_asociacion[:15]):
                ant_str = f"{{Productos: {', '.join(map(str, regla['antecedente']))}}}"
                cons_str = f"{{Productos: {', '.join(map(str, regla['consecuente']))}}}"
                
                print(f"\n{i+1}. {ant_str} => {cons_str}")
                print(f"   Soporte: {regla['soporte']:.3f} ({regla['soporte']:.1%})")
                print(f"   Confianza: {regla['confianza']:.3f} ({regla['confianza']:.1%})")
                print(f"   Lift: {regla['lift']:.3f}")
    
    def exportar_resultados(self, nombre_archivo="resultados_apriori.json"):
        """
        Exporta los resultados a un archivo JSON
        """
        resultados = {
            'parametros': {
                'min_support': self.min_support,
                'min_confidence': self.min_confidence,
                'total_transacciones': len(self.transacciones)
            },
            'itemsets_frecuentes': {
                str(k): [list(itemset) for itemset in itemsets] 
                for k, itemsets in self.itemsets_frecuentes.items()
            },
            'reglas_asociacion': [
                {
                    'antecedente': list(regla['antecedente']),
                    'consecuente': list(regla['consecuente']),
                    'soporte': regla['soporte'],
                    'confianza': regla['confianza'],
                    'lift': regla['lift']
                }
                for regla in self.reglas_asociacion
            ]
        }
        
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(resultados, archivo, indent=2, ensure_ascii=False)
        
        print(f"\nResultados exportados a '{nombre_archivo}'")

# Función para generar datos de ejemplo
def generar_datos_ventas(num_ventas=100, num_productos=25, min_productos_por_venta=1, max_productos_por_venta=8):
    """Genera datos sintéticos de ventas (misma función del código anterior)"""
    datos_ventas = []
    
    for id_venta in range(1, num_ventas + 1):
        num_productos_venta = random.randint(min_productos_por_venta, max_productos_por_venta)
        productos_seleccionados = random.sample(range(1, num_productos + 1), num_productos_venta)
        
        for id_producto in productos_seleccionados:
            datos_ventas.append({
                "id_venta": id_venta,
                "producto": {
                    "id_producto": id_producto
                }
            })
    
    return datos_ventas

def cargar_datos_desde_archivo(nombre_archivo="ventas_fit.json"):
    """
    Carga datos de ventas desde un archivo JSON
    
    Args:
        nombre_archivo: Nombre del archivo JSON a cargar
        
    Returns:
        list: Datos de ventas en formato esperado
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        
        print(f"Datos cargados exitosamente desde '{nombre_archivo}'")
        print(f"Total de registros: {len(datos)}")
        
        # Verificar estructura de datos
        if datos and isinstance(datos[0], dict):
            if 'id_venta' in datos[0] and 'producto' in datos[0]:
                print("[OK] Estructura de datos correcta detectada")
                return datos
            else:
                print("⚠️  Estructura de datos no reconocida. Intentando adaptación...")
                # Aquí podrías añadir lógica para adaptar otros formatos
                return datos
        
        return datos
        
    except FileNotFoundError:
        print(f"[X] Error: No se encontró el archivo '{nombre_archivo}'")
        print("Asegúrate de que el archivo esté en la misma carpeta que este script")
        return None
    except json.JSONDecodeError:
        print(f"[X] Error: El archivo '{nombre_archivo}' no tiene formato JSON válido")
        return None
    except Exception as e:
        print(f"[X] Error inesperado al cargar '{nombre_archivo}': {str(e)}")
        return None

# Ejemplo de uso completo
if __name__ == "__main__":
    print("Cargando datos desde ventas_fit.json...")
    
    # Intentar cargar datos desde archivo
    datos_ventas = cargar_datos_desde_archivo("ventas_fit.json")
    
    if datos_ventas is None:
        print("\n🔄 Fallback: Generando datos sintéticos como ejemplo...")
        datos_ventas = generar_datos_ventas(
            num_ventas=200,
            num_productos=25,
            min_productos_por_venta=2,
            max_productos_por_venta=6
        )
    
    print("\nEjecutando análisis Apriori...")
    
    # Crear analizador con parámetros ajustados
    analizador = AprioriAnalyzer(
        min_support=0.05,    # 5% mínimo de soporte
        min_confidence=0.5   # 50% mínimo de confianza
    )
    
    # Cargar datos y ejecutar análisis
    transacciones = analizador.cargar_datos(datos_ventas)
    
    if transacciones:
        analizador.ejecutar_apriori()
        analizador.generar_reglas_asociacion()
        
        # Mostrar y exportar resultados
        analizador.mostrar_resultados()
        analizador.exportar_resultados()
    else:
        print("[X] No se pudieron procesar los datos para el análisis Apriori")