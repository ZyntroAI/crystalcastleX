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
