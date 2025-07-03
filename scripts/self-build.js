#!/usr/bin/env node

/**
 * CROD HELPER SELF-BUILD
 * Der Helper baut sich selbst und dann das echte System
 * Mit oder ohne Claude!
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class CRODSelfBuilder {
    constructor() {
        this.mode = process.argv[2] || 'with-claude';  // 'with-claude' or 'standalone'
        this.helperPath = path.dirname(__filename);
        this.targetPath = path.join(this.helperPath, '..', 'CROD-POLYGLOT-CITY');
        
        console.log(`
╔═══════════════════════════════════════════╗
║      CROD HELPER SELF-BUILD v1.0          ║
║   Building myself, then the real CROD     ║
║        Mode: ${this.mode.toUpperCase()}              ║
╚═══════════════════════════════════════════╝
        `);
    }
    
    async buildHelper() {
        console.log('\n🔨 Phase 1: Building Helper Components...\n');
        
        // 1. Ensure all integrations are ready
        const components = [
            'claude-imitation/crod-learning-imitation.js',
            'quantum/crod-quantum-states.js',
            'crod-chat-learner.js',
            'crod-session-manager.js'
        ];
        
        for (const component of components) {
            const componentPath = path.join(this.helperPath, 'integrations', component);
            if (fs.existsSync(componentPath)) {
                console.log(`✅ ${component} ready`);
            } else {
                console.log(`❌ Missing: ${component}`);
            }
        }
        
        // 2. Build helper Docker image
        await this.buildDockerImage('helper', `
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm init -y && npm install
CMD ["node", "self-build.js", "${this.mode}"]
        `);
    }
    
    async buildPolyglotCity() {
        console.log('\n🏗️ Phase 2: Building Polyglot City...\n');
        
        // Create target directory
        if (!fs.existsSync(this.targetPath)) {
            fs.mkdirSync(this.targetPath, { recursive: true });
        }
        
        // Build each district
        const districts = [
            {
                name: 'meta-chain',
                language: 'elixir',
                port: 8000,
                buildCmd: this.mode === 'with-claude' 
                    ? this.buildWithClaude('elixir')
                    : this.buildStandalone('elixir')
            },
            {
                name: 'pattern-district',
                language: 'rust',
                port: 7007,
                buildCmd: this.mode === 'with-claude'
                    ? this.buildWithClaude('rust')
                    : this.buildStandalone('rust')
            },
            {
                name: 'memory-quarter',
                language: 'go',
                port: 7031,
                buildCmd: this.mode === 'with-claude'
                    ? this.buildWithClaude('go')
                    : this.buildStandalone('go')
            },
            {
                name: 'intelligence-hub',
                language: 'python',
                port: 7113,
                buildCmd: this.mode === 'with-claude'
                    ? this.buildWithClaude('python')
                    : this.buildStandalone('python')
            }
        ];
        
        for (const district of districts) {
            console.log(`\n🏢 Building ${district.name} (${district.language})...`);
            await this.buildDistrict(district);
        }
    }
    
    buildWithClaude(language) {
        // Use Claude's knowledge to generate code
        return `
# Claude-assisted build
echo "🤖 Using Claude knowledge for ${language}..."

# Import CROD imitation
node -e "
const CROD = require('${this.helperPath}/integrations/claude-imitation/crod-learning-imitation.js');
const crod = new CROD();

// Generate ${language} code using CROD knowledge
const code = crod.generateDistrictCode('${language}');
console.log(code);
"
        `;
    }
    
    buildStandalone(language) {
        // Build without Claude
        return `
# Standalone build
echo "🔨 Building ${language} standalone..."

# Use pre-built templates
cp -r ${this.helperPath}/templates/${language}/* .
        `;
    }
    
    async buildDistrict(district) {
        const districtPath = path.join(this.targetPath, district.name);
        fs.mkdirSync(districtPath, { recursive: true });
        
        // Generate district code
        const buildScript = path.join(districtPath, 'build.sh');
        fs.writeFileSync(buildScript, district.buildCmd);
        fs.chmodSync(buildScript, '755');
        
        // Create Dockerfile
        const dockerfile = this.generateDockerfile(district);
        fs.writeFileSync(path.join(districtPath, 'Dockerfile'), dockerfile);
        
        // Build Docker image
        await this.buildDockerImage(`crod/${district.name}`, dockerfile, districtPath);
    }
    
    generateDockerfile(district) {
        const dockerfiles = {
            elixir: `
FROM elixir:1.14-alpine
RUN mix local.hex --force && mix local.rebar --force
WORKDIR /app
COPY . .
RUN mix deps.get && mix compile
CMD ["mix", "run", "--no-halt"]
            `,
            rust: `
FROM rust:1.70-alpine
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY . .
RUN cargo build --release
CMD ["./target/release/pattern-district"]
            `,
            go: `
FROM golang:1.20-alpine
WORKDIR /app
COPY . .
RUN go mod init memory-quarter && go build -o memory-quarter
CMD ["./memory-quarter"]
            `,
            python: `
FROM python:3.11-alpine
RUN apk add --no-cache gcc musl-dev
WORKDIR /app
COPY . .
RUN pip install torch numpy scikit-learn
CMD ["python", "intelligence_hub.py"]
            `
        };
        
        return dockerfiles[district.language] || dockerfiles.python;
    }
    
    async buildDockerImage(name, dockerfile, context = '.') {
        console.log(`🐳 Building Docker image: ${name}`);
        
        try {
            // Write temp Dockerfile if needed
            if (typeof dockerfile === 'string' && !fs.existsSync(path.join(context, 'Dockerfile'))) {
                fs.writeFileSync(path.join(context, 'Dockerfile.tmp'), dockerfile);
                execSync(`docker build -t ${name} -f Dockerfile.tmp ${context}`, { stdio: 'inherit' });
                fs.unlinkSync(path.join(context, 'Dockerfile.tmp'));
            } else {
                execSync(`docker build -t ${name} ${context}`, { stdio: 'inherit' });
            }
            
            console.log(`✅ Image built: ${name}`);
        } catch (error) {
            console.log(`⚠️  Could not build ${name}: ${error.message}`);
        }
    }
    
    async deployToK8s() {
        console.log('\n🚀 Phase 3: Deploying to Kubernetes...\n');
        
        const deployments = fs.readdirSync(path.join(this.helperPath, 'pod-configs'))
            .filter(f => f.endsWith('.yaml'));
        
        for (const deployment of deployments) {
            console.log(`📦 Deploying ${deployment}...`);
            try {
                execSync(`kubectl apply -f ${path.join(this.helperPath, 'pod-configs', deployment)}`, 
                    { stdio: 'inherit' });
            } catch (error) {
                console.log(`⚠️  Deployment failed: ${error.message}`);
            }
        }
    }
    
    async selfImprove() {
        console.log('\n🧠 Phase 4: Self-Improvement Loop...\n');
        
        if (this.mode === 'with-claude') {
            // Use CROD learning to improve
            const learner = require(path.join(this.helperPath, 'integrations/crod-chat-learner.js'));
            const crod = new learner();
            
            // Learn from build process
            crod.processMessage('System', 'Build completed successfully');
            crod.crod.saveState();
            
            console.log('✅ CROD learned from build process!');
        } else {
            console.log('📝 Standalone mode - no learning');
        }
    }
    
    async run() {
        console.log('\n🏗️ Starting CROD Self-Build Process...\n');
        
        // Phase 1: Build helper
        await this.buildHelper();
        
        // Phase 2: Build city
        await this.buildPolyglotCity();
        
        // Phase 3: Deploy
        await this.deployToK8s();
        
        // Phase 4: Learn
        await this.selfImprove();
        
        console.log('\n🎉 CROD SELF-BUILD COMPLETE!');
        console.log(`   Mode: ${this.mode}`);
        console.log('   Next: kubectl get pods -n crod-polyglot');
    }
}

// Run if called directly
if (require.main === module) {
    const builder = new CRODSelfBuilder();
    builder.run().catch(console.error);
}

module.exports = CRODSelfBuilder;