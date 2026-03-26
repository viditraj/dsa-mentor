import { useState } from 'react'
import { teachELI5, teachSocratic } from '../api/client'
import { Baby, HelpCircle, Send, Loader2, Lightbulb, RotateCcw, ChevronDown, ChevronUp } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

/**
 * Reusable teaching mode widget — embed anywhere to offer ELI5 / Socratic learning.
 * Props:
 *   topic     – (string) The DSA topic to teach (e.g. "binary search", "Two Sum")
 *   compact   – (bool)   If true, renders as a collapsible card instead of full section
 */
export default function TeachingModeWidget({ topic, compact = false }) {
  const [open, setOpen] = useState(!compact)
  const [mode, setMode] = useState(null) // null | 'eli5' | 'socratic'
  const [loading, setLoading] = useState(false)
  // ELI5
  const [eli5Result, setEli5Result] = useState(null)
  // Socratic
  const [socraticConversation, setSocraticConversation] = useState([])
  const [socraticResult, setSocraticResult] = useState(null)
  const [socraticAnswer, setSocraticAnswer] = useState('')

  const handleELI5 = async () => {
    if (!topic) return
    setMode('eli5'); setLoading(true); setEli5Result(null)
    try { setEli5Result(await teachELI5({ topic })) } catch {}
    setLoading(false)
  }

  const startSocratic = async () => {
    if (!topic) return
    setMode('socratic'); setLoading(true); setSocraticConversation([]); setSocraticResult(null)
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

  const reset = () => { setMode(null); setEli5Result(null); setSocraticConversation([]); setSocraticResult(null); setSocraticAnswer('') }

  if (compact && !open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="w-full glass-card rounded-xl p-3 flex items-center justify-center gap-2 text-sm text-amber-400 hover:text-amber-300 hover:border-amber-500/40 transition-all group"
      >
        <Lightbulb className="w-4 h-4 group-hover:scale-110 transition-transform" />
        Need help understanding? Try ELI5 or Socratic mode
      </button>
    )
  }

  return (
    <div className="glass-card rounded-xl overflow-hidden border border-amber-500/20">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-gray-800 bg-gradient-to-r from-amber-600/10 to-blue-600/10">
        <div className="flex items-center gap-2">
          <Lightbulb className="w-4 h-4 text-amber-400" />
          <span className="text-sm font-medium text-gray-300">Learning Modes</span>
          {topic && <span className="text-[10px] text-gray-500 truncate max-w-[200px]">— {topic}</span>}
        </div>
        <div className="flex items-center gap-1">
          {mode && <button onClick={reset} className="p-1 rounded hover:bg-gray-800 text-gray-500 hover:text-gray-300 text-xs" title="Reset"><RotateCcw className="w-3 h-3" /></button>}
          {compact && <button onClick={() => setOpen(false)} className="p-1 rounded hover:bg-gray-800 text-gray-500 hover:text-gray-300"><ChevronUp className="w-3.5 h-3.5" /></button>}
        </div>
      </div>

      <div className="p-4">
        {/* Mode selection */}
        {!mode && (
          <div className="flex gap-3">
            <button onClick={handleELI5} disabled={loading || !topic} className="flex-1 p-4 rounded-lg border border-gray-700 hover:border-amber-500/40 hover:bg-amber-500/5 transition-all text-left disabled:opacity-40">
              <Baby className="w-6 h-6 text-amber-400 mb-1.5" />
              <p className="text-sm font-semibold">ELI5</p>
              <p className="text-[11px] text-gray-500">Simple analogy-based explanation</p>
            </button>
            <button onClick={startSocratic} disabled={loading || !topic} className="flex-1 p-4 rounded-lg border border-gray-700 hover:border-blue-500/40 hover:bg-blue-500/5 transition-all text-left disabled:opacity-40">
              <HelpCircle className="w-6 h-6 text-blue-400 mb-1.5" />
              <p className="text-sm font-semibold">Socratic</p>
              <p className="text-[11px] text-gray-500">Learn through guided questions</p>
            </button>
          </div>
        )}

        {loading && !eli5Result && !socraticResult && (
          <div className="flex items-center justify-center py-6 gap-2 text-sm text-gray-400">
            <Loader2 className="w-4 h-4 animate-spin" /> Generating...
          </div>
        )}

        {/* ELI5 Results */}
        {mode === 'eli5' && eli5Result && (
          <div className="space-y-3 animate-fade-in">
            {eli5Result.title && <h3 className="text-base font-bold text-amber-400">{eli5Result.title}</h3>}
            {eli5Result.analogy && (
              <div className="bg-amber-500/10 rounded-lg p-3 border border-amber-500/20">
                <p className="text-[11px] font-semibold text-amber-400 mb-0.5">The Analogy</p>
                <p className="text-sm text-gray-200">{eli5Result.analogy}</p>
              </div>
            )}
            {eli5Result.explanation && (
              <div className="prose prose-invert prose-sm max-w-none text-sm">
                <ReactMarkdown>{eli5Result.explanation}</ReactMarkdown>
              </div>
            )}
            {eli5Result.key_takeaway && (
              <div className="bg-emerald-500/10 rounded-lg p-3 border border-emerald-500/20">
                <p className="text-[11px] font-semibold text-emerald-400 mb-0.5">Key Takeaway</p>
                <p className="text-sm text-gray-200">{eli5Result.key_takeaway}</p>
              </div>
            )}
            {eli5Result.now_the_grown_up_version && (
              <details className="text-xs">
                <summary className="text-gray-400 cursor-pointer font-medium">Technical version</summary>
                <p className="text-gray-300 mt-1 ml-3 text-sm">{eli5Result.now_the_grown_up_version}</p>
              </details>
            )}
          </div>
        )}

        {/* Socratic Mode */}
        {mode === 'socratic' && (socraticResult || socraticConversation.length > 0) && (
          <div className="space-y-3 animate-fade-in">
            {/* Progress */}
            {socraticResult?.progress_assessment != null && (
              <div className="flex items-center gap-3">
                <div className="h-1.5 flex-1 bg-gray-700 rounded-full"><div className="h-1.5 bg-blue-500 rounded-full transition-all" style={{ width: `${socraticResult.progress_assessment}%` }} /></div>
                <span className="text-[10px] text-gray-400">{socraticResult.progress_assessment}%</span>
              </div>
            )}
            {/* History */}
            {socraticConversation.map((qa, i) => (
              <div key={i} className="space-y-1">
                <div className="flex gap-2"><Lightbulb className="w-3.5 h-3.5 text-blue-400 mt-0.5 flex-shrink-0" /><p className="text-xs text-gray-200">{qa.question}</p></div>
                <div className="flex gap-2 ml-6"><span className="text-[10px] text-indigo-400">You:</span><p className="text-xs text-gray-400">{qa.answer}</p></div>
              </div>
            ))}
            {/* Current question */}
            {socraticResult && (
              <div className="space-y-2">
                <div className="flex gap-2 bg-blue-500/10 rounded-lg p-3">
                  <Lightbulb className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm text-gray-200 font-medium">{socraticResult.question}</p>
                    {socraticResult.concept_being_explored && <p className="text-[10px] text-gray-400 mt-0.5">Exploring: {socraticResult.concept_being_explored}</p>}
                  </div>
                </div>
                {socraticResult.encouragement && <p className="text-[10px] text-emerald-400 italic">{socraticResult.encouragement}</p>}
                <div className="flex gap-2">
                  <input value={socraticAnswer} onChange={e => setSocraticAnswer(e.target.value)} onKeyDown={e => e.key === 'Enter' && answerSocratic()} placeholder="Your answer..." className="flex-1 bg-gray-900 rounded-lg px-3 py-2 text-sm text-white border border-gray-700" />
                  <button onClick={answerSocratic} disabled={loading || !socraticAnswer.trim()} className="px-3 py-2 bg-blue-600 rounded-lg hover:bg-blue-500 disabled:opacity-50"><Send className="w-3.5 h-3.5" /></button>
                </div>
                {socraticResult.if_they_struggle && <details className="text-[11px]"><summary className="text-gray-400 cursor-pointer">Need a hint?</summary><p className="text-amber-400 mt-1 ml-3">{socraticResult.if_they_struggle}</p></details>}
              </div>
            )}
            {loading && <div className="flex items-center gap-2 text-xs text-gray-400"><Loader2 className="w-3 h-3 animate-spin" />Thinking...</div>}
          </div>
        )}
      </div>
    </div>
  )
}
