from emergency.location_service import LocationService

location_service = LocationService()

location = location_service.get_location()

print("\n--- LOCATION TEST OUTPUT ---")
print("City      :", location.get("city", "N/A"))
print("Region    :", location.get("region", "N/A"))
print("Country   :", location.get("country", "N/A"))
print("ISP       :", location.get("isp", "N/A"))
print("Latitude  :", location.get("latitude", "N/A"))
print("Longitude :", location.get("longitude", "N/A"))
print("Accuracy  :", location.get("accuracy", "N/A"))
print("Maps लिंक :", location.get("maps", "N/A"))
print("-----------------------------\n")
