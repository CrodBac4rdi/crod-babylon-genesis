"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.CRODNeuralNetwork = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class CRODNeuralNetwork {
    layers = [];
    patterns = [];
    parameters = 88; // Starting with 88 parameters as requested
    learningRate = 0.01;
    storagePath;
    memoryPath;
    growthThreshold = 0.85;
    currentActivations = new Map();
    constructor(context) {
        this.storagePath = context.globalStorageUri.fsPath;
        this.memoryPath = path.join(this.storagePath, 'crod-memory');
        this.initializeNetwork();
        this.loadMemory();
    }
    initializeNetwork() {
        // Initialize with 88 parameters distributed across layers
        // Input layer: 20 neurons
        // Hidden layer: 40 neurons  
        // Output layer: 20 neurons
        // Connections: 8 initial connections
        const inputLayer = {
            type: 'input',
            neurons: this.createNeurons(20)
        };
        const hiddenLayer = {
            type: 'hidden',
            neurons: this.createNeurons(40)
        };
        const outputLayer = {
            type: 'output',
            neurons: this.createNeurons(20)
        };
        // Create initial connections (8 connections to start)
        this.createConnections(inputLayer, hiddenLayer, 4);
        this.createConnections(hiddenLayer, outputLayer, 4);
        this.layers = [inputLayer, hiddenLayer, outputLayer];
        console.log(`CROD Neural Network initialized with ${this.parameters} parameters`);
    }
    createNeurons(count) {
        const neurons = [];
        for (let i = 0; i < count; i++) {
            neurons.push({
                id: Math.random() * 1000000,
                weights: [Math.random() * 2 - 1],
                bias: Math.random() * 2 - 1,
                activation: 0,
                connections: []
            });
        }
        return neurons;
    }
    createConnections(fromLayer, toLayer, count) {
        for (let i = 0; i < count; i++) {
            const fromNeuron = fromLayer.neurons[Math.floor(Math.random() * fromLayer.neurons.length)];
            const toNeuron = toLayer.neurons[Math.floor(Math.random() * toLayer.neurons.length)];
            if (!fromNeuron.connections.includes(toNeuron.id)) {
                fromNeuron.connections.push(toNeuron.id);
                toNeuron.weights.push(Math.random() * 2 - 1);
                this.parameters += 1;
            }
        }
    }
    async learnFromConversation(userInput, claudeResponse, context) {
        // Process the conversation and extract patterns
        const pattern = {
            input: this.preprocessText(userInput),
            output: this.preprocessText(claudeResponse),
            confidence: 1.0,
            timestamp: Date.now(),
            context: context
        };
        this.patterns.push(pattern);
        // Forward propagation
        const activations = this.forwardPropagate(pattern.input);
        // Calculate error and backpropagate
        const error = this.calculateError(activations, pattern.output);
        // If error is high, consider growing the network
        if (error > this.growthThreshold) {
            this.growNetwork();
        }
        // Backpropagation
        this.backpropagate(error);
        // Save the updated network
        await this.saveMemory();
        console.log(`CROD learned from conversation. Current parameters: ${this.parameters}`);
    }
    preprocessText(text) {
        // Simple preprocessing - can be enhanced
        return text.toLowerCase().trim().substring(0, 500);
    }
    forwardPropagate(input) {
        const activations = new Map();
        // Convert input to numerical representation
        const inputVector = this.textToVector(input);
        // Set input layer activations
        this.layers[0].neurons.forEach((neuron, idx) => {
            neuron.activation = inputVector[idx] || 0;
            activations.set(neuron.id, neuron.activation);
        });
        // Propagate through hidden and output layers
        for (let l = 1; l < this.layers.length; l++) {
            const prevLayer = this.layers[l - 1];
            const currentLayer = this.layers[l];
            currentLayer.neurons.forEach(neuron => {
                let sum = neuron.bias;
                // Find neurons from previous layer connected to this neuron
                prevLayer.neurons.forEach(prevNeuron => {
                    if (prevNeuron.connections.includes(neuron.id)) {
                        const weightIdx = prevNeuron.connections.indexOf(neuron.id);
                        sum += prevNeuron.activation * neuron.weights[weightIdx];
                    }
                });
                neuron.activation = this.sigmoid(sum);
                activations.set(neuron.id, neuron.activation);
            });
        }
        this.currentActivations = activations;
        return activations;
    }
    textToVector(text) {
        // Simple character frequency based vectorization
        const vector = new Array(20).fill(0);
        const chars = text.split('');
        chars.forEach((char, idx) => {
            const charCode = char.charCodeAt(0);
            const bucketIdx = charCode % 20;
            vector[bucketIdx] += 1 / chars.length;
        });
        return vector;
    }
    sigmoid(x) {
        return 1 / (1 + Math.exp(-x));
    }
    calculateError(activations, expectedOutput) {
        const outputVector = this.textToVector(expectedOutput);
        const outputLayer = this.layers[this.layers.length - 1];
        let totalError = 0;
        outputLayer.neurons.forEach((neuron, idx) => {
            const expected = outputVector[idx] || 0;
            const actual = neuron.activation;
            totalError += Math.pow(expected - actual, 2);
        });
        return totalError / outputLayer.neurons.length;
    }
    backpropagate(error) {
        // Simplified backpropagation
        for (let l = this.layers.length - 1; l > 0; l--) {
            const currentLayer = this.layers[l];
            const prevLayer = this.layers[l - 1];
            currentLayer.neurons.forEach(neuron => {
                // Update bias
                neuron.bias -= this.learningRate * error * neuron.activation;
                // Update weights
                neuron.weights = neuron.weights.map((weight, idx) => {
                    return weight - this.learningRate * error * neuron.activation;
                });
            });
        }
    }
    growNetwork() {
        // Add new neurons or connections when needed
        const hiddenLayer = this.layers[1];
        // Add a new neuron to hidden layer
        const newNeuron = this.createNeurons(1)[0];
        hiddenLayer.neurons.push(newNeuron);
        // Connect to random neurons in adjacent layers
        const inputLayer = this.layers[0];
        const outputLayer = this.layers[2];
        // Connect from input layer
        const randomInput = inputLayer.neurons[Math.floor(Math.random() * inputLayer.neurons.length)];
        randomInput.connections.push(newNeuron.id);
        // Connect to output layer
        const randomOutput = outputLayer.neurons[Math.floor(Math.random() * outputLayer.neurons.length)];
        newNeuron.connections.push(randomOutput.id);
        randomOutput.weights.push(Math.random() * 2 - 1);
        this.parameters += 3; // New neuron + 2 connections
        console.log(`CROD Network grew! New parameters: ${this.parameters}`);
    }
    async getSuggestion(input) {
        // Use the network to generate suggestions
        const activations = this.forwardPropagate(input);
        // Find similar patterns
        const similarPatterns = this.findSimilarPatterns(input);
        if (similarPatterns.length > 0) {
            // Return the output of the most similar pattern
            return similarPatterns[0].output;
        }
        return null;
    }
    findSimilarPatterns(input) {
        const inputVector = this.textToVector(input);
        return this.patterns
            .map(pattern => ({
            pattern,
            similarity: this.cosineSimilarity(inputVector, this.textToVector(pattern.input))
        }))
            .filter(item => item.similarity > 0.7)
            .sort((a, b) => b.similarity - a.similarity)
            .map(item => item.pattern);
    }
    cosineSimilarity(vec1, vec2) {
        let dotProduct = 0;
        let norm1 = 0;
        let norm2 = 0;
        for (let i = 0; i < vec1.length; i++) {
            dotProduct += vec1[i] * vec2[i];
            norm1 += vec1[i] * vec1[i];
            norm2 += vec2[i] * vec2[i];
        }
        return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
    }
    async loadMemory() {
        try {
            // Ensure directory exists
            if (!fs.existsSync(this.memoryPath)) {
                fs.mkdirSync(this.memoryPath, { recursive: true });
            }
            const networkPath = path.join(this.memoryPath, 'network.json');
            const patternsPath = path.join(this.memoryPath, 'patterns.json');
            if (fs.existsSync(networkPath)) {
                const networkData = JSON.parse(fs.readFileSync(networkPath, 'utf8'));
                this.layers = networkData.layers;
                this.parameters = networkData.parameters;
                this.learningRate = networkData.learningRate;
            }
            if (fs.existsSync(patternsPath)) {
                this.patterns = JSON.parse(fs.readFileSync(patternsPath, 'utf8'));
            }
            console.log(`CROD Memory loaded. Parameters: ${this.parameters}, Patterns: ${this.patterns.length}`);
        }
        catch (error) {
            console.error('Failed to load CROD memory:', error);
        }
    }
    async saveMemory() {
        try {
            // Ensure directory exists
            if (!fs.existsSync(this.memoryPath)) {
                fs.mkdirSync(this.memoryPath, { recursive: true });
            }
            const networkPath = path.join(this.memoryPath, 'network.json');
            const patternsPath = path.join(this.memoryPath, 'patterns.json');
            const networkData = {
                layers: this.layers,
                parameters: this.parameters,
                learningRate: this.learningRate,
                timestamp: Date.now()
            };
            fs.writeFileSync(networkPath, JSON.stringify(networkData, null, 2));
            fs.writeFileSync(patternsPath, JSON.stringify(this.patterns, null, 2));
            console.log(`CROD Memory saved. Parameters: ${this.parameters}`);
        }
        catch (error) {
            console.error('Failed to save CROD memory:', error);
        }
    }
    getNetworkStats() {
        return {
            parameters: this.parameters,
            patterns: this.patterns.length,
            layers: this.layers.length
        };
    }
    visualizeNetwork() {
        let viz = 'CROD Neural Network Visualization:\n';
        viz += `Total Parameters: ${this.parameters}\n`;
        viz += `Learning Rate: ${this.learningRate}\n\n`;
        this.layers.forEach((layer, idx) => {
            viz += `Layer ${idx} (${layer.type}): ${layer.neurons.length} neurons\n`;
            if (idx < this.layers.length - 1) {
                let connections = 0;
                layer.neurons.forEach(neuron => {
                    connections += neuron.connections.length;
                });
                viz += `  Connections to next layer: ${connections}\n`;
            }
        });
        return viz;
    }
}
exports.CRODNeuralNetwork = CRODNeuralNetwork;
//# sourceMappingURL=crodNeuralNetwork.js.map