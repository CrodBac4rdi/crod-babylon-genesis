#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime
import json

def analyze_database(db_path):
    """Analyze a single SQLite database"""
    result = {
        'path': db_path,
        'exists': os.path.exists(db_path),
        'size': 0,
        'modified': None,
        'is_valid': False,
        'tables': {},
        'total_rows': 0,
        'error': None
    }
    
    if not result['exists']:
        result['error'] = 'File not found'
        return result
    
    # Get file stats
    stat = os.stat(db_path)
    result['size'] = stat.st_size
    result['size_human'] = format_bytes(stat.st_size)
    result['modified'] = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    if result['size'] == 0:
        result['error'] = 'Empty file'
        return result
    
    # Try to open as SQLite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            result['error'] = 'No tables found'
        else:
            result['is_valid'] = True
            for (table_name,) in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    result['tables'][table_name] = count
                    result['total_rows'] += count
                except Exception as e:
                    result['tables'][table_name] = f"Error: {str(e)}"
        
        conn.close()
    except sqlite3.DatabaseError as e:
        result['error'] = f'Not a valid SQLite database: {str(e)}'
    except Exception as e:
        result['error'] = f'Error: {str(e)}'
    
    return result

def format_bytes(bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024.0
    return f"{bytes:.1f}TB"

# List of databases to analyze
databases = [
    "/home/daniel/Schreibtisch/Crod Programming/crod_3d_database.db",
    "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/advanced/alt2/crod.db",
    "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/advanced/Crod1/crod.db",
    "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_3d_database.db",
    "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_data/crod.db",
    "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_memory.db",
    "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_parasite_data/crod_parasite.db",
    "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_python_city/crod_city.db",
    "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/unified_crod.db"
]

# Analyze all databases
results = []
for db_path in databases:
    print(f"\nAnalyzing: {db_path}")
    result = analyze_database(db_path)
    results.append(result)
    
    # Print summary
    print(f"  Size: {result['size_human']}")
    print(f"  Modified: {result['modified']}")
    if result['is_valid']:
        print(f"  Tables: {len(result['tables'])}")
        print(f"  Total rows: {result['total_rows']}")
        for table, count in result['tables'].items():
            print(f"    - {table}: {count} rows")
    else:
        print(f"  Status: {result['error']}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

# Group by status
valid_dbs = [r for r in results if r['is_valid']]
empty_dbs = [r for r in results if r['error'] == 'Empty file']
invalid_dbs = [r for r in results if r['error'] and r['error'] != 'Empty file']

print(f"\nTotal databases found: {len(results)}")
print(f"Valid databases: {len(valid_dbs)}")
print(f"Empty databases: {len(empty_dbs)}")
print(f"Invalid/Corrupted: {len(invalid_dbs)}")

if valid_dbs:
    print("\n--- VALID DATABASES ---")
    for db in sorted(valid_dbs, key=lambda x: x['total_rows'], reverse=True):
        print(f"\n{db['path']}")
        print(f"  Size: {db['size_human']} | Rows: {db['total_rows']} | Tables: {len(db['tables'])}")
        print(f"  Modified: {db['modified']}")

print("\n--- RECOMMENDATIONS ---")
print("Keep these databases:")
for db in valid_dbs:
    if db['total_rows'] > 0:
        print(f"  ✓ {db['path']} ({db['total_rows']} rows)")

print("\nDelete these empty databases:")
for db in empty_dbs:
    print(f"  ✗ {db['path']}")

print("\nCheck these invalid databases:")
for db in invalid_dbs:
    print(f"  ? {db['path']} - {db['error']}")