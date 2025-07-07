#!/usr/bin/env python3
"""CROD Babylon Genesis Cleanup - Clean up READMEs and SVGs."""

import os
import shutil
from pathlib import Path

def analyze_crod_babylon(base_path):
    """Analyze crod-babylon-genesis directory."""
    base = Path(base_path)
    
    print("🔍 Analyzing CROD Babylon Genesis...")
    
    # Find all README files
    readme_files = list(base.rglob("README.md"))
    print(f"📄 Found {len(readme_files)} README files")
    
    # Find all SVG files
    svg_files = list(base.rglob("*.svg"))
    print(f"🎨 Found {len(svg_files)} SVG files")
    
    # Analyze directory structure
    subdirs = [d for d in base.iterdir() if d.is_dir() and not d.name.startswith('.')]
    print(f"📁 Found {len(subdirs)} main directories")
    
    for subdir in subdirs[:10]:  # Show first 10
        file_count = sum(1 for _ in subdir.rglob('*') if _.is_file())
        size = sum(f.stat().st_size for f in subdir.rglob('*') if f.is_file()) / 1024 / 1024
        print(f"   • {subdir.name}/ ({file_count} files, {size:.1f} MB)")
    
    return readme_files, svg_files, subdirs

def create_clean_readme(base_path):
    """Create a clean, functional README."""
    clean_readme = """# CROD Babylon Genesis

A sophisticated polyglot architecture system with distributed language districts.

## 🏗️ Architecture

CROD Babylon Genesis implements a "Polyglot City" where different programming languages work together:

- **Phoenix/Elixir**: Orchestration and real-time communication
- **Rust**: High-performance pattern recognition  
- **Python**: Machine learning and neural processing
- **Go**: Concurrent memory management
- **JavaScript/TypeScript**: Web interfaces and frontend
- **PostgreSQL**: Data persistence with event sourcing
- **NATS JetStream**: Inter-service messaging

## 🚀 Quick Start

```bash
# Start the orchestrator
./start-crod.sh

# Or use Docker
docker-compose up -d
```

## 📊 Services

- Phoenix Dashboard: http://localhost:4000
- n8n Workflows: http://localhost:5678  
- NATS Monitoring: http://localhost:8222

## 🏙️ Project Structure

```
crod-babylon-genesis/
├── crod-phoenix/          # Elixir orchestrator
├── src/                   # Core source code
├── polyglot/             # Language-specific modules
├── visualization/        # Architecture diagrams
├── projects/             # Sub-projects
├── docs/                 # Documentation
└── docker-compose.yml    # Container orchestration
```

## 🛠️ Development

The system is designed for:
- Distributed neural processing
- Real-time inter-language communication
- Scalable microservice orchestration
- Event-driven architecture

## 📝 Notes

This project implements practical distributed systems without blockchain or quantum buzzwords.
Focus is on real-world performance and maintainability.

---
*CROD Genesis: Practical Polyglot Architecture* 🏗️
"""
    
    with open(Path(base_path) / "README.md", "w") as f:
        f.write(clean_readme)
    print("📝 Created clean README.md")

def cleanup_crod_babylon(base_path):
    """Clean up CROD Babylon Genesis directory."""
    base = Path(base_path)
    
    print("🧹 Starting CROD Babylon Cleanup...")
    
    # Analyze first
    readme_files, svg_files, subdirs = analyze_crod_babylon(base_path)
    
    # Create backup of main README
    main_readme = base / "README.md"
    if main_readme.exists():
        backup_readme = base / "README_backup.md"
        shutil.copy2(main_readme, backup_readme)
        print("💾 Backed up original README.md")
    
    # Remove all README files except the main one
    removed_count = 0
    for readme in readme_files:
        if readme != main_readme:
            try:
                readme.unlink()
                removed_count += 1
                print(f"🗑️ Removed {readme.relative_to(base)}")
            except Exception as e:
                print(f"❌ Could not remove {readme}: {e}")
    
    print(f"✅ Removed {removed_count} duplicate README files")
    
    # Archive SVG files (keep useful ones, remove duplicates)
    svg_archive = base / "archive" / "old_svgs"
    svg_archive.mkdir(parents=True, exist_ok=True)
    
    # Keep only essential SVGs (architecture diagrams)
    essential_svg_patterns = [
        "crod-architecture",
        "polyglot-city-architecture", 
        "architecture-overview",
        "tech-stack-overview"
    ]
    
    kept_svgs = []
    archived_svgs = []
    
    for svg in svg_files:
        svg_name = svg.stem.lower()
        is_essential = any(pattern in svg_name for pattern in essential_svg_patterns)
        
        if is_essential and len([s for s in kept_svgs if s.stem == svg.stem]) == 0:
            # Keep essential SVGs (no duplicates)
            kept_svgs.append(svg)
        else:
            # Archive the rest
            try:
                archive_path = svg_archive / svg.name
                if archive_path.exists():
                    archive_path.unlink()
                shutil.move(str(svg), str(archive_path))
                archived_svgs.append(svg)
                print(f"📦 Archived {svg.relative_to(base)}")
            except Exception as e:
                print(f"❌ Could not archive {svg}: {e}")
    
    print(f"🎨 Kept {len(kept_svgs)} essential SVGs")
    print(f"📦 Archived {len(archived_svgs)} redundant SVGs")
    
    # Create the clean README
    create_clean_readme(base_path)
    
    print("\n✅ CROD BABYLON CLEANUP COMPLETE!")
    print(f"📊 README files removed: {removed_count}")
    print(f"🎨 SVG files archived: {len(archived_svgs)}")
    print(f"📝 Clean README created")
    print(f"💾 Original README backed up as README_backup.md")
    
    # Show final structure
    print(f"\n🎯 MAIN DIRECTORIES:")
    for item in sorted(base.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            file_count = sum(1 for _ in item.rglob('*') if _.is_file())
            print(f"   📁 {item.name}/ ({file_count} files)")

if __name__ == "__main__":
    base_path = "/home/daniel/Schreibtisch/crod-babylon-genesis"
    
    print("🚨 CROD BABYLON CLEANUP SCRIPT")
    print("This will:")
    print("- Remove duplicate README files")
    print("- Archive redundant SVG files") 
    print("- Create one clean, functional README")
    print("- Keep only essential architecture diagrams")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    cleanup_crod_babylon(base_path)
