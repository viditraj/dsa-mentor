import { useState, useEffect } from 'react'
import { Sparkles, Eye, ChevronDown, ChevronUp, Zap, Target, BookOpen } from 'lucide-react'
import * as api from '../api/client'

/**
 * Pattern recognition cards - "When you see X, think Y"
 * Shows pattern info for a problem, before and after solving.
 */

const PATTERN_EMOJI = {
  two_pointers: '👉👈', sliding_window: '🪟', hash_map: '🗺️',
  binary_search: '🔍', bfs: '🌊', dfs: '🌲', backtracking: '🔙',
  dp_linear: '📈', dp_grid: '🧮', monotonic_stack: '📊',
  greedy: '🤑', union_find: '🔗', topological_sort: '📋',
  trie: '🌳', heap_top_k: '⛰️',
}

/* ─── Small badge for problem list items ─── */
export function PatternBadge({ patternKey, patternName }) {
  if (!patternKey) return null
  const emoji = PATTERN_EMOJI[patternKey] || '🧩'
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-purple-500/15 text-purple-300 border border-purple-500/30">
      {emoji} {patternName || patternKey.replace(/_/g, ' ')}
    </span>
  )
}

/* ─── "When you see X, think Y" Card ─── */
export function WhenYouSeeCard({ cue, pattern, reason }) {
  if (!cue) return null
  return (
    <div className="relative overflow-hidden rounded-xl border border-purple-500/30 bg-gradient-to-br from-purple-900/20 to-indigo-900/20 p-4">
      <div className="absolute top-2 right-2 opacity-20">
        <Sparkles className="w-8 h-8 text-purple-400" />
      </div>
      <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
        <Eye className="w-3.5 h-3.5" /> Pattern Recognition
      </h4>
      <div className="space-y-2">
        <p className="text-sm text-gray-200">
          <span className="text-purple-300 font-semibold">When you see</span>{' '}
          {cue.replace(/^When you see\s*/i, '')}
        </p>
        <p className="text-sm text-gray-200">
          <span className="text-indigo-300 font-semibold">Think →</span>{' '}
          {pattern.replace(/^think\s*/i, '')}
        </p>
        {reason && (
          <p className="text-xs text-gray-400 mt-1 italic">
            💡 {reason.replace(/^because\s*/i, '')}
          </p>
        )}
      </div>
    </div>
  )
}

/* ─── Full Pattern Info Panel ─── */
export function PatternInfoPanel({ problemId, problemTitle }) {
  const [patternData, setPatternData] = useState(null)
  const [expanded, setExpanded] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!problemId) return
    setLoading(true)
    api.getProblemPatterns(problemId)
      .then(data => setPatternData(data))
      .catch(() => setPatternData(null))
      .finally(() => setLoading(false))
  }, [problemId])

  if (loading) {
    return (
      <div className="glass-card rounded-xl p-4 animate-pulse">
        <div className="h-4 bg-gray-700 rounded w-1/3 mb-2" />
        <div className="h-3 bg-gray-800 rounded w-2/3" />
      </div>
    )
  }

  if (!patternData?.primary_pattern) return null

  const p = patternData.primary_pattern
  const emoji = PATTERN_EMOJI[p.key] || '🧩'

  return (
    <div className="glass-card rounded-xl overflow-hidden border border-purple-500/20">
      {/* Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-4 hover:bg-purple-500/5 transition-colors"
      >
        <div className="flex items-center gap-2">
          <span className="text-xl">{emoji}</span>
          <div className="text-left">
            <h3 className="text-sm font-semibold text-purple-300">{p.name}</h3>
            <p className="text-xs text-gray-500">Optimal pattern for this problem</p>
          </div>
        </div>
        {expanded ? <ChevronUp className="w-4 h-4 text-gray-500" /> : <ChevronDown className="w-4 h-4 text-gray-500" />}
      </button>

      {/* Expanded details */}
      {expanded && (
        <div className="px-4 pb-4 space-y-3 border-t border-gray-800 pt-3 animate-fade-in">
          <p className="text-sm text-gray-300">{p.description}</p>

          {p.when_to_use && (
            <div>
              <h4 className="text-xs font-semibold text-gray-400 flex items-center gap-1 mb-1">
                <Target className="w-3 h-3" /> When to Use
              </h4>
              <ul className="space-y-1">
                {(Array.isArray(p.when_to_use) ? p.when_to_use : [p.when_to_use]).map((item, i) => (
                  <li key={i} className="text-xs text-gray-400 flex items-start gap-1.5">
                    <span className="text-purple-400 mt-0.5">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {p.recognition_cues && (
            <div>
              <h4 className="text-xs font-semibold text-gray-400 flex items-center gap-1 mb-1">
                <Eye className="w-3 h-3" /> Recognition Cues
              </h4>
              <ul className="space-y-1">
                {(Array.isArray(p.recognition_cues) ? p.recognition_cues : [p.recognition_cues]).map((cue, i) => (
                  <li key={i} className="text-xs text-gray-400 flex items-start gap-1.5">
                    <span className="text-indigo-400 mt-0.5">→</span> {cue}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {p.complexity && (
            <div className="flex gap-4">
              <div className="text-xs"><span className="text-gray-500">Time:</span> <span className="text-indigo-400 font-mono">{p.complexity.time}</span></div>
              <div className="text-xs"><span className="text-gray-500">Space:</span> <span className="text-indigo-400 font-mono">{p.complexity.space}</span></div>
            </div>
          )}

          {patternData.secondary_patterns?.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-gray-500 mb-1">Also useful:</h4>
              <div className="flex flex-wrap gap-1.5">
                {patternData.secondary_patterns.map(sp => (
                  <span key={sp.key} className="text-[10px] px-2 py-0.5 rounded-full bg-gray-800 text-gray-400 border border-gray-700">
                    {PATTERN_EMOJI[sp.key] || '🧩'} {sp.name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

/* ─── AI Pattern Analysis Result (shown after submitting) ─── */
export function PatternAnalysisResult({ analysis }) {
  if (!analysis) return null

  const isOptimal = analysis.is_optimal_pattern
  const wys = analysis.when_you_see_think

  return (
    <div className="glass-card rounded-xl p-5 border-l-4 border-l-purple-500 animate-fade-in space-y-3">
      <div className="flex items-center gap-2">
        <Zap className="w-5 h-5 text-purple-400" />
        <h3 className="font-semibold text-white">Pattern Analysis</h3>
      </div>

      {/* Pattern comparison */}
      <div className="flex items-center gap-3">
        <div className="flex-1 text-center p-2 rounded-lg bg-gray-800/50">
          <p className="text-[10px] text-gray-500 uppercase">Your Pattern</p>
          <p className="text-sm font-semibold text-gray-200">
            {PATTERN_EMOJI[analysis.detected_pattern] || '🧩'} {analysis.detected_pattern_name}
          </p>
        </div>
        <span className={`text-lg ${isOptimal ? 'text-emerald-400' : 'text-amber-400'}`}>
          {isOptimal ? '✓' : '→'}
        </span>
        <div className="flex-1 text-center p-2 rounded-lg bg-gray-800/50">
          <p className="text-[10px] text-gray-500 uppercase">Optimal Pattern</p>
          <p className="text-sm font-semibold text-gray-200">
            {PATTERN_EMOJI[analysis.optimal_pattern] || '🧩'} {analysis.optimal_pattern_name}
          </p>
        </div>
      </div>

      {/* Complexity comparison */}
      {analysis.student_complexity && analysis.optimal_complexity && (
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="p-2 rounded bg-gray-800/30">
            <p className="text-gray-500">Your complexity</p>
            <p className="font-mono text-gray-300">
              Time: {analysis.student_complexity.time} · Space: {analysis.student_complexity.space}
            </p>
          </div>
          <div className="p-2 rounded bg-gray-800/30">
            <p className="text-gray-500">Optimal</p>
            <p className="font-mono text-indigo-300">
              Time: {analysis.optimal_complexity.time} · Space: {analysis.optimal_complexity.space}
            </p>
          </div>
        </div>
      )}

      {analysis.pattern_match_explanation && (
        <p className="text-sm text-gray-300">{analysis.pattern_match_explanation}</p>
      )}

      {/* When you see / think card */}
      {wys && <WhenYouSeeCard cue={wys.cue} pattern={wys.pattern} reason={wys.reason} />}

      {/* Tips */}
      {analysis.improvement_tips?.length > 0 && (
        <div>
          <h4 className="text-xs font-semibold text-gray-400 mb-1 flex items-center gap-1">
            <BookOpen className="w-3 h-3" /> Improvement Tips
          </h4>
          <ul className="space-y-1">
            {analysis.improvement_tips.map((tip, i) => (
              <li key={i} className="text-xs text-gray-400 flex items-start gap-1.5">
                <span className="text-emerald-400 mt-0.5">✦</span> {tip}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
