#!/usr/bin/env python3
import os
import sys
import subprocess

def setup_api_key():
    print("=== IPFinder API Key Setup ===")
    print("\n1. First, go to https://ipinfo.io/signup")
    print("2. Sign up for a free account")
    print("3. Once registered, get your API token from https://ipinfo.io/account/token")
    
    api_key = input("\nPaste your API key here: ").strip()
    
    if not api_key:
        print("Error: API key cannot be empty")
        sys.exit(1)
    
    # Add to current session
    os.environ['IPFINDER_API_KEY'] = api_key
    
    # Add to shell rc file
    shell = os.environ.get('SHELL', '/bin/bash').split('/')[-1]
    rc_file = os.path.expanduser(f'~/.{shell}rc')
    
    try:
        with open(rc_file, 'a') as f:
            f.write(f'\n# IPFinder API Key\nexport IPFINDER_API_KEY="{api_key}"\n')
        
        print(f"\nSuccess! API key has been added to {rc_file}")
        print("To use it in the current session, run:")
        print(f'export IPFINDER_API_KEY="{api_key}"')
        
        # Test the API key
        print("\nTesting API key with a sample lookup...")
        cmd = f'PYTHONPATH=/workspaces/ipfinder IPFINDER_API_KEY="{api_key}" python infotool.py google.com'
        subprocess.run(cmd, shell=True)
        
    except Exception as e:
        print(f"Error saving API key: {str(e)}")
        print("You can manually set it by running:")
        print(f'export IPFINDER_API_KEY="{api_key}"')

if __name__ == "__main__":
    setup_api_key()
