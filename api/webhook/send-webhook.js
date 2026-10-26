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
