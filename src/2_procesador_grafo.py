import osmnx as ox
import pandas as pd

def construir_grafo_ponderado():
    print("--- BLOQUE 2: PROCESAMIENTO DE GRAFO ESPACIOTEMPORAL ---")
    G = ox.load_graphml("data/red_vial_LA.graphml")
    df = pd.read_csv("data/dataset_trafico_LA.csv")

    
    metricas_por_arista = {}
    
    for _, row in df.iterrows():
        u, v, k = int(row['u']), int(row['v']), int(row['key'])
        t_ideal = row['t_ideal_min']
        dist_km = row['longitud_m'] / 1000.0

       
        t_14h = (dist_km / row['vel_14h_valle']) * 60.0
        fc_14h = t_14h / t_ideal

        t_08h = (dist_km / row['vel_08h_manana']) * 60.0
        fc_08h = t_08h / t_ideal

        t_18h = (dist_km / row['vel_18h_noche']) * 60.0
        fc_18h = t_18h / t_ideal

        metricas_por_arista[(u, v, k)] = {
            'calle': row['calle'],
            't_ideal': t_ideal,
            '14h': {'peso_min': t_14h, 'fc': fc_14h, 'vel': row['vel_14h_valle']},
            '08h': {'peso_min': t_08h, 'fc': fc_08h, 'vel': row['vel_08h_manana']},
            '18h': {'peso_min': t_18h, 'fc': fc_18h, 'vel': row['vel_18h_noche']}
        }

    
    cuellos_18h = 0
    for u, v, k, data in G.edges(keys=True, data=True):
        m = metricas_por_arista.get((u, v, k))
        if m:
            data['calle'] = m['calle']
            data['peso_14h'] = m['14h']['peso_min']
            data['fc_14h'] = m['14h']['fc']
            data['vel_14h'] = m['14h']['vel']

            data['peso_08h'] = m['08h']['peso_min']
            data['fc_08h'] = m['08h']['fc']
            data['vel_08h'] = m['08h']['vel']

            data['peso_18h'] = m['18h']['peso_min']
            data['fc_18h'] = m['18h']['fc']
            data['vel_18h'] = m['18h']['vel']

            if m['18h']['fc'] >= 2.0:
                cuellos_18h += 1

    print(f"-> Grafo hidratado exitosamente. Cuellos de botella detectados en Hora Punta (18:00): {cuellos_18h} tramos.")
    return G

if __name__ == "__main__":
    construir_grafo_ponderado()
