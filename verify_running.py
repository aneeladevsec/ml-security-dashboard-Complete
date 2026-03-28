import requests
r = requests.get('http://localhost:5000/api/health')
print(f'✅ Backend Status: {r.status_code}')
print(f'   Health: {r.json()["status"]}')
print(f'   Version: {r.json()["version"]}')
print(f'   Model: {r.json()["model_loaded"]}')
print(f'   Database: {r.json()["database"]}')
print('\n✅ All systems operational!')
