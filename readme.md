# VTS Mock API

This is a mock API for a Vehicle Tracking System (VTS) that generates random telematics data for multiple drivers. It provides real-time vehicle positions, trip history, and nearby vehicle information.

## Features
- Generates random latitude/longitude within Dhaka, Bangladesh.
- Updates vehicle data every 5 seconds.
- Provides real-time location, speed, and fuel level.
- Stores trip history with a limit of 100 records.
- Cleans up old data after 10 minutes.
- API endpoints to get live position, trip history, and nearby vehicles.

## Requirements
- Python 3.7+
- Virtual environment (optional but recommended)
- Flask
- Faker

## Installation & Setup

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/vts-mock-api.git
cd vts-mock-api
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the Application
```sh
python app.py
```
By default, it runs on `http://localhost:5001`.

## Accessing the API

### 1. Get Live Position
```sh
GET http://localhost:5001/api/live/D_ID_1
```
Response:
```json
{
  "driver_id": "D_ID_1",
  "position": { "latitude": 23.726, "longitude": 90.419 },
  "timestamp": "2025-02-05T12:00:00Z",
  "speed": 45
}
```

### 2. Get Nearby Vehicles
```sh
GET http://localhost:5001/api/nearby/D_ID_1?radius=5
```
Response:
```json
{
  "radius": 5,
  "center": { "latitude": 23.726, "longitude": 90.419 },
  "nearby_vehicles": [
    {
      "driver_id": "D_ID_2",
      "distance": 3.2,
      "position": { "latitude": 23.728, "longitude": 90.422 },
      "timestamp": "2025-02-05T12:00:00Z"
    }
  ]
}
```

### 3. Get Trip History
```sh
GET http://localhost:5001/api/history/D_ID_1?limit=10
```
Response:
```json
{
  "driver_id": "D_ID_1",
  "trip_start": "2025-02-05T11:50:00Z",
  "positions": [
    { "timestamp": "2025-02-05T11:55:00Z", "coordinates": { "latitude": 23.726, "longitude": 90.419 }, "speed": 40 }
  ]
}
```

## Sharing on Local Network
Find your local IP:
```sh
ipconfig getifaddr en0  # macOS (Wi-Fi)
ipconfig getifaddr en1  # macOS (Ethernet)
```
Run the app with:
```sh
python app.py
```
Access it from other devices on the same network:
```sh
http://<your-local-ip>:5001/api/live/D_ID_1
```

## Troubleshooting
- Ensure your firewall allows incoming connections to Python.
- Use `netstat -an | grep 5001` to check if the port is open.
- Run `pip install -r requirements.txt` to install missing dependencies.

