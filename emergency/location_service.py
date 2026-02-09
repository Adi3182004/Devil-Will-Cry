import requests
import time
import os
import json

class LocationService:
    def __init__(self, cache_ttl=300, manual_file="data/user_location.json"):
        self.cache = None
        self.last_fetch = 0
        self.cache_ttl = cache_ttl
        self.manual_file = manual_file

        # 🔒 HARD-CODED EXACT FALLBACK LOCATION
        self.default_location = {
            "city": "Home Location",
            "region": "Maharashtra",
            "country": "India",
            "isp": "User Provided",
            "latitude": "19.249513160839154",
            "longitude": "73.15467808465651",
            "accuracy": "Exact (hardcoded)",
            "maps": "https://www.google.com/maps?q=19.249513160839154,73.15467808465651"
        }

    def _load_manual_location(self):
        if not os.path.exists(self.manual_file):
            return None

        try:
            with open(self.manual_file, "r") as f:
                data = json.load(f)

            lat = data.get("latitude")
            lon = data.get("longitude")

            if lat is None or lon is None:
                return None

            lat = str(lat)
            lon = str(lon)

            return {
                "city": data.get("label", "User Defined Location"),
                "region": data.get("region", "Exact"),
                "country": data.get("country", "Exact"),
                "isp": "User Provided",
                "latitude": lat,
                "longitude": lon,
                "accuracy": "Exact (user-defined)",
                "maps": f"https://www.google.com/maps?q={lat},{lon}"
            }

        except Exception as e:
            print(f"[LOCATION] Failed to load manual location: {e}")
            return None

    def _fetch_ip_location(self):
        try:
            r = requests.get("https://ipinfo.io/json", timeout=5)
            data = r.json()

            loc = data.get("loc")
            if loc and "," in loc:
                lat, lon = loc.split(",")
            else:
                lat, lon = "0", "0"

            return {
                "city": data.get("city") or "Unknown",
                "region": data.get("region") or "Unknown",
                "country": data.get("country") or "Unknown",
                "isp": data.get("org") or "Unknown ISP",
                "latitude": lat,
                "longitude": lon,
                "accuracy": "IP-based (approximate)",
                "maps": (
                    f"https://www.google.com/maps?q={lat},{lon}"
                    if lat != "0" else "Location unavailable"
                )
            }

        except Exception as e:
            print(f"[LOCATION] IP lookup failed: {e}")
            return None

    def get_location(self):
        now = time.time()

        if self.cache and (now - self.last_fetch) < self.cache_ttl:
            return self.cache

        # 1️⃣ Manual user-defined location (JSON file)
        manual = self._load_manual_location()
        if manual:
            self.cache = manual
            self.last_fetch = now
            return manual

        # 2️⃣ Hardcoded exact fallback (SAFE & OFFLINE)
        self.cache = self.default_location
        self.last_fetch = now
        return self.default_location
