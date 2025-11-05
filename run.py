"""Simple run script for RealFlow"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main run function"""
    print("🚀 RealFlow CRE Agent")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists("pyproject.toml"):
        print("❌ Please run this script from the RealFlow directory")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("poetry install", "Installing dependencies"):
        sys.exit(1)
    
    # Check if setup has been run
    if not os.path.exists("assistant_id.txt"):
        print("\n⚠️  Assistant not configured. Running setup...")
        if not run_command("poetry run python setup.py", "Running setup"):
            print("❌ Setup failed. Please check your configuration.")
            sys.exit(1)
    
    # Start the server
    print("\n🌐 Starting RealFlow server...")
    print("   Server will be available at: http://localhost:8000")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        subprocess.run("poetry run python -m assistant.main", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server error: {e}")


if __name__ == "__main__":
    main()