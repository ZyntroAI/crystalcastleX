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
