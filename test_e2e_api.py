import threading
import time
import requests
import uvicorn
from src.milestone_1.main import app

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def test_api():
    print("Starting API server in background...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start and load dataset by polling
    print("Waiting for server to become ready...")
    for _ in range(30):
        try:
            requests.get("http://127.0.0.1:8000/docs")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    
    print("Sending POST request to /api/v1/recommend...")
    payload = {
        "location": "Bellandur",
        "cuisines": "italian, desserts",
        "budget": {
            "mode": "range",
            "min_cost": 0,
            "max_cost": 2000
        },
        "min_rating": 4.0,
        "extra_preferences": ""
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/recommend", json=payload)
        data = response.json()
        
        if data.get("ok"):
            print(f"SUCCESS: Received {len(data['recommendations'])} recommendations!")
            print(f"Top rank: {data['recommendations'][0]['restaurant_name']}")
        else:
            print("FAILED:", data)
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    test_api()
