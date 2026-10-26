🚀 API & Webhook Examples — Pure JavaScript (Node.js)
 
All examples are ready-to-run, minimal, no fancy frameworks unless noted. Pick what you need!
 
 
 
📦 1. Simple REST API — Node.js Native (No Framework)
 
 api-server.js 
 
javascript  
const http = require('http');

const PORT = 3000;

const server = http.createServer((req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');

  // GET /api/hello
  if (req.method === 'GET' && req.url === '/api/hello') {
    return res.end(JSON.stringify({
      status: 'ok',
      message: 'Hello from API!',
      timestamp: new Date().toISOString()
    }));
  }

  // POST /api/data
  if (req.method === 'POST' && req.url === '/api/data') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      res.end(JSON.stringify({
        success: true,
        received: JSON.parse(body || '{}')
      }));
    });
    return;
  }

  res.statusCode = 404;
  res.end(JSON.stringify({ error: 'Not Found' }));
});

server.listen(PORT, () => {
  console.log(`✅ API running on http://localhost:${PORT}`);
});
 
 
Run:  node api-server.js 
 
 
 
🪝 2. Webhook Receiver — Node.js Native
 
 webhook-server.js 
 
javascript  
const http = require('http');
const crypto = require('crypto');

const PORT = 4000;
// Your secret key from the service provider
const WEBHOOK_SECRET = 'your-secret-key-here';

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');

  if (req.method !== 'POST') {
    res.statusCode = 405;
    return res.end(JSON.stringify({ error: 'Method Not Allowed' }));
  }

  let rawBody = '';
  req.on('data', chunk => rawBody += chunk);
  req.on('end', () => {
    try {
      // 🔐 Verify signature (critical for security!)
      const signature = req.headers['x-webhook-signature'] || '';
      const expectedSignature = crypto
        .createHmac('sha256', WEBHOOK_SECRET)
        .update(rawBody)
        .digest('hex');

      if (signature && signature !== expectedSignature) {
        console.warn('⚠️ Invalid webhook signature');
        res.statusCode = 403;
        return res.end(JSON.stringify({ error: 'Invalid signature' }));
      }

      // ✅ Process webhook
      const payload = JSON.parse(rawBody);
      console.log('📥 Webhook received:', payload);

      // Do your logic here → save to DB, call another API, etc.

      res.end(JSON.stringify({ status: 'received' }));
    } catch (err) {
      console.error('❌ Webhook error:', err.message);
      res.statusCode = 400;
      res.end(JSON.stringify({ error: 'Invalid payload' }));
    }
  });
});

server.listen(PORT, () => {
  console.log(`✅ Webhook listening on http://localhost:${PORT}/webhook`);
  console.log(`🔐 Use secret: ${WEBHOOK_SECRET}`);
});
 
 
Run:  node webhook-server.js 
 
 
 
📤 3. Webhook Sender — Pure JavaScript
 
 send-webhook.js 
 
javascript  
const https = require('https');
const http = require('http');

function sendWebhook(url, payload, secret = '') {
  const parsedUrl = new URL(url);
  const data = JSON.stringify(payload);
  
  const options = {
    hostname: parsedUrl.hostname,
    port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
    path: parsedUrl.pathname,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(data)
    }
  };

  // Sign payload if secret provided
  if (secret) {
    const signature = require('crypto')
      .createHmac('sha256', secret)
      .update(data)
      .digest('hex');
    options.headers['x-webhook-signature'] = signature;
  }

  const client = parsedUrl.protocol === 'https:' ? https : http;
  
  return new Promise((resolve, reject) => {
    const req = client.request(options, (res) => {
      let resData = '';
      res.on('data', c => resData += c);
      res.on('end', () => resolve({ status: res.statusCode, body: resData }));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// Example usage
sendWebhook(
  'http://localhost:4000/webhook',
  {
    event: 'payment.completed',
    amount: 2500,
    currency: 'THB',
    orderId: 'ORD-' + Date.now()
  },
  'your-secret-key-here'
).then(console.log).catch(console.error);
 
 
Run:  node send-webhook.js 
 
 
 
⚡ 4. Express.js Versions (Simpler & Production-Ready)
 
Express API:  api-express.js 
 
javascript  
const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from Express API!' });
});

app.post('/api/data', (req, res) => {
  res.json({ received: req.body, ok: true });
});

app.listen(3000, () => console.log('🚀 API on port 3000'));
 
 
Express Webhook:  webhook-express.js 
 
javascript  
const express = require('express');
const crypto = require('crypto');
const app = express();

// ⚠️ Use raw body for signature verification!
app.use('/webhook', express.raw({ type: 'application/json' }));

const SECRET = 'your-secret-key-here';

app.post('/webhook', (req, res) => {
  const sig = req.headers['x-webhook-signature'];
  const expected = crypto.createHmac('sha256', SECRET).update(req.body).digest('hex');
  
  if (sig && sig !== expected) return res.sendStatus(403);
  
  const payload = JSON.parse(req.body);
  console.log('✅ Event:', payload.event);
  res.sendStatus(200);
});

app.listen(4000, () => console.log('🪝 Webhook on port 4000'));
 
 
 
 
📝 Quick Setup Notes
 
Item Details 
Install Express  npm install express  
Local Testing Use  localhost  + port 
Public Access Use ngrok:  npx ngrok http 4000  → get public URL for webhook 
Security Always verify webhook signatures! Never skip this 
Methods Webhooks = POST only usually 
 
 
 
Want me to tailor these for Telegram, Discord, Stripe, Line, or GitHub webhooks specifically? Just tell me the service! 😊
 
Would you like a ready-to-download ZIP file with all these  .js  files +  package.json ? Tap Fast then Pro ✅