import json
import random

def generate_cameras():
    cameras = []
    
    # Hardcoded real ones
    cameras.extend([
        {
            "id": "cam_iss",
            "title": "NASA ISS Live HD Stream",
            "city": "Space",
            "country": "Space",
            "continent": "Polar/Oceans/Space",
            "lat": 0.0,
            "lon": 0.0,
            "category": "Space/Orbital",
            "stream_type": "youtube",
            "stream_url": "https://www.youtube.com/watch?v=86YLFOog4GM",
            "poster_url": "https://img.youtube.com/vi/86YLFOog4GM/maxresdefault.jpg",
            "status": "online"
        },
        {
            "id": "cam_times_square",
            "title": "Times Square Live Cam",
            "city": "New York",
            "country": "USA",
            "continent": "North America",
            "lat": 40.7580,
            "lon": -73.9855,
            "category": "City/Landmark",
            "stream_type": "youtube",
            "stream_url": "https://www.youtube.com/watch?v=1-iS7LArMPA",
            "poster_url": "https://img.youtube.com/vi/1-iS7LArMPA/maxresdefault.jpg",
            "status": "online"
        }
    ])
    
    categories = [
        "City/Landmark", "Storm/Coast/Beach", "Traffic/Highway", 
        "Mountain/Volcano", "Weather/Sky", "Wildlife/Nature"
    ]
    
    continents = {
        "North America": {"countries": ["USA", "Canada"], "lat_range": (25, 55), "lon_range": (-125, -70)},
        "Europe": {"countries": ["UK", "France", "Germany", "Italy"], "lat_range": (35, 65), "lon_range": (-10, 30)},
        "Asia": {"countries": ["China", "Japan", "India"], "lat_range": (10, 50), "lon_range": (70, 140)},
        "South America": {"countries": ["Brazil", "Argentina"], "lat_range": (-40, 10), "lon_range": (-80, -40)},
        "Oceania": {"countries": ["Australia", "New Zealand"], "lat_range": (-45, -10), "lon_range": (110, 175)},
        "Africa": {"countries": ["South Africa", "Kenya"], "lat_range": (-35, 30), "lon_range": (-15, 50)}
    }

    camera_types = ["hls", "mjpeg", "snapshot", "youtube"]

    idx = len(cameras)
    while len(cameras) < 5500:
        continent = random.choice(list(continents.keys()))
        data = continents[continent]
        country = random.choice(data["countries"])
        lat = random.uniform(data["lat_range"][0], data["lat_range"][1])
        lon = random.uniform(data["lon_range"][0], data["lon_range"][1])
        category = random.choice(categories)
        stream_type = random.choice(camera_types)
        
        url_map = {
            "hls": f"https://example.com/hls/cam_{idx}.m3u8",
            "mjpeg": f"https://example.com/mjpeg/cam_{idx}.mjpg",
            "snapshot": f"https://example.com/snapshot/cam_{idx}.jpg",
            "youtube": f"https://www.youtube.com/watch?v=dummy_{idx}"
        }
        
        cameras.append({
            "id": f"cam_{idx:05d}",
            "title": f"Live {category} Cam - {country} {idx}",
            "city": f"City_{idx}",
            "country": country,
            "continent": continent,
            "lat": round(lat, 5),
            "lon": round(lon, 5),
            "category": category,
            "stream_type": stream_type,
            "stream_url": url_map[stream_type],
            "poster_url": f"https://example.com/posters/cam_{idx}.jpg",
            "status": "online"
        })
        idx += 1

    with open(r"D:\projects\omniscope-osint\backend\data\cameras_db.json", "w", encoding="utf-8") as f:
        json.dump(cameras, f, indent=2)

    print(f"Generated {len(cameras)} cameras successfully.")

if __name__ == '__main__':
    generate_cameras()
