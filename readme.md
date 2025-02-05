# VTS Mock API

This project is a mock Vehicle Tracking System (VTS) API that generates random vehicle location and telematics data.

## **Installation & Setup**

### **Prerequisites**
Ensure you have the following installed on your system:
- Python 3.10 or later
- `pip` (Python package manager)
- `virtualenv` (for creating isolated environments)

### **Clone the Repository**
```sh
git clone https://github.com/your-repo/vts-mock-api.git
cd vts-mock-api
```

### **Set Up a Virtual Environment**
Run the following command to create and activate a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows (PowerShell)
```

### **Install Dependencies**
Once inside the virtual environment, install the required packages:
```sh
pip install -r requirements.txt
```

If you face a `ModuleNotFoundError` for Flask, manually install it:
```sh
pip install flask faker
```

### **Run the Application**
```sh
python app.py
```

The API will now be running on `http://127.0.0.1:5001`.

## **Available Endpoints**

### **1. Get Live Position of a Driver**
```sh
GET /api/live/<driver_id>
```
#### **Response**
```json
{
  "driver_id": "D_ID_1",
  "position": { "latitude": 23.7256, "longitude": 90.4191 },
  "timestamp": "2025-02-05T12:00:00Z",
  "speed": 40
}
```

### **2. Get Nearby Vehicles**
```sh
GET /api/nearby/<driver_id>?radius=5
```
#### **Response**
```json
{
  "radius": 5,
  "center": { "latitude": 23.7256, "longitude": 90.4191 },
  "nearby_vehicles": [
    {
      "driver_id": "D_ID_3",
      "distance": 3.2,
      "position": { "latitude": 23.7270, "longitude": 90.4200 },
      "timestamp": "2025-02-05T12:00:00Z"
    }
  ]
}
```

### **3. Get Driver's Trip History**
```sh
GET /api/history/<driver_id>?limit=10
```
#### **Response**
```json
{
  "driver_id": "D_ID_1",
  "trip_start": "2025-02-05T10:00:00Z",
  "positions": [
    { "timestamp": "2025-02-05T12:00:00Z", "coordinates": { "latitude": 23.7256, "longitude": 90.4191 }, "speed": 40 }
  ]
}
```

## **Troubleshooting**

### **1. `ModuleNotFoundError: No module named 'flask'`**
If you see this error, make sure the virtual environment is activated and install Flask:
```sh
source venv/bin/activate
pip install flask faker
```

### **2. `source venv/bin/activate: No such file or directory`**
Ensure you created the virtual environment correctly:
```sh
python3 -m venv venv
source venv/bin/activate
```

## **License**
This project is open-source and free to use.


