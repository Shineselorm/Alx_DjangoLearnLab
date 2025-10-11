#!/usr/bin/env python3
"""
Checker Debug Script
Helps diagnose why the checker might be failing to find settings.py
"""

import os
import sys
from pathlib import Path

def check_from_directory(base_path, description):
    """Check for settings.py from a specific directory"""
    print(f"\n{'='*70}")
    print(f"Checking from: {description}")
    print(f"Directory: {base_path}")
    print(f"{'='*70}")
    
    original_dir = os.getcwd()
    try:
        os.chdir(base_path)
        current = os.getcwd()
        print(f"Current working directory: {current}")
        
        # Check different path variations
        paths_to_check = [
            'social_media_api/settings.py',
            'social_media_api/social_media_api/settings.py',
            './social_media_api/settings.py',
            './social_media_api/social_media_api/settings.py',
        ]
        
        for path in paths_to_check:
            print(f"\n  Testing path: {path}")
            
            # os.path methods
            exists = os.path.exists(path)
            is_file = os.path.isfile(path)
            is_link = os.path.islink(path)
            
            print(f"    os.path.exists(): {exists}")
            print(f"    os.path.isfile(): {is_file}")
            print(f"    os.path.islink(): {is_link}")
            
            # pathlib methods
            p = Path(path)
            print(f"    Path.exists(): {p.exists()}")
            print(f"    Path.is_file(): {p.is_file()}")
            
            if exists:
                print(f"    ✅ FILE FOUND")
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                    print(f"    ✅ File readable ({len(content)} bytes)")
                    
                    # Check for required content
                    has_accounts = "'accounts'" in content or '"accounts"' in content
                    has_auth_model = "AUTH_USER_MODEL" in content
                    
                    print(f"    'accounts' in INSTALLED_APPS: {'✅' if has_accounts else '❌'}")
                    print(f"    AUTH_USER_MODEL present: {'✅' if has_auth_model else '❌'}")
                except Exception as e:
                    print(f"    ❌ Error reading: {e}")
            else:
                print(f"    ❌ FILE NOT FOUND")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        os.chdir(original_dir)

def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║           CHECKER DEBUG - FINDING settings.py                   ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    # Get the base directories
    script_dir = Path(__file__).parent.absolute()
    parent_dir = script_dir.parent
    
    # Check from multiple locations
    check_from_directory(script_dir, "PROJECT ROOT (where manage.py is)")
    check_from_directory(parent_dir, "PARENT DIRECTORY (Alx_DjangoLearnLab)")
    check_from_directory(Path.home(), "USER HOME DIRECTORY")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("\nIf the checker is still failing, please provide:")
    print("1. The exact error message from the checker")
    print("2. The command you're using to run the checker")
    print("3. The directory you're running the checker from")
    print("\nPossible issues:")
    print("- Checker might be running from a different directory")
    print("- Checker might not follow symlinks (use real file copy instead)")
    print("- Checker might have cached results")
    print("- Checker might be running in a container/sandbox")
    print("\nAll checks above should show ✅ for the file to be found properly.")

if __name__ == "__main__":
    main()

