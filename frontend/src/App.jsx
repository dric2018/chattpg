import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [models, setModels]                         = useState([])
  const [selected, setSelected]                     = useState('')
  const [prompt, setPrompt]                         = useState('')
  const [response, setResponse]                     = useState('')
  const [history, setHistory]                       = useState([])
  const [error, setError]                           = useState(null)
  const [loadingModel, setLoadingModel]             = useState(false)
  const [waitingForResponse, setWaitingForResponse] = useState(false)
  const [hfKey, setHfKey]                           = useState(localStorage.getItem("HF_TOKEN") || "")
  const [showKey, setShowKey]                       = useState(false)
  const [showHistory, setShowHistory]               = useState(false)

  const saveKey = () => {
    localStorage.setItem("HF_TOKEN", hfKey)
    alert("API key saved locally.")
  }

  useEffect(() => {
    fetch('/api/models')
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch models")
        return res.json()
      })
      .then(data => {
        if (!Array.isArray(data)) throw new Error("Expected an array of models")
        setModels(data)
      })
      .catch(err => {
        console.error("Error loading models:", err)
        setError("Failed to load models")
        setModels([])
      })
  }, [])

  useEffect(() => {
    const updateStatus = () => {
      if (!navigator.onLine) alert("You are offline. Some features may not work.")
    }
    window.addEventListener('offline', updateStatus)
    return () => window.removeEventListener('offline', updateStatus)
  }, [])  

  const loadModel = () => {
    setLoadingModel(true)
    fetch('/api/load', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: selected })
    })
      .then(res => res.json())
      .then(data => {
        alert(`Model "${data.model}" loaded.`)
      })
      .catch(() => {
        alert("Failed to load model.")
      })
      .finally(() => {
        setLoadingModel(false)
      })
  }

  // const handleDrop = async (e) => {
  //   e.preventDefault()
  //   const file = e.dataTransfer.files[0]
  //   const formData = new FormData()
  //   formData.append("file", file)
  //   await fetch('/api/upload', { method: 'POST', body: formData })
  //   alert(`Uploaded: ${file.name}`)
  // }

const summarizeText = () => {
  setWaitingForResponse(true)
  fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: prompt })
  })
  .then(res => res.json())
  .then(data => {
    setResponse(data.response)
    setHistory(h => [...h, { prompt: prompt, response: data.response }])
  })
  .catch(() => alert("Failed to get a response...try to load the model first."))
  .finally(() => setWaitingForResponse(false))
}

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>Local Chat App</h2>
      

      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={() => setShowHistory(prev => !prev)}>
      {showHistory ? "Hide Chat History" : "Show Chat History"}
    </button>

    {showHistory && (
     <div style={{
          position: 'fixed',
          left: showHistory ? 0 : '-300px',
          top: 0,
          bottom: 0,
          width: 300,
          background: '#f7f7f7',
          padding: 20,
          boxShadow: '2px 0 5px rgba(0,0,0,0.1)',
          transition: 'left 0.3s ease-in-out',
          overflowY: 'auto'
        }}>
        <h4>Chat History</h4>
        <ul>
          {history.map((h, i) => (
            <li key={i} style={{ marginBottom: 8 }}>
              <b>You:</b> {h.prompt}<br />
              <b>AI:</b> {h.response}
            </li>
          ))}
        </ul>
      </div>
    )}


      <select value={selected} onChange={e => setSelected(e.target.value)}>
        <option value="">-- Select model --</option>
        {models.map(model => <option key={model}>{model}</option>)}
      </select>
      <button onClick={loadModel} disabled={!selected || loadingModel}>
      {loadingModel ? "Loading..." : "Load Model"}
    </button>

      {/* <div
        onDrop={handleDrop}
        onDragOver={e => e.preventDefault()}
        style={{ marginTop: 20, padding: 20, border: '2px dashed gray', textAlign: 'center' }}
      >
        Drag and drop a document here to upload
      </div> */}

      <textarea
        placeholder="Paste document text here"
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        rows={6}
        style={{ width: '100%', marginTop: 10 }}
      />
    <button onClick={summarizeText} disabled={waitingForResponse || !prompt}>
      {waitingForResponse ? "Generating..." : "Send"}
    </button>      

    <div style={{
      background: '#f2f2f2',
      padding: '1rem',
      marginTop: '1rem',
      maxHeight: '300px',
      overflowY: 'auto',
      whiteSpace: 'pre-wrap',
      wordBreak: 'break-word',
      borderRadius: '8px'
    }}>
      <strong>Response:</strong>
      <div>{response}</div>
    </div>

      <div style={{ marginTop: 20 }}>
        <button onClick={() => setShowKey(!showKey)}>
          {showKey ? "Hide API Key" : "Enter Hugging Face API Key"}
        </button>
        {showKey && (
          <div style={{ marginTop: 10 }}>
            <input
              type="text"
              value={hfKey}
              onChange={e => setHfKey(e.target.value)}
              placeholder="hf_xxx..."
              style={{ width: "100%" }}
            />
            <button onClick={saveKey} style={{ marginTop: 5 }}>Save Key</button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
