import osmnx as ox
import pandas as pd
import random
import os

def generar_dataset_urbano():
    print("--- BLOQUE 1: INGESTA DE DATOS ESPACIOTEMPORALES ---")
    print("1. Conectando con OpenStreetMap para extraer red vial real (Los Ángeles)...")
    
    
    centro_la = (34.0488, -118.2518)
    G = ox.graph_from_point(centro_la, dist=1500, network_type='drive')
    
    
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    
  
    os.makedirs("data", exist_ok=True)
    ox.save_graphml(G, filepath="data/red_vial_LA.graphml")
    print(f"-> Topología guardada en 'data/red_vial_LA.graphml' ({len(G.nodes)} nodos, {len(G.edges)} aristas).")

    print("2. Construyendo matriz horaria de velocidades (Valle vs. Punta)...")
    random.seed(42)  
    registros = []

    for u, v, k, data in G.edges(keys=True, data=True):
        longitud_m = data.get('length', 100.0)
        vel_libre = data.get('speed_kph', 40.0)
        t_ideal_min = (data.get('travel_time', longitud_m / (vel_libre / 3.6))) / 60.0
        
        
        tipo_via = str(data.get('highway', ''))
        es_arteria = any(t in tipo_via for t in ['primary', 'secondary', 'trunk'])

       
        deg_valle = random.uniform(1.0, 1.15)
        vel_14h = vel_libre / deg_valle

        
        deg_08h = random.uniform(1.8, 2.5) if (es_arteria and random.random() < 0.4) else random.uniform(1.1, 1.5)
        vel_08h = vel_libre / deg_08h

        
        deg_18h = random.uniform(2.2, 3.4) if (es_arteria and random.random() < 0.5) else random.uniform(1.2, 1.8)
        vel_18h = vel_libre / deg_18h

        registros.append({
            'u': u,
            'v': v,
            'key': k,
            'calle': str(data.get('name', 'Vía local')),
            'tipo_via': tipo_via,
            'longitud_m': round(longitud_m, 2),
            'vel_libre_kmh': round(vel_libre, 2),
            't_ideal_min': round(t_ideal_min, 4),
            'vel_14h_valle': round(vel_14h, 2),
            'vel_08h_manana': round(vel_08h, 2),
            'vel_18h_noche': round(vel_18h, 2)
        })

    df = pd.DataFrame(registros)
    ruta_csv = "data/dataset_trafico_LA.csv"
    df.to_csv(ruta_csv, index=False)
    print(f"-> Dataset horario generado exitosamente en '{ruta_csv}' ({len(df)} tramos procesados).")

if __name__ == "__main__":
    generar_dataset_urbano()
