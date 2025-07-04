#!/bin/bash

# Function to analyze a single database
analyze_db() {
    local db_path="$1"
    echo "=== Analyzing: $db_path ==="
    
    # Get file size and last modified date
    if [ -f "$db_path" ]; then
        size=$(ls -lh "$db_path" | awk '{print $5}')
        modified=$(stat -c "%y" "$db_path" | cut -d' ' -f1,2 | cut -d'.' -f1)
        echo "Size: $size"
        echo "Last modified: $modified"
        
        # Check if file is empty
        if [ ! -s "$db_path" ]; then
            echo "Status: EMPTY FILE"
            echo
            return
        fi
        
        # Try to open with sqlite3
        if sqlite3 "$db_path" ".tables" 2>/dev/null | grep -q .; then
            # Get table count and list
            table_count=$(sqlite3 "$db_path" ".tables" 2>/dev/null | wc -w)
            echo "Tables: $table_count"
            
            # List tables and row counts
            sqlite3 "$db_path" ".tables" 2>/dev/null | tr ' ' '\n' | while read table; do
                if [ ! -z "$table" ]; then
                    count=$(sqlite3 "$db_path" "SELECT COUNT(*) FROM $table;" 2>/dev/null || echo "error")
                    echo "  - $table: $count rows"
                fi
            done
            
            # Get total row count across all tables
            total_rows=$(sqlite3 "$db_path" "SELECT SUM(cnt) FROM ($(sqlite3 "$db_path" ".tables" 2>/dev/null | tr ' ' '\n' | grep -v '^$' | awk '{print "SELECT COUNT(*) as cnt FROM " $1 " UNION ALL"}' | sed '$ s/ UNION ALL$//' | grep -v '^$'));" 2>/dev/null || echo "0")
            echo "Total rows: ${total_rows:-0}"
        else
            echo "Status: NOT A VALID SQLITE DATABASE"
        fi
    else
        echo "Status: FILE NOT FOUND"
    fi
    echo
}

# Main script
echo "CROD SQLite Database Analysis"
echo "============================="
echo "Date: $(date)"
echo

# Analyze each database
while IFS= read -r db; do
    analyze_db "$db"
done << EOF
/home/daniel/Schreibtisch/Crod Programming/crod_3d_database.db
/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/advanced/alt2/crod.db
/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/advanced/Crod1/crod.db
/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_3d_database.db
/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_data/crod.db
/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_memory.db
/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_parasite_data/crod_parasite.db
/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/crod_python_city/crod_city.db
/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod/unified_crod.db
EOF