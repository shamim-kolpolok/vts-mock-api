from flask import Flask, jsonify, request
from faker import Faker
from random import uniform, randint, choice
import time
from threading import Thread
from datetime import datetime, timezone, timedelta
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
fake = Faker('bn_BD')

# Configuration
DHAKA_CENTER = (23.7254, 90.4189)
COORDINATE_RANGE = 0.1
DRIVER_IDS = ["D_ID_1", "D_ID_2", "D_ID_3", "D_ID_4", "D_ID_5", "D_ID_6", "D_ID_7", "D_ID_8"]
UPDATE_INTERVAL = 5
MAX_SPEED_KPH = 60
TRIP_HISTORY_LIMIT = 100
DATA_RETENTION = 600

# Data storage structure
telematics_data = {
    driver_id: {
        'history': [],
        'latest': None,
        'trip_start': datetime.now(timezone.utc)
    } for driver_id in DRIVER_IDS
}

def generate_dhaka_coordinates():
    """Generate random coordinates within Dhaka area"""
    lat = DHAKA_CENTER[0] + uniform(-COORDINATE_RANGE, COORDINATE_RANGE)
    lng = DHAKA_CENTER[1] + uniform(-COORDINATE_RANGE, COORDINATE_RANGE)
    return round(lat, 6), round(lng, 6)

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers"""
    R = 6371.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def generate_telematics_data():
    """Generate random telematics data within Dhaka"""
    lat, lng = generate_dhaka_coordinates()
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "coordinates": {"latitude": lat, "longitude": lng},
        "speed": randint(0, MAX_SPEED_KPH),
        "fuel_level": round(uniform(0, 100), 1),
        "driver_id": choice(DRIVER_IDS)
    }

def data_generator():
    """Background data generator"""
    while True:
        data = generate_telematics_data()
        driver_id = data['driver_id']
        
        telematics_data[driver_id]['latest'] = data
        telematics_data[driver_id]['history'].append(data)
        
        if len(telematics_data[driver_id]['history']) > TRIP_HISTORY_LIMIT:
            telematics_data[driver_id]['history'].pop(0)
        
        time.sleep(UPDATE_INTERVAL)

def data_cleanup():
    """Periodically clear old data to simulate trips"""
    while True:
        time.sleep(DATA_RETENTION)
        now = datetime.now(timezone.utc)
        for driver_id in DRIVER_IDS:
            if now - telematics_data[driver_id]['trip_start'] > timedelta(seconds=DATA_RETENTION):
                telematics_data[driver_id]['history'] = []
                telematics_data[driver_id]['trip_start'] = now

# API Endpoints
@app.route('/api/live/<driver_id>', methods=['GET'])
def get_live_position(driver_id):
    if driver_id not in telematics_data:
        return jsonify({"error": "Driver not found"}), 404
    latest = telematics_data[driver_id]['latest']
    if not latest:
        return jsonify({"message": "No data available"}), 404
    return jsonify({
        "driver_id": driver_id,
        "position": latest['coordinates'],
        "timestamp": latest['timestamp'],
        "speed": latest['speed']
    })

@app.route('/api/nearby/<driver_id>', methods=['GET'])
def get_nearby_vehicles(driver_id):
    radius = request.args.get('radius', default=5, type=float)
    if driver_id not in telematics_data or not telematics_data[driver_id]['latest']:
        return jsonify({"error": "Driver not found or no data"}), 404
    source = telematics_data[driver_id]['latest']['coordinates']
    nearby = []
    for vehicle in DRIVER_IDS:
        if vehicle == driver_id or not telematics_data[vehicle]['latest']:
            continue
        target = telematics_data[vehicle]['latest']['coordinates']
        distance = haversine(
            source['latitude'], source['longitude'],
            target['latitude'], target['longitude']
        )
        if distance <= radius:
            nearby.append({
                "driver_id": vehicle,
                "distance": round(distance, 2),
                "position": target,
                "timestamp": telematics_data[vehicle]['latest']['timestamp']
            })
    return jsonify({
        "radius": radius,
        "center": source,
        "nearby_vehicles": sorted(nearby, key=lambda x: x['distance'])
    })

@app.route('/api/history/<driver_id>', methods=['GET'])
def get_trip_history(driver_id):
    if driver_id not in telematics_data:
        return jsonify({"error": "Driver not found"}), 404
    limit = request.args.get('limit', default=10, type=int)
    history = telematics_data[driver_id]['history'][-limit:]
    return jsonify({
        "driver_id": driver_id,
        "trip_start": telematics_data[driver_id]['trip_start'].isoformat(),
        "positions": [{
            "timestamp": entry['timestamp'],
            "coordinates": entry['coordinates'],
            "speed": entry['speed']
        } for entry in history]
    })

if __name__ == '__main__':
    Thread(target=data_generator).start()
    Thread(target=data_cleanup).start()
    app.run(host='0.0.0.0', port=5001, debug=True)