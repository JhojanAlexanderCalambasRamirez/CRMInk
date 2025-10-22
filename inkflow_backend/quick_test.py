import requests
import sys

BASE_URL = "http://localhost:8000"

def quick_test():
    print("⚡ PRUEBA RÁPIDA DEL BACKEND")
    print("=" * 40)
    
    # Solo probar lo esencial
    tests = [
        ("GET", "/health", None),
        ("GET", "/info", None),
    ]
    
    for method, endpoint, data in tests:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=3)
            print(f"{'✅' if response.status_code == 200 else '❌'} {endpoint}: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"❌ {endpoint}: TIMEOUT")
            return False
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
            return False
    
    # Solo si lo básico funciona, probar login
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data={"username": "admin@inkmasters.com", "password": "admin123"},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ /api/auth/login: 200 OK")
            print("🎉 Backend funcionando correctamente!")
            return True
        else:
            print(f"❌ /api/auth/login: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ /api/auth/login: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
