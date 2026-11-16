import folium
from importlib import import_module

# Importamos el grafo ya procesado del Bloque 2
procesador = import_module("2_procesador_grafo")

def obtener_color_y_grosor(fc):
    if fc >= 2.0:
        return '#d90429', 4.5   # Rojo: Cuello de botella crítico
    elif fc > 1.2:
        return '#f77f00', 3.0   # Naranja: Congestión moderada
    else:
        return '#2b9348', 2.0   # Verde: Flujo fluido

def generar_mapa_interactivo():
    G = procesador.construir_grafo_ponderado()
    print("--- BLOQUE 3: RENDERIZANDO MAPA ESTILO GOOGLE MAPS ---")
    
    centro_la = [34.0488, -118.2518]
    # Usamos OpenStreetMap como capa base limpia, gratuita y con nombres reales de calles
    mapa = folium.Map(
    location=centro_la,
    zoom_start=15,
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Esri World Street Map'
)


    # Creamos 3 grupos de capas independientes para alternar horarios en vivo
    capa_14h = folium.FeatureGroup(name="14:00 - Hora Valle (Fluido)", show=False)
    capa_08h = folium.FeatureGroup(name="08:00 - Hora Punta Mañana", show=False)
    capa_18h = folium.FeatureGroup(name="18:00 - Hora Punta Noche (Saturado)", show=True)

    capas_config = [
        ('14h', capa_14h, 'fc_14h', 'peso_14h', 'vel_14h'),
        ('08h', capa_08h, 'fc_08h', 'peso_08h', 'vel_08h'),
        ('18h', capa_18h, 'fc_18h', 'peso_18h', 'vel_18h')
    ]

    for u, v, k, data in G.edges(keys=True, data=True):
        if 'fc_18h' not in data:
            continue
            
        if 'geometry' in data:
            coords = [(lat, lon) for lon, lat in data['geometry'].coords]
        else:
            coords = [(G.nodes[u]['y'], G.nodes[u]['x']), (G.nodes[v]['y'], G.nodes[v]['x'])]

        calle = data.get('calle', 'Vía local')

        for _, grupo_capa, key_fc, key_peso, key_vel in capas_config:
            fc = data[key_fc]
            peso = data[key_peso]
            vel = data[key_vel]
            color, grosor = obtener_color_y_grosor(fc)

            tooltip_html = (
                f"<b>Vía:</b> {calle}<br>"
                f"<b>Velocidad:</b> {vel:.1f} km/h<br>"
                f"<b>Tiempo tramo:</b> {peso:.2f} min<br>"
                f"<b>Factor FC:</b> {fc:.2f}"
            )

            folium.PolyLine(
                coords,
                color=color,
                weight=grosor,
                opacity=0.85,
                tooltip=tooltip_html
            ).add_to(grupo_capa)

    # Agregamos las 3 capas al mapa y activamos el control de intercambio en la esquina superior derecha
    capa_14h.add_to(mapa)
    capa_08h.add_to(mapa)
    capa_18h.add_to(mapa)
    folium.LayerControl(collapsed=False).add_to(mapa)

    archivo_salida = "mapa_fluctuacion_horaria.html"
    mapa.save(archivo_salida)
    print(f"-> ¡Mapa generado con éxito! Abre '{archivo_salida}' en Google Chrome.")

if __name__ == "__main__":
    generar_mapa_interactivo()