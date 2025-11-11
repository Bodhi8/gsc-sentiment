"""
Setup script to help users get started quickly
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing packages")
        return False


def download_spacy_model():
    """Download spaCy language model"""
    print("\n📥 Downloading spaCy language model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error downloading spaCy model")
        print("   You can download it manually later with: python -m spacy download en_core_web_sm")
        return False


def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if os.path.exists('.env'):
        print("\n✅ .env file already exists")
        return True
    
    if not os.path.exists('.env.example'):
        print("\n❌ .env.example file not found")
        return False
    
    print("\n📝 Creating .env file from template...")
    try:
        with open('.env.example', 'r') as example:
            content = example.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✅ .env file created")
        print("   ⚠️  Please edit .env and add your credentials")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = ['outputs', 'data']
    print("\n📁 Creating directories...")
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")
    
    return True


def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "=" * 80)
    print("🎉 SETUP COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("\n1. Set up Google Cloud credentials:")
    print("   a. Go to https://console.cloud.google.com/")
    print("   b. Create a service account with Search Console API access")
    print("   c. Download the credentials JSON file")
    print("   d. Add the service account to your Search Console property")
    print("\n2. Update the .env file with:")
    print("   - Path to your credentials JSON file")
    print("   - Your Search Console site URL")
    print("   - Date range for analysis")
    print("\n3. Run the analysis:")
    print("   python gsc_sentiment_analyzer.py")
    print("\n4. Or run examples:")
    print("   python examples.py")
    print("\n" + "=" * 80)
    print("\nFor detailed instructions, see README.md")
    print("=" * 80)


def main():
    """Run setup process"""
    print("=" * 80)
    print("GSC Sentiment Analyzer - Setup")
    print("=" * 80)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        print("\n⚠️  Setup incomplete due to errors")
        return
    
    # Download spaCy model
    download_spacy_model()
    
    # Create .env file
    create_env_file()
    
    # Create directories
    create_directories()
    
    # Print next steps
    print_next_steps()


if __name__ == '__main__':
    main()
