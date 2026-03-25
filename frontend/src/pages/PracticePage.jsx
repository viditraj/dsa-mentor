import { useState, useEffect, useCallback, useRef } from 'react'
import { useParams } from 'react-router-dom'
import {
  CheckCircle2, XCircle, Clock, Play, Lightbulb, ChevronRight,
  Code2, Send, RotateCcw, Trophy, ArrowLeft, Loader2, Sparkles, Brain, BookOpen, ChevronDown, ChevronUp,
  MessageCircle, Trash2
} from 'lucide-react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import * as api from '../api/client'
import { PatternBadge, PatternInfoPanel, PatternAnalysisResult } from '../components/PatternCard'
import CodeRunner from '../components/CodeRunner'

const STATUS_CONFIG = {
  not_started: { icon: Clock, label: 'Not Started', color: 'text-gray-400', bg: 'bg-gray-500/10' },
  attempted: { icon: XCircle, label: 'Attempted', color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
  solved: { icon: CheckCircle2, label: 'Solved', color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
  needs_review: { icon: RotateCcw, label: 'Needs Review', color: 'text-orange-400', bg: 'bg-orange-500/10' },
}

const DIFF_COLORS = {
  easy: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
  medium: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30',
  hard: 'text-red-400 bg-red-500/10 border-red-500/30',
}

/* ─── Quick AI Chat ─── */
function QuickChat({ problemTitle, problemDescription, userCode }) {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (open) inputRef.current?.focus()
  }, [open])

  async function send() {
    const q = input.trim()
    if (!q || sending) return
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: q }])
    setSending(true)
    try {
      const context = `Problem: ${problemTitle || 'Unknown'}\nDescription: ${(problemDescription || '').slice(0, 500)}\nUser code:\n${(userCode || '').slice(0, 800)}`
      const res = await api.sendMessage(q, context)
      setMessages(prev => [...prev, { role: 'assistant', content: res.response || 'No response.' }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, something went wrong. Try again.' }])
    } finally {
      setSending(false)
    }
  }

  const mdComps = {
    code({ inline, className, children, ...props }) {
      const match = /language-(\w+)/.exec(className || '')
      if (!inline && match) {
        return (
          <SyntaxHighlighter style={oneDark} language={match[1]} PreTag="div"
            customStyle={{ borderRadius: '6px', fontSize: '0.75rem', margin: '4px 0' }} {...props}>
            {String(children).replace(/\n$/, '')}
          </SyntaxHighlighter>
        )
      }
      return <code className="text-indigo-300 bg-gray-800 px-1 rounded text-xs" {...props}>{children}</code>
    },
    p: ({ children }) => <p className="mb-1.5 last:mb-0 text-[13px] leading-relaxed">{children}</p>,
    ul: ({ children }) => <ul className="list-disc list-inside mb-1.5 space-y-0.5 text-[13px]">{children}</ul>,
    ol: ({ children }) => <ol className="list-decimal list-inside mb-1.5 space-y-0.5 text-[13px]">{children}</ol>,
    strong: ({ children }) => <strong className="text-indigo-300 font-semibold">{children}</strong>,
    table: ({children}) => (
      <div className="overflow-x-auto my-2 rounded border border-gray-700">
        <table className="w-full text-xs text-left">{children}</table>
      </div>
    ),
    thead: ({children}) => <thead className="bg-gray-800/80 text-gray-300 uppercase text-[10px]">{children}</thead>,
    tbody: ({children}) => <tbody className="divide-y divide-gray-800">{children}</tbody>,
    tr: ({children}) => <tr className="hover:bg-gray-800/40">{children}</tr>,
    th: ({children}) => <th className="px-2 py-1.5 font-semibold text-indigo-300">{children}</th>,
    td: ({children}) => <td className="px-2 py-1.5 text-gray-300">{children}</td>,
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="w-full glass-card rounded-xl p-3 flex items-center justify-center gap-2 text-sm text-indigo-400 hover:text-indigo-300 hover:border-indigo-500/40 transition-all group"
      >
        <MessageCircle className="w-4 h-4 group-hover:scale-110 transition-transform" />
        Quick AI Chat
        {messages.length > 0 && (
          <span className="ml-1 px-1.5 py-0.5 rounded-full bg-indigo-500/20 text-[10px] font-medium">{messages.length}</span>
        )}
      </button>
    )
  }

  return (
    <div className="glass-card rounded-xl overflow-hidden border border-indigo-500/30 animate-fade-in flex flex-col" style={{ maxHeight: '420px' }}>
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-gray-800 bg-gray-900/60">
        <div className="flex items-center gap-2">
          <MessageCircle className="w-3.5 h-3.5 text-indigo-400" />
          <span className="text-xs font-medium text-gray-300">AI Chat</span>
          <span className="text-[10px] text-gray-600">• context-aware</span>
        </div>
        <div className="flex items-center gap-1">
          {messages.length > 0 && (
            <button onClick={() => setMessages([])} className="p-1 rounded hover:bg-gray-800 text-gray-600 hover:text-gray-400" title="Clear chat">
              <Trash2 className="w-3 h-3" />
            </button>
          )}
          <button onClick={() => setOpen(false)} className="p-1 rounded hover:bg-gray-800 text-gray-600 hover:text-gray-400" title="Minimize">
            <ChevronDown className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-2 min-h-[120px]" style={{ maxHeight: '300px' }}>
        {messages.length === 0 && (
          <div className="text-center py-6">
            <MessageCircle className="w-6 h-6 text-gray-700 mx-auto mb-2" />
            <p className="text-[11px] text-gray-600">Ask anything about this problem.</p>
            <p className="text-[10px] text-gray-700 mt-1">Your code & problem context are shared automatically.</p>
            <div className="flex flex-wrap gap-1.5 justify-center mt-3">
              {['Give me a hint', 'Explain the approach', 'What pattern fits here?', 'Fix my code'].map(q => (
                <button key={q} onClick={() => { setInput(q); inputRef.current?.focus() }}
                  className="px-2 py-1 rounded-full bg-gray-800/60 text-[10px] text-gray-400 hover:text-indigo-300 hover:bg-indigo-500/10 border border-gray-800 hover:border-indigo-500/20 transition-all">
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[88%] rounded-xl px-3 py-2 ${
              msg.role === 'user'
                ? 'bg-indigo-600 text-white text-[13px] rounded-tr-sm'
                : 'bg-gray-800/60 text-gray-200 rounded-tl-sm'
            }`}>
              {msg.role === 'assistant' ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComps}>
                  {msg.content}
                </ReactMarkdown>
              ) : msg.content}
            </div>
          </div>
        ))}
        {sending && (
          <div className="flex justify-start">
            <div className="bg-gray-800/60 rounded-xl px-3 py-2 rounded-tl-sm">
              <Loader2 className="w-3.5 h-3.5 animate-spin text-indigo-400" />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="px-2 py-2 border-t border-gray-800 bg-gray-900/40">
        <div className="flex items-center gap-1.5">
          <input
            ref={inputRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}
            placeholder="Ask about this problem..."
            disabled={sending}
            className="flex-1 bg-gray-800/60 text-gray-200 text-xs rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500/50 placeholder-gray-600 disabled:opacity-50"
          />
          <button
            onClick={send}
            disabled={!input.trim() || sending}
            className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-30 transition-colors"
          >
            <Send className="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  )
}

/* ─── AI Solution Walkthrough Panel ─── */
function AiSolutionPanel({ solution, onClose }) {
  const [expandedSections, setExpandedSections] = useState({
    understanding: true, thinking: false, approach: false,
    walkthrough: false, code: false, complexity: false, mistakes: false, followup: false,
  })

  const toggleSection = (key) =>
    setExpandedSections(prev => ({ ...prev, [key]: !prev[key] }))

  const sections = [
    { key: 'understanding', icon: '🧠', title: 'Understanding the Problem', content: solution.problem_understanding },
    { key: 'thinking', icon: '💡', title: 'How to Think About It', content: solution.thinking_process },
    { key: 'approach', icon: '🗺️', title: 'Approach & Strategy', content: solution.approach },
    { key: 'walkthrough', icon: '👣', title: 'Step-by-Step Walkthrough', content: solution.walkthrough },
    { key: 'code', icon: '💻', title: 'Solution Code', content: null, isCode: true },
    { key: 'complexity', icon: '⏱️', title: 'Complexity Analysis', content: null, isComplexity: true },
    { key: 'mistakes', icon: '⚠️', title: 'Common Mistakes', content: null, isMistakes: true },
    { key: 'followup', icon: '🔗', title: 'Follow-up Variations', content: null, isFollowup: true },
  ]

  const mdComponents = {
    code({ inline, className, children, ...props }) {
      const match = /language-(\w+)/.exec(className || '')
      if (!inline && match) {
        return (
          <SyntaxHighlighter style={oneDark} language={match[1]} PreTag="div" {...props}>
            {String(children).replace(/\n$/, '')}
          </SyntaxHighlighter>
        )
      }
      return <code className="text-indigo-300 bg-gray-800 px-1 rounded text-xs" {...props}>{children}</code>
    },
    table: ({children}) => (
      <div className="overflow-x-auto my-3 rounded-lg border border-gray-700">
        <table className="w-full text-sm text-left">{children}</table>
      </div>
    ),
    thead: ({children}) => <thead className="bg-gray-800/80 text-gray-300 uppercase text-xs">{children}</thead>,
    tbody: ({children}) => <tbody className="divide-y divide-gray-800">{children}</tbody>,
    tr: ({children}) => <tr className="hover:bg-gray-800/40 transition-colors">{children}</tr>,
    th: ({children}) => <th className="px-3 py-2 font-semibold text-indigo-300 whitespace-nowrap">{children}</th>,
    td: ({children}) => <td className="px-3 py-2 text-gray-300">{children}</td>,
  }

  return (
    <div className="glass-card rounded-xl overflow-hidden border border-purple-500/30 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3 bg-gradient-to-r from-purple-600/20 to-indigo-600/20 border-b border-purple-500/20">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-purple-400" />
          <h3 className="font-semibold text-purple-300">AI Solution Walkthrough</h3>
        </div>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-300 text-xs px-2 py-1 rounded hover:bg-gray-800">
          ✕ Close
        </button>
      </div>

      {/* Key Insight Banner */}
      {solution.key_insight && (
        <div className="mx-4 mt-4 p-3 rounded-lg bg-gradient-to-r from-amber-600/15 to-orange-600/15 border border-amber-500/20">
          <div className="flex items-start gap-2">
            <Sparkles className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" />
            <div>
              <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider">Key Insight</span>
              <p className="text-sm text-amber-200 mt-0.5">{solution.key_insight}</p>
            </div>
          </div>
        </div>
      )}

      {/* Accordion Sections */}
      <div className="p-4 space-y-2">
        {sections.map(({ key, icon, title, content, isCode, isComplexity, isMistakes, isFollowup }) => (
          <div key={key} className="rounded-lg border border-gray-800 overflow-hidden">
            <button
              onClick={() => toggleSection(key)}
              className="w-full flex items-center justify-between px-4 py-2.5 hover:bg-gray-800/30 transition-colors"
            >
              <span className="flex items-center gap-2 text-sm font-medium text-gray-200">
                <span>{icon}</span> {title}
              </span>
              {expandedSections[key]
                ? <ChevronUp className="w-4 h-4 text-gray-500" />
                : <ChevronDown className="w-4 h-4 text-gray-500" />
              }
            </button>
            {expandedSections[key] && (
              <div className="px-4 pb-4 border-t border-gray-800/50">
                {content && (
                  <div className="text-sm text-gray-300 leading-relaxed mt-3 prose prose-invert prose-sm max-w-none
                    prose-strong:text-white prose-code:text-indigo-300 prose-code:bg-gray-800 prose-code:px-1 prose-code:rounded
                    prose-li:marker:text-gray-500 prose-headings:text-white">
                    <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{content}</ReactMarkdown>
                  </div>
                )}
                {isCode && solution.solution_code && (
                  <div className="mt-3">
                    <SyntaxHighlighter
                      style={oneDark}
                      language="python"
                      customStyle={{ borderRadius: '0.5rem', fontSize: '0.8rem' }}
                    >
                      {solution.solution_code}
                    </SyntaxHighlighter>
                  </div>
                )}
                {isComplexity && (
                  <div className="mt-3 space-y-2">
                    <div className="flex gap-4">
                      <div className="flex-1 p-3 rounded-lg bg-gray-800/50">
                        <span className="text-xs text-gray-500">Time Complexity</span>
                        <p className="text-lg font-mono text-indigo-400 font-bold">{solution.time_complexity || 'N/A'}</p>
                      </div>
                      <div className="flex-1 p-3 rounded-lg bg-gray-800/50">
                        <span className="text-xs text-gray-500">Space Complexity</span>
                        <p className="text-lg font-mono text-indigo-400 font-bold">{solution.space_complexity || 'N/A'}</p>
                      </div>
                    </div>
                    {solution.complexity_explanation && (
                      <p className="text-sm text-gray-400 leading-relaxed">{solution.complexity_explanation}</p>
                    )}
                  </div>
                )}
                {isMistakes && solution.common_mistakes?.length > 0 && (
                  <div className="mt-3 space-y-2">
                    {solution.common_mistakes.map((m, i) => (
                      <div key={i} className="flex items-start gap-2 p-2 rounded-lg bg-red-500/5 border border-red-500/10">
                        <XCircle className="w-4 h-4 text-red-400 mt-0.5 flex-shrink-0" />
                        <p className="text-sm text-gray-300">{m}</p>
                      </div>
                    ))}
                  </div>
                )}
                {isFollowup && solution.follow_up?.length > 0 && (
                  <div className="mt-3 space-y-2">
                    {solution.follow_up.map((f, i) => (
                      <div key={i} className="flex items-start gap-2 p-2 rounded-lg bg-indigo-500/5 border border-indigo-500/10">
                        <BookOpen className="w-4 h-4 text-indigo-400 mt-0.5 flex-shrink-0" />
                        <p className="text-sm text-gray-300">{f}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default function PracticePage({ userId, user }) {
  const { topicId } = useParams()
  const [problems, setProblems] = useState([])
  const [selectedProblem, setSelectedProblem] = useState(null)
  const [loading, setLoading] = useState(true)
  const [topics, setTopics] = useState([])

  // Solution submission state
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [submitting, setSubmitting] = useState(false)
  const [feedback, setFeedback] = useState(null)

  // Hints state
  const [hints, setHints] = useState([])
  const [hintLoading, setHintLoading] = useState(false)
  const [showHints, setShowHints] = useState(false)

  // Pattern analysis state
  const [patternAnalysis, setPatternAnalysis] = useState(null)
  const [analyzingPattern, setAnalyzingPattern] = useState(false)
  const [problemPatterns, setProblemPatterns] = useState({})  // cache: problemId -> patternData

  // AI Solve state
  const [aiSolution, setAiSolution] = useState(null)
  const [aiSolving, setAiSolving] = useState(false)
  const [showAiSolution, setShowAiSolution] = useState(false)

  const loadProblems = useCallback(async () => {
    if (!userId) return
    setLoading(true)
    try {
      if (topicId) {
        const data = await api.getTopicProblems(topicId)
        setProblems(data)

        // Pre-fetch pattern info for each problem (non-blocking)
        data.forEach(p => {
          api.getProblemPatterns(p.id).then(pd => {
            setProblemPatterns(prev => ({ ...prev, [p.id]: pd }))
          }).catch(() => {})
        })
      } else {
        // Load topics from roadmap to let user pick
        const roadmap = await api.getRoadmap(userId)
        if (roadmap?.topics) {
          const available = roadmap.topics.filter(t =>
            t.status !== 'locked'
          )
          setTopics(available)
        }
      }
    } catch (err) {
      console.error('Failed to load problems:', err)
    } finally {
      setLoading(false)
    }
  }, [userId, topicId])

  useEffect(() => { loadProblems() }, [loadProblems])

  async function submitSolution() {
    if (!code.trim() || !selectedProblem) return
    setSubmitting(true)
    setFeedback(null)
    setPatternAnalysis(null)
    try {
      const result = await api.submitSolution(selectedProblem.id, {
        user_id: userId,
        code,
        language,
        time_taken_minutes: 0,
      })
      // Normalize feedback from backend
      const review = result.review || {}
      setFeedback({
        is_correct: review.is_correct ?? false,
        feedback: review.summary || result.ai_feedback || 'Solution submitted.',
        score: review.score,
        time_complexity: review.time_complexity,
        space_complexity: review.space_complexity,
        strengths: review.strengths,
        improvements: review.improvements,
        optimal_solution: review.optimal_solution,
      })

      // Also trigger pattern analysis in background
      setAnalyzingPattern(true)
      api.analyzeCodePattern({
        problem_title: selectedProblem.title,
        code,
        language,
      }).then(analysis => {
        setPatternAnalysis(analysis)
      }).catch(() => {}).finally(() => setAnalyzingPattern(false))
    } catch (err) {
      setFeedback({ is_correct: false, feedback: 'Failed to submit. Please try again.' })
    } finally {
      setSubmitting(false)
    }
  }

  async function getHint() {
    if (!selectedProblem) return
    setHintLoading(true)
    try {
      const result = await api.getHint(selectedProblem.id, hints.length + 1)
      setHints(prev => [...prev, result.hint])
      setShowHints(true)
    } catch (err) {
      console.error('Failed to get hint:', err)
    } finally {
      setHintLoading(false)
    }
  }

  function selectProblem(problem) {
    setSelectedProblem(problem)
    setCode(getTemplate(problem, language))
    setFeedback(null)
    setPatternAnalysis(null)
    setHints([])
    setShowHints(false)
    setAiSolution(null)
    setShowAiSolution(false)
  }

  async function solveWithAI() {
    if (!selectedProblem) return
    setAiSolving(true)
    try {
      const result = await api.aiSolve(selectedProblem.id)
      setAiSolution(result)
      setShowAiSolution(true)
    } catch (err) {
      console.error('AI solve failed:', err)
      setAiSolution({ error: 'Failed to get AI solution. Please try again.' })
      setShowAiSolution(true)
    } finally {
      setAiSolving(false)
    }
  }

  function getTemplate(problem, lang) {
    const name = problem?.title?.replace(/\s+/g, '_').toLowerCase() || 'solution'
    if (lang === 'python') {
      return `class Solution:\n    def ${name}(self, nums):\n        # Write your solution here\n        pass\n`
    }
    if (lang === 'javascript') {
      return `function ${name}(nums) {\n    // Write your solution here\n}\n`
    }
    return `// Write your solution here\n`
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-400" />
      </div>
    )
  }

  // Topic selection view (no topicId in URL)
  if (!topicId && !problems.length) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold gradient-text">Practice Problems</h1>
          <p className="text-gray-400 mt-1">Choose a topic to practice</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {topics.map(topic => {
            const StatusIcon = STATUS_CONFIG[topic.status]?.icon || Clock
            return (
              <a
                key={topic.id}
                href={`/practice/${topic.id}`}
                className="glass-card p-4 rounded-xl hover:border-indigo-500/50 transition-all group"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-white group-hover:text-indigo-300 transition-colors">
                    {topic.name}
                  </span>
                  <StatusIcon className={`w-4 h-4 ${STATUS_CONFIG[topic.status]?.color}`} />
                </div>
                <p className="text-xs text-gray-500">{topic.category}</p>
                <div className="mt-3 w-full bg-gray-800 rounded-full h-1.5">
                  <div
                    className="h-1.5 rounded-full bg-indigo-500"
                    style={{ width: `${topic.mastery_level || 0}%` }}
                  />
                </div>
              </a>
            )
          })}
          {topics.length === 0 && (
            <div className="col-span-full text-center py-12 text-gray-500">
              <Code2 className="w-12 h-12 mx-auto mb-3 opacity-40" />
              <p>No topics available yet. Generate your roadmap first!</p>
            </div>
          )}
        </div>
      </div>
    )
  }

  // Problem solving view
  if (selectedProblem) {
    return (
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center gap-3">
          <button onClick={() => setSelectedProblem(null)} className="p-1.5 rounded-lg bg-gray-800 hover:bg-gray-700">
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h2 className="text-lg font-bold text-white">{selectedProblem.title}</h2>
            <div className="flex items-center gap-2 mt-0.5">
              <span className={`px-2 py-0.5 rounded-full text-xs border ${DIFF_COLORS[selectedProblem.difficulty]}`}>
                {selectedProblem.difficulty}
              </span>
              {selectedProblem.leetcode_number && (
                <a
                  href={`https://leetcode.com/problems/${selectedProblem.title?.replace(/\s+/g, '-').toLowerCase()}/`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-indigo-400 hover:text-indigo-300"
                >
                  LeetCode #{selectedProblem.leetcode_number} ↗
                </a>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Left: Problem description + code editor + code runner */}
          <div className="space-y-4">
            {/* Problem Description */}
            <div className="glass-card rounded-xl p-5">
              <h3 className="text-sm font-semibold text-gray-400 mb-2">Problem Description</h3>
              <div className="text-gray-300 text-sm leading-relaxed prose prose-invert prose-sm max-w-none
                prose-strong:text-white prose-code:text-indigo-300 prose-code:bg-gray-800 prose-code:px-1 prose-code:rounded
                prose-li:marker:text-gray-500 prose-headings:text-white">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    code({ inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '')
                      return !inline && match ? (
                        <SyntaxHighlighter style={oneDark} language={match[1]} PreTag="div" {...props}>
                          {String(children).replace(/\n$/, '')}
                        </SyntaxHighlighter>
                      ) : (
                        <code className={className} {...props}>{children}</code>
                      )
                    },
                    table: ({children}) => (
                      <div className="overflow-x-auto my-3 rounded-lg border border-gray-700">
                        <table className="w-full text-sm text-left">{children}</table>
                      </div>
                    ),
                    thead: ({children}) => <thead className="bg-gray-800/80 text-gray-300 uppercase text-xs">{children}</thead>,
                    tbody: ({children}) => <tbody className="divide-y divide-gray-800">{children}</tbody>,
                    tr: ({children}) => <tr className="hover:bg-gray-800/40 transition-colors">{children}</tr>,
                    th: ({children}) => <th className="px-3 py-2 font-semibold text-indigo-300 whitespace-nowrap">{children}</th>,
                    td: ({children}) => <td className="px-3 py-2 text-gray-300">{children}</td>,
                  }}
                >
                  {selectedProblem.description || `Solve the "${selectedProblem.title}" problem. Apply the concepts you've learned.`}
                </ReactMarkdown>
              </div>
              {selectedProblem.hints && (
                <div className="mt-3 space-y-1">
                  <h4 className="text-xs text-gray-500 font-semibold">Key Concepts:</h4>
                  <p className="text-xs text-gray-400">{selectedProblem.hints}</p>
                </div>
              )}
            </div>

            {/* Pattern Info Panel */}
            <PatternInfoPanel
              problemId={selectedProblem.id}
              problemTitle={selectedProblem.title}
            />

            {/* Code Editor */}
            <div className="glass-card rounded-xl overflow-hidden">
              <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800">
                <div className="flex items-center gap-2">
                  <Code2 className="w-4 h-4 text-gray-400" />
                  <span className="text-sm font-medium text-gray-300">Solution</span>
                </div>
                <select
                  value={language}
                  onChange={e => {
                    setLanguage(e.target.value)
                    setCode(getTemplate(selectedProblem, e.target.value))
                  }}
                  className="px-2 py-1 bg-gray-800 border border-gray-700 rounded text-xs text-gray-300"
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="java">Java</option>
                  <option value="cpp">C++</option>
                </select>
              </div>
              <textarea
                value={code}
                onChange={e => setCode(e.target.value)}
                onKeyDown={e => {
                  const ta = e.target
                  const start = ta.selectionStart
                  const end = ta.selectionEnd
                  const val = ta.value

                  if (e.key === 'Tab') {
                    e.preventDefault()
                    const spaces = '    '
                    if (e.shiftKey) {
                      // Un-indent current line(s)
                      const before = val.substring(0, start)
                      const lineStart = before.lastIndexOf('\n') + 1
                      const line = val.substring(lineStart)
                      if (line.startsWith(spaces)) {
                        const newCode = val.substring(0, lineStart) + val.substring(lineStart + 4)
                        setCode(newCode)
                        requestAnimationFrame(() => {
                          ta.selectionStart = Math.max(lineStart, start - 4)
                          ta.selectionEnd = Math.max(lineStart, end - 4)
                        })
                      }
                    } else if (start !== end) {
                      // Indent selected lines
                      const lines = val.split('\n')
                      const startLine = val.substring(0, start).split('\n').length - 1
                      const endLine = val.substring(0, end).split('\n').length - 1
                      for (let i = startLine; i <= endLine; i++) lines[i] = spaces + lines[i]
                      setCode(lines.join('\n'))
                      requestAnimationFrame(() => {
                        ta.selectionStart = start + 4
                        ta.selectionEnd = end + 4 * (endLine - startLine + 1)
                      })
                    } else {
                      // Insert 4 spaces at cursor
                      const newCode = val.substring(0, start) + spaces + val.substring(end)
                      setCode(newCode)
                      requestAnimationFrame(() => {
                        ta.selectionStart = ta.selectionEnd = start + 4
                      })
                    }
                  } else if (e.key === 'Enter') {
                    // Auto-indent: match previous line indentation, +4 if line ends with ':'
                    e.preventDefault()
                    const before = val.substring(0, start)
                    const currentLine = before.substring(before.lastIndexOf('\n') + 1)
                    const indent = currentLine.match(/^(\s*)/)[1]
                    const extra = currentLine.trimEnd().endsWith(':') ? '    ' : ''
                    const insertion = '\n' + indent + extra
                    const newCode = val.substring(0, start) + insertion + val.substring(end)
                    setCode(newCode)
                    requestAnimationFrame(() => {
                      const pos = start + insertion.length
                      ta.selectionStart = ta.selectionEnd = pos
                    })
                  }
                }}
                className="w-full h-64 p-4 bg-gray-950 text-gray-200 font-mono text-sm resize-none focus:outline-none"
                spellCheck={false}
                placeholder="Write your solution here..."
              />
              <div className="flex items-center justify-between px-4 py-2 border-t border-gray-800 bg-gray-900/50">
                <div className="flex items-center gap-2">
                  <button
                    onClick={getHint}
                    disabled={hintLoading}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-600/20 text-amber-400 hover:bg-amber-600/30 text-xs font-medium disabled:opacity-40"
                  >
                    {hintLoading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Lightbulb className="w-3 h-3" />}
                    Get Hint ({hints.length}/3)
                  </button>
                  <button
                    onClick={solveWithAI}
                    disabled={aiSolving}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-purple-600/20 text-purple-400 hover:bg-purple-600/30 text-xs font-medium disabled:opacity-40 transition-colors"
                  >
                    {aiSolving ? <Loader2 className="w-3 h-3 animate-spin" /> : <Brain className="w-3 h-3" />}
                    {aiSolving ? 'AI Thinking...' : 'Solve with AI'}
                  </button>
                </div>
                <button
                  onClick={submitSolution}
                  disabled={submitting || !code.trim()}
                  className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium disabled:opacity-40 transition-all"
                >
                  {submitting ? <Loader2 className="w-3 h-3 animate-spin" /> : <Send className="w-3 h-3" />}
                  Submit Solution
                </button>
              </div>
            </div>

            {/* Code Runner (Pyodide) */}
            {language === 'python' && (
              <CodeRunner
                code={code}
                problemTitle={selectedProblem.title}
                problemDescription={selectedProblem.description}
                difficulty={selectedProblem.difficulty}
              />
            )}
          </div>

          {/* Right: Feedback + Pattern Analysis + Hints */}
          <div className="space-y-4">
            {/* Feedback */}
            {feedback && (
              <div className={`glass-card rounded-xl p-5 border-l-4 animate-fade-in ${
                feedback.is_correct ? 'border-l-emerald-500' : 'border-l-red-500'
              }`}>
                <div className="flex items-center gap-2 mb-3">
                  {feedback.is_correct
                    ? <Trophy className="w-5 h-5 text-emerald-400" />
                    : <XCircle className="w-5 h-5 text-red-400" />
                  }
                  <h3 className="font-semibold text-white">
                    {feedback.is_correct ? 'Correct! Great job!' : 'Not quite right'}
                  </h3>
                </div>
                <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">{feedback.feedback}</p>
                {feedback.time_complexity && (
                  <div className="flex gap-4 mt-3">
                    <div className="text-xs"><span className="text-gray-500">Time:</span> <span className="text-indigo-400 font-mono">{feedback.time_complexity}</span></div>
                    <div className="text-xs"><span className="text-gray-500">Space:</span> <span className="text-indigo-400 font-mono">{feedback.space_complexity}</span></div>
                  </div>
                )}
              </div>
            )}

            {/* Pattern Analysis (after submission) */}
            {analyzingPattern && (
              <div className="glass-card rounded-xl p-5 animate-fade-in flex items-center gap-3">
                <Loader2 className="w-5 h-5 animate-spin text-purple-400" />
                <div>
                  <h3 className="text-sm font-medium text-purple-300">Analyzing your pattern...</h3>
                  <p className="text-xs text-gray-500">Comparing to optimal approach</p>
                </div>
              </div>
            )}
            <PatternAnalysisResult analysis={patternAnalysis} />

            {/* Hints */}
            {showHints && hints.length > 0 && (
              <div className="glass-card rounded-xl p-5 animate-fade-in">
                <h3 className="text-sm font-semibold text-amber-400 flex items-center gap-2 mb-3">
                  <Lightbulb className="w-4 h-4" /> Hints
                </h3>
                <div className="space-y-3">
                  {hints.map((hint, i) => (
                    <div key={i} className="flex gap-3">
                      <span className="flex-shrink-0 w-5 h-5 rounded-full bg-amber-500/20 text-amber-400 text-xs flex items-center justify-center font-bold">
                        {i + 1}
                      </span>
                      <p className="text-sm text-gray-300 leading-relaxed">{hint}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* AI Solution Walkthrough */}
            {aiSolving && (
              <div className="glass-card rounded-xl p-5 animate-fade-in flex items-center gap-3 border border-purple-500/30">
                <Loader2 className="w-6 h-6 animate-spin text-purple-400" />
                <div>
                  <h3 className="text-sm font-medium text-purple-300">AI is solving this problem...</h3>
                  <p className="text-xs text-gray-500">Generating a complete walkthrough with explanation, approach, and solution</p>
                </div>
              </div>
            )}
            {showAiSolution && aiSolution && !aiSolution.error && (
              <AiSolutionPanel solution={aiSolution} onClose={() => setShowAiSolution(false)} />
            )}
            {showAiSolution && aiSolution?.error && (
              <div className="glass-card rounded-xl p-5 border-l-4 border-l-red-500 animate-fade-in">
                <p className="text-sm text-red-400">{aiSolution.error}</p>
              </div>
            )}

            {/* Quick AI Chat */}
            <QuickChat
              problemTitle={selectedProblem.title}
              problemDescription={selectedProblem.description}
              userCode={code}
            />

            {/* No feedback yet placeholder */}
            {!feedback && !showHints && !patternAnalysis && !showAiSolution && (
              <div className="glass-card rounded-xl p-8 flex flex-col items-center justify-center text-center">
                <Play className="w-12 h-12 text-gray-600 mb-3" />
                <h3 className="text-gray-400 font-medium">Ready to solve?</h3>
                <p className="text-gray-600 text-sm mt-1">
                  Write your solution and hit Submit, or request a hint if you're stuck.
                </p>
                {language === 'python' && (
                  <p className="text-purple-500 text-xs mt-2 flex items-center gap-1">
                    <Sparkles className="w-3 h-3" />
                    Use the Code Runner below to test your Python code in the browser
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  // Problem list view
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold gradient-text">Practice Problems</h1>
        <p className="text-gray-400 mt-1">{problems.length} problems to solve</p>
      </div>

      <div className="space-y-3">
        {problems.map((problem, i) => {
          const status = STATUS_CONFIG[problem.status || 'not_started']
          const StatusIcon = status.icon
          return (
            <button
              key={problem.id || i}
              onClick={() => selectProblem(problem)}
              className="w-full glass-card rounded-xl p-4 hover:border-indigo-500/50 transition-all text-left group"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-lg ${status.bg} flex items-center justify-center`}>
                    <StatusIcon className={`w-4 h-4 ${status.color}`} />
                  </div>
                  <div>
                    <h3 className="font-medium text-white group-hover:text-indigo-300 transition-colors">
                      {problem.leetcode_number && <span className="text-gray-500 mr-1">#{problem.leetcode_number}</span>}
                      {problem.title}
                    </h3>
                    <div className="flex items-center gap-2 mt-0.5">
                      <p className="text-xs text-gray-500">{problem.hints || 'No hints'}</p>
                      {problemPatterns[problem.id]?.primary_pattern && (
                        <PatternBadge
                          patternKey={problemPatterns[problem.id].primary_pattern.key}
                          patternName={problemPatterns[problem.id].primary_pattern.name}
                        />
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs border ${DIFF_COLORS[problem.difficulty]}`}>
                    {problem.difficulty}
                  </span>
                  <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-indigo-400 transition-colors" />
                </div>
              </div>
            </button>
          )
        })}
        {problems.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <Code2 className="w-12 h-12 mx-auto mb-3 opacity-40" />
            <p>No problems found for this topic.</p>
          </div>
        )}
      </div>
    </div>
  )
}
