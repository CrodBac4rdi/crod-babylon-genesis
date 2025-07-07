# CROD 2025 - 3-Tier Branch Strategy (SAP-Style)

## 🏗️ Branch Architecture

### 1. **main** (Production)
- **Purpose**: Stable, production-ready code
- **Protection**: Required PR reviews, passing tests
- **Deploy**: Only tested & approved features
- **Tags**: Version releases (v1.0.0, v1.1.0, etc.)

### 2. **quality** (Q-System)
- **Purpose**: Quality assurance & integration testing
- **Merges from**: development
- **Testing**: Full integration tests, performance tests
- **Deploy**: Staging environment in Codespaces

### 3. **development** (Dev)
- **Purpose**: Active development & feature integration
- **Merges from**: Feature branches
- **Testing**: Unit tests, basic integration
- **Deploy**: Dev environment

### 4. **crod-clean-2025** (Test/Experimental)
- **Purpose**: Clean slate testing & experiments
- **Special**: Can be reset anytime for fresh starts

## 🔄 Workflow

```
feature/xyz → development → quality → main
     ↓            ↓           ↓        ↓
   Local      Dev Test    Q-Testing  Production
```

## 📋 Rules

1. **Never commit directly to main**
2. **All features start in feature branches**
3. **PR required for each promotion**
4. **Tests must pass at each level**
5. **Rollback plan for production**

## 🚀 Commands

```bash
# Start new feature
git checkout development
git checkout -b feature/new-feature

# Promote to quality
git checkout quality
git merge development

# Promote to production
git checkout main
git merge quality
git tag -a v1.0.0 -m "Release 1.0.0"
```