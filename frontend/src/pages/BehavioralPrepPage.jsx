import { useState } from 'react'
import { getBehavioralFrameworks, generateBehavioralQuestions, reviewBehavioralAnswer, getStarCoaching } from '../api/client'
import { Users, MessageSquare, Star, Sparkles, ChevronDown, ChevronRight, Loader2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function BehavioralPrepPage({ userId, user }) {
  const [activeTab, setActiveTab] = useState('questions')
  const [loading, setLoading] = useState('')
  const [questions, setQuestions] = useState(null)
  const [company, setCompany] = useState('')
  const [reviewResult, setReviewResult] = useState(null)
  const [reviewForm, setReviewForm] = useState({ question: '', answer: '' })
  const [starForm, setStarForm] = useState({ experience: '', target_question_type: '' })
  const [starResult, setStarResult] = useState(null)
  const [expandedQ, setExpandedQ] = useState(null)
  const [answerInputs, setAnswerInputs] = useState({})

  const loadQuestions = async () => {
    setLoading('questions')
    try { setQuestions(await generateBehavioralQuestions({ user_id: userId, company: company || undefined, num_questions: 5 })) } catch {}
    setLoading('')
  }

  const handleReview = async (question = null, answer = null) => {
    const q = question || reviewForm.question
    const a = answer || reviewForm.answer
    if (!q || !a) return
    setLoading('review'); setReviewResult(null)
    try { setReviewResult(await reviewBehavioralAnswer({ question: q, answer: a, company: company || undefined })) } catch {}
    setLoading('')
  }

  const handleStar = async () => {
    if (!starForm.experience) return
    setLoading('star'); setStarResult(null)
    try { setStarResult(await getStarCoaching({ experience: starForm.experience, target_question_type: starForm.target_question_type || undefined })) } catch {}
    setLoading('')
  }

  const Tab = ({ id, label, icon: Icon }) => (
    <button onClick={() => setActiveTab(id)} className={`flex items-center gap-2 px-5 py-3 text-sm font-medium border-b-2 transition-colors ${activeTab === id ? 'border-indigo-500 text-white' : 'border-transparent text-gray-400 hover:text-gray-200'}`}><Icon className="w-4 h-4" />{label}</button>
  )

  const ScoreCircle = ({ score, max = 10, size = 'md' }) => {
    const color = score >= 7 ? 'text-green-400' : score >= 5 ? 'text-amber-400' : 'text-red-400'
    return <span className={`${color} font-bold ${size === 'lg' ? 'text-4xl' : 'text-xl'}`}>{score}/{max}</span>
  }

  return (
    <div className="space-y-6">
      <div><h1 className="text-3xl font-bold gradient-text">Behavioral Interview Prep</h1><p className="text-gray-400 mt-1">Master the STAR method and company-specific frameworks</p></div>

      <div className="flex border-b border-gray-800">
        <Tab id="questions" label="Practice Questions" icon={MessageSquare} />
        <Tab id="review" label="Review Answers" icon={Star} />
        <Tab id="star" label="STAR Coaching" icon={Sparkles} />
      </div>

      {/* Practice Questions */}
      {activeTab === 'questions' && (
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <select value={company} onChange={e => setCompany(e.target.value)} className="bg-gray-700 rounded-lg px-4 py-2.5 text-sm border border-gray-600">
              <option value="">Any Company</option><option value="amazon">Amazon</option><option value="google">Google</option><option value="meta">Meta</option><option value="microsoft">Microsoft</option><option value="apple">Apple</option>
            </select>
            <button onClick={loadQuestions} disabled={!!loading} className="px-5 py-2.5 bg-indigo-600 rounded-lg text-sm hover:bg-indigo-500 disabled:opacity-50 flex items-center gap-2">
              {loading === 'questions' ? <Loader2 className="w-4 h-4 animate-spin" /> : <MessageSquare className="w-4 h-4" />}Generate Questions
            </button>
          </div>
          {questions?.questions?.map((q, i) => (
            <div key={i} className="bg-gray-800/60 rounded-xl border border-gray-700 overflow-hidden">
              <button onClick={() => setExpandedQ(expandedQ === i ? null : i)} className="w-full flex items-center gap-3 p-4 text-left hover:bg-gray-800/80">
                {expandedQ === i ? <ChevronDown className="w-4 h-4 text-gray-400" /> : <ChevronRight className="w-4 h-4 text-gray-400" />}
                <span className="flex-1 text-sm font-medium">{q.question}</span>
                <span className={`text-xs px-2 py-0.5 rounded ${q.difficulty === 'hard' ? 'bg-red-500/20 text-red-400' : q.difficulty === 'medium' ? 'bg-amber-500/20 text-amber-400' : 'bg-green-500/20 text-green-400'}`}>{q.difficulty}</span>
                {q.competency && <span className="text-xs text-indigo-400">{q.competency}</span>}
              </button>
              {expandedQ === i && (
                <div className="px-4 pb-4 space-y-3 border-t border-gray-700 pt-3">
                  {q.what_they_look_for && <p className="text-xs text-gray-400"><span className="text-gray-300 font-medium">Looking for:</span> {q.what_they_look_for}</p>}
                  {q.principle && <p className="text-xs text-purple-400">Principle: {q.principle}</p>}
                  {q.sample_structure && <p className="text-xs text-emerald-400">Structure: {q.sample_structure}</p>}
                  <div>
                    <label className="text-xs text-gray-400 block mb-1">Your Answer</label>
                    <textarea value={answerInputs[i] || ''} onChange={e => setAnswerInputs({...answerInputs, [i]: e.target.value})} rows={4} className="w-full bg-gray-900 rounded-lg p-3 text-sm text-white border border-gray-700 resize-none" placeholder="Practice your STAR answer..." />
                    <button onClick={() => handleReview(q.question, answerInputs[i])} disabled={!answerInputs[i] || !!loading} className="mt-2 px-4 py-1.5 bg-indigo-600/80 rounded-lg text-xs hover:bg-indigo-500 disabled:opacity-50">Review My Answer</button>
                  </div>
                  {q.follow_ups?.length > 0 && <div><p className="text-xs text-gray-400 font-medium">Follow-ups:</p>{q.follow_ups.map((f,j) => <p key={j} className="text-xs text-gray-300 ml-3">• {f}</p>)}</div>}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Review Answers */}
      {activeTab === 'review' && (
        <div className="space-y-4">
          <div className="bg-gray-800/60 rounded-xl p-6 border border-gray-700">
            <div className="space-y-3">
              <div><label className="text-sm text-gray-400 block mb-1">Interview Question</label><input value={reviewForm.question} onChange={e => setReviewForm({...reviewForm, question: e.target.value})} className="w-full bg-gray-700 rounded-lg px-4 py-2.5 text-sm text-white border border-gray-600" placeholder="e.g. Tell me about a time you showed leadership" /></div>
              <div><label className="text-sm text-gray-400 block mb-1">Your Answer</label><textarea value={reviewForm.answer} onChange={e => setReviewForm({...reviewForm, answer: e.target.value})} rows={6} className="w-full bg-gray-700 rounded-lg px-4 py-3 text-sm text-white border border-gray-600 resize-none" placeholder="Practice your STAR response..." /></div>
              <button onClick={() => handleReview()} disabled={!!loading || !reviewForm.question || !reviewForm.answer} className="px-6 py-2.5 bg-indigo-600 rounded-lg text-sm hover:bg-indigo-500 disabled:opacity-50 flex items-center gap-2">
                {loading === 'review' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Star className="w-4 h-4" />}Review Answer
              </button>
            </div>
          </div>
          {reviewResult && (
            <div className="bg-gray-800/60 rounded-xl p-6 border border-indigo-500/30 space-y-4">
              <div className="text-center"><ScoreCircle score={reviewResult.overall_score} size="lg" /><p className="text-gray-400 text-sm mt-1">Overall Score</p></div>
              {reviewResult.star_breakdown && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {['situation', 'task', 'action', 'result'].map(key => {
                    const s = reviewResult.star_breakdown[key]
                    return s ? (
                      <div key={key} className={`p-3 rounded-lg ${s.present ? 'bg-green-500/10 border border-green-500/20' : 'bg-red-500/10 border border-red-500/20'}`}>
                        <p className="text-xs font-semibold uppercase text-gray-300">{key}</p>
                        <ScoreCircle score={s.score} /><p className="text-xs text-gray-400 mt-1">{s.feedback}</p>
                      </div>
                    ) : null
                  })}
                </div>
              )}
              {reviewResult.strengths?.length > 0 && <div><h4 className="text-sm font-semibold text-green-400">Strengths</h4>{reviewResult.strengths.map((s,i) => <p key={i} className="text-xs text-gray-300 ml-3">+ {s}</p>)}</div>}
              {reviewResult.improvements?.length > 0 && <div><h4 className="text-sm font-semibold text-amber-400">Improvements</h4>{reviewResult.improvements.map((s,i) => <p key={i} className="text-xs text-gray-300 ml-3">- {s}</p>)}</div>}
              {reviewResult.improved_version && <div><h4 className="text-sm font-semibold text-indigo-400 mb-1">Improved Version</h4><div className="text-sm text-gray-300 bg-gray-900/50 rounded-lg p-4 prose prose-invert max-w-none"><ReactMarkdown>{reviewResult.improved_version}</ReactMarkdown></div></div>}
            </div>
          )}
        </div>
      )}

      {/* STAR Coaching */}
      {activeTab === 'star' && (
        <div className="space-y-4">
          <div className="bg-gray-800/60 rounded-xl p-6 border border-gray-700">
            <h3 className="font-semibold mb-3">Transform Experience into STAR Responses</h3>
            <div className="space-y-3">
              <div><label className="text-sm text-gray-400 block mb-1">Describe your experience/project</label><textarea value={starForm.experience} onChange={e => setStarForm({...starForm, experience: e.target.value})} rows={5} className="w-full bg-gray-700 rounded-lg px-4 py-3 text-sm text-white border border-gray-600 resize-none" placeholder="e.g. I led a team of 5 to redesign our authentication system. We had tight deadlines and disagreements on the approach..." /></div>
              <div><label className="text-sm text-gray-400 block mb-1">Target Question Type (optional)</label>
                <select value={starForm.target_question_type} onChange={e => setStarForm({...starForm, target_question_type: e.target.value})} className="w-full bg-gray-700 rounded-lg px-4 py-2.5 text-sm border border-gray-600">
                  <option value="">Auto-detect (multiple types)</option><option value="leadership">Leadership</option><option value="conflict">Conflict Resolution</option><option value="failure">Failure/Learning</option><option value="teamwork">Teamwork</option><option value="innovation">Innovation</option>
                </select></div>
              <button onClick={handleStar} disabled={!!loading || !starForm.experience} className="px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-emerald-600 rounded-lg text-sm hover:opacity-90 disabled:opacity-50 flex items-center gap-2">
                {loading === 'star' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}Generate STAR Responses
              </button>
            </div>
          </div>
          {starResult && (
            <div className="space-y-4">
              {starResult.versatility_note && <p className="text-sm text-indigo-400 bg-indigo-500/10 rounded-lg p-3">{starResult.versatility_note}</p>}
              {starResult.star_responses?.map((r, i) => (
                <div key={i} className="bg-gray-800/60 rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center gap-2 mb-3"><span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded">{r.question_type}</span>{r.time_to_deliver && <span className="text-xs text-gray-400 ml-auto">{r.time_to_deliver}</span>}</div>
                  <p className="text-sm font-medium text-gray-200 mb-3">Q: {r.target_question}</p>
                  <div className="space-y-2 text-sm">
                    <div className="p-3 bg-blue-500/10 rounded-lg"><p className="text-xs font-semibold text-blue-400 mb-1">SITUATION</p><p className="text-gray-300">{r.situation}</p></div>
                    <div className="p-3 bg-purple-500/10 rounded-lg"><p className="text-xs font-semibold text-purple-400 mb-1">TASK</p><p className="text-gray-300">{r.task}</p></div>
                    <div className="p-3 bg-indigo-500/10 rounded-lg"><p className="text-xs font-semibold text-indigo-400 mb-1">ACTION</p><p className="text-gray-300">{r.action}</p></div>
                    <div className="p-3 bg-emerald-500/10 rounded-lg"><p className="text-xs font-semibold text-emerald-400 mb-1">RESULT</p><p className="text-gray-300">{r.result}</p></div>
                  </div>
                  {r.full_response && <details className="mt-3"><summary className="text-xs text-indigo-400 cursor-pointer">Full Polished Response</summary><div className="mt-2 text-sm text-gray-300 bg-gray-900/50 rounded-lg p-4 prose prose-invert max-w-none"><ReactMarkdown>{r.full_response}</ReactMarkdown></div></details>}
                </div>
              ))}
              {starResult.coaching_tips?.length > 0 && <div className="bg-amber-500/10 rounded-lg p-4 border border-amber-500/20"><h4 className="text-sm font-semibold text-amber-400 mb-2">Coaching Tips</h4>{starResult.coaching_tips.map((t,i) => <p key={i} className="text-xs text-gray-300">• {t}</p>)}</div>}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
