import { useState, useEffect, useCallback } from 'react'
import {
  RotateCcw, Brain, ChevronRight, CheckCircle2, AlertTriangle,
  Clock, Flame, Star, BarChart3, Eye, EyeOff, Loader2, Zap, CalendarDays
} from 'lucide-react'
import {
  getReviewQueue, getReviewStats, getUpcomingReviews,
  submitReview, getReviewQuestion, triggerDecay
} from '../api/client'

const QUALITY_LABELS = [
  { q: 0, label: 'Blackout', desc: 'Complete failure to recall', color: '#ef4444', emoji: '😵' },
  { q: 1, label: 'Wrong', desc: 'Incorrect, but recognized answer', color: '#f97316', emoji: '😟' },
  { q: 2, label: 'Hard', desc: 'Correct with serious difficulty', color: '#f59e0b', emoji: '😓' },
  { q: 3, label: 'Good', desc: 'Correct with some hesitation', color: '#84cc16', emoji: '🙂' },
  { q: 4, label: 'Easy', desc: 'Correct with little hesitation', color: '#10b981', emoji: '😊' },
  { q: 5, label: 'Perfect', desc: 'Instant, perfect recall', color: '#8b5cf6', emoji: '🤩' },
]

const STRENGTH_COLORS = {
  new: { bg: '#1e3a5f', border: '#3b82f6', text: '#93c5fd' },
  weak: { bg: '#4c1d1d', border: '#ef4444', text: '#fca5a5' },
  moderate: { bg: '#78350f', border: '#f59e0b', text: '#fcd34d' },
  good: { bg: '#064e3b', border: '#10b981', text: '#6ee7b7' },
  strong: { bg: '#4c1d95', border: '#8b5cf6', text: '#c4b5fd' },
}

export default function ReviewQueuePage({ userId }) {
  const [tab, setTab] = useState('review') // review | upcoming | stats
  const [queue, setQueue] = useState([])
  const [stats, setStats] = useState(null)
  const [upcoming, setUpcoming] = useState(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)
  const [aiQuestion, setAiQuestion] = useState(null)
  const [loadingAi, setLoadingAi] = useState(false)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [sessionStats, setSessionStats] = useState({ reviewed: 0, avgQuality: 0, totalQ: 0 })

  useEffect(() => {
    loadData()
  }, [userId])

  async function loadData() {
    setLoading(true)
    try {
      const [queueData, statsData] = await Promise.all([
        getReviewQueue(userId).catch(() => ({ cards: [] })),
        getReviewStats(userId).catch(() => null),
      ])
      setQueue(queueData.cards || [])
      setStats(statsData)
    } finally {
      setLoading(false)
    }
  }

  async function loadUpcoming() {
    try {
      const data = await getUpcomingReviews(userId, 7)
      setUpcoming(data)
    } catch (e) {
      console.error(e)
    }
  }

  async function handleGetAiQuestion(card) {
    setLoadingAi(true)
    try {
      const data = await getReviewQuestion(userId, card.id)
      setAiQuestion(data.question)
    } catch (e) {
      console.error(e)
      setAiQuestion(null)
    } finally {
      setLoadingAi(false)
    }
  }

  async function handleSubmitReview(quality) {
    const card = queue[currentIndex]
    if (!card) return
    setSubmitting(true)
    try {
      await submitReview(userId, card.id, quality)
      setSessionStats(s => ({
        reviewed: s.reviewed + 1,
        totalQ: s.totalQ + quality,
        avgQuality: (s.totalQ + quality) / (s.reviewed + 1),
      }))
      // Move to next card
      setShowAnswer(false)
      setAiQuestion(null)
      setQueue(q => q.filter((_, i) => i !== currentIndex))
      if (currentIndex >= queue.length - 1) setCurrentIndex(Math.max(0, queue.length - 2))
    } catch (e) {
      console.error(e)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleTriggerDecay() {
    try {
      await triggerDecay(userId)
      await loadData()
    } catch (e) {
      console.error(e)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-8 h-8 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    )
  }

  const currentCard = queue[currentIndex]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text flex items-center gap-2">
            <Brain className="w-7 h-7" /> Spaced Repetition
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Review cards using SM-2 algorithm for optimal retention
          </p>
        </div>
        <div className="flex gap-2">
          {['review', 'upcoming', 'stats'].map(t => (
            <button
              key={t}
              onClick={() => { setTab(t); if (t === 'upcoming') loadUpcoming() }}
              className={`px-3 py-1.5 text-sm rounded-lg ${tab === t
                ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'}`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Session Stats Bar */}
      {sessionStats.reviewed > 0 && (
        <div className="glass-card p-3 flex items-center gap-6 text-sm">
          <div className="flex items-center gap-2 text-gray-400">
            <Flame className="w-4 h-4 text-orange-400" />
            <span>Session: <span className="text-white font-medium">{sessionStats.reviewed}</span> reviewed</span>
          </div>
          <div className="flex items-center gap-2 text-gray-400">
            <Star className="w-4 h-4 text-yellow-400" />
            <span>Avg quality: <span className="text-white font-medium">{sessionStats.avgQuality.toFixed(1)}</span></span>
          </div>
          <div className="flex items-center gap-2 text-gray-400">
            <CheckCircle2 className="w-4 h-4 text-green-400" />
            <span>Remaining: <span className="text-white font-medium">{queue.length}</span></span>
          </div>
        </div>
      )}

      {tab === 'review' && (
        <ReviewTab
          queue={queue}
          currentCard={currentCard}
          currentIndex={currentIndex}
          showAnswer={showAnswer}
          aiQuestion={aiQuestion}
          loadingAi={loadingAi}
          submitting={submitting}
          onShowAnswer={() => setShowAnswer(true)}
          onGetAiQuestion={handleGetAiQuestion}
          onSubmitReview={handleSubmitReview}
          onPrev={() => { setCurrentIndex(i => Math.max(0, i-1)); setShowAnswer(false); setAiQuestion(null) }}
          onNext={() => { setCurrentIndex(i => Math.min(queue.length-1, i+1)); setShowAnswer(false); setAiQuestion(null) }}
        />
      )}

      {tab === 'upcoming' && <UpcomingTab upcoming={upcoming} />}

      {tab === 'stats' && (
        <StatsTab stats={stats} onTriggerDecay={handleTriggerDecay} />
      )}
    </div>
  )
}

function ReviewTab({ queue, currentCard, currentIndex, showAnswer, aiQuestion, loadingAi, submitting, onShowAnswer, onGetAiQuestion, onSubmitReview, onPrev, onNext }) {
  if (queue.length === 0) {
    return (
      <div className="glass-card p-12 text-center">
        <CheckCircle2 className="w-16 h-16 mx-auto mb-4 text-green-400 opacity-60" />
        <h3 className="text-xl font-bold text-gray-200 mb-2">All caught up!</h3>
        <p className="text-gray-500">No cards due for review right now. Great job!</p>
      </div>
    )
  }

  const strength = STRENGTH_COLORS[currentCard?.strength] || STRENGTH_COLORS.new

  return (
    <div className="max-w-2xl mx-auto space-y-4">
      {/* Progress bar */}
      <div className="flex items-center gap-3 text-sm text-gray-500">
        <span>{currentIndex + 1} / {queue.length}</span>
        <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
          <div className="h-full bg-indigo-500 rounded-full transition-all" style={{ width: `${((currentIndex+1)/queue.length)*100}%` }} />
        </div>
        {currentCard?.is_overdue && (
          <span className="text-xs text-red-400 flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" /> {currentCard.days_overdue}d overdue
          </span>
        )}
      </div>

      {/* Card */}
      <div className="glass-card p-6 space-y-4 min-h-[300px]" style={{ borderColor: strength.border }}>
        {/* Card header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-xs px-2 py-0.5 rounded-full" style={{ backgroundColor: strength.bg, color: strength.text, border: `1px solid ${strength.border}` }}>
              {currentCard?.strength}
            </span>
            <span className="text-xs text-gray-500">{currentCard?.card_type}</span>
          </div>
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <span>EF: {currentCard?.easiness_factor}</span>
            <span>Interval: {currentCard?.interval_days}d</span>
            <span>Reviews: {currentCard?.total_reviews}</span>
          </div>
        </div>

        {/* Question side */}
        <div className="py-4">
          <h3 className="text-xl font-bold text-gray-100 mb-3">{currentCard?.title}</h3>
          {currentCard?.content?.description && (
            <p className="text-gray-400">{currentCard.content.description}</p>
          )}
        </div>

        {/* AI Question */}
        {aiQuestion && (
          <div className="bg-indigo-950/30 border border-indigo-500/20 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-indigo-300 mb-2 flex items-center gap-1">
              <Brain className="w-4 h-4" /> AI Review Question
            </h4>
            {typeof aiQuestion === 'string' ? (
              <p className="text-sm text-gray-300 whitespace-pre-wrap">{aiQuestion}</p>
            ) : (
              <div className="space-y-2">
                {aiQuestion.question && <p className="text-sm text-gray-300">{aiQuestion.question}</p>}
                {aiQuestion.hint && <p className="text-xs text-gray-500 italic">Hint: {aiQuestion.hint}</p>}
              </div>
            )}
          </div>
        )}

        {/* Answer side */}
        {showAnswer ? (
          <div className="border-t border-gray-700 pt-4 space-y-3 animate-fade-in">
            <h4 className="text-sm font-semibold text-gray-300 flex items-center gap-1">
              <Eye className="w-4 h-4" /> Answer
            </h4>
            {currentCard?.content?.key_points && (
              <ul className="space-y-1.5">
                {currentCard.content.key_points.map((p, i) => (
                  <li key={i} className="text-sm text-gray-400 flex items-start gap-2">
                    <ChevronRight className="w-4 h-4 text-gray-600 mt-0.5 flex-shrink-0" />{p}
                  </li>
                ))}
              </ul>
            )}
            {currentCard?.content?.patterns && (
              <div className="flex flex-wrap gap-1.5 mt-2">
                {currentCard.content.patterns.map((p, i) => (
                  <span key={i} className="text-xs px-2 py-0.5 bg-gray-800 text-gray-400 rounded">{p}</span>
                ))}
              </div>
            )}
            {aiQuestion?.answer && (
              <div className="bg-green-950/20 border border-green-700/30 rounded-lg p-3 mt-3">
                <p className="text-sm text-gray-300">{aiQuestion.answer}</p>
              </div>
            )}

            {/* Quality Rating */}
            <div className="pt-4">
              <p className="text-sm text-gray-400 mb-3">How well did you recall this?</p>
              <div className="grid grid-cols-6 gap-2">
                {QUALITY_LABELS.map(({ q, label, desc, color, emoji }) => (
                  <button
                    key={q}
                    disabled={submitting}
                    onClick={() => onSubmitReview(q)}
                    className="flex flex-col items-center gap-1 p-2 rounded-lg border border-gray-700 hover:border-opacity-100 transition-all disabled:opacity-50"
                    style={{ '--hover-color': color }}
                    onMouseEnter={e => { e.currentTarget.style.borderColor = color; e.currentTarget.style.backgroundColor = color + '15' }}
                    onMouseLeave={e => { e.currentTarget.style.borderColor = '#374151'; e.currentTarget.style.backgroundColor = 'transparent' }}
                  >
                    <span className="text-lg">{emoji}</span>
                    <span className="text-xs font-medium text-gray-300">{label}</span>
                    <span className="text-[10px] text-gray-600 leading-tight text-center">{desc}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="flex gap-3 pt-4">
            <button
              onClick={onShowAnswer}
              className="flex-1 py-3 bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 rounded-lg text-sm font-medium flex items-center justify-center gap-2 border border-indigo-500/30 transition-all"
            >
              <Eye className="w-4 h-4" /> Show Answer
            </button>
            <button
              onClick={() => onGetAiQuestion(currentCard)}
              disabled={loadingAi}
              className="px-4 py-3 bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 rounded-lg text-sm font-medium flex items-center gap-2 border border-purple-500/30 transition-all disabled:opacity-50"
            >
              {loadingAi ? <Loader2 className="w-4 h-4 animate-spin" /> : <Brain className="w-4 h-4" />}
              AI Question
            </button>
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between">
        <button onClick={onPrev} disabled={currentIndex === 0}
          className="px-4 py-2 text-sm text-gray-400 hover:text-gray-200 disabled:opacity-30">← Previous</button>
        <button onClick={onNext} disabled={currentIndex >= queue.length - 1}
          className="px-4 py-2 text-sm text-gray-400 hover:text-gray-200 disabled:opacity-30">Next →</button>
      </div>
    </div>
  )
}

function UpcomingTab({ upcoming }) {
  if (!upcoming) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-indigo-400" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="glass-card p-4 flex items-center gap-3">
        <CalendarDays className="w-5 h-5 text-indigo-400" />
        <span className="text-sm text-gray-300">
          <span className="font-medium text-white">{upcoming.total}</span> reviews in the next 7 days
        </span>
      </div>

      {Object.entries(upcoming.by_day || {}).map(([day, cards]) => (
        <div key={day} className="glass-card p-4 space-y-3">
          <h3 className="text-sm font-semibold text-gray-200 flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-500" />
            {day}
            <span className="text-xs text-gray-500">({cards.length} cards)</span>
          </h3>
          <div className="space-y-1.5">
            {cards.map((card) => {
              const s = STRENGTH_COLORS[card.strength] || STRENGTH_COLORS.new
              return (
                <div key={card.id} className="flex items-center gap-3 px-3 py-2 bg-gray-800/30 rounded-lg">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: s.border }} />
                  <span className="text-sm text-gray-300 flex-1">{card.title}</span>
                  <span className="text-xs" style={{ color: s.text }}>{card.strength}</span>
                  <span className="text-xs text-gray-600">EF {card.easiness_factor}</span>
                </div>
              )
            })}
          </div>
        </div>
      ))}

      {Object.keys(upcoming.by_day || {}).length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <CheckCircle2 className="w-10 h-10 mx-auto mb-3 opacity-40" />
          No upcoming reviews in the next 7 days
        </div>
      )}
    </div>
  )
}

function StatsTab({ stats, onTriggerDecay }) {
  if (!stats) return <p className="text-gray-500 text-center py-8">No statistics yet</p>

  const statItems = [
    { label: 'Total Cards', value: stats.total_cards, icon: BarChart3, color: '#6366f1' },
    { label: 'Due Now', value: stats.due_now, icon: AlertTriangle, color: stats.due_now > 0 ? '#ef4444' : '#10b981' },
    { label: 'Reviewed Today', value: stats.reviewed_today, icon: CheckCircle2, color: '#10b981' },
    { label: 'Mastered', value: stats.mastered_cards, icon: Star, color: '#8b5cf6' },
    { label: 'Struggling', value: stats.struggling_cards, icon: AlertTriangle, color: '#f59e0b' },
    { label: 'Retention', value: `${stats.retention_rate}%`, icon: Zap, color: '#10b981' },
  ]

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {statItems.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="glass-card p-4 text-center">
            <Icon className="w-6 h-6 mx-auto mb-2" style={{ color }} />
            <div className="text-2xl font-bold" style={{ color }}>{value}</div>
            <div className="text-xs text-gray-500 mt-1">{label}</div>
          </div>
        ))}
      </div>

      <div className="glass-card p-4">
        <h3 className="text-sm font-semibold text-gray-300 mb-2">Avg Easiness Factor</h3>
        <div className="flex items-center gap-3">
          <div className="flex-1 h-3 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: `${Math.min(100, (stats.avg_easiness_factor / 3) * 100)}%`,
                backgroundColor: stats.avg_easiness_factor >= 2.5 ? '#10b981' : stats.avg_easiness_factor >= 2.0 ? '#f59e0b' : '#ef4444'
              }}
            />
          </div>
          <span className="text-sm font-medium text-gray-300">{stats.avg_easiness_factor}</span>
        </div>
        <p className="text-xs text-gray-600 mt-1">
          {stats.avg_easiness_factor >= 2.5 ? 'Great retention!' : stats.avg_easiness_factor >= 2.0 ? 'Room for improvement' : 'Focus on these topics'}
        </p>
      </div>

      <button
        onClick={onTriggerDecay}
        className="text-sm text-gray-500 hover:text-gray-300 flex items-center gap-2"
      >
        <RotateCcw className="w-4 h-4" /> Apply mastery decay (simulates time passing)
      </button>
    </div>
  )
}
