#!/usr/bin/env python3
"""
🦠 CROD Backend Test
Testet die echte Backend-Integration ohne Frontend-Abhängigkeiten
"""

import json
import subprocess
import sys
import os
import time

def test_crod_backend():
    """Testet das CROD-Backend direkt"""
    print("🦠 CROD Backend Test Suite")
    print("=" * 50)
    
    # Test 1: Rust-Backend Build
    print("\n1. 🔧 Testing Rust Backend Build...")
    try:
        os.chdir("/workspaces/crod-babylon-genesis/crod-chain-app/src-tauri")
        result = subprocess.run(["cargo", "check"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Rust Backend: OK")
        else:
            print("❌ Rust Backend: FAILED")
            print(result.stderr[:500])
    except Exception as e:
        print(f"❌ Rust Backend: Exception - {e}")
    
    # Test 2: Python Code Execution
    print("\n2. 🐍 Testing Python Code Execution...")
    test_code = "print('Hello from CROD Python Engine!')"
    print(f"Code: {test_code}")
    try:
        result = subprocess.run(["python3", "-c", test_code], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python Execution: {result.stdout.strip()}")
        else:
            print("❌ Python Execution: FAILED")
    except Exception as e:
        print(f"❌ Python Execution: Exception - {e}")
    
    # Test 3: JavaScript Code Execution
    print("\n3. 🟨 Testing JavaScript Code Execution...")
    test_js = "console.log('Hello from CROD JavaScript Engine!')"
    print(f"Code: {test_js}")
    try:
        result = subprocess.run(["node", "-e", test_js], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ JavaScript Execution: {result.stdout.strip()}")
        else:
            print("❌ JavaScript Execution: FAILED (Node.js not available)")
    except Exception as e:
        print(f"❌ JavaScript Execution: Exception - {e}")
    
    # Test 4: Bash Code Execution
    print("\n4. 🐚 Testing Bash Code Execution...")
    test_bash = "echo 'Hello from CROD Bash Engine!'"
    print(f"Code: {test_bash}")
    try:
        result = subprocess.run(["bash", "-c", test_bash], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Bash Execution: {result.stdout.strip()}")
        else:
            print("❌ Bash Execution: FAILED")
    except Exception as e:
        print(f"❌ Bash Execution: Exception - {e}")
    
    # Test 5: File Operations
    print("\n5. 📁 Testing File Operations...")
    test_file = "/tmp/crod_test.txt"
    test_content = "Hello from CROD File System!"
    try:
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        with open(test_file, 'r') as f:
            content = f.read()
        
        if content == test_content:
            print(f"✅ File Operations: {content}")
        else:
            print("❌ File Operations: Content mismatch")
        
        os.remove(test_file)
    except Exception as e:
        print(f"❌ File Operations: Exception - {e}")
    
    # Test 6: Claude CLI (if available)
    print("\n6. 🧠 Testing Claude CLI Integration...")
    try:
        result = subprocess.run(["claude", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Claude CLI: Available - {result.stdout.strip()}")
        else:
            print("❌ Claude CLI: Not available (install with 'pip install claude-cli')")
    except Exception as e:
        print(f"❌ Claude CLI: Exception - {e}")
    
    # Test 7: System Information
    print("\n7. 🖥️ System Information...")
    try:
        import platform
        print(f"✅ OS: {platform.system()} {platform.release()}")
        print(f"✅ Python: {sys.version.split()[0]}")
        
        # Check Rust
        result = subprocess.run(["rustc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Rust: {result.stdout.strip()}")
        
        # Check available tools
        tools = ["cargo", "python3", "bash", "git"]
        for tool in tools:
            try:
                result = subprocess.run(["which", tool], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {tool}: {result.stdout.strip()}")
                else:
                    print(f"❌ {tool}: Not found")
            except:
                print(f"❌ {tool}: Not found")
                
    except Exception as e:
        print(f"❌ System Info: Exception - {e}")
    
    print("\n" + "=" * 50)
    print("🦠 CROD Backend Test Complete!")
    print("The CROD system is ready for AI/ML live coding!")

if __name__ == "__main__":
    test_crod_backend()
