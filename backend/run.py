"""
Startup script - Initialize and run the Guru.ai backend

Usage:
    python run.py
    
Or for development with auto-reload:
    python run.py --reload
"""
import sys
import argparse
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from app import config
from train_model import train_guardrail_model

logger = logging.getLogger(__name__)


def check_models_exist():
    """Check if trained models exist"""
    classifier_exists = config.CLASSIFIER_MODEL_PATH.exists()
    vectorizer_exists = config.VECTORIZER_MODEL_PATH.exists()

    return classifier_exists and vectorizer_exists


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Guru.ai Backend Server")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes (development only)",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind to (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)",
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Train the guardrail model before starting the server",
    )

    args = parser.parse_args()

    # Check and train models if needed
    if args.train or not check_models_exist():
        print("\n" + "=" * 60)
        print("🤖 Training Guardrail Model...")
        print("=" * 60)

        if not train_guardrail_model():
            print("\n❌ Failed to train model. Exiting.")
            sys.exit(1)

        print("\n✅ Model training completed!\n")

    # Verify models exist
    if not check_models_exist():
        print(
            "\n⚠️  Trained models not found. Run with --train flag to train them:\n"
            "   python run.py --train\n"
        )
        sys.exit(1)

    # Start server
    print("\n" + "=" * 60)
    print("🚀 Starting Guru.ai Backend Server")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Auto-reload: {args.reload}")
    print("\n📖 API Documentation:")
    print(f"   Swagger UI: http://{args.host}:{args.port}/docs")
    print(f"   ReDoc: http://{args.host}:{args.port}/redoc")
    print("\n💡 Health Check:")
    print(f"   curl http://{args.host}:{args.port}/health")
    print("\n" + "=" * 60 + "\n")

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
