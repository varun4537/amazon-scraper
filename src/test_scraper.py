import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def test_packages():
    """Test if required packages are installed"""
    packages = {
        'aiohttp': 'For async HTTP requests',
        'beautifulsoup4': 'For HTML parsing',
        'pandas': 'For data handling',
        'pymongo': 'For MongoDB operations',
        'python-dotenv': 'For environment variables',
        'fastapi': 'For API creation',
        'uvicorn': 'For ASGI server'
    }
    
    all_installed = True
    print("\nTesting package installation:")
    print("-" * 50)
    
    for package, purpose in packages.items():
        try:
            if package == 'beautifulsoup4':
                import bs4
                print(f"✓ {package:15} - {purpose}")
            elif package == 'python-dotenv':
                import dotenv
                print(f"✓ {package:15} - {purpose}")
            else:
                __import__(package.replace('-', '_'))
                print(f"✓ {package:15} - {purpose}")
        except ImportError as e:
            all_installed = False
            print(f"✗ {package:15} - {purpose} - ERROR: {str(e)}")
    
    return all_installed

async def test_amazon_connection():
    """Test if we can connect to Amazon"""
    print("\nTesting Amazon connection:")
    print("-" * 50)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.amazon.com', headers=headers) as response:
                print(f"Status Code: {response.status}")
                
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    title = soup.title.string
                    print(f"Successfully connected to Amazon")
                    print(f"Page Title: {title}")
                    return True
                else:
                    print(f"Failed to connect to Amazon. Status: {response.status}")
                    return False
    except Exception as e:
        print(f"Error connecting to Amazon: {str(e)}")
        return False

async def main():
    print("\nStarting tests...")
    
    # Test 1: Package Installation
    packages_ok = await test_packages()
    
    # Test 2: Amazon Connection
    connection_ok = await test_amazon_connection()
    
    # Summary
    print("\nTest Summary:")
    print("-" * 50)
    print(f"Packages Installation: {'✓ OK' if packages_ok else '✗ FAILED'}")
    print(f"Amazon Connection: {'✓ OK' if connection_ok else '✗ FAILED'}")
    
    if packages_ok and connection_ok:
        print("\n✓ All tests passed successfully!")
    else:
        print("\n✗ Some tests failed. Please check the logs above.")

if __name__ == "__main__":
    asyncio.run(main())