import folium
import requests

# Replace with your API key
API_KEY = 'https://maps.app.goo.gl/R9KmpLEKpDr36WSY7'

def get_current_location():
    # This is a placeholder for the actual geolocation code
    # In practice, you might use an IP-based geolocation service or get coordinates from the user
    # Here we use a fixed location for demonstration
    return (53.48, -2.24)

def get_route(start_location, end_location):
    directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_location}&destination={end_location}&key={API_KEY}"
    response = requests.get(directions_url)
    directions_data = response.json()
    
    routes = directions_data.get('routes', [])
    if not routes:
        return [], []
    
    route = routes[0]['legs'][0]['steps']
    latitude_list = []
    longitude_list = []

    for step in route:
        start_lat = step['start_location']['lat']
        start_lng = step['start_location']['lng']
        latitude_list.append(start_lat)
        longitude_list.append(start_lng)

    return latitude_list, longitude_list

def create_map(center, route_coords=None):
    # Create the map centered around the current location
    map_obj = folium.Map(location=center, zoom_start=15)

    # Add a marker at the current location
    folium.Marker(location=center, popup="You are here").add_to(map_obj)

    # Optionally, add a route to the map
    if route_coords:
        folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(map_obj)
    
    # Save the map to an HTML file
    map_obj.save('map.html')

if __name__ == "__main__":
    # Current location (you could use a real geolocation service in practice)
    current_location = get_current_location()

    # Define the destination location (replace with your actual destination)
    destination_location = 'Boston, MA'

    # Get route coordinates
    latitude_list, longitude_list = get_route(f"{current_location[0]},{current_location[1]}", destination_location)
    route_coords = list(zip(latitude_list, longitude_list))

    # Create the map with the current location and route
    create_map(current_location, route_coords)
