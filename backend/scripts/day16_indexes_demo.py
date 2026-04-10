import os
import sys
import psycopg
import time
import uuid
import random

# Forzar la inclusión del root del backend en PYTHONPATH para que importe src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.config.config import DATABASE_URL

def print_separator():
    print("\n" + "="*70 + "\n")

def run_demo():
    print_separator()
    print("🚀 DÍA 16: SIMULADOR INTERACTIVO DE PERFORMANCE DE BASE DE DATOS")
    print("Objetivo: Enseñar cómo un Índice baja los tiempos de consulta de Segundos a Milisegundos.")
    print_separator()

    # 1. Establecer conexión
    print("🔌 Conectando a la base de datos PostgreSQL de Producción...")
    try:
        conn = psycopg.connect(DATABASE_URL)
        conn.autocommit = True
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return

    try:
        with conn.cursor() as cur:
            # 2. Verificar cuántas filas hay
            cur.execute("SELECT count(*) FROM items")
            count = cur.fetchone()[0]
            print(f"✅ ¡Conectado! Tu tabla 'items' tiene actualmente {count} registros.")

            # 2. Carga masiva de datos (solamente si hay pocos registros para no asfixiar el demo si se repite)
            TARGET_ROWS = 500000
            if count < TARGET_ROWS:
                rows_to_insert = TARGET_ROWS - count
                print(f"\n⚠️ Tienes muy pocos registros (menos de 500k).")
                print(f"🏗️  Iniciando Carga Masiva (Ultra-rápida vía COPY) de {rows_to_insert} ítems 'falsos'...")
                print("⏳ Esto tardará unos 3 a 5 segundos, agárrate fuerte...")
                
                start_insert = time.time()
                with cur.copy("COPY items (id, name, description, price) FROM STDIN") as copy:
                    for i in range(rows_to_insert):
                        # Precio especial: $999.99 (asegurar que exista al menos uno así)
                        price = 999.99 if i == 250000 else round(random.uniform(10.0, 500.0), 2)
                        item_id = str(uuid.uuid4())
                        copy.write_row((item_id, f"Fake Item #{i}", "Un item generado masivamente", price))
                print(f"✅ ¡Completado velozmente en {round(time.time() - start_insert, 2)} segundos!")
            else:
                print("👍 ¡Tienes suficientes datos pesados! Excelente para hacer que PostgreSQL transpire.")

            # Limpiar un posible índice anterior si el usuario quiere correr de cero este demo:
            cur.execute("DROP INDEX IF EXISTS idx_items_price")
            print("🧹 Nos aseguramos de eliminar el Índice antiguo para que la BD sufra esta primera vez.")

            print_separator()
            print("🔪 ESCENARIO 1: Consulta LENTA (Seq Scan) -> ESCANEO SECUENCIAL COMPLETO")
            input("👉 Presiona ENTER para ejecutar el EXPLAIN ANALYZE buscando el precio $999.99...")
            
            # 3. Lanzar EXPLAIN ANALYZE sin índices
            print("\n⏳ Postgres está leyendo tu disco duro página por página recorriendo 500,000 registros...")
            cur.execute("EXPLAIN ANALYZE SELECT id, name, price FROM items WHERE price = 999.99;")
            results_slow = cur.fetchall()
            for row in results_slow:
                print(f"   {row[0]}")
            
            print_separator()
            print("🔥 ¡FÍJATE ARRIBA! El 'Execution Time' probablemente fue de varios milisegundos largos.")
            print("🚨 Y el 'Node Type' fue un 'Seq Scan' (Búsqueda secuencial exhaustiva y destructiva).")
            print("Imagínate multiplicar esa demora por 1,000 usuarios buscando productos simultáneamente. ¡Servidor caído!")
            print_separator()
            
            # 4. Inyección mágica de Índice
            print("🪄 ESCENARIO 2: ¡Hora de crear el Índice B-Tree de rescate!")
            input("👉 Presiona ENTER en tu teclado para que lancemos el CREATE INDEX en la BD...")

            print("\n⏳ Creando Índice: 'CREATE INDEX idx_items_price ON items(price);'")
            start_idx = time.time()
            cur.execute("CREATE INDEX idx_items_price ON items(price);")
            print(f"✅ Índice creado maravillosamente en: {round(time.time() - start_idx, 2)} segundos.")

            # 5. Volver a probar
            print_separator()
            input("👉 Presiona ENTER una ultimísima vez para CORRER NUEVAMENTE la Búsqueda de $999.99...")
            
            cur.execute("EXPLAIN ANALYZE SELECT id, name, price FROM items WHERE price = 999.99;")
            results_fast = cur.fetchall()
            for row in results_fast:
                print(f"   {row[0]}")
            
            print_separator()
            print("⚡ ¡MAGIA! Observa el Execution Time final y el 'Index Scan'.")
            print("¡Redujiste el tiempo violentamente, pasando de un impacto alto a escasos milisegundos!")
            print("🚀 Acabas de pasar al nivel semi-senior de bases de datos. ¡Felicidades!")
            print_separator()
            
    finally:
        conn.close()

if __name__ == "__main__":
    run_demo()
