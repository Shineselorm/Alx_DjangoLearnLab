#!/usr/bin/env python3
"""
Verification script to check all ALX Django Social Media API requirements.
This script verifies that all checker requirements are properly implemented.
"""

import os
import sys
from pathlib import Path

def print_result(check_name, passed, details=""):
    """Print a formatted result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {check_name}")
    if details:
        print(f"   {details}")
    print()

def check_file_exists(file_path, description):
    """Check if a file exists."""
    exists = os.path.isfile(file_path)
    print_result(
        description,
        exists,
        f"File: {file_path}" if exists else f"Missing: {file_path}"
    )
    return exists

def check_content_in_file(file_path, search_string, description):
    """Check if a string exists in a file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            found = search_string in content
            print_result(
                description,
                found,
                f"Found '{search_string}' in {file_path}" if found else f"Not found: '{search_string}'"
            )
            return found
    except Exception as e:
        print_result(description, False, f"Error reading file: {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 80)
    print("ALX DJANGO SOCIAL MEDIA API - REQUIREMENT VERIFICATION")
    print("=" * 80)
    print()
    
    # Determine project root
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir
    
    print(f"Project Root: {project_root}")
    print()
    
    all_checks_passed = True
    
    # ========================================================================
    # CHECK 1: Settings.py Configuration
    # ========================================================================
    print("-" * 80)
    print("CHECK 1: Settings.py Configuration")
    print("-" * 80)
    
    settings_path = project_root / "social_media_api" / "settings.py"
    
    check1a = check_file_exists(
        settings_path,
        "Settings.py file exists"
    )
    all_checks_passed &= check1a
    
    if check1a:
        check1b = check_content_in_file(
            settings_path,
            "'accounts'",
            "Accounts app in INSTALLED_APPS"
        )
        all_checks_passed &= check1b
        
        check1c = check_content_in_file(
            settings_path,
            "AUTH_USER_MODEL = 'accounts.CustomUser'",
            "Custom user model configured"
        )
        all_checks_passed &= check1c
        
        check1d = check_content_in_file(
            settings_path,
            "'rest_framework.authtoken'",
            "Token authentication app installed"
        )
        all_checks_passed &= check1d
    
    # ========================================================================
    # CHECK 2: Custom User Model
    # ========================================================================
    print("-" * 80)
    print("CHECK 2: Custom User Model")
    print("-" * 80)
    
    models_path = project_root / "accounts" / "models.py"
    
    check2a = check_file_exists(
        models_path,
        "Models.py file exists"
    )
    all_checks_passed &= check2a
    
    if check2a:
        check2b = check_content_in_file(
            models_path,
            "class CustomUser(AbstractUser):",
            "CustomUser extends AbstractUser"
        )
        all_checks_passed &= check2b
        
        check2c = check_content_in_file(
            models_path,
            "bio = models.TextField(",
            "Bio field exists"
        )
        all_checks_passed &= check2c
        
        check2d = check_content_in_file(
            models_path,
            "profile_picture = models.ImageField(",
            "Profile picture field exists"
        )
        all_checks_passed &= check2d
        
        check2e = check_content_in_file(
            models_path,
            "followers = models.ManyToManyField(",
            "Followers field exists (ManyToMany)"
        )
        all_checks_passed &= check2e
        
        check2f = check_content_in_file(
            models_path,
            "symmetrical=False",
            "Followers field has symmetrical=False"
        )
        all_checks_passed &= check2f
    
    # ========================================================================
    # CHECK 3: Serializers
    # ========================================================================
    print("-" * 80)
    print("CHECK 3: Serializers Implementation")
    print("-" * 80)
    
    serializers_path = project_root / "accounts" / "serializers.py"
    
    check3a = check_file_exists(
        serializers_path,
        "Serializers.py file exists"
    )
    all_checks_passed &= check3a
    
    if check3a:
        check3b = check_content_in_file(
            serializers_path,
            "class UserRegistrationSerializer",
            "Registration serializer exists"
        )
        all_checks_passed &= check3b
        
        check3c = check_content_in_file(
            serializers_path,
            "class UserLoginSerializer",
            "Login serializer exists"
        )
        all_checks_passed &= check3c
        
        check3d = check_content_in_file(
            serializers_path,
            "Token.objects.create",
            "Token creation on registration"
        )
        all_checks_passed &= check3d
        
        check3e = check_content_in_file(
            serializers_path,
            "Token.objects.get_or_create",
            "Token retrieval on login"
        )
        all_checks_passed &= check3e
    
    # ========================================================================
    # CHECK 4: Views
    # ========================================================================
    print("-" * 80)
    print("CHECK 4: Views Implementation")
    print("-" * 80)
    
    views_path = project_root / "accounts" / "views.py"
    
    check4a = check_file_exists(
        views_path,
        "Views.py file exists"
    )
    all_checks_passed &= check4a
    
    if check4a:
        check4b = check_content_in_file(
            views_path,
            "class UserRegistrationView",
            "Registration view exists"
        )
        all_checks_passed &= check4b
        
        check4c = check_content_in_file(
            views_path,
            "class UserLoginView",
            "Login view exists"
        )
        all_checks_passed &= check4c
        
        check4d = check_content_in_file(
            views_path,
            "class UserProfileView",
            "Profile view exists"
        )
        all_checks_passed &= check4d
    
    # ========================================================================
    # CHECK 5: URL Configuration
    # ========================================================================
    print("-" * 80)
    print("CHECK 5: URL Configuration")
    print("-" * 80)
    
    urls_path = project_root / "accounts" / "urls.py"
    
    check5a = check_file_exists(
        urls_path,
        "Accounts urls.py file exists"
    )
    all_checks_passed &= check5a
    
    if check5a:
        check5b = check_content_in_file(
            urls_path,
            "path('register/',",
            "/register route exists"
        )
        all_checks_passed &= check5b
        
        check5c = check_content_in_file(
            urls_path,
            "path('login/',",
            "/login route exists"
        )
        all_checks_passed &= check5c
        
        check5d = check_content_in_file(
            urls_path,
            "path('profile/',",
            "/profile route exists"
        )
        all_checks_passed &= check5d
    
    # Check main project URLs
    main_urls_path = project_root / "social_media_api" / "urls.py"
    
    check5e = check_file_exists(
        main_urls_path,
        "Main urls.py file exists"
    )
    all_checks_passed &= check5e
    
    if check5e:
        check5f = check_content_in_file(
            main_urls_path,
            "include('accounts.urls')",
            "Accounts URLs included in main project"
        )
        all_checks_passed &= check5f
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("All requirements are properly implemented.")
        print("The project meets all ALX Django Social Media API specifications.")
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print()
        print("Please review the failed checks above and fix the issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

