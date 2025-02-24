import time
from geopy.geocoders import Nominatim
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from geopy.exc import GeocoderTimedOut

# Inicializa el geolocalizador
geolocator = Nominatim(user_agent="geoapi")  # Aumentar timeout para estabilidad
def reverse_geocode(lat, lon):
    print(f"Procesando coordenadas: {lat}, {lon}")  # Debugging
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        print(f"Resultado: {location}")  # Debugging
        if location and location.raw.get('address'):
            address = location.raw['address']
            return address.get('postcode', 'N/A'), address.get('suburb', 'N/A')
    except Exception as e:
        print(f"Error en reverse_geocode: {e}")
    return "N/A", "N/A"

df = pd.read_csv("C:/Users/aleja/OneDrive - The University of Chicago/Winter 2025/Project/crime2024.csv")
df = df.dropna(subset=['Latitude', 'Longitude'])
df = df[(df["Arrest"] == True) & (df["Domestic"] == False)]
# Aplicar la función a cada fila
df[['postal_code', 'neighborhood']] = df.apply(
    lambda row: reverse_geocode(row['Latitude'], row['Longitude']), axis=1, result_type='expand'
)

# Guardar los resultados en un nuevo CSV
df.to_csv("resultado_con_direcciones.csv", index=False)


