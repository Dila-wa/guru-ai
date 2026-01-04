"""
Project Verification Checklist
This script verifies that all required files and dependencies are in place
"""
import sys
from pathlib import Path

def check_file_exists(file_path: str, description: str) -> bool:
    """Check if a file exists and print status"""
    exists = Path(file_path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists

def check_directory_exists(dir_path: str, description: str) -> bool:
    """Check if a directory exists and print status"""
    exists = Path(dir_path).is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists

def main():
    """Run verification checks"""
    print("\n" + "=" * 70)
    print("🔍 GURU.AI PROJECT VERIFICATION CHECKLIST")
    print("=" * 70 + "\n")

    all_checks = []

    # Project structure
    print("📁 PROJECT STRUCTURE")
    print("-" * 70)
    all_checks.append(check_directory_exists("backend", "backend/ folder"))
    all_checks.append(check_directory_exists("backend/app", "backend/app/ folder"))
    all_checks.append(check_directory_exists("backend/app/routes", "backend/app/routes/ folder"))
    all_checks.append(check_directory_exists("backend/app/services", "backend/app/services/ folder"))
    all_checks.append(check_directory_exists("backend/app/models", "backend/app/models/ folder"))
    all_checks.append(check_directory_exists("backend/data", "backend/data/ folder"))
    all_checks.append(check_directory_exists("backend/data/textbooks", "backend/data/textbooks/ folder"))
    all_checks.append(check_directory_exists("backend/data/textbooks/raw_pdfs", "backend/data/textbooks/raw_pdfs/ folder"))
    all_checks.append(check_directory_exists("backend/data/training", "backend/data/training/ folder"))

    # Core application files
    print("\n🐍 CORE APPLICATION FILES")
    print("-" * 70)
    all_checks.append(check_file_exists("backend/app/__init__.py", "app/__init__.py"))
    all_checks.append(check_file_exists("backend/app/main.py", "app/main.py (FastAPI)"))
    all_checks.append(check_file_exists("backend/app/config.py", "app/config.py (configuration)"))
    all_checks.append(check_file_exists("backend/app/routes/__init__.py", "routes/__init__.py"))
    all_checks.append(check_file_exists("backend/app/routes/chat.py", "routes/chat.py (API endpoints)"))
    all_checks.append(check_file_exists("backend/app/services/__init__.py", "services/__init__.py"))
    all_checks.append(check_file_exists("backend/app/services/guardrail.py", "services/guardrail.py (safety)"))
    all_checks.append(check_file_exists("backend/app/services/syllabus_classifier.py", "services/syllabus_classifier.py (ML)"))
    all_checks.append(check_file_exists("backend/app/services/ai_engine.py", "services/ai_engine.py (answer gen)"))
    all_checks.append(check_file_exists("backend/app/services/vector_store.py", "services/vector_store.py (FAISS)"))
    all_checks.append(check_file_exists("backend/app/services/chunker.py", "services/chunker.py (text chunking)"))
    all_checks.append(check_file_exists("backend/app/services/textbook_loader.py", "services/textbook_loader.py (PDF)"))
    all_checks.append(check_file_exists("backend/app/models/__init__.py", "models/__init__.py"))
    all_checks.append(check_file_exists("backend/app/models/schema.py", "models/schema.py (Pydantic)"))

    # Configuration and dependencies
    print("\n⚙️ CONFIGURATION & DEPENDENCIES")
    print("-" * 70)
    all_checks.append(check_file_exists("backend/requirements.txt", "requirements.txt (dependencies)"))
    all_checks.append(check_file_exists("backend/.gitignore", ".gitignore"))

    # Scripts
    print("\n🚀 SCRIPTS")
    print("-" * 70)
    all_checks.append(check_file_exists("backend/run.py", "run.py (startup script)"))
    all_checks.append(check_file_exists("backend/train_model.py", "train_model.py (training)"))
    all_checks.append(check_file_exists("backend/test_integration.py", "test_integration.py (tests)"))

    # Documentation
    print("\n📚 DOCUMENTATION")
    print("-" * 70)
    all_checks.append(check_file_exists("backend/README.md", "backend/README.md"))
    all_checks.append(check_file_exists("backend/SETUP.md", "backend/SETUP.md"))
    all_checks.append(check_file_exists("README.md", "root/README.md"))
    all_checks.append(check_file_exists("PROJECT_SUMMARY.md", "PROJECT_SUMMARY.md"))

    # Data
    print("\n📊 DATA")
    print("-" * 70)
    all_checks.append(check_file_exists("backend/data/training/question_labels.csv", "question_labels.csv (training data)"))

    # Summary
    print("\n" + "=" * 70)
    total_checks = len(all_checks)
    passed_checks = sum(all_checks)
    failed_checks = total_checks - passed_checks

    print(f"📊 VERIFICATION SUMMARY")
    print("-" * 70)
    print(f"Total Checks: {total_checks}")
    print(f"✅ Passed: {passed_checks}")
    print(f"❌ Failed: {failed_checks}")

    if failed_checks == 0:
        print("\n" + "=" * 70)
        print("🎉 ALL CHECKS PASSED!")
        print("=" * 70)
        print("\n✨ Your Guru.ai backend is ready to use!")
        print("\nNext steps:")
        print("  1. cd backend")
        print("  2. python -m venv venv")
        print("  3. venv\\Scripts\\activate  # Windows (or source venv/bin/activate)")
        print("  4. pip install -r requirements.txt")
        print("  5. python run.py --train")
        print("  6. python run.py")
        print("\nThen visit: http://localhost:8000/docs")
        print("=" * 70)
        return 0
    else:
        print("\n" + "=" * 70)
        print("⚠️ SOME CHECKS FAILED")
        print("=" * 70)
        print("\nPlease ensure all files are present in the correct locations.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
