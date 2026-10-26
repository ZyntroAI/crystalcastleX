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
