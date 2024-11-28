import express from 'express'
import { json } from 'body-parser'

const app = express()
const port = 3000 // Your local server will run on http://localhost:3000

app.use(json())

// Handle POST requests to /api/drones
app.post('/api/drones', (req, res) => {
  console.log('Received data:', req.body)
  res.status(200).send({ message: 'Data received successfully!' })
})

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`)
})
