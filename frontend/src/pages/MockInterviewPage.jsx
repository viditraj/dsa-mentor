import { useState, useEffect, useRef } from 'react'
import { startMockInterview, sendInterviewMessage, endMockInterview, getInterviewHistory } from '../api/client'
import { Play, Send, Square, Clock, Trophy, MessageCircle, Code2, ChevronDown, History } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

export default function MockInterviewPage({ userId, user }) {
  const [session, setSession] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [code, setCode] = useState('')
  const [showCode, setShowCode] = useState(false)
  const [loading, setLoading] = useState(false)
  const [scoring, setScoring] = useState(null)
  const [history, setHistory] = useState([])
  const [showHistory, setShowHistory] = useState(false)
  const [elapsed, setElapsed] = useState(0)
  const [config, setConfig] = useState({ difficulty: 'medium', focus_area: '', duration_minutes: 45, company_style: '' })
  const messagesEndRef = useRef(null)
  const timerRef = useRef(null)

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  useEffect(() => {
    if (session && !scoring) {
      timerRef.current = setInterval(() => setElapsed(e => e + 1), 1000)
      return () => clearInterval(timerRef.current)
    }
    return () => clearInterval(timerRef.current)
  }, [session, scoring])

  const loadHistory = async () => {
    try { const data = await getInterviewHistory(userId); setHistory(data.sessions || []); setShowHistory(true) } catch {}
  }

  const handleStart = async () => {
    setLoading(true)
    try {
      const data = await startMockInterview({ user_id: userId, ...config })
      setSession(data)
      setMessages([{ role: 'interviewer', content: data.opening_message }])
      setScoring(null)
      setElapsed(0)
    } catch (e) { alert('Failed to start: ' + e.message) }
    setLoading(false)
  }

  const handleSend = async () => {
    if (!input.trim() && !code.trim()) return
    const userMsg = { role: 'candidate', content: input, code: code || undefined }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const resp = await sendInterviewMessage({ session_id: session.session_id, message: input, code: code || undefined })
      setMessages(prev => [...prev, { role: 'interviewer', content: resp.message, hint: resp.hint, phase: resp.phase }])
      if (code) setCode('')
    } catch (e) { setMessages(prev => [...prev, { role: 'interviewer', content: "Let's continue. Can you elaborate?" }]) }
    setLoading(false)
  }

  const handleEnd = async () => {
    setLoading(true)
    clearInterval(timerRef.current)
    try {
      const result = await endMockInterview(session.session_id)
      setScoring(result)
    } catch (e) { alert('Failed to end: ' + e.message) }
    setLoading(false)
  }

  const formatTime = (s) => `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`

  const ScoreBar = ({ label, score, max = 10 }) => (
    <div className="mb-3">
      <div className="flex justify-between text-sm mb-1"><span className="text-gray-300">{label}</span><span className="font-bold text-white">{score}/{max}</span></div>
      <div className="h-2 bg-gray-700 rounded-full"><div className="h-2 rounded-full transition-all" style={{ width: `${(score/max)*100}%`, backgroundColor: score >= 7 ? '#10b981' : score >= 5 ? '#f59e0b' : '#ef4444' }} /></div>
    </div>
  )

  if (scoring) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold gradient-text">Interview Results</h1>
          <button onClick={() => { setSession(null); setScoring(null); setMessages([]) }} className="px-4 py-2 bg-indigo-600 rounded-lg hover:bg-indigo-500 text-sm">New Interview</button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-800/60 rounded-xl p-6 border border-gray-700">
            <div className="text-center mb-6">
              <div className="text-6xl font-bold gradient-text">{scoring.overall_score}/10</div>
              <p className="text-gray-400 mt-2">Overall Score</p>
              <span className={`inline-block mt-2 px-3 py-1 rounded-full text-xs font-medium ${scoring.hire_recommendation?.includes('no') ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>{scoring.hire_recommendation}</span>
            </div>
            <ScoreBar label="Communication" score={scoring.communication_score} />
            <ScoreBar label="Problem Solving" score={scoring.problem_solving_score} />
            <ScoreBar label="Code Quality" score={scoring.code_quality_score} />
            <ScoreBar label="Time Management" score={scoring.time_management_score} />
          </div>
          <div className="bg-gray-800/60 rounded-xl p-6 border border-gray-700 space-y-4">
            {scoring.strengths?.length > 0 && <div><h3 className="text-green-400 font-semibold mb-2">Strengths</h3>{scoring.strengths.map((s,i) => <p key={i} className="text-sm text-gray-300 ml-4">+ {s}</p>)}</div>}
            {scoring.improvements?.length > 0 && <div><h3 className="text-amber-400 font-semibold mb-2">Areas to Improve</h3>{scoring.improvements.map((s,i) => <p key={i} className="text-sm text-gray-300 ml-4">- {s}</p>)}</div>}
            {scoring.detailed_feedback && <div><h3 className="text-indigo-400 font-semibold mb-2">Detailed Feedback</h3><div className="text-sm text-gray-300 prose prose-invert max-w-none"><ReactMarkdown>{scoring.detailed_feedback}</ReactMarkdown></div></div>}
          </div>
        </div>
      </div>
    )
  }

  if (!session) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div><h1 className="text-3xl font-bold gradient-text">Mock Interview</h1><p className="text-gray-400 mt-1">Practice with an AI interviewer</p></div>
          <button onClick={loadHistory} className="flex items-center gap-2 px-4 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 text-sm text-gray-300"><History className="w-4 h-4" />History</button>
        </div>
        <div className="bg-gray-800/60 rounded-xl p-8 border border-gray-700 max-w-xl mx-auto">
          <h2 className="text-xl font-semibold mb-6">Configure Interview</h2>
          <div className="space-y-4">
            <div><label className="block text-sm text-gray-400 mb-1">Difficulty</label>
              <select value={config.difficulty} onChange={e => setConfig({...config, difficulty: e.target.value})} className="w-full bg-gray-700 rounded-lg px-4 py-2.5 text-white border border-gray-600">
                <option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option><option value="mixed">Mixed</option>
              </select></div>
            <div><label className="block text-sm text-gray-400 mb-1">Focus Area (optional)</label>
              <input value={config.focus_area} onChange={e => setConfig({...config, focus_area: e.target.value})} placeholder="e.g. trees, dp, graphs" className="w-full bg-gray-700 rounded-lg px-4 py-2.5 text-white border border-gray-600" /></div>
            <div><label className="block text-sm text-gray-400 mb-1">Company Style (optional)</label>
              <select value={config.company_style} onChange={e => setConfig({...config, company_style: e.target.value})} className="w-full bg-gray-700 rounded-lg px-4 py-2.5 text-white border border-gray-600">
                <option value="">Generic FAANG</option><option value="google">Google</option><option value="meta">Meta</option><option value="amazon">Amazon</option><option value="apple">Apple</option><option value="microsoft">Microsoft</option>
              </select></div>
            <div><label className="block text-sm text-gray-400 mb-1">Duration (minutes)</label>
              <select value={config.duration_minutes} onChange={e => setConfig({...config, duration_minutes: parseInt(e.target.value)})} className="w-full bg-gray-700 rounded-lg px-4 py-2.5 text-white border border-gray-600">
                <option value={30}>30 min</option><option value={45}>45 min</option><option value={60}>60 min</option>
              </select></div>
            <button onClick={handleStart} disabled={loading} className="w-full py-3 bg-gradient-to-r from-indigo-600 to-emerald-600 rounded-lg font-semibold hover:opacity-90 disabled:opacity-50 flex items-center justify-center gap-2">
              <Play className="w-5 h-5" />{loading ? 'Starting...' : 'Start Interview'}</button>
          </div>
        </div>
        {showHistory && history.length > 0 && (
          <div className="bg-gray-800/60 rounded-xl p-6 border border-gray-700">
            <h3 className="font-semibold mb-4">Past Interviews</h3>
            <div className="space-y-2">{history.map(h => (
              <div key={h.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
                <div><p className="text-sm font-medium">{h.problem_title}</p><p className="text-xs text-gray-400">{h.difficulty} | {h.company_style || 'Generic'}</p></div>
                <div className="text-right">{h.score != null && <span className="text-lg font-bold text-indigo-400">{h.score}/10</span>}<p className="text-xs text-gray-400">{h.status}</p></div>
              </div>
            ))}</div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)]">
      <div className="flex items-center justify-between mb-4">
        <div><h1 className="text-xl font-bold">{session.problem_title}</h1><p className="text-sm text-gray-400">{config.difficulty} | {config.company_style || 'FAANG'}</p></div>
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1 text-sm text-gray-400"><Clock className="w-4 h-4" />{formatTime(elapsed)}</span>
          <button onClick={handleEnd} className="px-4 py-2 bg-red-600/80 rounded-lg hover:bg-red-500 text-sm flex items-center gap-1"><Square className="w-4 h-4" />End Interview</button>
        </div>
      </div>
      {session.problem_description && <div className="bg-gray-800/60 rounded-lg p-4 mb-4 border border-gray-700 text-sm max-h-40 overflow-y-auto"><ReactMarkdown>{session.problem_description}</ReactMarkdown></div>}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'candidate' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-xl px-4 py-3 ${msg.role === 'candidate' ? 'bg-indigo-600/30 border border-indigo-500/30' : 'bg-gray-800/60 border border-gray-700'}`}>
              <p className="text-xs text-gray-400 mb-1">{msg.role === 'candidate' ? 'You' : 'Interviewer'}{msg.phase ? ` (${msg.phase})` : ''}</p>
              <div className="text-sm prose prose-invert max-w-none"><ReactMarkdown>{msg.content}</ReactMarkdown></div>
              {msg.code && <SyntaxHighlighter language="python" style={oneDark} customStyle={{ fontSize: '0.75rem', marginTop: 8, borderRadius: 8 }}>{msg.code}</SyntaxHighlighter>}
              {msg.hint && <p className="text-xs text-amber-400 mt-2 italic">Hint: {msg.hint}</p>}
            </div>
          </div>
        ))}
        {loading && <div className="flex justify-start"><div className="bg-gray-800/60 rounded-xl px-4 py-3 border border-gray-700"><p className="text-sm text-gray-400 animate-pulse">Interviewer is thinking...</p></div></div>}
        <div ref={messagesEndRef} />
      </div>
      <div className="border-t border-gray-800 pt-3">
        {showCode && <textarea value={code} onChange={e => setCode(e.target.value)} placeholder="Paste your code here..." rows={6} className="w-full bg-gray-800 rounded-lg px-4 py-3 text-sm font-mono text-white border border-gray-700 mb-2 resize-none" />}
        <div className="flex gap-2">
          <button onClick={() => setShowCode(!showCode)} className={`p-2.5 rounded-lg border ${showCode ? 'bg-indigo-600/20 border-indigo-500/30 text-indigo-400' : 'bg-gray-800 border-gray-700 text-gray-400'}`}><Code2 className="w-5 h-5" /></button>
          <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSend()} placeholder="Type your response..." className="flex-1 bg-gray-800 rounded-lg px-4 py-2.5 text-white border border-gray-700" />
          <button onClick={handleSend} disabled={loading || (!input.trim() && !code.trim())} className="px-4 py-2.5 bg-indigo-600 rounded-lg hover:bg-indigo-500 disabled:opacity-50"><Send className="w-5 h-5" /></button>
        </div>
      </div>
    </div>
  )
}
