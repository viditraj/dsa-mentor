import { useState, useEffect, useCallback } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import {
  Server, ChevronDown, ChevronRight, BookOpen, CheckCircle2,
  Clock, Building2, Zap, ArrowRight, Brain, Sparkles, ExternalLink,
  Play, ChevronLeft, Lightbulb, Tag, Search, Filter, Youtube,
  AlertTriangle, MessageSquare, Layers, Globe, Database, BarChart3,
  Loader2, Star, X
} from 'lucide-react'
import {
  getSystemDesignOverview, getSystemDesignConcept,
  getRecommendedVideos, searchVideos,
} from '../api/client'

/* ─── Difficulty badge ─── */
const DiffBadge = ({ d }) => {
  const c = d === 'easy' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
    : d === 'medium' ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
    : 'bg-red-500/20 text-red-400 border-red-500/30'
  return <span className={`text-xs px-2 py-0.5 rounded-full border ${c}`}>{d}</span>
}

/* ─── Frequency badge ─── */
const FreqBadge = ({ f }) => {
  const styles = {
    very_high: 'bg-red-500/20 text-red-400 border-red-500/30',
    high: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    medium: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    low: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
  }
  const labels = { very_high: 'Very Common', high: 'Common', medium: 'Moderate', low: 'Rare' }
  return <span className={`text-xs px-2 py-0.5 rounded-full border ${styles[f] || styles.medium}`}>{labels[f] || f}</span>
}

/* ─── Company tag ─── */
const CompanyTag = ({ name }) => (
  <span className="text-[10px] px-1.5 py-0.5 rounded bg-gray-700/60 text-gray-400 border border-gray-600/40">
    {name}
  </span>
)

/* ─── Progress bar ─── */
const ProgressBar = ({ value, max, className = '' }) => {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0
  return (
    <div className={`w-full bg-gray-800 rounded-full h-2 ${className}`}>
      <div
        className="h-2 rounded-full transition-all duration-500 bg-gradient-to-r from-cyan-500 to-blue-500"
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
          <code className="bg-gray-800 px-1.5 py-0.5 rounded text-sm text-cyan-300" {...props}>{children}</code>
        )
      },
      h1: ({ children }) => <h1 className="text-2xl font-bold mt-6 mb-3">{children}</h1>,
      h2: ({ children }) => <h2 className="text-xl font-bold mt-5 mb-2 text-cyan-300">{children}</h2>,
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

/* ─── Phase icons ─── */
const phaseIcons = { 1: Globe, 2: Layers, 3: Database, 4: Server }
const phaseColors = {
  1: 'from-cyan-500 to-blue-500',
  2: 'from-blue-500 to-indigo-500',
  3: 'from-indigo-500 to-purple-500',
  4: 'from-purple-500 to-pink-500',
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   MAIN PAGE COMPONENT
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

export default function SystemDesignPage({ userId, user }) {
  const [overview, setOverview] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activePhase, setActivePhase] = useState(1)
  const [selectedConcept, setSelectedConcept] = useState(null)
  const [conceptDetail, setConceptDetail] = useState(null)
  const [conceptLoading, setConceptLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('explanation')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedTag, setSelectedTag] = useState(null)
  const [view, setView] = useState('overview') // overview | concept-detail
  const [videoPlaying, setVideoPlaying] = useState(null)

  /* ── Fetch overview data ── */
  const fetchData = useCallback(async () => {
    try {
      const data = await getSystemDesignOverview()
      setOverview(data)
    } catch (e) {
      console.error('Failed to load System Design data:', e)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  /* ── Load concept detail ── */
  const loadConcept = async (conceptId) => {
    setConceptLoading(true)
    setView('concept-detail')
    setActiveTab('explanation')
    try {
      const data = await getSystemDesignConcept(conceptId)
      setConceptDetail(data)
      setSelectedConcept(conceptId)
    } catch (e) {
      console.error('Failed to load concept:', e)
    } finally {
      setConceptLoading(false)
    }
  }

  /* ── Go back to overview ── */
  const goBack = () => {
    setView('overview')
    setConceptDetail(null)
    setSelectedConcept(null)
  }

  /* ── Filter concepts ── */
  const getFilteredConcepts = () => {
    if (!overview) return []
    const phase = overview.phases[activePhase]
    if (!phase) return []
    let concepts = phase.concepts_preview || []
    if (searchQuery) {
      const q = searchQuery.toLowerCase()
      concepts = concepts.filter(c =>
        c.title.toLowerCase().includes(q) ||
        c.tags.some(t => t.toLowerCase().includes(q))
      )
    }
    if (selectedTag) {
      concepts = concepts.filter(c => c.tags.includes(selectedTag))
    }
    return concepts
  }

  /* ── Loading state ── */
  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Server className="w-12 h-12 mx-auto mb-4 text-cyan-400 animate-pulse" />
          <p className="text-gray-400">Loading System Design curriculum...</p>
        </div>
      </div>
    )
  }

  if (!overview) {
    return (
      <div className="text-center py-20">
        <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-amber-400" />
        <p className="text-gray-400">Failed to load curriculum. Please try again.</p>
        <button onClick={fetchData} className="mt-4 px-4 py-2 bg-cyan-500/20 text-cyan-400 rounded-lg hover:bg-cyan-500/30 transition-colors">
          Retry
        </button>
      </div>
    )
  }

  /* ━━━ CONCEPT DETAIL VIEW ━━━ */
  if (view === 'concept-detail') {
    if (conceptLoading) {
      return (
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <Brain className="w-12 h-12 mx-auto mb-4 text-cyan-400 animate-pulse" />
            <p className="text-gray-400">Loading concept...</p>
          </div>
        </div>
      )
    }

    if (!conceptDetail) return null

    const tabs = [
      { key: 'explanation', label: 'Explanation', icon: BookOpen },
      { key: 'interview', label: 'Interview Tips', icon: MessageSquare },
      { key: 'practice', label: 'Practice', icon: Lightbulb },
      { key: 'videos', label: 'Videos', icon: Youtube },
    ]

    return (
      <div className="animate-fade-in">
        {/* Back button */}
        <button onClick={goBack} className="flex items-center gap-2 text-gray-400 hover:text-cyan-400 transition-colors mb-6">
          <ChevronLeft className="w-4 h-4" /> Back to Overview
        </button>

        {/* Concept Header */}
        <div className="glass-card p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold mb-2">{conceptDetail.title}</h1>
              <div className="flex items-center gap-3 flex-wrap">
                <DiffBadge d={conceptDetail.difficulty} />
                <FreqBadge f={conceptDetail.frequency} />
                <span className="flex items-center gap-1 text-xs text-gray-400">
                  <Clock className="w-3 h-3" /> {conceptDetail.estimated_minutes} min
                </span>
              </div>
            </div>
            <div className="flex items-center gap-1 flex-wrap justify-end">
              {(conceptDetail.companies_asking || []).map(c => (
                <CompanyTag key={c} name={c} />
              ))}
            </div>
          </div>

          {/* Tags */}
          <div className="flex items-center gap-2 flex-wrap">
            {(conceptDetail.tags || []).map(tag => (
              <span key={tag} className="text-xs px-2 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                <Tag className="w-3 h-3 inline mr-1" />{tag}
              </span>
            ))}
          </div>

          {/* Cheat Sheet */}
          {conceptDetail.cheat_sheet && (
            <div className="mt-4 p-3 bg-cyan-500/10 border border-cyan-500/20 rounded-lg">
              <div className="flex items-center gap-2 text-cyan-400 text-sm font-semibold mb-1">
                <Zap className="w-4 h-4" /> Quick Reference
              </div>
              <p className="text-sm text-gray-300">{conceptDetail.cheat_sheet}</p>
            </div>
          )}
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 overflow-x-auto pb-2">
          {tabs.map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setActiveTab(key)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all
                ${activeTab === key
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
                }`}
            >
              <Icon className="w-4 h-4" /> {label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="glass-card p-6">
          {activeTab === 'explanation' && (
            <div className="animate-fade-in">
              {/* Main Explanation */}
              <Md>{conceptDetail.explanation || 'No explanation available yet.'}</Md>

              {/* Key Points */}
              {conceptDetail.key_points?.length > 0 && (
                <div className="mt-6 p-4 bg-gray-800/50 rounded-lg border border-gray-700/50">
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <CheckCircle2 className="w-5 h-5 text-cyan-400" /> Key Points
                  </h3>
                  <ul className="space-y-2">
                    {conceptDetail.key_points.map((pt, i) => (
                      <li key={i} className="flex items-start gap-2 text-gray-300 text-sm">
                        <ArrowRight className="w-4 h-4 text-cyan-400 mt-0.5 flex-shrink-0" />
                        {pt}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Real-world Examples */}
              {conceptDetail.real_world_examples?.length > 0 && (
                <div className="mt-6 p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <Globe className="w-5 h-5 text-blue-400" /> Real-World Examples
                  </h3>
                  <ul className="space-y-2">
                    {conceptDetail.real_world_examples.map((ex, i) => (
                      <li key={i} className="flex items-start gap-2 text-gray-300 text-sm">
                        <Building2 className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
                        {ex}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Diagram Description */}
              {conceptDetail.diagram_description && (
                <div className="mt-6 p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <Layers className="w-5 h-5 text-purple-400" /> Architecture Overview
                  </h3>
                  <p className="text-sm text-gray-300 leading-relaxed">{conceptDetail.diagram_description}</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'interview' && (
            <div className="animate-fade-in space-y-6">
              {/* Interview Tips */}
              {conceptDetail.interview_tips?.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-amber-400" /> Interview Tips
                  </h3>
                  <div className="space-y-3">
                    {conceptDetail.interview_tips.map((tip, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 bg-amber-500/10 rounded-lg border border-amber-500/20">
                        <Lightbulb className="w-5 h-5 text-amber-400 mt-0.5 flex-shrink-0" />
                        <p className="text-sm text-gray-300">{tip}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Common Mistakes */}
              {conceptDetail.common_mistakes?.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <AlertTriangle className="w-5 h-5 text-red-400" /> Common Mistakes
                  </h3>
                  <div className="space-y-3">
                    {conceptDetail.common_mistakes.map((mistake, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 bg-red-500/10 rounded-lg border border-red-500/20">
                        <AlertTriangle className="w-4 h-4 text-red-400 mt-0.5 flex-shrink-0" />
                        <p className="text-sm text-gray-300">{mistake}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Related Concepts */}
              {conceptDetail.related_concepts?.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <ArrowRight className="w-5 h-5 text-cyan-400" /> Related Concepts
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {conceptDetail.related_concepts.map(id => (
                      <button
                        key={id}
                        onClick={() => loadConcept(id)}
                        className="px-3 py-1.5 bg-gray-800 rounded-lg text-sm text-cyan-400 hover:bg-cyan-500/20 transition-colors border border-gray-700"
                      >
                        Concept #{id} <ExternalLink className="w-3 h-3 inline ml-1" />
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'practice' && (
            <div className="animate-fade-in space-y-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <Brain className="w-5 h-5 text-cyan-400" /> Practice Questions
              </h3>
              {conceptDetail.practice_questions?.length > 0 ? (
                <div className="space-y-3">
                  {conceptDetail.practice_questions.map((q, i) => (
                    <div key={i} className="p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-cyan-500/30 transition-colors">
                      <div className="flex items-start gap-3">
                        <span className="flex items-center justify-center w-7 h-7 rounded-full bg-cyan-500/20 text-cyan-400 text-sm font-bold flex-shrink-0">
                          {i + 1}
                        </span>
                        <p className="text-gray-300">{q}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No practice questions available yet.</p>
              )}
            </div>
          )}

          {activeTab === 'videos' && (
            <div className="animate-fade-in">
              <VideoTutorials topicName={conceptDetail.youtube_keywords || conceptDetail.title + ' system design'} />
            </div>
          )}
        </div>
      </div>
    )
  }

  /* ━━━ OVERVIEW VIEW ━━━ */
  const filteredConcepts = getFilteredConcepts()
  const totalConcepts = overview.total_concepts || 0

  return (
    <div className="animate-fade-in">
      {/* Hero Header */}
      <div className="glass-card p-6 mb-6 bg-gradient-to-br from-cyan-500/10 to-blue-500/5 border-cyan-500/20">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
            <Server className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">System Design</h1>
            <p className="text-gray-400">Master the building blocks of distributed systems</p>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
          <div className="p-3 bg-gray-800/50 rounded-lg text-center">
            <p className="text-2xl font-bold text-cyan-400">{totalConcepts}</p>
            <p className="text-xs text-gray-400">Total Concepts</p>
          </div>
          <div className="p-3 bg-gray-800/50 rounded-lg text-center">
            <p className="text-2xl font-bold text-blue-400">{overview.total_phases || 0}</p>
            <p className="text-xs text-gray-400">Phases</p>
          </div>
          <div className="p-3 bg-gray-800/50 rounded-lg text-center">
            <p className="text-2xl font-bold text-indigo-400">{(overview.all_tags || []).length}</p>
            <p className="text-xs text-gray-400">Topics</p>
          </div>
          <div className="p-3 bg-gray-800/50 rounded-lg text-center">
            <p className="text-2xl font-bold text-purple-400">
              {Object.values(overview.phases || {}).reduce((sum, p) => sum + (p.concept_count || 0), 0)}
            </p>
            <p className="text-xs text-gray-400">Lessons</p>
          </div>
        </div>
      </div>

      {/* Phase Tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {Object.entries(overview.phases || {}).map(([num, phase]) => {
          const PhaseIcon = phaseIcons[Number(num)] || Server
          const isActive = activePhase === Number(num)
          return (
            <button
              key={num}
              onClick={() => { setActivePhase(Number(num)); setSelectedTag(null); setSearchQuery('') }}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium whitespace-nowrap transition-all
                ${isActive
                  ? `bg-gradient-to-r ${phaseColors[Number(num)]} text-white shadow-lg`
                  : 'bg-gray-800/60 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
                }`}
            >
              <PhaseIcon className="w-4 h-4" />
              Phase {num}: {phase.name}
              <span className="text-xs opacity-70">({phase.concept_count})</span>
            </button>
          )
        })}
      </div>

      {/* Phase Description */}
      {overview.phases[activePhase] && (
        <div className="glass-card p-5 mb-6">
          <div className="flex items-start gap-3">
            <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${phaseColors[activePhase]} flex items-center justify-center flex-shrink-0`}>
              {(() => { const I = phaseIcons[activePhase] || Server; return <I className="w-5 h-5 text-white" /> })()}
            </div>
            <div>
              <h2 className="text-lg font-bold">{overview.phases[activePhase].name}</h2>
              <p className="text-sm text-gray-400 mt-1">{overview.phases[activePhase].tagline || overview.phases[activePhase].description}</p>
              {overview.phases[activePhase].motivation_start && (
                <p className="text-xs text-cyan-400/80 mt-2 italic">{overview.phases[activePhase].motivation_start}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Search & Filter */}
      <div className="flex gap-3 mb-4 flex-wrap">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input
            type="text"
            placeholder="Search concepts..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-gray-800/60 border border-gray-700/50 rounded-lg text-sm text-gray-300 placeholder-gray-500 focus:outline-none focus:border-cyan-500/50"
          />
        </div>
        <div className="flex gap-1 flex-wrap">
          <button
            onClick={() => setSelectedTag(null)}
            className={`text-xs px-3 py-1.5 rounded-full transition-colors ${!selectedTag ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'bg-gray-800 text-gray-400 hover:text-gray-200'}`}
          >
            All
          </button>
          {(overview.all_tags || []).slice(0, 8).map(tag => (
            <button
              key={tag}
              onClick={() => setSelectedTag(selectedTag === tag ? null : tag)}
              className={`text-xs px-3 py-1.5 rounded-full transition-colors ${selectedTag === tag ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'bg-gray-800 text-gray-400 hover:text-gray-200'}`}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* Concept Cards */}
      <div className="grid gap-4 md:grid-cols-2">
        {filteredConcepts.map(concept => (
          <button
            key={concept.id}
            onClick={() => loadConcept(concept.id)}
            className="glass-card p-5 text-left hover:border-cyan-500/30 transition-all duration-200 group"
          >
            <div className="flex items-start justify-between mb-3">
              <h3 className="font-semibold text-gray-100 group-hover:text-cyan-300 transition-colors">
                {concept.title}
              </h3>
              <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-cyan-400 transition-colors" />
            </div>

            <div className="flex items-center gap-2 flex-wrap mb-3">
              <DiffBadge d={concept.difficulty} />
              <FreqBadge f={concept.frequency} />
              <span className="flex items-center gap-1 text-xs text-gray-500">
                <Clock className="w-3 h-3" /> {concept.estimated_minutes}m
              </span>
            </div>

            {/* Tags */}
            <div className="flex items-center gap-1 flex-wrap mb-3">
              {(concept.tags || []).map(tag => (
                <span key={tag} className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400/70">
                  {tag}
                </span>
              ))}
            </div>

            {/* Companies */}
            <div className="flex items-center gap-1 flex-wrap">
              <Building2 className="w-3 h-3 text-gray-600 mr-1" />
              {(concept.companies_asking || []).slice(0, 4).map(c => (
                <CompanyTag key={c} name={c} />
              ))}
              {(concept.companies_asking || []).length > 4 && (
                <span className="text-[10px] text-gray-500">+{concept.companies_asking.length - 4}</span>
              )}
            </div>

            {/* Cheat Sheet Preview */}
            {concept.cheat_sheet && (
              <p className="mt-3 text-xs text-gray-500 line-clamp-2">{concept.cheat_sheet}</p>
            )}
          </button>
        ))}
      </div>

      {filteredConcepts.length === 0 && (
        <div className="text-center py-12">
          <Search className="w-10 h-10 mx-auto mb-3 text-gray-600" />
          <p className="text-gray-500">No concepts found matching your search.</p>
        </div>
      )}
    </div>
  )
}

/* ─── Video Tutorials Component ─── */
function VideoTutorials({ topicName }) {
  const [videos, setVideos] = useState([])
  const [bestPick, setBestPick] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeVideo, setActiveVideo] = useState(null)
  const [customSearch, setCustomSearch] = useState('')
  const [searching, setSearching] = useState(false)

  useEffect(() => {
    loadVideos()
  }, [topicName])

  async function loadVideos() {
    setLoading(true)
    setActiveVideo(null)
    try {
      const data = await getRecommendedVideos(topicName, 8)
      setVideos(data.videos || [])
      setBestPick(data.best_pick || null)
    } catch (e) {
      console.error('Failed to load videos:', e)
      setVideos([])
    } finally {
      setLoading(false)
    }
  }

  async function handleCustomSearch(e) {
    e.preventDefault()
    if (!customSearch.trim()) return
    setSearching(true)
    try {
      const data = await searchVideos(topicName, { query: customSearch.trim(), limit: 8 })
      setVideos(data.videos || [])
      setBestPick(data.best_pick || null)
    } catch (e) {
      console.error(e)
    } finally {
      setSearching(false)
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <Loader2 className="w-8 h-8 animate-spin text-red-400 mb-3" />
        <p className="text-sm text-gray-500">Finding the best video tutorials...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Custom search */}
      <form onSubmit={handleCustomSearch} className="flex gap-2">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            value={customSearch}
            onChange={e => setCustomSearch(e.target.value)}
            placeholder={`Search videos for "${topicName}"...`}
            className="w-full pl-10 pr-4 py-2.5 bg-gray-800/60 border border-gray-700 rounded-lg text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-cyan-500/50"
          />
        </div>
        <button
          type="submit"
          disabled={searching}
          className="px-4 py-2.5 bg-red-500/20 hover:bg-red-500/30 text-red-300 rounded-lg text-sm font-medium border border-red-500/30 disabled:opacity-50 flex items-center gap-2"
        >
          {searching ? <Loader2 className="w-4 h-4 animate-spin" /> : <Youtube className="w-4 h-4" />}
          Search
        </button>
        <button
          type="button"
          onClick={loadVideos}
          className="px-3 py-2.5 text-gray-400 hover:text-gray-200 text-sm"
          title="Reset to recommendations"
        >
          Reset
        </button>
      </form>

      {/* Embedded player */}
      {activeVideo && (
        <div className="space-y-2 animate-fade-in">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-gray-200 truncate flex-1 mr-3">
              <Play className="w-4 h-4 inline mr-1 text-red-400" />
              {activeVideo.title}
            </h3>
            <button
              onClick={() => setActiveVideo(null)}
              className="p-1 text-gray-500 hover:text-gray-300 rounded"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="relative w-full rounded-xl overflow-hidden bg-black" style={{ paddingBottom: '56.25%' }}>
            <iframe
              className="absolute inset-0 w-full h-full"
              src={`${activeVideo.embed_url}?autoplay=1&rel=0`}
              title={activeVideo.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <span>{activeVideo.channel}</span>
            <span>&middot;</span>
            <span>{activeVideo.views}</span>
            <span>&middot;</span>
            <span>{activeVideo.duration}</span>
            <a
              href={activeVideo.url}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-auto flex items-center gap-1 text-red-400 hover:text-red-300"
            >
              Open in YouTube <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      )}

      {/* Best pick highlight */}
      {bestPick && !activeVideo && (
        <div
          className="p-4 bg-gradient-to-r from-red-950/30 to-gray-900 border border-red-500/20 rounded-xl cursor-pointer hover:border-red-500/40 transition-all group"
          onClick={() => setActiveVideo(bestPick)}
        >
          <div className="flex gap-4">
            <div className="relative flex-shrink-0 w-48 h-28 rounded-lg overflow-hidden bg-gray-800">
              {bestPick.thumbnail ? (
                <img src={bestPick.thumbnail} alt={bestPick.title} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <Youtube className="w-8 h-8 text-gray-600" />
                </div>
              )}
              <div className="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <Play className="w-10 h-10 text-white" fill="white" />
              </div>
              <span className="absolute bottom-1 right-1 text-[10px] bg-black/80 text-white px-1.5 py-0.5 rounded">
                {bestPick.duration}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <Star className="w-4 h-4 text-yellow-400" />
                <span className="text-xs font-medium text-yellow-400">TOP PICK</span>
              </div>
              <h3 className="font-semibold text-gray-100 line-clamp-2 group-hover:text-white transition-colors">
                {bestPick.title}
              </h3>
              <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                <span className={bestPick.is_trusted_channel ? 'text-green-400 font-medium' : ''}>
                  {bestPick.channel}
                </span>
                {bestPick.is_trusted_channel && <span className="text-green-600">&#10003; Trusted</span>}
                <span>&middot;</span>
                <span>{bestPick.views}</span>
                <span>&middot;</span>
                <span>{bestPick.published}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Video grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {videos
          .filter(v => !activeVideo || v.id !== activeVideo.id)
          .filter(v => !bestPick || activeVideo || v.id !== bestPick.id)
          .map(video => (
            <div
              key={video.id}
              className="flex gap-3 p-3 bg-gray-800/30 border border-gray-700/50 rounded-lg cursor-pointer hover:border-gray-600 hover:bg-gray-800/50 transition-all group"
              onClick={() => setActiveVideo(video)}
            >
              <div className="relative flex-shrink-0 w-36 h-20 rounded-lg overflow-hidden bg-gray-800">
                {video.thumbnail ? (
                  <img src={video.thumbnail} alt={video.title} className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <Youtube className="w-6 h-6 text-gray-600" />
                  </div>
                )}
                <div className="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <Play className="w-7 h-7 text-white" fill="white" />
                </div>
                <span className="absolute bottom-0.5 right-0.5 text-[10px] bg-black/80 text-white px-1 py-0.5 rounded">
                  {video.duration}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium text-gray-200 line-clamp-2 group-hover:text-white transition-colors">
                  {video.title}
                </h4>
                <div className="flex items-center gap-2 mt-1.5 text-xs text-gray-500">
                  <span className={video.is_trusted_channel ? 'text-green-400' : ''}>
                    {video.channel}
                  </span>
                  {video.is_trusted_channel && <span className="text-green-600 text-[10px]">&#10003;</span>}
                </div>
                <div className="flex items-center gap-2 mt-0.5 text-[11px] text-gray-600">
                  <span>{video.views}</span>
                  <span>&middot;</span>
                  <span>{video.published}</span>
                </div>
              </div>
            </div>
          ))}
      </div>

      {videos.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <Youtube className="w-10 h-10 mx-auto mb-3 opacity-40" />
          <p>No videos found. Try a different search.</p>
        </div>
      )}
    </div>
  )
}
