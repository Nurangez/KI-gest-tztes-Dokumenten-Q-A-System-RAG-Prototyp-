import { useState } from 'react'

function App() {
  const [frage, setFrage] = useState('')
  const [antwort, setAntwort] = useState('')
  const [loading, setLoading] = useState(false)

  const handleAsk = async () => {
    setLoading(true)
    const response = await fetch('http://localhost:8000/ask/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frage })
    })
    const data = await response.json()
    setAntwort(data.antwort)
    setLoading(false)
  }

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      textAlign: 'center'
    }}>
      <h1>Firmen-Dokumente Q&A</h1>
      <input
        type="text"
        value={frage}
        onChange={(e) => setFrage(e.target.value)}
        placeholder="Stelle deine Frage..."
        style={{ width: "500px", padding: "10px", fontSize: "16px" }}
      />
      <button
        onClick={handleAsk}
        disabled={loading}
        style={{ padding: "10px 20px", fontSize: "16px", marginLeft: "10px" }}
      >
        {loading ? "Suche..." : "Fragen"}
      </button>
      {antwort && (
        <p style={{ whiteSpace: "pre-wrap", maxWidth: "600px", margin: "20px auto", textAlign: "left" }}>
          {antwort}
        </p>
      )}
    </div>
  )
}

export default App