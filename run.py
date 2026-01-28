import os
import sys

def main():
    print("🌍 Starting Grid Guessr...")
    print("=" * 50)
    
    # Check if uvicorn is installed
    try:
        import uvicorn
    except ImportError:
        print("❌ Error: uvicorn not installed")
        print("Run: pip install fastapi uvicorn --break-system-packages")
        sys.exit(1)
    
    # Check if FastAPI is installed
    try:
        import fastapi
    except ImportError:
        print("❌ Error: fastapi not installed")
        print("Run: pip install fastapi uvicorn --break-system-packages")
        sys.exit(1)
    
    print("✅ Dependencies installed")
    print("🚀 Starting server on http://localhost:8000")
    print("=" * 50)
    print("\nPress CTRL+C to stop the server\n")
    
    # Run the server
    uvicorn.run(
        "grid_guessr:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
