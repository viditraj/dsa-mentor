import { useState } from 'react'
import { teachELI5, teachSocratic } from '../api/client'
import { Baby, HelpCircle, Send, Loader2, Lightbulb, RotateCcw } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function TeachingModesPage({ userId, user }) {
  const [mode, setMode] = useState('eli5')
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  // ELI5
  const [eli5Result, setEli5Result] = useState(null)
  // Socratic
  const [socraticConversation, setSocraticConversation] = useState([])
  const [socraticResult, setSocraticResult] = useState(null)
  const [socraticAnswer, setSocraticAnswer] = useState('')
  const [socraticStarted, setSocraticStarted] = useState(false)

  const handleELI5 = async () => {
    if (!topic.trim()) return
    setLoading(true); setEli5Result(null)
    try { setEli5Result(await teachELI5({ topic })) } catch {}
    setLoading(false)
  }

  const startSocratic = async () => {
    if (!topic.trim()) return
    setLoading(true); setSocraticConversation([]); setSocraticResult(null); setSocraticStarted(true)
    try { setSocraticResult(await teachSocratic({ topic })) } catch {}
    setLoading(false)
  }

  const answerSocratic = async () => {
    if (!socraticAnswer.trim()) return
    const newConv = [...socraticConversation]
    if (socraticResult?.question) newConv.push({ question: socraticResult.question, answer: socraticAnswer })
    setLoading(true); setSocraticAnswer('')
    try {
      const result = await teachSocratic({ topic, current_understanding: socraticAnswer, previous_answers: newConv })
      setSocraticConversation(newConv)
      setSocraticResult(result)
    } catch {}
    setLoading(false)
  }

  const resetSocratic = () => { setSocraticConversation([]); setSocraticResult(null); setSocraticStarted(false); setSocraticAnswer('') }

  return (
    <div className="space-y-6">
      <div><h1 className="text-3xl font-bold gradient-text">Teaching Modes</h1><p className="text-gray-400 mt-1">Choose how you want to learn</p></div>

      {/* Mode Selector */}
      <div className="grid grid-cols-2 gap-4 max-w-xl">
        <button onClick={() => setMode('eli5')} className={`p-5 rounded-xl border transition-all text-left ${mode === 'eli5' ? 'bg-amber-500/10 border-amber-500/30' : 'bg-gray-800/60 border-gray-700 hover:border-gray-600'}`}>
          <Baby className={`w-8 h-8 mb-2 ${mode === 'eli5' ? 'text-amber-400' : 'text-gray-400'}`} />
          <p className="font-semibold">ELI5 Mode</p>
          <p className="text-xs text-gray-400 mt-1">Zero jargon, everyday analogies</p>
        </button>
        <button onClick={() => setMode('socratic')} className={`p-5 rounded-xl border transition-all text-left ${mode === 'socratic' ? 'bg-blue-500/10 border-blue-500/30' : 'bg-gray-800/60 border-gray-700 hover:border-gray-600'}`}>
          <HelpCircle className={`w-8 h-8 mb-2 ${mode === 'socratic' ? 'text-blue-400' : 'text-gray-400'}`} />
          <p className="font-semibold">Socratic Mode</p>
          <p className="text-xs text-gray-400 mt-1">Learn through guided questions</p>
        </button>
      </div>

      {/* Topic Input */}
      <div className="flex gap-3 max-w-xl">
        <input value={topic} onChange={e => setTopic(e.target.value)} onKeyDown={e => e.key === 'Enter' && (mode === 'eli5' ? handleELI5() : startSocratic())} placeholder="Enter a DSA topic (e.g. dynamic programming, binary search, graphs)" className="flex-1 bg-gray-800 rounded-lg px-4 py-3 text-white border border-gray-700" />
        <button onClick={mode === 'eli5' ? handleELI5 : startSocratic} disabled={loading || !topic.trim()} className={`px-6 py-3 rounded-lg font-semibold text-sm disabled:opacity-50 ${mode === 'eli5' ? 'bg-amber-600 hover:bg-amber-500' : 'bg-blue-600 hover:bg-blue-500'}`}>
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : mode === 'eli5' ? 'Explain!' : 'Start!'}
        </button>
      </div>

      {/* ELI5 Results */}
      {mode === 'eli5' && eli5Result && (
        <div className="bg-gray-800/60 rounded-xl p-6 border border-amber-500/30 space-y-5">
          <h2 className="text-xl font-bold text-amber-400">{eli5Result.title}</h2>

          {eli5Result.analogy && (
            <div className="bg-amber-500/10 rounded-lg p-4 border border-amber-500/20">
              <p className="text-xs font-semibold text-amber-400 mb-1">The Analogy</p>
              <p className="text-sm text-gray-200">{eli5Result.analogy}</p>
            </div>
          )}

          {eli5Result.explanation && (
            <div className="prose prose-invert max-w-none text-sm">
              <ReactMarkdown>{eli5Result.explanation}</ReactMarkdown>
            </div>
          )}

          {eli5Result.key_takeaway && (
            <div className="bg-emerald-500/10 rounded-lg p-4 border border-emerald-500/20">
              <p className="text-xs font-semibold text-emerald-400 mb-1">Key Takeaway</p>
              <p className="text-sm text-gray-200 font-medium">{eli5Result.key_takeaway}</p>
            </div>
          )}

          {eli5Result.try_it_yourself && (
            <div className="bg-indigo-500/10 rounded-lg p-4 border border-indigo-500/20">
              <p className="text-xs font-semibold text-indigo-400 mb-1">Try It Yourself</p>
              <p className="text-sm text-gray-200">{eli5Result.try_it_yourself}</p>
            </div>
          )}

          {eli5Result.now_the_grown_up_version && (
            <div className="bg-gray-900/50 rounded-lg p-4">
              <p className="text-xs font-semibold text-gray-400 mb-1">Now the Grown-Up Version</p>
              <p className="text-sm text-gray-300">{eli5Result.now_the_grown_up_version}</p>
            </div>
          )}

          {eli5Result.fun_fact && (
            <p className="text-xs text-purple-400 italic">Fun fact: {eli5Result.fun_fact}</p>
          )}
        </div>
      )}

      {/* Socratic Mode */}
      {mode === 'socratic' && socraticStarted && (
        <div className="bg-gray-800/60 rounded-xl p-6 border border-blue-500/30 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-blue-400">Socratic Dialogue: {topic}</h2>
            <button onClick={resetSocratic} className="text-xs text-gray-400 hover:text-white flex items-center gap-1"><RotateCcw className="w-3 h-3" />Reset</button>
          </div>

          {/* Progress */}
          {socraticResult?.progress_assessment != null && (
            <div className="flex items-center gap-3">
              <div className="h-2 flex-1 bg-gray-700 rounded-full"><div className="h-2 bg-blue-500 rounded-full transition-all" style={{ width: `${socraticResult.progress_assessment}%` }} /></div>
              <span className="text-xs text-gray-400">{socraticResult.progress_assessment}% understanding</span>
            </div>
          )}

          {/* Conversation History */}
          {socraticConversation.map((qa, i) => (
            <div key={i} className="space-y-2">
              <div className="flex gap-3"><Lightbulb className="w-4 h-4 text-blue-400 mt-1 flex-shrink-0" /><p className="text-sm text-gray-200">{qa.question}</p></div>
              <div className="flex gap-3 ml-8"><span className="text-xs text-indigo-400 mt-1">You:</span><p className="text-sm text-gray-400">{qa.answer}</p></div>
            </div>
          ))}

          {/* Current Question */}
          {socraticResult && (
            <div className="space-y-3">
              <div className="flex gap-3 bg-blue-500/10 rounded-lg p-4">
                <Lightbulb className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm text-gray-200 font-medium">{socraticResult.question}</p>
                  {socraticResult.concept_being_explored && <p className="text-xs text-gray-400 mt-1">Exploring: {socraticResult.concept_being_explored}</p>}
                </div>
              </div>
              {socraticResult.encouragement && <p className="text-xs text-emerald-400 italic">{socraticResult.encouragement}</p>}
              <div className="flex gap-2">
                <input value={socraticAnswer} onChange={e => setSocraticAnswer(e.target.value)} onKeyDown={e => e.key === 'Enter' && answerSocratic()} placeholder="Type your answer..." className="flex-1 bg-gray-900 rounded-lg px-4 py-2.5 text-sm text-white border border-gray-700" />
                <button onClick={answerSocratic} disabled={loading || !socraticAnswer.trim()} className="px-4 py-2.5 bg-blue-600 rounded-lg hover:bg-blue-500 disabled:opacity-50"><Send className="w-4 h-4" /></button>
              </div>
              {socraticResult.if_they_struggle && <details className="text-xs"><summary className="text-gray-400 cursor-pointer">Need a hint?</summary><p className="text-amber-400 mt-1 ml-3">{socraticResult.if_they_struggle}</p></details>}
            </div>
          )}

          {loading && <div className="flex items-center gap-2 text-sm text-gray-400"><Loader2 className="w-4 h-4 animate-spin" />Thinking of the next question...</div>}
        </div>
      )}
    </div>
  )
}
