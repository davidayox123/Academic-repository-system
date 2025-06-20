#!/usr/bin/env python3
"""
Test script to verify configuration loading
"""
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    print("🔍 Testing configuration loading...")
    
    # Import the settings
    from app.core.config import Settings
    
    # Create settings instance
    settings = Settings()
    
    print("✅ Configuration loaded successfully!")
    print(f"📊 Configuration details:")
    print(f"   Database URL: {settings.DATABASE_URL}")
    print(f"   CORS Origins: {settings.CORS_ORIGINS}")
    print(f"   CORS Origins Type: {type(settings.CORS_ORIGINS)}")
    print(f"   Debug Mode: {settings.DEBUG}")
    print(f"   App Name: {settings.APP_NAME}")
    
    # Test that CORS_ORIGINS is a list
    if isinstance(settings.CORS_ORIGINS, list):
        print("✅ CORS_ORIGINS is correctly parsed as a list")
        print(f"   Number of origins: {len(settings.CORS_ORIGINS)}")
        for i, origin in enumerate(settings.CORS_ORIGINS, 1):
            print(f"   Origin {i}: {origin}")
    else:
        print(f"❌ CORS_ORIGINS is not a list: {type(settings.CORS_ORIGINS)}")
        sys.exit(1)
        
    print("\n🎉 All configuration tests passed!")
    
except Exception as e:
    print(f"❌ Configuration test failed: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
