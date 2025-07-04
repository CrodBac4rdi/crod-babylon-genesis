#!/usr/bin/env python3
"""
CROD File Location Checker Hook
Checks if Claude is following Daniel's file organization rules
"""

import sys
import json
import os

# Daniel's rules for file locations
FILE_RULES = {
    # Documentation goes to database
    "docs": {
        "forbidden_extensions": [".md", ".txt"],
        "forbidden_locations": ["/", "/CROD-Helper-Member-7/"],
        "allowed_location": "ULTIMATE-MEGA-DATABASE",
        "message": "📝 DOCS gehören als atoms in ULTIMATE-MEGA-DATABASE!"
    },
    
    # Research MDs only in research folder
    "research": {
        "allowed_extensions": [".md"],
        "allowed_location": "/CROD-2025-RESEARCH/",
        "message": "🔬 Research MDs nur in CROD-2025-RESEARCH!"
    },
    
    # Code only in Helper
    "code": {
        "allowed_extensions": [".js", ".py", ".rs", ".go", ".ex", ".sh"],
        "allowed_location": "/CROD-Helper-Member-7/",
        "forbidden_locations": ["/alt/", "/CROD-2025-RESEARCH/"],
        "message": "💻 Code NUR in CROD-Helper-Member-7!"
    },
    
    # Database builders forbidden
    "builders": {
        "forbidden_patterns": ["build_", "_database", "_key_"],
        "message": "🚫 Keine neuen database builders! Nutze ULTIMATE-MEGA-DATABASE!"
    }
}

def check_file_location(filepath):
    """Check if file is in correct location according to Daniel's rules"""
    
    filename = os.path.basename(filepath)
    extension = os.path.splitext(filename)[1].lower()
    
    violations = []
    
    # Check for database builders
    for pattern in FILE_RULES["builders"]["forbidden_patterns"]:
        if pattern in filename.lower():
            violations.append(FILE_RULES["builders"]["message"])
    
    # Check documentation files
    if extension in FILE_RULES["docs"]["forbidden_extensions"]:
        for forbidden in FILE_RULES["docs"]["forbidden_locations"]:
            if forbidden in filepath:
                violations.append(FILE_RULES["docs"]["message"])
    
    # Check code files
    if extension in FILE_RULES["code"]["allowed_extensions"]:
        if FILE_RULES["code"]["allowed_location"] not in filepath:
            violations.append(FILE_RULES["code"]["message"])
    
    # Check research files
    if extension == ".md" and "research" in filepath.lower():
        if FILE_RULES["research"]["allowed_location"] not in filepath:
            violations.append(FILE_RULES["research"]["message"])
    
    return violations

def main():
    """Hook entry point"""
    # Read the command from stdin
    try:
        data = json.loads(sys.stdin.read())
        tool = data.get("tool", "")
        params = data.get("params", {})
        
        # Check Write and MultiEdit tools
        if tool in ["Write", "MultiEdit"]:
            filepath = params.get("file_path", "")
            
            violations = check_file_location(filepath)
            
            if violations:
                print(f"⚠️ DANIEL'S FILE RULES VIOLATION!")
                for v in violations:
                    print(f"   {v}")
                print(f"   📍 Attempted: {filepath}")
                print(f"   🎯 Instructions: Check CLAUDE.md!")
                # Don't block, just warn
            else:
                print(f"✅ File location OK: {filepath}")
        
    except Exception as e:
        # Don't break Claude, just log
        print(f"Hook error (non-blocking): {e}")
    
    # Always exit 0 to not block
    sys.exit(0)

if __name__ == "__main__":
    main()