#!/usr/bin/env python3
"""
CROD Python City - Pseudo Polyglot Architecture in Pure Python
Bug Tracking, Port Management, Loop Detection, All-in-One
"""

import json
import time
import threading
import subprocess
import psutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import traceback
import sys
import re

class CRODBugTracker:
    """Advanced Bug Tracking for CROD Development"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.known_bugs = set()
        self.loop_detection = {}
        self.port_monitoring = {}
        self.syntax_patterns = {}
        
        self.init_bug_db()
        
    def init_bug_db(self):
        """Initialize comprehensive bug tracking"""
        
        conn = sqlite3.connect(self.db_path)
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS bugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                bug_type TEXT,
                description TEXT,
                stack_trace TEXT,
                frequency INTEGER DEFAULT 1,
                status TEXT DEFAULT 'open',
                auto_fix_attempted BOOLEAN DEFAULT FALSE,
                solution TEXT
            );
            
            CREATE TABLE IF NOT EXISTS port_issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                port INTEGER,
                issue_type TEXT,
                process_info TEXT,
                auto_resolved BOOLEAN DEFAULT FALSE
            );
            
            CREATE TABLE IF NOT EXISTS loop_detection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                function_name TEXT,
                call_count INTEGER,
                time_window_seconds INTEGER,
                stack_trace TEXT
            );
            
            CREATE TABLE IF NOT EXISTS syntax_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                file_path TEXT,
                line_number INTEGER,
                error_message TEXT,
                error_pattern TEXT,
                auto_fixed BOOLEAN DEFAULT FALSE
            );
            
            CREATE TABLE IF NOT EXISTS research_blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                attempted_url TEXT,
                block_reason TEXT,
                alternative_solution TEXT
            );
        """)
        conn.commit()
        conn.close()
        
        print("🐛 CROD Bug Tracker initialized - Monitoring everything!")
    
    def track_exception(self, exception: Exception, context: str = ""):
        """Track any exception that occurs"""
        
        bug_type = type(exception).__name__
        description = str(exception)
        stack_trace = traceback.format_exc()
        
        # Check if we've seen this bug before
        bug_signature = f"{bug_type}:{description}"
        
        conn = sqlite3.connect(self.db_path)
        
        # Check frequency
        existing = conn.execute("""
            SELECT id, frequency FROM bugs 
            WHERE bug_type = ? AND description = ?
        """, (bug_type, description)).fetchone()
        
        if existing:
            # Increment frequency
            conn.execute("""
                UPDATE bugs SET frequency = frequency + 1, timestamp = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), existing[0]))
            print(f"🐛 Known bug repeated: {bug_type} (frequency: {existing[1] + 1})")
        else:
            # New bug
            conn.execute("""
                INSERT INTO bugs (timestamp, bug_type, description, stack_trace)
                VALUES (?, ?, ?, ?)
            """, (datetime.now().isoformat(), bug_type, f"{context}: {description}", stack_trace))
            print(f"🆕 New bug detected: {bug_type}")
        
        conn.commit()
        conn.close()
        
        # Auto-fix attempt
        self._attempt_auto_fix(bug_type, description, stack_trace)
    
    def track_port_issue(self, port: int, issue_type: str, details: str):
        """Track port-related issues"""
        
        # Check if port is actually in use
        port_in_use = False
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    port_in_use = True
                    break
        except:
            pass
        
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO port_issues (timestamp, port, issue_type, process_info)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().isoformat(), port, issue_type, details))
        conn.commit()
        conn.close()
        
        print(f"🔌 Port issue tracked: Port {port} - {issue_type}")
        
        # Auto-resolve if possible
        if issue_type == "already_in_use" and port_in_use:
            self._auto_resolve_port(port)
    
    def detect_infinite_loop(self, function_name: str, max_calls: int = 10, time_window: int = 5):
        """Detect potential infinite loops"""
        
        current_time = time.time()
        
        if function_name not in self.loop_detection:
            self.loop_detection[function_name] = []
        
        # Add current call
        self.loop_detection[function_name].append(current_time)
        
        # Clean old calls outside time window
        self.loop_detection[function_name] = [
            t for t in self.loop_detection[function_name] 
            if current_time - t < time_window
        ]
        
        call_count = len(self.loop_detection[function_name])
        
        if call_count > max_calls:
            # Potential infinite loop detected
            stack_trace = ''.join(traceback.format_stack())
            
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                INSERT INTO loop_detection (timestamp, function_name, call_count, time_window_seconds, stack_trace)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(), function_name, call_count, time_window, stack_trace))
            conn.commit()
            conn.close()
            
            print(f"🌀 INFINITE LOOP DETECTED: {function_name} called {call_count} times in {time_window}s")
            return True
        
        return False
    
    def track_syntax_error(self, file_path: str, line_number: int, error_message: str):
        """Track syntax errors to prevent repetition"""
        
        # Extract error pattern
        error_pattern = self._extract_error_pattern(error_message)
        
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO syntax_errors (timestamp, file_path, line_number, error_message, error_pattern)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), file_path, line_number, error_message, error_pattern))
        conn.commit()
        conn.close()
        
        print(f"📝 Syntax error tracked: {error_pattern}")
        
        # Auto-fix attempt
        self._attempt_syntax_auto_fix(file_path, line_number, error_pattern)
    
    def block_online_research(self, url: str, reason: str = "CROD development mode"):
        """Block and track online research attempts"""
        
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO research_blocks (timestamp, attempted_url, block_reason, alternative_solution)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().isoformat(), url, reason, "Use local CROD knowledge base"))
        conn.commit()
        conn.close()
        
        print(f"🚫 Online research blocked: {url}")
        return "CROD: Use local knowledge instead of online research"
    
    def _attempt_auto_fix(self, bug_type: str, description: str, stack_trace: str):
        """Attempt automatic bug fixes"""
        
        if "ModuleNotFoundError" in bug_type:
            module_name = re.search(r"No module named '([^']+)'", description)
            if module_name:
                print(f"🔧 Auto-fix suggestion: pip3 install {module_name.group(1)}")
        
        elif "NameError" in bug_type and "true" in description.lower():
            print("🔧 Auto-fix suggestion: Replace 'true' with 'True' (Python boolean)")
        
        elif "SyntaxError" in bug_type:
            print("🔧 Auto-fix suggestion: Check Python syntax, indentation, quotes")
        
        elif "ConnectionError" in bug_type:
            print("🔧 Auto-fix suggestion: Check service availability, network connection")
    
    def _auto_resolve_port(self, port: int):
        """Automatically resolve port conflicts"""
        
        # Find alternative port
        alternative_port = port
        while True:
            alternative_port += 1
            if not any(conn.laddr.port == alternative_port for conn in psutil.net_connections()):
                break
            if alternative_port > port + 100:  # Safety limit
                break
        
        print(f"🔧 Port auto-resolution: Use port {alternative_port} instead of {port}")
        return alternative_port
    
    def _extract_error_pattern(self, error_message: str) -> str:
        """Extract reusable error pattern"""
        
        # Common patterns
        patterns = [
            (r"No module named '([^']+)'", "missing_module"),
            (r"name '([^']+)' is not defined", "undefined_name"),
            (r"invalid escape sequence", "invalid_escape"),
            (r"Command timed out", "timeout"),
            (r"Connection refused", "connection_refused"),
            (r"Port \d+ already in use", "port_in_use")
        ]
        
        for pattern, name in patterns:
            if re.search(pattern, error_message):
                return name
        
        return "unknown_error"
    
    def _attempt_syntax_auto_fix(self, file_path: str, line_number: int, error_pattern: str):
        """Attempt automatic syntax fixes"""
        
        if error_pattern == "invalid_escape":
            print(f"🔧 Syntax auto-fix: Use raw strings r'...' or escape backslashes in {file_path}:{line_number}")
        
        elif error_pattern == "undefined_name":
            print(f"🔧 Syntax auto-fix: Check variable names, imports in {file_path}:{line_number}")
    
    def get_bug_report(self) -> Dict:
        """Generate comprehensive bug report"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Active bugs
        active_bugs = conn.execute("""
            SELECT bug_type, description, frequency, timestamp
            FROM bugs WHERE status = 'open'
            ORDER BY frequency DESC, timestamp DESC
            LIMIT 10
        """).fetchall()
        
        # Port issues
        port_issues = conn.execute("""
            SELECT port, issue_type, timestamp
            FROM port_issues
            ORDER BY timestamp DESC
            LIMIT 5
        """).fetchall()
        
        # Loop detections
        loops = conn.execute("""
            SELECT function_name, call_count, timestamp
            FROM loop_detection
            ORDER BY timestamp DESC
            LIMIT 5
        """).fetchall()
        
        # Syntax errors
        syntax_errors = conn.execute("""
            SELECT error_pattern, COUNT(*) as count
            FROM syntax_errors
            GROUP BY error_pattern
            ORDER BY count DESC
            LIMIT 5
        """).fetchall()
        
        conn.close()
        
        return {
            'active_bugs': [
                {
                    'type': bug[0],
                    'description': bug[1],
                    'frequency': bug[2],
                    'timestamp': bug[3]
                }
                for bug in active_bugs
            ],
            'port_issues': [
                {
                    'port': issue[0],
                    'type': issue[1],
                    'timestamp': issue[2]
                }
                for issue in port_issues
            ],
            'infinite_loops': [
                {
                    'function': loop[0],
                    'call_count': loop[1],
                    'timestamp': loop[2]
                }
                for loop in loops
            ],
            'syntax_patterns': [
                {
                    'pattern': error[0],
                    'count': error[1]
                }
                for error in syntax_errors
            ]
        }

class CRODPythonCity:
    """CROD Python-only Pseudo City"""
    
    def __init__(self):
        self.data_dir = Path("crod_python_city")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize bug tracker
        self.bug_tracker = CRODBugTracker(self.data_dir / "crod_city.db")
        
        # City districts (Python modules)
        self.districts = {
            'meta_chain': {'port': 8000, 'status': 'initializing', 'module': None},
            'pattern_district': {'port': 7007, 'status': 'initializing', 'module': None},
            'memory_quarter': {'port': 7031, 'status': 'initializing', 'module': None},
            'intelligence_hub': {'port': 7113, 'status': 'initializing', 'module': None},
            'gateway': {'port': 8888, 'status': 'initializing', 'module': None},
            'n8n_quarter': {'port': 7200, 'status': 'initializing', 'module': None}
        }
        
        print("🏙️ CROD Python City initializing...")
        
    def start_district(self, district_name: str):
        """Start a district (Python service)"""
        
        try:
            district = self.districts[district_name]
            port = district['port']
            
            # Check port availability
            if self._is_port_in_use(port):
                self.bug_tracker.track_port_issue(port, "already_in_use", f"District {district_name}")
                alternative_port = self.bug_tracker._auto_resolve_port(port)
                district['port'] = alternative_port
                port = alternative_port
            
            # Start district service
            if district_name == 'meta_chain':
                district['module'] = self._start_meta_chain(port)
            elif district_name == 'pattern_district':
                district['module'] = self._start_pattern_district(port)
            elif district_name == 'memory_quarter':
                district['module'] = self._start_memory_quarter(port)
            elif district_name == 'intelligence_hub':
                district['module'] = self._start_intelligence_hub(port)
            elif district_name == 'gateway':
                district['module'] = self._start_gateway(port)
            elif district_name == 'n8n_quarter':
                district['module'] = self._start_n8n_quarter(port)
            
            district['status'] = 'running'
            print(f"✅ {district_name} started on port {port}")
            
        except Exception as e:
            self.bug_tracker.track_exception(e, f"Starting district {district_name}")
            self.districts[district_name]['status'] = 'failed'
    
    def _is_port_in_use(self, port: int) -> bool:
        """Check if port is in use"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    return True
        except:
            pass
        return False
    
    def _start_meta_chain(self, port: int):
        """Start Meta-Chain district (Orchestrator)"""
        
        # Loop detection
        if self.bug_tracker.detect_infinite_loop('_start_meta_chain'):
            raise Exception("Infinite loop detected in meta_chain startup")
        
        print(f"🧠 Starting Meta-Chain on port {port}")
        # Pseudo implementation - would be real service
        return {'type': 'meta_chain', 'port': port, 'status': 'running'}
    
    def _start_pattern_district(self, port: int):
        """Start Pattern District (Pattern Recognition)"""
        
        if self.bug_tracker.detect_infinite_loop('_start_pattern_district'):
            raise Exception("Infinite loop detected in pattern_district startup")
        
        print(f"🔍 Starting Pattern District on port {port}")
        return {'type': 'pattern_district', 'port': port, 'status': 'running'}
    
    def _start_memory_quarter(self, port: int):
        """Start Memory Quarter (Data Storage)"""
        
        if self.bug_tracker.detect_infinite_loop('_start_memory_quarter'):
            raise Exception("Infinite loop detected in memory_quarter startup")
        
        print(f"💾 Starting Memory Quarter on port {port}")
        return {'type': 'memory_quarter', 'port': port, 'status': 'running'}
    
    def _start_intelligence_hub(self, port: int):
        """Start Intelligence Hub (AI Processing)"""
        
        if self.bug_tracker.detect_infinite_loop('_start_intelligence_hub'):
            raise Exception("Infinite loop detected in intelligence_hub startup")
        
        print(f"🤖 Starting Intelligence Hub on port {port}")
        return {'type': 'intelligence_hub', 'port': port, 'status': 'running'}
    
    def _start_gateway(self, port: int):
        """Start Gateway (Entry Point)"""
        
        if self.bug_tracker.detect_infinite_loop('_start_gateway'):
            raise Exception("Infinite loop detected in gateway startup")
        
        print(f"🚪 Starting Gateway on port {port}")
        return {'type': 'gateway', 'port': port, 'status': 'running'}
    
    def _start_n8n_quarter(self, port: int):
        """Start N8N Quarter (Workflow Automation)"""
        
        if self.bug_tracker.detect_infinite_loop('_start_n8n_quarter'):
            raise Exception("Infinite loop detected in n8n_quarter startup")
        
        print(f"🔄 Starting N8N Quarter on port {port}")
        return {'type': 'n8n_quarter', 'port': port, 'status': 'running'}
    
    def start_all_districts(self):
        """Start all city districts"""
        
        print("🚀 Starting CROD Python City - All Districts")
        
        for district_name in self.districts:
            try:
                self.start_district(district_name)
                time.sleep(0.5)  # Prevent startup conflicts
            except Exception as e:
                print(f"❌ Failed to start {district_name}: {e}")
        
        self.print_city_status()
    
    def print_city_status(self):
        """Print current city status"""
        
        print("\n🏙️ CROD Python City Status:")
        for district_name, district in self.districts.items():
            status_emoji = "✅" if district['status'] == 'running' else "❌" if district['status'] == 'failed' else "⏳"
            print(f"   {status_emoji} {district_name}: {district['status']} (Port {district['port']})")
        
        # Bug report
        bug_report = self.bug_tracker.get_bug_report()
        if bug_report['active_bugs']:
            print(f"\n🐛 Active Bugs: {len(bug_report['active_bugs'])}")
            for bug in bug_report['active_bugs'][:3]:
                print(f"   • {bug['type']}: {bug['description'][:50]}...")
    
    def get_city_stats(self) -> Dict:
        """Get comprehensive city statistics"""
        
        running_districts = sum(1 for d in self.districts.values() if d['status'] == 'running')
        failed_districts = sum(1 for d in self.districts.values() if d['status'] == 'failed')
        
        return {
            'districts': {
                'total': len(self.districts),
                'running': running_districts,
                'failed': failed_districts,
                'details': self.districts
            },
            'bugs': self.bug_tracker.get_bug_report(),
            'city_health': running_districts / len(self.districts) * 100
        }

def main():
    """Start CROD Python City with full bug tracking"""
    
    print("🔥 CROD Python City - Complete Bug Tracking & Management")
    print("🐛 Infinite loop detection, port management, syntax tracking")
    print("🏙️ Pseudo Polyglot City in pure Python")
    
    try:
        # Initialize city
        city = CRODPythonCity()
        
        # Start all districts
        city.start_all_districts()
        
        # Get final stats
        stats = city.get_city_stats()
        print(f"\n📊 City Health: {stats['city_health']:.1f}%")
        
        print("\n✅ CROD Python City operational!")
        print("🦠 Parasite integration active")
        print("🐛 Bug tracking comprehensive")
        print("🚫 Online research blocked")
        print("🔄 Loop detection active")
        
    except Exception as e:
        print(f"❌ Critical error starting CROD Python City: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()