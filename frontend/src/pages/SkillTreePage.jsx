import { useState, useEffect, useRef, useCallback } from 'react'
import {
  GitBranch, Lock, Unlock, CheckCircle2, Star, Zap,
  ChevronRight, ArrowRight, BookOpen, X, Loader2, Brain
} from 'lucide-react'
import { getSkillTree, getNodeDetails, getBridgeLesson } from '../api/client'

const STATUS_COLORS = {
  locked:      { bg: '#1f2937', border: '#374151', text: '#6b7280', glow: 'none' },
  available:   { bg: '#312e81', border: '#6366f1', text: '#a5b4fc', glow: '0 0 20px rgba(99,102,241,0.3)' },
  in_progress: { bg: '#78350f', border: '#f59e0b', text: '#fcd34d', glow: '0 0 20px rgba(245,158,11,0.3)' },
  completed:   { bg: '#064e3b', border: '#10b981', text: '#6ee7b7', glow: '0 0 20px rgba(16,185,129,0.3)' },
  mastered:    { bg: '#4c1d95', border: '#8b5cf6', text: '#c4b5fd', glow: '0 0 20px rgba(139,92,246,0.4)' },
}

const STATUS_ICONS = {
  locked: Lock,
  available: Unlock,
  in_progress: Zap,
  completed: CheckCircle2,
  mastered: Star,
}

export default function SkillTreePage({ userId }) {
  const [treeData, setTreeData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedNode, setSelectedNode] = useState(null)
  const [nodeDetails, setNodeDetails] = useState(null)
  const [loadingDetails, setLoadingDetails] = useState(false)
  const [bridgeLesson, setBridgeLesson] = useState(null)
  const [loadingBridge, setLoadingBridge] = useState(false)
  const [bridgeEdge, setBridgeEdge] = useState(null)
  const svgRef = useRef(null)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [zoom, setZoom] = useState(1)
  const [dragging, setDragging] = useState(false)
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 })

  useEffect(() => {
    loadTree()
  }, [userId])

  async function loadTree() {
    try {
      setLoading(true)
      const data = await getSkillTree(userId)
      setTreeData(data)
    } catch (e) {
      console.error('Failed to load skill tree:', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleNodeClick(node) {
    setSelectedNode(node)
    setBridgeLesson(null)
    setBridgeEdge(null)
    try {
      setLoadingDetails(true)
      const details = await getNodeDetails(userId, node.name)
      setNodeDetails(details)
    } catch (e) {
      console.error('Failed to load node details:', e)
      setNodeDetails(null)
    } finally {
      setLoadingDetails(false)
    }
  }

  async function handleBridgeClick(fromTopic, toTopic) {
    setBridgeEdge({ from: fromTopic, to: toTopic })
    try {
      setLoadingBridge(true)
      const lesson = await getBridgeLesson(userId, fromTopic, toTopic)
      setBridgeLesson(lesson)
    } catch (e) {
      console.error('Failed to get bridge lesson:', e)
      setBridgeLesson(null)
    } finally {
      setLoadingBridge(false)
    }
  }

  // Pan & zoom handlers
  const handleMouseDown = useCallback((e) => {
    if (e.target.closest('.node-group') || e.target.closest('.edge-click-zone')) return
    setDragging(true)
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y })
  }, [pan])

  const handleMouseMove = useCallback((e) => {
    if (!dragging) return
    setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y })
  }, [dragging, dragStart])

  const handleMouseUp = useCallback(() => setDragging(false), [])

  const handleWheel = useCallback((e) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? 0.9 : 1.1
    setZoom(z => Math.max(0.3, Math.min(3, z * delta)))
  }, [])

  // Attach wheel listener with { passive: false } so preventDefault works
  useEffect(() => {
    const svg = svgRef.current
    if (!svg) return
    svg.addEventListener('wheel', handleWheel, { passive: false })
    return () => svg.removeEventListener('wheel', handleWheel)
  }, [handleWheel])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-8 h-8 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    )
  }

  if (!treeData) {
    return (
      <div className="text-center py-20 text-gray-500">
        <GitBranch className="w-12 h-12 mx-auto mb-4 opacity-40" />
        <p>Generate a roadmap first to see your skill tree</p>
      </div>
    )
  }

  const { nodes, edges, category_colors } = treeData
  const SVG_W = 1400
  const SVG_H = 1000

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text flex items-center gap-2">
            <GitBranch className="w-7 h-7" /> Concept Skill Tree
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Click nodes to explore • Click edges for bridge lessons connecting concepts
          </p>
        </div>
        <Legend />
      </div>

      {/* Graph area */}
      <div className="relative glass-card p-0 overflow-hidden" style={{ height: '70vh' }}>
        <svg
          ref={svgRef}
          width="100%" height="100%"
          viewBox={`0 0 ${SVG_W} ${SVG_H}`}
          className="cursor-grab active:cursor-grabbing"
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
        >
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#4b5563" />
            </marker>
          </defs>

          <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
            {/* Edges */}
            {edges.map((edge, i) => {
              const from = nodes.find(n => n.name === edge.from)
              const to = nodes.find(n => n.name === edge.to)
              if (!from || !to) return null

              const x1 = (from.x / 100) * SVG_W
              const y1 = (from.y / 100) * SVG_H
              const x2 = (to.x / 100) * SVG_W
              const y2 = (to.y / 100) * SVG_H

              // Offset endpoints to node edges
              const dx = x2 - x1, dy = y2 - y1
              const len = Math.sqrt(dx*dx + dy*dy) || 1
              const nx = dx/len, ny = dy/len
              const sx = x1 + nx*45, sy = y1 + ny*30
              const ex = x2 - nx*45, ey = y2 - ny*30

              const isHighlighted = selectedNode &&
                (selectedNode.name === edge.from || selectedNode.name === edge.to)

              return (
                <g key={`edge-${i}`}>
                  <line
                    x1={sx} y1={sy} x2={ex} y2={ey}
                    stroke={isHighlighted ? '#6366f1' : '#374151'}
                    strokeWidth={isHighlighted ? 2.5 : 1.5}
                    strokeDasharray={edge.explanation ? '' : '6,4'}
                    markerEnd="url(#arrowhead)"
                    opacity={isHighlighted ? 1 : 0.5}
                  />
                  {/* Clickable zone for bridge lessons */}
                  {edge.explanation && (
                    <line
                      className="edge-click-zone"
                      x1={sx} y1={sy} x2={ex} y2={ey}
                      stroke="transparent"
                      strokeWidth={16}
                      style={{ cursor: 'pointer' }}
                      onClick={() => handleBridgeClick(edge.from, edge.to)}
                    >
                      <title>Click for bridge lesson: {edge.from} → {edge.to}</title>
                    </line>
                  )}
                  {/* Edge label */}
                  {edge.explanation && isHighlighted && (
                    <text
                      x={(sx+ex)/2} y={(sy+ey)/2 - 8}
                      textAnchor="middle"
                      fill="#9ca3af"
                      fontSize="10"
                      className="pointer-events-none"
                    >
                      {edge.explanation.length > 40 ? edge.explanation.slice(0,37)+'...' : edge.explanation}
                    </text>
                  )}
                </g>
              )
            })}

            {/* Nodes */}
            {nodes.map((node) => {
              const x = (node.x / 100) * SVG_W
              const y = (node.y / 100) * SVG_H
              const colors = STATUS_COLORS[node.status] || STATUS_COLORS.locked
              const Icon = STATUS_ICONS[node.status] || Lock
              const isSelected = selectedNode?.name === node.name
              const catColor = category_colors?.[node.category] || '#6366f1'

              return (
                <g
                  key={node.name}
                  className="node-group"
                  style={{ cursor: 'pointer' }}
                  onClick={() => handleNodeClick(node)}
                >
                  {/* Outer glow for selected */}
                  {isSelected && (
                    <circle cx={x} cy={y} r={50}
                      fill="none" stroke={colors.border}
                      strokeWidth={2} opacity={0.3}
                      strokeDasharray="4,3"
                    />
                  )}
                  {/* Node circle */}
                  <circle
                    cx={x} cy={y} r={38}
                    fill={colors.bg}
                    stroke={isSelected ? '#fff' : colors.border}
                    strokeWidth={isSelected ? 3 : 2}
                    filter={node.status !== 'locked' ? 'url(#glow)' : ''}
                  />
                  {/* Category color indicator */}
                  <circle cx={x} cy={y-28} r={5} fill={catColor} stroke={colors.bg} strokeWidth={2} />
                  {/* Mastery ring */}
                  {node.mastery > 0 && (
                    <circle
                      cx={x} cy={y} r={42}
                      fill="none"
                      stroke={colors.border}
                      strokeWidth={3}
                      strokeDasharray={`${node.mastery * 2.64} ${264 - node.mastery * 2.64}`}
                      strokeDashoffset={66}
                      opacity={0.6}
                    />
                  )}
                  {/* Label */}
                  <text
                    x={x} y={y + 4}
                    textAnchor="middle"
                    fill={colors.text}
                    fontSize={node.name.length > 14 ? '9' : '11'}
                    fontWeight="600"
                  >
                    {node.name.length > 18 ? node.name.slice(0,16)+'...' : node.name}
                  </text>
                  {/* Mastery % */}
                  {node.mastery > 0 && (
                    <text x={x} y={y+16} textAnchor="middle" fill={colors.text} fontSize="8" opacity="0.7">
                      {Math.round(node.mastery)}%
                    </text>
                  )}
                </g>
              )
            })}
          </g>
        </svg>

        {/* Zoom controls */}
        <div className="absolute bottom-4 right-4 flex flex-col gap-2">
          <button onClick={() => setZoom(z => Math.min(3, z*1.2))}
            className="w-8 h-8 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 flex items-center justify-center text-lg font-bold">+</button>
          <button onClick={() => setZoom(z => Math.max(0.3, z*0.8))}
            className="w-8 h-8 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 flex items-center justify-center text-lg font-bold">−</button>
          <button onClick={() => { setZoom(1); setPan({x:0,y:0}) }}
            className="w-8 h-8 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 flex items-center justify-center text-xs">⟳</button>
        </div>
      </div>

      {/* Side Panel - Node Details */}
      {selectedNode && (
        <NodeDetailPanel
          node={selectedNode}
          details={nodeDetails}
          loading={loadingDetails}
          onClose={() => { setSelectedNode(null); setNodeDetails(null) }}
          onBridgeClick={handleBridgeClick}
        />
      )}

      {/* Bridge Lesson Modal */}
      {(bridgeEdge || bridgeLesson) && (
        <BridgeLessonModal
          edge={bridgeEdge}
          lesson={bridgeLesson}
          loading={loadingBridge}
          onClose={() => { setBridgeEdge(null); setBridgeLesson(null) }}
        />
      )}
    </div>
  )
}

function Legend() {
  const items = [
    { label: 'Locked', color: STATUS_COLORS.locked },
    { label: 'Available', color: STATUS_COLORS.available },
    { label: 'In Progress', color: STATUS_COLORS.in_progress },
    { label: 'Completed', color: STATUS_COLORS.completed },
    { label: 'Mastered', color: STATUS_COLORS.mastered },
  ]
  return (
    <div className="flex gap-3 text-xs">
      {items.map(({ label, color }) => (
        <div key={label} className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color.border, boxShadow: color.glow }} />
          <span className="text-gray-400">{label}</span>
        </div>
      ))}
    </div>
  )
}

function NodeDetailPanel({ node, details, loading, onClose, onBridgeClick }) {
  const colors = STATUS_COLORS[node.status] || STATUS_COLORS.locked

  return (
    <div className="glass-card p-5 space-y-4 animate-fade-in">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-bold" style={{ color: colors.text }}>{node.name}</h3>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs px-2 py-0.5 rounded-full" style={{ backgroundColor: colors.bg, color: colors.text, border: `1px solid ${colors.border}` }}>
              {node.status.replace('_', ' ')}
            </span>
            <span className="text-xs text-gray-500">{node.category}</span>
            <span className="text-xs text-gray-500">Tier {node.tier}</span>
          </div>
        </div>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-300">
          <X className="w-5 h-5" />
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-indigo-400" />
        </div>
      ) : details ? (
        <>
          <div className="grid grid-cols-3 gap-3">
            <Stat label="Mastery" value={`${Math.round(details.mastery)}%`}
              color={details.mastery >= 70 ? '#10b981' : details.mastery >= 40 ? '#f59e0b' : '#6b7280'} />
            <Stat label="Difficulty" value={details.difficulty} color="#a5b4fc" />
            <Stat label="Est. Days" value={details.estimated_days || '—'} color="#9ca3af" />
          </div>

          {/* Key Concepts */}
          {details.key_concepts?.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-300 mb-2">Key Concepts</h4>
              <div className="flex flex-wrap gap-1.5">
                {details.key_concepts.map((c, i) => (
                  <span key={i} className="text-xs px-2 py-1 rounded-md bg-gray-800 text-gray-300 border border-gray-700">{c}</span>
                ))}
              </div>
            </div>
          )}

          {/* Prerequisites */}
          {details.prerequisites?.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-300 mb-2">Prerequisites</h4>
              <div className="space-y-1.5">
                {details.prerequisites.map((p, i) => (
                  <div key={i} className="flex items-center gap-2 text-sm">
                    <div className="w-2 h-2 rounded-full" style={{
                      backgroundColor: p.status === 'completed' || p.status === 'mastered' ? '#10b981' : '#f59e0b'
                    }} />
                    <span className="text-gray-300">{p.name}</span>
                    <span className="text-xs text-gray-600">{Math.round(p.mastery)}%</span>
                    <button
                      onClick={() => onBridgeClick(p.name, node.name)}
                      className="ml-auto text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
                    >
                      <BookOpen className="w-3 h-3" /> Bridge lesson
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Unlocks */}
          {details.unlocks?.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-300 mb-2">Unlocks</h4>
              <div className="flex flex-wrap gap-2">
                {details.unlocks.map((u, i) => (
                  <span key={i} className="text-xs px-2 py-1 rounded-md bg-gray-800/60 text-gray-400 border border-gray-700/50 flex items-center gap-1">
                    <ArrowRight className="w-3 h-3" />{u}
                  </span>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <p className="text-sm text-gray-500 py-4">No details available</p>
      )}
    </div>
  )
}

function Stat({ label, value, color }) {
  return (
    <div className="bg-gray-800/50 rounded-lg p-3 text-center">
      <div className="text-lg font-bold" style={{ color }}>{value}</div>
      <div className="text-xs text-gray-500">{label}</div>
    </div>
  )
}

function BridgeLessonModal({ edge, lesson, loading, onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="glass-card p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto space-y-4 animate-fade-in">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-bold gradient-text flex items-center gap-2">
              <Brain className="w-5 h-5" /> Bridge Lesson
            </h3>
            {edge && (
              <p className="text-sm text-gray-400 mt-1 flex items-center gap-2">
                <span className="text-indigo-300">{edge.from}</span>
                <ArrowRight className="w-4 h-4 text-gray-600" />
                <span className="text-emerald-300">{edge.to}</span>
              </p>
            )}
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-300">
            <X className="w-5 h-5" />
          </button>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-400 mb-3" />
            <p className="text-sm text-gray-500">Generating bridge lesson…</p>
          </div>
        ) : lesson ? (
          <div className="prose prose-invert prose-sm max-w-none">
            {typeof lesson === 'string' ? (
              <p className="whitespace-pre-wrap text-gray-300">{lesson}</p>
            ) : lesson.bridge_lesson ? (
              <div className="space-y-4">
                {lesson.bridge_lesson.connection_summary && (
                  <div className="bg-indigo-950/30 border border-indigo-500/20 rounded-lg p-4">
                    <h4 className="text-sm font-semibold text-indigo-300 mb-1">How they connect</h4>
                    <p className="text-sm text-gray-300">{lesson.bridge_lesson.connection_summary}</p>
                  </div>
                )}
                {lesson.bridge_lesson.key_concepts?.map((concept, i) => (
                  <div key={i} className="bg-gray-800/50 rounded-lg p-4 border border-gray-700/50">
                    <h4 className="text-sm font-semibold text-gray-200 mb-1">{concept.concept || concept}</h4>
                    {concept.explanation && <p className="text-sm text-gray-400">{concept.explanation}</p>}
                    {concept.example && (
                      <pre className="mt-2 text-xs bg-gray-900 rounded p-2 overflow-x-auto text-gray-300">{concept.example}</pre>
                    )}
                  </div>
                ))}
                {lesson.bridge_lesson.practice_problems?.map((prob, i) => (
                  <div key={i} className="text-sm text-gray-400">
                    <span className="text-gray-300 font-medium">{i+1}.</span> {prob.title || prob}
                    {prob.hint && <span className="text-xs text-gray-600 ml-2">(Hint: {prob.hint})</span>}
                  </div>
                ))}
              </div>
            ) : (
              <p className="whitespace-pre-wrap text-gray-300">{JSON.stringify(lesson, null, 2)}</p>
            )}
          </div>
        ) : (
          <p className="text-sm text-gray-500 py-8 text-center">Failed to generate bridge lesson</p>
        )}
      </div>
    </div>
  )
}
