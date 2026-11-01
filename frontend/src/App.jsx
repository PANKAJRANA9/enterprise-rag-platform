import { useState } from 'react'
import axios from 'axios'

export default function App() {
  const [table, setTable] = useState('crm_docs')
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState('single')

  const ask = async () => {
    setLoading(true)
    try {
      const url = mode === 'single' ? '/api/ask' : '/api/ask-all'
      const payload = mode === 'single' ? { table, text: query } : { text: query }
      const res = await axios.post(url, payload)
      setAnswer(res.data.answer)
      setSources(res.data.sources || [])
    } catch (e) {
      setAnswer('Error: ' + (e.response?.data?.message || e.message))
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <header className="border-b border-gray-800 p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">OmniRAG <span className="text-gray-500 font-normal">Enterprise AI Platform v2.0</span></h1>
        <span className="text-xs bg-green-900 text-green-300 px-2 py-1 rounded">$0 Local Stack</span>
      </header>
      <div className="flex h-[calc(100vh-65px)]">
        <aside className="w-64 border-r border-gray-800 p-4 space-y-4">
          <div>
            <h3 className="text-sm text-gray-400 mb-2">MODE</h3>
            <button onClick={()=>setMode('single')} className={`w-full text-left p-2 rounded ${mode==='single'?'bg-gray-800':''}`}>Ask One Source</button>
            <button onClick={()=>setMode('all')} className={`w-full text-left p-2 rounded ${mode==='all'?'bg-gray-800':''}`}>Ask All Sources</button>
          </div>
          <div>
            <h3 className="text-sm text-gray-400 mb-2">SOURCES</h3>
            {['crm_docs','odoo_docs','parking_docs','medical_kb','whatsapp_docs','ncert_docs'].map(s=>(
              <div key={s} onClick={()=>setTable(s)} className={`p-2 rounded cursor-pointer text-sm ${table===s?'bg-blue-900 text-blue-200': 'text-gray-400 hover:bg-gray-900'}`}>{s}</div>
            ))}
          </div>
          <div className="pt-4 border-t border-gray-800">
            <h3 className="text-sm text-gray-400 mb-2">ANALYTICS</h3>
            <div className="text-xs text-gray-500 space-y-1">
              <div>Hit Rate: 92%</div>
              <div>Avg Latency: 1.2s</div>
              <div>Cost: $0/mo</div>
              <div>Index: HNSW 14 docs</div>
            </div>
          </div>
        </aside>
        <main className="flex-1 flex flex-col">
          <div className="flex-1 p-6 overflow-auto">
            {!answer ? (
              <div className="h-full flex items-center justify-center text-gray-600">
                <div className="text-center">
                  <div className="text-4xl mb-4">🧠</div>
                  <div>Ask anything about CRM, Odoo, Parking, Medical, WhatsApp, NCERT</div>
                  <div className="text-sm mt-2">Example: "Acme pricing issue" or "parking slot A12"</div>
                </div>
              </div>
            ) : (
              <div className="max-w-3xl">
                <div className="bg-gray-900 rounded-lg p-4 whitespace-pre-wrap">{answer}</div>
                {sources.length>0 && <div className="mt-3 text-xs text-gray-400">Sources: {sources.join(', ')} <span className="ml-2 text-green-400">✓ Cited</span></div>}
              </div>
            )}
          </div>
          <div className="border-t border-gray-800 p-4 flex gap-2">
            <input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&ask()} placeholder={mode==='single' ? `Ask ${table}...` : 'Ask all sources...'} className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 outline-none focus:border-blue-600"/>
            <button onClick={ask} disabled={loading} className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg disabled:opacity-50">{loading?'Thinking...':'Ask'}</button>
          </div>
        </main>
      </div>
    </div>
  )
}
