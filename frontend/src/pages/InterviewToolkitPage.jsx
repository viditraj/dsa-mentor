import { useState } from 'react'
import { getPatternQuiz, getCheatSheet, getWarmup, getCompanyFocus } from '../api/client'
import { Zap, FileText, Dumbbell, Building2, Timer, CheckCircle2, XCircle, Loader2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

export default function InterviewToolkitPage({ userId, user }) {
  const [activeSection, setActiveSection] = useState(null)
  const [loading, setLoading] = useState('')
  const [quiz, setQuiz] = useState(null)
  const [quizState, setQuizState] = useState({ current: 0, answers: [], started: false, finished: false, timer: 0 })
  const [cheatSheet, setCheatSheet] = useState(null)
  const [warmup, setWarmup] = useState(null)
  const [companyFocus, setCompanyFocus] = useState(null)
  const [company, setCompany] = useState('google')

  const loadQuiz = async () => {
    setLoading('quiz'); setActiveSection('quiz')
    try { const d = await getPatternQuiz(userId, 10); setQuiz(d); setQuizState({ current: 0, answers: [], started: true, finished: false, timer: 0 }) } catch {}
    setLoading('')
  }
  const loadCheatSheet = async () => {
    setLoading('cheat'); setActiveSection('cheat')
    try { setCheatSheet(await getCheatSheet(userId)) } catch {}
    setLoading('')
  }
  const loadWarmup = async () => {
    setLoading('warmup'); setActiveSection('warmup')
    try { setWarmup(await getWarmup(userId)) } catch {}
    setLoading('')
  }
  const loadCompanyFocus = async () => {
    setLoading('company'); setActiveSection('company')
    try { setCompanyFocus(await getCompanyFocus(userId, company)) } catch {}
    setLoading('')
  }

  const answerQuiz = (pattern) => {
    const q = quiz.questions[quizState.current]
    const newAnswers = [...quizState.answers, { question_index: quizState.current, selected_pattern: pattern, correct_pattern: q.correct_pattern, time_taken_seconds: quizState.timer }]
    const next = quizState.current + 1
    if (next >= quiz.questions.length) {
      setQuizState({ ...quizState, answers: newAnswers, finished: true })
    } else {
      setQuizState({ ...quizState, current: next, answers: newAnswers, timer: 0 })
    }
  }

  const tools = [
    { id: 'quiz', label: 'Pattern Quiz', desc: 'Quick-fire pattern recognition', icon: Timer, color: 'indigo', action: loadQuiz },
    { id: 'cheat', label: 'Cheat Sheet', desc: 'Condensed review of weak areas', icon: FileText, color: 'emerald', action: loadCheatSheet },
    { id: 'warmup', label: 'Warm-Up', desc: '2 easy problems for flow state', icon: Dumbbell, color: 'amber', action: loadWarmup },
    { id: 'company', label: 'Company Focus', desc: 'Company-specific prep guide', icon: Building2, color: 'purple', action: loadCompanyFocus },
  ]

  return (
    <div className="space-y-6">
      <div><h1 className="text-3xl font-bold gradient-text">Interview Day Toolkit</h1><p className="text-gray-400 mt-1">Last-minute tools to ace your interview</p></div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {tools.map(t => (
          <button key={t.id} onClick={t.action} disabled={!!loading} className={`p-5 rounded-xl border transition-all text-left hover:scale-[1.02] ${activeSection === t.id ? `bg-${t.color}-500/10 border-${t.color}-500/30` : 'bg-gray-800/60 border-gray-700 hover:border-gray-600'}`}>
            <t.icon className={`w-8 h-8 text-${t.color}-400 mb-3`} />
            <p className="font-semibold text-sm">{t.label}</p>
            <p className="text-xs text-gray-400 mt-1">{t.desc}</p>
          </button>
        ))}
      </div>

      {loading && <div className="flex items-center justify-center py-12"><Loader2 className="w-8 h-8 animate-spin text-indigo-400" /></div>}

      {/* Pattern Quiz */}
      {activeSection === 'quiz' && quiz && !loading && (
        <div className="bg-gray-800/60 rounded-xl p-6 border border-indigo-500/30">
          <h2 className="text-xl font-bold text-indigo-400 mb-4">{quiz.quiz_title || 'Pattern Recognition Quiz'}</h2>
          {!quizState.finished ? (
            quiz.questions?.[quizState.current] && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm text-gray-400">Question {quizState.current + 1} of {quiz.questions.length}</span>
                  <div className="h-2 flex-1 mx-4 bg-gray-700 rounded-full"><div className="h-2 bg-indigo-500 rounded-full transition-all" style={{ width: `${((quizState.current) / quiz.questions.length) * 100}%` }} /></div>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-4 mb-4">
                  <p className="text-sm text-gray-300">{quiz.questions[quizState.current].problem_snippet}</p>
                </div>
                <p className="text-sm text-gray-400 mb-3">Which pattern is optimal?</p>
                <div className="grid grid-cols-2 gap-3">
                  {quiz.questions[quizState.current].choices?.map((c, i) => (
                    <button key={i} onClick={() => answerQuiz(c)} className="p-3 bg-gray-700/50 rounded-lg text-sm hover:bg-indigo-600/20 hover:border-indigo-500/30 border border-gray-600 transition-colors text-left">{c.replace(/_/g, ' ')}</button>
                  ))}
                </div>
              </div>
            )
          ) : (
            <div className="space-y-4">
              <div className="text-center py-4">
                <p className="text-4xl font-bold text-indigo-400">{quizState.answers.filter(a => a.selected_pattern === a.correct_pattern).length}/{quizState.answers.length}</p>
                <p className="text-gray-400 mt-1">Correct Answers</p>
              </div>
              {quizState.answers.map((a, i) => (
                <div key={i} className={`flex items-center gap-3 p-3 rounded-lg ${a.selected_pattern === a.correct_pattern ? 'bg-green-500/10' : 'bg-red-500/10'}`}>
                  {a.selected_pattern === a.correct_pattern ? <CheckCircle2 className="w-5 h-5 text-green-400" /> : <XCircle className="w-5 h-5 text-red-400" />}
                  <div className="flex-1"><p className="text-sm">{quiz.questions[i]?.problem_snippet?.slice(0, 80)}...</p><p className="text-xs text-gray-400 mt-0.5">Your answer: {a.selected_pattern} {a.selected_pattern !== a.correct_pattern ? `| Correct: ${a.correct_pattern}` : ''}</p></div>
                </div>
              ))}
              <button onClick={loadQuiz} className="w-full py-2 bg-indigo-600 rounded-lg text-sm hover:bg-indigo-500">Retry Quiz</button>
            </div>
          )}
        </div>
      )}

      {/* Cheat Sheet */}
      {activeSection === 'cheat' && cheatSheet && !loading && (
        <div className="bg-gray-800/60 rounded-xl p-6 border border-emerald-500/30">
          <h2 className="text-xl font-bold text-emerald-400 mb-4">{cheatSheet.title || 'Cheat Sheet'}</h2>
          <div className="space-y-4">
            {cheatSheet.sections?.map((s, i) => (
              <div key={i} className="bg-gray-900/50 rounded-lg p-4">
                <h3 className="font-semibold text-sm text-indigo-300 mb-2">{s.topic}</h3>
                {s.key_template && <SyntaxHighlighter language="python" style={oneDark} customStyle={{ fontSize: '0.7rem', borderRadius: 8, margin: '4px 0 8px' }}>{s.key_template}</SyntaxHighlighter>}
                <p className="text-xs text-gray-400"><span className="text-gray-300">When:</span> {s.when_to_use}</p>
                {s.one_liner && <p className="text-xs text-emerald-400 mt-1">{s.one_liner}</p>}
                <p className="text-xs text-gray-500 mt-1">{s.time_complexity}</p>
              </div>
            ))}
          </div>
          {cheatSheet.emergency_tips?.length > 0 && <div className="mt-4 p-4 bg-amber-500/10 rounded-lg border border-amber-500/20"><h3 className="text-sm font-semibold text-amber-400 mb-2">Emergency Tips</h3>{cheatSheet.emergency_tips.map((t,i) => <p key={i} className="text-xs text-gray-300">• {t}</p>)}</div>}
          {cheatSheet.time_management && <p className="text-xs text-gray-400 mt-3">Time: {cheatSheet.time_management}</p>}
        </div>
      )}

      {/* Warm-Up */}
      {activeSection === 'warmup' && warmup && !loading && (
        <div className="bg-gray-800/60 rounded-xl p-6 border border-amber-500/30">
          <h2 className="text-xl font-bold text-amber-400 mb-2">{warmup.title || 'Warm-Up'}</h2>
          {warmup.message && <p className="text-sm text-gray-300 mb-4">{warmup.message}</p>}
          <div className="space-y-4">
            {warmup.problems?.map((p, i) => (
              <div key={i} className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center gap-2 mb-2"><span className="text-sm font-semibold">{p.title}</span><span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded">{p.difficulty}</span>{p.time_target_minutes && <span className="text-xs text-gray-400 ml-auto">{p.time_target_minutes} min</span>}</div>
                <div className="text-sm text-gray-300 prose prose-invert max-w-none"><ReactMarkdown>{p.description}</ReactMarkdown></div>
                {p.solution && <details className="mt-3"><summary className="text-xs text-indigo-400 cursor-pointer">Show Solution</summary><SyntaxHighlighter language="python" style={oneDark} customStyle={{ fontSize: '0.75rem', marginTop: 8, borderRadius: 8 }}>{p.solution}</SyntaxHighlighter>{p.walkthrough && <p className="text-xs text-gray-400 mt-2">{p.walkthrough}</p>}</details>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Company Focus */}
      {activeSection === 'company' && (
        <div className="bg-gray-800/60 rounded-xl p-6 border border-purple-500/30">
          <div className="flex items-center gap-3 mb-4">
            <select value={company} onChange={e => setCompany(e.target.value)} className="bg-gray-700 rounded-lg px-3 py-2 text-sm border border-gray-600">
              <option value="google">Google</option><option value="meta">Meta</option><option value="amazon">Amazon</option><option value="apple">Apple</option><option value="microsoft">Microsoft</option>
            </select>
            <button onClick={loadCompanyFocus} disabled={!!loading} className="px-4 py-2 bg-purple-600 rounded-lg text-sm hover:bg-purple-500 disabled:opacity-50">Load</button>
          </div>
          {companyFocus && !loading && (
            <div className="space-y-4">
              {companyFocus.interview_format && <p className="text-sm text-gray-300">{companyFocus.interview_format}</p>}
              {companyFocus.top_patterns?.length > 0 && <div className="flex flex-wrap gap-2">{companyFocus.top_patterns.map((p,i) => <span key={i} className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-xs">{p}</span>)}</div>}
              {companyFocus.focus_areas?.map((f, i) => (
                <div key={i} className="bg-gray-900/50 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-1"><span className="text-sm font-semibold">{f.area}</span><span className={`text-xs px-2 py-0.5 rounded ${f.importance === 'high' ? 'bg-red-500/20 text-red-400' : 'bg-gray-600 text-gray-300'}`}>{f.importance}</span></div>
                  <p className="text-xs text-gray-400">{f.why}</p>
                  {f.practice_problems?.length > 0 && <p className="text-xs text-indigo-400 mt-1">Practice: {f.practice_problems.join(', ')}</p>}
                </div>
              ))}
              {companyFocus.company_specific_tips?.length > 0 && <div className="p-4 bg-purple-500/10 rounded-lg"><h4 className="text-sm font-semibold text-purple-300 mb-2">Tips</h4>{companyFocus.company_specific_tips.map((t,i) => <p key={i} className="text-xs text-gray-300">• {t}</p>)}</div>}
              {companyFocus.day_before_plan && <div className="p-4 bg-indigo-500/10 rounded-lg"><h4 className="text-sm font-semibold text-indigo-300 mb-2">Day Before Plan</h4><p className="text-xs text-gray-300">{companyFocus.day_before_plan}</p></div>}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
