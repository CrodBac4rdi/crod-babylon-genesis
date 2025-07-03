const express = require('express');
const crypto = require('crypto');
const axios = require('axios');

const app = express();
app.use(express.json());

// GitHub Webhook Secret
const WEBHOOK_SECRET = process.env.GITHUB_WEBHOOK_SECRET || 'crod-secret';
const BLOCKCHAIN_URL = process.env.BLOCKCHAIN_URL || 'http://blockchain-core:8085';

// Verify GitHub signature
function verifySignature(payload, signature) {
    const hmac = crypto.createHmac('sha256', WEBHOOK_SECRET);
    const digest = 'sha256=' + hmac.update(payload).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
}

// Handle GitHub events
app.post('/webhook', async (req, res) => {
    const signature = req.headers['x-hub-signature-256'];
    
    if (!verifySignature(JSON.stringify(req.body), signature)) {
        return res.status(401).send('Invalid signature');
    }
    
    const event = req.headers['x-github-event'];
    const payload = req.body;
    
    console.log(`Received ${event} event`);
    
    // Handle different events
    switch(event) {
        case 'push':
            await handlePush(payload);
            break;
        case 'workflow_run':
            await handleWorkflowRun(payload);
            break;
        case 'deployment':
            await handleDeployment(payload);
            break;
    }
    
    res.status(200).send('OK');
});

async function handlePush(payload) {
    const blockData = {
        district: "github-webhook",
        pattern: "code-push",
        atoms: [
            payload.repository.name,
            payload.ref,
            payload.head_commit.id
        ],
        metadata: {
            type: "git_push",
            repo: payload.repository.full_name,
            branch: payload.ref,
            commit: payload.head_commit.id,
            message: payload.head_commit.message,
            author: payload.head_commit.author.name,
            timestamp: payload.head_commit.timestamp,
            files_changed: payload.head_commit.modified.length + 
                          payload.head_commit.added.length + 
                          payload.head_commit.removed.length
        }
    };
    
    // Send to blockchain
    try {
        await axios.post(`${BLOCKCHAIN_URL}/block`, blockData);
        console.log('Push event recorded in blockchain');
    } catch (error) {
        console.error('Failed to record in blockchain:', error.message);
    }
}

async function handleWorkflowRun(payload) {
    if (payload.workflow_run.status !== 'completed') return;
    
    const blockData = {
        district: "github-webhook",
        pattern: "build-result",
        atoms: [
            payload.workflow_run.name,
            payload.workflow_run.conclusion,
            payload.workflow_run.head_sha
        ],
        metadata: {
            type: "workflow_run",
            workflow: payload.workflow_run.name,
            conclusion: payload.workflow_run.conclusion,
            commit: payload.workflow_run.head_sha,
            duration: payload.workflow_run.run_duration_ms,
            started_at: payload.workflow_run.run_started_at,
            completed_at: payload.workflow_run.updated_at
        }
    };
    
    // Send to blockchain
    try {
        await axios.post(`${BLOCKCHAIN_URL}/block`, blockData);
        console.log('Workflow run recorded in blockchain');
    } catch (error) {
        console.error('Failed to record in blockchain:', error.message);
    }
}

async function handleDeployment(payload) {
    const blockData = {
        district: "github-webhook",
        pattern: "deployment",
        atoms: [
            payload.deployment.environment,
            payload.deployment.ref,
            payload.deployment.task
        ],
        metadata: {
            type: "deployment",
            environment: payload.deployment.environment,
            ref: payload.deployment.ref,
            task: payload.deployment.task,
            description: payload.deployment.description,
            created_at: payload.deployment.created_at
        }
    };
    
    // Send to blockchain
    try {
        await axios.post(`${BLOCKCHAIN_URL}/block`, blockData);
        console.log('Deployment recorded in blockchain');
    } catch (error) {
        console.error('Failed to record in blockchain:', error.message);
    }
}

const PORT = process.env.PORT || 8086;
app.listen(PORT, () => {
    console.log(`GitHub Webhook listener running on port ${PORT}`);
    console.log(`Will send blocks to: ${BLOCKCHAIN_URL}`);
});