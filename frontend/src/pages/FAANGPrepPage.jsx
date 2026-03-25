import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import {
  Flame, Trophy, Target, ChevronDown, ChevronRight, BookOpen, Code2,
  CheckCircle2, Circle, Clock, Building2, Star, Zap, ArrowRight,
  Lock, Unlock, Brain, Sparkles, ExternalLink, Play, ChevronLeft,
  Award, TrendingUp, BarChart3, Lightbulb, X
} from 'lucide-react'
import {
  getFAANGOverview, getFAANGProgress, getFAANGPatternDetail,
  getFAANGPatternStory, submitFAANGQuestion, markFAANGStoryRead,
  markFAANGTemplatePracticed, getFAANGQuestionWalkthrough,
} from '../api/client'

/* ─── Difficulty badge ─── */
const DiffBadge = ({ d }) => {
  const c = d === 'easy' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
    : d === 'medium' ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
    : 'bg-red-500/20 text-red-400 border-red-500/30'
  return <span className={`text-xs px-2 py-0.5 rounded-full border ${c}`}>{d}</span>
}

/* ─── Company tag ─── */
const CompanyTag = ({ name }) => (
  <span className="text-[10px] px-1.5 py-0.5 rounded bg-gray-700/60 text-gray-400 border border-gray-600/40">
    {name}
  </span>
)

/* ─── Mastery level badge ─── */
const MasteryBadge = ({ level }) => {
  const styles = {
    locked: 'bg-gray-700/40 text-gray-500 border-gray-600/30',
    learning: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    practiced: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    mastered: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  }
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full border ${styles[level] || styles.locked}`}>
      {level}
    </span>
  )
}

/* ─── Progress bar ─── */
const ProgressBar = ({ value, max, className = '' }) => {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0
  return (
    <div className={`w-full bg-gray-800 rounded-full h-2 ${className}`}>
      <div
        className="h-2 rounded-full transition-all duration-500 bg-gradient-to-r from-indigo-500 to-emerald-500"
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}

/* ─── Markdown renderer ─── */
const Md = ({ children }) => (
  <ReactMarkdown
    remarkPlugins={[remarkGfm]}
    components={{
      code({ inline, className, children, ...props }) {
        const match = /language-(\w+)/.exec(className || '')
        return !inline && match ? (
          <SyntaxHighlighter style={oneDark} language={match[1]} PreTag="div" className="rounded-lg text-sm my-3" {...props}>
            {String(children).replace(/\n$/, '')}
          </SyntaxHighlighter>
        ) : (
          <code className="bg-gray-800 px-1.5 py-0.5 rounded text-sm text-indigo-300" {...props}>{children}</code>
        )
      },
      h1: ({ children }) => <h1 className="text-2xl font-bold mt-6 mb-3">{children}</h1>,
      h2: ({ children }) => <h2 className="text-xl font-bold mt-5 mb-2 text-indigo-300">{children}</h2>,
      h3: ({ children }) => <h3 className="text-lg font-semibold mt-4 mb-2 text-gray-200">{children}</h3>,
      p: ({ children }) => <p className="mb-3 leading-relaxed text-gray-300">{children}</p>,
      ul: ({ children }) => <ul className="list-disc ml-5 mb-3 space-y-1 text-gray-300">{children}</ul>,
      ol: ({ children }) => <ol className="list-decimal ml-5 mb-3 space-y-1 text-gray-300">{children}</ol>,
      strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
      table: ({ children }) => <div className="overflow-x-auto my-3"><table className="w-full text-sm border-collapse">{children}</table></div>,
      th: ({ children }) => <th className="border border-gray-700 px-3 py-2 bg-gray-800/60 text-left font-semibold">{children}</th>,
      td: ({ children }) => <td className="border border-gray-700 px-3 py-2">{children}</td>,
    }}
  >
    {children}
  </ReactMarkdown>
)

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   MAIN PAGE COMPONENT
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

export default function FAANGPrepPage({ userId, user }) {
  const navigate = useNavigate()

  const [overview, setOverview] = useState(null)
  const [progress, setProgress] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activePhase, setActivePhase] = useState(null)
  const [expandedPattern, setExpandedPattern] = useState(null)
  const [patternDetail, setPatternDetail] = useState(null)
  const [storyData, setStoryData] = useState(null)
  const [storyLoading, setStoryLoading] = useState(false)
  const [walkthroughData, setWalkthroughData] = useState(null)
  const [walkthroughLoading, setWalkthroughLoading] = useState(false)
  const [activeQuestion, setActiveQuestion] = useState(null)
  const [submitModal, setSubmitModal] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [view, setView] = useState('overview') // overview | pattern-story | question-walkthrough

  /* ── Fetch data ── */
  const fetchData = useCallback(async () => {
    try {
      const [ov, pr] = await Promise.all([getFAANGOverview(), getFAANGProgress(userId)])
      setOverview(ov)
      setProgress(pr)
      // Default to first incomplete phase
      if (!activePhase) {
        const firstIncomplete = Object.entries(pr.phase_completion || {}).find(([, v]) => !v.complete)
        setActivePhase(firstIncomplete ? Number(firstIncomplete[0]) : 1)
      }
    } catch (e) {
      console.error('Failed to load FAANG data:', e)
    } finally {
      setLoading(false)
    }
  }, [userId, activePhase])

  useEffect(() => { fetchData() }, [fetchData])

  /* ── Expand pattern ── */
  const togglePattern = async (key) => {
    if (expandedPattern === key) {
      setExpandedPattern(null)
      setPatternDetail(null)
      return
    }
    setExpandedPattern(key)
    try {
      const detail = await getFAANGPatternDetail(key)
      setPatternDetail(detail)
    } catch (e) { console.error(e) }
  }

  /* ── Load AI story ── */
  const loadStory = async (patternKey) => {
    setStoryLoading(true)
    setView('pattern-story')
    try {
      const data = await getFAANGPatternStory(patternKey, user?.preferred_language || 'python')
      setStoryData({ ...data, patternKey })
      await markFAANGStoryRead(userId, patternKey)
    } catch (e) { console.error(e) }
    setStoryLoading(false)
  }

  /* ── Load question walkthrough ── */
  const loadWalkthrough = async (question) => {
    setWalkthroughLoading(true)
    setActiveQuestion(question)
    setView('question-walkthrough')
    try {
      const data = await getFAANGQuestionWalkthrough(question.id, user?.preferred_language || 'python')
      setWalkthroughData(data)
    } catch (e) { console.error(e) }
    setWalkthroughLoading(false)
  }

  /* ── Submit question as solved ── */
  const handleSubmit = async (questionId, confidence) => {
    setSubmitting(true)
    try {
      await submitFAANGQuestion({
        user_id: userId,
        question_id: questionId,
        status: 'solved',
        confidence,
      })
      await fetchData()
      setSubmitModal(null)
    } catch (e) { console.error(e) }
    setSubmitting(false)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Flame className="w-12 h-12 text-orange-500 animate-pulse mx-auto mb-4" />
          <p className="text-gray-400">Loading your FAANG 75 crash course...</p>
        </div>
      </div>
    )
  }

  /* ═══════════════════════════════════════
     PATTERN STORY VIEW
     ═══════════════════════════════════════ */
  if (view === 'pattern-story') {
    const pk = storyData?.patternKey || expandedPattern
    const pattern = overview?.phases?.[activePhase]?.patterns_detail?.find(p => p.key === pk)
      || { name: pk, emoji: '' }
    return (
      <div className="space-y-6 animate-fade-in">
        <button onClick={() => setView('overview')} className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
          <ChevronLeft className="w-4 h-4" /> Back to FAANG 75
        </button>

        {storyLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <BookOpen className="w-10 h-10 text-indigo-400 animate-pulse mx-auto mb-3" />
              <p className="text-gray-400">Generating your pattern story...</p>
            </div>
          </div>
        ) : storyData ? (
          <div className="space-y-6">
            <div className="glass-card p-6 rounded-xl border border-indigo-500/30">
              <h1 className="text-2xl font-bold gradient-text mb-2">{storyData.title}</h1>
              <p className="text-indigo-300 italic">{storyData.aha_moment}</p>
            </div>

            {/* Story */}
            <div className="glass-card p-6 rounded-xl">
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><BookOpen className="w-5 h-5 text-indigo-400" /> The Story</h2>
              <Md>{storyData.story}</Md>
            </div>

            {/* Template */}
            <div className="glass-card p-6 rounded-xl">
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><Code2 className="w-5 h-5 text-emerald-400" /> The Template</h2>
              <Md>{storyData.template_breakdown}</Md>
            </div>

            {/* Problems Walkthrough */}
            <div className="glass-card p-6 rounded-xl">
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><Target className="w-5 h-5 text-amber-400" /> Pattern in Action</h2>
              <Md>{storyData.problems_walkthrough}</Md>
            </div>

            {/* Recognition Guide */}
            {storyData.recognition_guide?.length > 0 && (
              <div className="glass-card p-6 rounded-xl border border-purple-500/20">
                <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><Lightbulb className="w-5 h-5 text-purple-400" /> Recognition Guide</h2>
                <div className="space-y-2">
                  {storyData.recognition_guide.map((item, i) => (
                    <div key={i} className="p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
                      <p className="text-purple-300 font-medium">{item.trigger}</p>
                      <p className="text-gray-400 text-sm mt-1">{item.think}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Pitfalls */}
            {storyData.common_pitfalls?.length > 0 && (
              <div className="glass-card p-6 rounded-xl">
                <h2 className="text-lg font-bold mb-3 text-red-400">Common Pitfalls</h2>
                <ul className="space-y-2">
                  {storyData.common_pitfalls.map((p, i) => (
                    <li key={i} className="flex items-start gap-2 text-gray-300">
                      <span className="text-red-400 mt-0.5">!</span> {p}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Motivation */}
            {storyData.motivation && (
              <div className="p-4 bg-gradient-to-r from-indigo-500/10 to-emerald-500/10 rounded-xl border border-indigo-500/20 text-center">
                <p className="text-indigo-300 italic">{storyData.motivation}</p>
              </div>
            )}
          </div>
        ) : null}
      </div>
    )
  }

  /* ═══════════════════════════════════════
     QUESTION WALKTHROUGH VIEW
     ═══════════════════════════════════════ */
  if (view === 'question-walkthrough' && activeQuestion) {
    return (
      <div className="space-y-6 animate-fade-in">
        <button onClick={() => setView('overview')} className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
          <ChevronLeft className="w-4 h-4" /> Back to FAANG 75
        </button>

        {walkthroughLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Brain className="w-10 h-10 text-indigo-400 animate-pulse mx-auto mb-3" />
              <p className="text-gray-400">Generating interview walkthrough...</p>
            </div>
          </div>
        ) : walkthroughData ? (
          <div className="space-y-6">
            <div className="glass-card p-6 rounded-xl border border-indigo-500/30">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-2xl font-bold">{walkthroughData.problem_title}</h1>
                <DiffBadge d={walkthroughData.difficulty} />
                <a href={`https://leetcode.com/problems/${activeQuestion.title.toLowerCase().replace(/\s+/g, '-')}/`}
                   target="_blank" rel="noopener noreferrer"
                   className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 ml-auto">
                  LeetCode #{activeQuestion.leetcode} <ExternalLink className="w-3 h-3" />
                </a>
              </div>
              <p className="text-gray-400 text-sm">{activeQuestion.why}</p>
            </div>

            {/* What interviewer expects */}
            <div className="glass-card p-6 rounded-xl border border-amber-500/20">
              <h2 className="text-lg font-bold mb-2 flex items-center gap-2"><Building2 className="w-5 h-5 text-amber-400" /> What the Interviewer Expects</h2>
              <p className="text-gray-300">{walkthroughData.interviewer_expects}</p>
            </div>

            {/* Key insight */}
            <div className="p-4 bg-gradient-to-r from-purple-500/10 to-indigo-500/10 rounded-xl border border-purple-500/20">
              <h3 className="font-bold text-purple-300 mb-1 flex items-center gap-2"><Lightbulb className="w-4 h-4" /> Key Insight</h3>
              <p className="text-gray-300">{walkthroughData.key_insight}</p>
            </div>

            {/* Brute force */}
            <div className="glass-card p-6 rounded-xl">
              <h2 className="text-lg font-bold mb-2 text-red-400">Brute Force (Why It's Not Enough)</h2>
              <Md>{walkthroughData.brute_force}</Md>
            </div>

            {/* Optimal approach */}
            <div className="glass-card p-6 rounded-xl border border-emerald-500/20">
              <h2 className="text-lg font-bold mb-2 text-emerald-400">Optimal Approach</h2>
              <Md>{walkthroughData.optimal_approach}</Md>
            </div>

            {/* Dry run */}
            <div className="glass-card p-6 rounded-xl">
              <h2 className="text-lg font-bold mb-2 flex items-center gap-2"><Play className="w-5 h-5 text-indigo-400" /> Dry Run</h2>
              <Md>{walkthroughData.dry_run}</Md>
            </div>

            {/* Solution code */}
            <div className="glass-card p-6 rounded-xl">
              <h2 className="text-lg font-bold mb-2 flex items-center gap-2"><Code2 className="w-5 h-5 text-emerald-400" /> Solution</h2>
              <SyntaxHighlighter style={oneDark} language="python" className="rounded-lg text-sm">
                {walkthroughData.solution_code || '# Enable AI for solution'}
              </SyntaxHighlighter>
              <div className="flex gap-4 mt-3 text-sm">
                <span className="text-gray-400">Time: <span className="text-emerald-400 font-mono">{walkthroughData.complexity?.time}</span></span>
                <span className="text-gray-400">Space: <span className="text-emerald-400 font-mono">{walkthroughData.complexity?.space}</span></span>
              </div>
            </div>

            {/* Interview tips */}
            {walkthroughData.interview_tips?.length > 0 && (
              <div className="glass-card p-6 rounded-xl border border-amber-500/20">
                <h2 className="text-lg font-bold mb-3 text-amber-400">Interview Tips</h2>
                <ul className="space-y-2">
                  {walkthroughData.interview_tips.map((t, i) => (
                    <li key={i} className="flex items-start gap-2 text-gray-300">
                      <Star className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" /> {t}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Follow-up */}
            {walkthroughData.follow_up_questions?.length > 0 && (
              <div className="glass-card p-6 rounded-xl">
                <h2 className="text-lg font-bold mb-3">Follow-up Questions</h2>
                <ul className="space-y-2">
                  {walkthroughData.follow_up_questions.map((q, i) => (
                    <li key={i} className="text-gray-300 flex items-start gap-2">
                      <span className="text-indigo-400">Q:</span> {q}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Mark solved button */}
            {!progress?.solved_ids?.includes(activeQuestion.id) && (
              <div className="text-center">
                <button
                  onClick={() => setSubmitModal(activeQuestion)}
                  className="px-6 py-3 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 rounded-xl font-medium transition-all"
                >
                  Mark as Solved
                </button>
              </div>
            )}
          </div>
        ) : null}
      </div>
    )
  }

  /* ═══════════════════════════════════════
     MAIN OVERVIEW VIEW
     ═══════════════════════════════════════ */
  const phaseData = overview?.phases || {}
  const currentPhase = phaseData[activePhase] || {}
  const phasePct = progress?.phase_completion?.[activePhase]?.percentage || 0

  return (
    <div className="space-y-6 animate-fade-in">
      {/* ── Hero Header ── */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-orange-600/20 via-red-600/10 to-purple-600/20 border border-orange-500/20 p-6">
        <div className="absolute top-0 right-0 w-64 h-64 bg-orange-500/5 rounded-full -mr-20 -mt-20 blur-3xl" />
        <div className="relative">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center">
              <Flame className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">FAANG 75 Crash Course</h1>
              <p className="text-gray-400 text-sm">75 problems. 15 patterns. Interview ready.</p>
            </div>
          </div>

          {/* Readiness score */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
            <div className="bg-gray-900/50 rounded-xl p-3 border border-gray-800">
              <p className="text-xs text-gray-500 mb-1">Readiness</p>
              <p className="text-xl font-bold">{progress?.readiness_emoji} {progress?.percentage || 0}%</p>
              <p className="text-xs text-gray-400">{progress?.readiness_level}</p>
            </div>
            <div className="bg-gray-900/50 rounded-xl p-3 border border-gray-800">
              <p className="text-xs text-gray-500 mb-1">Solved</p>
              <p className="text-xl font-bold text-emerald-400">{progress?.solved || 0}<span className="text-gray-500 text-sm">/{progress?.total_problems || 75}</span></p>
            </div>
            <div className="bg-gray-900/50 rounded-xl p-3 border border-gray-800">
              <p className="text-xs text-gray-500 mb-1">Patterns</p>
              <p className="text-xl font-bold text-indigo-400">
                {Object.values(progress?.pattern_mastery || {}).filter(m => m.mastery_level === 'mastered').length}
                <span className="text-gray-500 text-sm">/15</span>
              </p>
            </div>
            <div className="bg-gray-900/50 rounded-xl p-3 border border-gray-800">
              <p className="text-xs text-gray-500 mb-1">Milestones</p>
              <p className="text-xl font-bold text-amber-400">
                {progress?.milestones_earned?.length || 0}
                <span className="text-gray-500 text-sm">/{progress?.milestones_total || 15}</span>
              </p>
            </div>
          </div>

          {/* Overall progress bar */}
          <div className="mt-4">
            <ProgressBar value={progress?.solved || 0} max={75} />
          </div>
        </div>
      </div>

      {/* ── Motivation quote ── */}
      {progress?.motivation_quote && (
        <div className="p-4 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 rounded-xl border border-indigo-500/10 text-center">
          <p className="text-gray-300 italic">"{progress.motivation_quote.quote}"</p>
        </div>
      )}

      {/* ── Milestones ribbon ── */}
      {progress?.milestones_earned?.length > 0 && (
        <div className="flex gap-2 overflow-x-auto pb-2">
          {progress.milestones_earned.map(m => (
            <div key={m.id} className="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-amber-500/10 border border-amber-500/20 rounded-full text-sm">
              <span>{m.emoji}</span>
              <span className="text-amber-300 font-medium whitespace-nowrap">{m.name}</span>
            </div>
          ))}
        </div>
      )}

      {/* ── Phase Tabs ── */}
      <div className="flex gap-2 overflow-x-auto">
        {Object.entries(phaseData).map(([num, phase]) => {
          const n = Number(num)
          const pCompletion = progress?.phase_completion?.[n] || {}
          const isActive = n === activePhase
          return (
            <button
              key={n}
              onClick={() => setActivePhase(n)}
              className={`flex-shrink-0 px-4 py-2.5 rounded-xl text-sm font-medium transition-all border
                ${isActive
                  ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40'
                  : pCompletion.complete
                    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20'
                    : 'bg-gray-800/40 text-gray-400 border-gray-700/40 hover:bg-gray-800/60'
                }`}
            >
              <span className="flex items-center gap-2">
                {pCompletion.complete ? <CheckCircle2 className="w-4 h-4" /> : <span className="font-bold">P{n}</span>}
                {phase.name}
                <span className="text-xs opacity-60">{pCompletion.percentage || 0}%</span>
              </span>
            </button>
          )
        })}
      </div>

      {/* ── Phase Header ── */}
      <div className="glass-card p-5 rounded-xl border border-gray-700/40">
        <div className="flex items-center justify-between mb-2">
          <div>
            <h2 className="text-lg font-bold">Phase {activePhase}: {currentPhase.name}</h2>
            <p className="text-sm text-gray-400 italic">{currentPhase.tagline}</p>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-indigo-400">{phasePct}%</p>
            <p className="text-xs text-gray-500">{currentPhase.estimated_days} days est.</p>
          </div>
        </div>
        <p className="text-sm text-gray-300 mb-3">{currentPhase.description}</p>
        <ProgressBar value={progress?.phase_completion?.[activePhase]?.solved || 0} max={progress?.phase_completion?.[activePhase]?.total || 1} />

        {/* Phase motivation */}
        {phasePct === 0 && currentPhase.motivation_start && (
          <p className="text-sm text-indigo-300 mt-3 italic">{currentPhase.motivation_start}</p>
        )}
        {phasePct >= 100 && currentPhase.motivation_complete && (
          <p className="text-sm text-emerald-300 mt-3 italic">{currentPhase.motivation_complete}</p>
        )}
      </div>

      {/* ── Pattern Modules ── */}
      <div className="space-y-4">
        {(currentPhase.patterns || []).map(patternKey => {
          const pInfo = currentPhase.patterns_detail?.find(p => p.key === patternKey) || {}
          const mastery = progress?.pattern_mastery?.[patternKey] || {}
          const isExpanded = expandedPattern === patternKey
          const questions = patternDetail?.questions || []

          return (
            <div key={patternKey} className="glass-card rounded-xl border border-gray-700/40 overflow-hidden">
              {/* Pattern header */}
              <button
                onClick={() => togglePattern(patternKey)}
                className="w-full p-4 flex items-center gap-4 hover:bg-gray-800/30 transition-colors text-left"
              >
                <div className="text-2xl w-10 h-10 flex items-center justify-center bg-gray-800/60 rounded-lg">
                  {pInfo.emoji}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-0.5">
                    <h3 className="font-bold truncate">{pInfo.name}</h3>
                    <DiffBadge d={pInfo.difficulty} />
                    <MasteryBadge level={mastery.mastery_level || 'locked'} />
                  </div>
                  <p className="text-xs text-gray-500 truncate">{pInfo.intuition}</p>
                  <div className="flex items-center gap-3 mt-1">
                    <span className="text-xs text-gray-500">
                      {mastery.problems_solved || 0}/{pInfo.question_count || 0} solved
                    </span>
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <Clock className="w-3 h-3" /> {pInfo.estimated_hours}h
                    </span>
                    {mastery.story_read && <span className="text-xs text-emerald-500 flex items-center gap-1"><BookOpen className="w-3 h-3" /> Story read</span>}
                    {mastery.template_practiced && <span className="text-xs text-emerald-500 flex items-center gap-1"><Code2 className="w-3 h-3" /> Template done</span>}
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-16">
                    <ProgressBar value={mastery.problems_solved || 0} max={pInfo.question_count || 1} />
                  </div>
                  {isExpanded ? <ChevronDown className="w-5 h-5 text-gray-500" /> : <ChevronRight className="w-5 h-5 text-gray-500" />}
                </div>
              </button>

              {/* Expanded pattern content */}
              {isExpanded && (
                <div className="border-t border-gray-800 p-4 space-y-4 animate-fade-in">
                  {/* Story + Template buttons */}
                  <div className="flex gap-3">
                    <button
                      onClick={() => loadStory(patternKey)}
                      className="flex items-center gap-2 px-4 py-2 bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 rounded-lg transition-colors text-sm font-medium border border-indigo-500/30"
                    >
                      <BookOpen className="w-4 h-4" />
                      {mastery.story_read ? 'Re-read Story' : 'Learn Pattern Story'}
                    </button>
                    <button
                      onClick={async () => {
                        await markFAANGTemplatePracticed(userId, patternKey)
                        fetchData()
                      }}
                      className="flex items-center gap-2 px-4 py-2 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 rounded-lg transition-colors text-sm font-medium border border-emerald-500/30"
                    >
                      <Code2 className="w-4 h-4" />
                      {mastery.template_practiced ? 'Template Done' : 'Practice Template'}
                    </button>
                  </div>

                  {/* Pattern template preview */}
                  <div className="bg-gray-900/60 rounded-lg p-4">
                    <h4 className="text-sm font-medium text-gray-400 mb-2">Pattern Template</h4>
                    <SyntaxHighlighter style={oneDark} language="python" className="rounded-lg text-xs">
                      {patternDetail?.pattern?.template || '# Loading...'}
                    </SyntaxHighlighter>
                    <div className="flex gap-4 mt-2 text-xs text-gray-500">
                      <span>Time: <span className="text-emerald-400">{patternDetail?.pattern?.complexity?.time}</span></span>
                      <span>Space: <span className="text-emerald-400">{patternDetail?.pattern?.complexity?.space}</span></span>
                    </div>
                  </div>

                  {/* When to use */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-400 mb-2">When to Use</h4>
                    <div className="flex flex-wrap gap-2">
                      {(patternDetail?.pattern?.when_to_use || []).map((use, i) => (
                        <span key={i} className="text-xs px-2 py-1 bg-purple-500/10 text-purple-300 rounded-lg border border-purple-500/20">
                          {use}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Questions list */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-400 mb-2">Problems ({questions.length})</h4>
                    <div className="space-y-2">
                      {questions.map(q => {
                        const isSolved = progress?.solved_ids?.includes(q.id)
                        const isAttempted = progress?.attempted_ids?.includes(q.id)
                        const qProgress = progress?.question_progress?.[q.id]
                        return (
                          <div key={q.id} className={`flex items-center gap-3 p-3 rounded-lg border transition-colors
                            ${isSolved
                              ? 'bg-emerald-500/5 border-emerald-500/20'
                              : 'bg-gray-800/30 border-gray-700/30 hover:bg-gray-800/50'
                            }`}
                          >
                            {/* Status icon */}
                            <div className="flex-shrink-0">
                              {isSolved ? (
                                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                              ) : (
                                <Circle className="w-5 h-5 text-gray-600" />
                              )}
                            </div>

                            {/* Problem info */}
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2">
                                <span className="font-medium text-sm truncate">{q.title}</span>
                                <DiffBadge d={q.difficulty} />
                                {q.is_blind75 && (
                                  <span className="text-[10px] px-1.5 py-0.5 bg-yellow-500/20 text-yellow-400 rounded border border-yellow-500/30">Blind 75</span>
                                )}
                              </div>
                              <div className="flex items-center gap-2 mt-1">
                                <span className="text-xs text-gray-500">#{q.leetcode}</span>
                                <div className="flex gap-1">
                                  {q.companies?.slice(0, 3).map(c => <CompanyTag key={c} name={c} />)}
                                  {q.companies?.length > 3 && <span className="text-[10px] text-gray-500">+{q.companies.length - 3}</span>}
                                </div>
                              </div>
                              <p className="text-xs text-gray-500 mt-1 truncate">{q.why}</p>
                            </div>

                            {/* Confidence stars */}
                            {isSolved && qProgress?.confidence && (
                              <div className="flex gap-0.5 flex-shrink-0">
                                {[1, 2, 3, 4, 5].map(s => (
                                  <Star key={s} className={`w-3 h-3 ${s <= qProgress.confidence ? 'text-amber-400 fill-amber-400' : 'text-gray-700'}`} />
                                ))}
                              </div>
                            )}

                            {/* Actions */}
                            <div className="flex items-center gap-2 flex-shrink-0">
                              <button
                                onClick={() => loadWalkthrough(q)}
                                className="text-xs px-2.5 py-1.5 bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 rounded-lg transition-colors border border-indigo-500/30"
                              >
                                Walkthrough
                              </button>
                              <a
                                href={`https://leetcode.com/problems/${q.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')}/`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-xs px-2.5 py-1.5 bg-gray-700/40 hover:bg-gray-700/60 text-gray-400 rounded-lg transition-colors border border-gray-600/30"
                              >
                                <ExternalLink className="w-3 h-3" />
                              </a>
                              {!isSolved && (
                                <button
                                  onClick={() => setSubmitModal(q)}
                                  className="text-xs px-2.5 py-1.5 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 rounded-lg transition-colors border border-emerald-500/30"
                                >
                                  Solved
                                </button>
                              )}
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* ── Submit Modal ── */}
      {submitModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 max-w-md w-full space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold">Mark as Solved</h3>
              <button onClick={() => setSubmitModal(null)} className="text-gray-500 hover:text-white"><X className="w-5 h-5" /></button>
            </div>
            <p className="text-gray-400 text-sm">{submitModal.title} (#{submitModal.leetcode})</p>
            <div>
              <p className="text-sm font-medium mb-2">How confident do you feel?</p>
              <div className="flex gap-2">
                {[
                  { val: 1, label: 'Struggled', color: 'border-red-500/40 hover:bg-red-500/20 text-red-400' },
                  { val: 2, label: 'Shaky', color: 'border-orange-500/40 hover:bg-orange-500/20 text-orange-400' },
                  { val: 3, label: 'OK', color: 'border-amber-500/40 hover:bg-amber-500/20 text-amber-400' },
                  { val: 4, label: 'Good', color: 'border-emerald-500/40 hover:bg-emerald-500/20 text-emerald-400' },
                  { val: 5, label: 'Nailed It', color: 'border-green-500/40 hover:bg-green-500/20 text-green-400' },
                ].map(({ val, label, color }) => (
                  <button
                    key={val}
                    onClick={() => handleSubmit(submitModal.id, val)}
                    disabled={submitting}
                    className={`flex-1 py-2 rounded-lg border text-xs font-medium transition-all ${color} ${submitting ? 'opacity-50' : ''}`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
