import { useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, BrainCircuit, Activity, FileText } from 'lucide-react'
import Mermaid from './Mermaid'
import './index.css'

function App() {
  const [goal, setGoal] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!goal.trim()) return

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('http://localhost:8000/run', { goal })
      setResult(response.data)
    } catch (err) {
      console.error(err)
      setError(err.message || 'Bir hata oluştu.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card"
        style={{ textAlign: 'center' }}
      >
        <h1 className="title">Project Apex</h1>
        <p className="subtitle">Otonom Çok-Yetenekli Yapay Zeka Ajanı</p>

        <form onSubmit={handleSubmit} className="input-group">
          <input
            type="text"
            className="main-input"
            placeholder="Hedefinizi yazın (örn: Galaxy S26 sızıntılarını araştır)..."
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" className="run-btn" disabled={isLoading}>
            {isLoading ? <div className="spinner"></div> : <Search size={20} />}
          </button>
        </form>
      </motion.div>

      <AnimatePresence>
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="status-indicator"
          >
            <BrainCircuit className="animate-pulse" />
            <span>Ajan düşünüyor ve çalışıyor... Lütfen bekleyin.</span>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card"
            style={{ borderColor: '#ff4b4b' }}
          >
            <h3 style={{ color: '#ff4b4b', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Activity /> Hata Oluştu
            </h3>
            <p>{error}</p>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-card"
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '1rem' }}>
              <FileText color="var(--primary-color)" />
              <h2 style={{ margin: 0 }}>Rapor Sonucu</h2>
            </div>

            <div className="markdown-content">
              <ReactMarkdown
                components={{
                  img: ({ node, ...props }) => {
                    // Fix image paths if they are local relative paths
                    let src = props.src;
                    if (src && !src.startsWith('http')) {
                      // Assuming images are served from root or reports/ folder
                      // We will need to correct this based on backend static serving
                      // For now, if path is "reports/image.png", map to "http://localhost:8000/reports/image.png"
                      src = `http://localhost:8000/${src}`;
                    }
                    return <img {...props} src={src} style={{ maxWidth: '100%' }} />
                  },
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '')
                    if (!inline && match && match[1] === 'mermaid') {
                      return <Mermaid chart={String(children).replace(/\n$/, '')} />
                    }
                    return (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    )
                  }
                }}
              >
                {result.report}
              </ReactMarkdown>
            </div>

            {result.files && result.files.length > 0 && (
              <div style={{ marginTop: '2rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                <strong>Oluşturulan Dosyalar:</strong>
                <ul>
                  {result.files.map((f, i) => (
                    <li key={i}>{f}</li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App
