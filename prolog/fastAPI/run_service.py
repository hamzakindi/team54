import uvicorn
import os
import sys
from subprocess import run, PIPE
from pathlib import Path

def verify_environment():
    # Check SWI-Prolog
    try:
        result = run(['swipl', '--version'], stdout=PIPE, stderr=PIPE)
        if result.returncode != 0:
            print("Error: SWI-Prolog is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("Error: SWI-Prolog not found. Please install SWI-Prolog and add it to PATH")
        return False

    # Check if Prolog file exists
    prolog_file = Path(__file__).parent.parent / "ruleset" / "test_recommendations.pl"
    if not prolog_file.exists():
        print(f"Error: Prolog file not found at {prolog_file}")
        return False

    return True

def main():
    if not verify_environment():
        sys.exit(1)

    print("Starting FastAPI server...")
    try:
        uvicorn.run(
            "api_service:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()