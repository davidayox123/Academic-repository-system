print("Testing auth router import...")

try:
    from app.api.v1.endpoints.auth import router as auth_router
    print("✅ Auth router imported successfully")
    print(f"📊 Auth router routes: {len(auth_router.routes)}")
    
    for route in auth_router.routes:
        print(f"  - {route.methods} {route.path}")
        
except Exception as e:
    print(f"❌ Auth router import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)

try:
    from app.api.v1.router import api_router
    print("✅ API router imported successfully")
    print(f"📊 API router routes: {len(api_router.routes)}")
    
    for route in api_router.routes:
        if hasattr(route, 'path'):
            print(f"  - {getattr(route, 'methods', 'N/A')} {route.path}")
        
except Exception as e:
    print(f"❌ API router import failed: {e}")
    import traceback
    traceback.print_exc()
