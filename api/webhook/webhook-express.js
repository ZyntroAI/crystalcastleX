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
