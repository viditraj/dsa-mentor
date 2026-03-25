import { useState, useEffect, useRef } from 'react'
import { Play, Pause, SkipForward, SkipBack, RotateCcw } from 'lucide-react'

const COLORS = {
  default: '#6366f1',
  highlight: '#f59e0b',
  sorted: '#10b981',
  comparing: '#ef4444',
  pivot: '#8b5cf6',
  visited: '#34d399',
  current: '#f59e0b',
  pointer1: '#ef4444',
  pointer2: '#3b82f6',
  window: '#8b5cf6',
  found: '#10b981',
  miss: '#ef4444',
  dp_filled: '#6366f1',
  dp_current: '#f59e0b',
  dp_dependency: '#8b5cf6',
}

/** Auto-detect the best visualization type from a topic name */
export function detectVisualizationType(topicName) {
  const t = (topicName || '').toLowerCase()
  if (/two.?pointer|2.?pointer/i.test(t)) return 'two_pointers'
  if (/sliding.?window/i.test(t)) return 'sliding_window'
  if (/binary.?search/i.test(t)) return 'binary_search'
  if (/hash|map|set|dictionary/i.test(t)) return 'hash_map'
  if (/queue/i.test(t) && !/priority/i.test(t)) return 'queue'
  if (/stack/i.test(t)) return 'stack'
  if (/heap|priority.?queue/i.test(t)) return 'heap'
  if (/linked.?list/i.test(t)) return 'linked_list'
  if (/tree|bst|trie/i.test(t)) return 'binary_tree'
  if (/graph|bfs|dfs|topological|shortest.?path/i.test(t)) return 'graph'
  if (/dynamic.?prog|dp|memoiz/i.test(t)) return 'dp'
  if (/recursion|backtrack/i.test(t)) return 'recursion'
  if (/sort/i.test(t)) return 'sorting'
  if (/greedy/i.test(t)) return 'greedy'
  if (/bit.?manip/i.test(t)) return 'bit_manipulation'
  if (/string|pattern/i.test(t)) return 'string_ops'
  if (/array/i.test(t)) return 'array'
  return 'array'
}

export default function AlgorithmVisualizer({ type, data, step, topicName }) {
  // Auto-detect from topicName if type is generic
  const effectiveType = (type === 'array' && topicName)
    ? detectVisualizationType(topicName)
    : type

  switch (effectiveType) {
    case 'two_pointers':
      return <TwoPointersVisualizer data={data} />
    case 'sliding_window':
      return <SlidingWindowVisualizer data={data} />
    case 'binary_search':
      return <BinarySearchVisualizer data={data} />
    case 'hash_map':
      return <HashMapVisualizer data={data} />
    case 'queue':
      return <QueueVisualizer data={data} />
    case 'heap':
      return <HeapVisualizer data={data} />
    case 'dp':
      return <DPVisualizer data={data} />
    case 'recursion':
      return <RecursionVisualizer data={data} />
    case 'greedy':
      return <GreedyVisualizer data={data} />
    case 'bit_manipulation':
      return <BitManipVisualizer data={data} />
    case 'string_ops':
      return <StringVisualizer data={data} />
    case 'linked_list':
    case 'linked_list_basic':
    case 'linked_list_operations':
      return <LinkedListVisualizer data={data} step={step} />
    case 'binary_tree':
    case 'binary_tree_basic':
    case 'tree_traversals':
      return <TreeVisualizer data={data} step={step} />
    case 'graph':
    case 'graph_representations':
    case 'bfs_vs_dfs':
      return <GraphVisualizer data={data} step={step} />
    case 'stack':
      return <StackVisualizer data={data} step={step} />
    case 'sorting':
      return <SortingVisualizer data={data} />
    case 'array':
    case 'array_basic':
    case 'array_operations':
    case 'array_patterns':
    default:
      return <ArrayVisualizer data={data} step={step} />
  }
}

// ═══════════════════════════════════════
// ARRAY VISUALIZER
// ═══════════════════════════════════════
function ArrayVisualizer({ data, step }) {
  const arr = data?.initial_state || [5, 3, 8, 1, 9, 2, 7, 4, 6]
  const [values, setValues] = useState(arr)
  const [highlights, setHighlights] = useState({})
  const [animating, setAnimating] = useState(false)
  const [sortStep, setSortStep] = useState(0)
  const [sortSteps, setSortSteps] = useState([])
  const intervalRef = useRef(null)

  // Generate bubble sort steps for animation
  useEffect(() => {
    const steps = []
    const a = [...arr]
    for (let i = 0; i < a.length; i++) {
      for (let j = 0; j < a.length - i - 1; j++) {
        steps.push({ type: 'compare', indices: [j, j + 1], values: [...a] })
        if (a[j] > a[j + 1]) {
          ;[a[j], a[j + 1]] = [a[j + 1], a[j]]
          steps.push({ type: 'swap', indices: [j, j + 1], values: [...a] })
        }
      }
      steps.push({ type: 'sorted', index: a.length - i - 1, values: [...a] })
    }
    setSortSteps(steps)
  }, [])

  function startAnimation() {
    if (animating) {
      clearInterval(intervalRef.current)
      setAnimating(false)
      return
    }
    setAnimating(true)
    let s = sortStep
    intervalRef.current = setInterval(() => {
      if (s >= sortSteps.length) {
        clearInterval(intervalRef.current)
        setAnimating(false)
        return
      }
      const currentStep = sortSteps[s]
      setValues(currentStep.values)
      if (currentStep.type === 'compare') {
        setHighlights({ [currentStep.indices[0]]: 'comparing', [currentStep.indices[1]]: 'comparing' })
      } else if (currentStep.type === 'swap') {
        setHighlights({ [currentStep.indices[0]]: 'highlight', [currentStep.indices[1]]: 'highlight' })
      } else if (currentStep.type === 'sorted') {
        setHighlights(prev => ({ ...prev, [currentStep.index]: 'sorted' }))
      }
      s++
      setSortStep(s)
    }, 300)
  }

  function reset() {
    clearInterval(intervalRef.current)
    setAnimating(false)
    setValues([...arr])
    setHighlights({})
    setSortStep(0)
  }

  const maxVal = Math.max(...values, 1)

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Array Visualization</h4>
        <div className="flex items-center gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700 transition-colors">
            <RotateCcw className="w-4 h-4 text-gray-400" />
          </button>
          <button
            onClick={startAnimation}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium transition-all"
          >
            {animating ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {animating ? 'Pause' : 'Animate Sort'}
          </button>
        </div>
      </div>

      {/* Array bars */}
      <div className="flex items-end gap-1 h-48 px-4 py-2 bg-gray-900 rounded-lg border border-gray-800">
        {values.map((val, i) => {
          const color = highlights[i] === 'comparing' ? COLORS.comparing
            : highlights[i] === 'highlight' ? COLORS.highlight
            : highlights[i] === 'sorted' ? COLORS.sorted
            : COLORS.default
          return (
            <div key={i} className="flex-1 flex flex-col items-center gap-1 transition-all duration-200">
              <div
                className="w-full rounded-t-md transition-all duration-200"
                style={{
                  height: `${(val / maxVal) * 160}px`,
                  backgroundColor: color,
                  boxShadow: highlights[i] ? `0 0 10px ${color}40` : 'none',
                }}
              />
              <span className="text-xs text-gray-500 font-mono">{val}</span>
            </div>
          )
        })}
      </div>

      {/* Index labels */}
      <div className="flex gap-1 px-4">
        {values.map((_, i) => (
          <div key={i} className="flex-1 text-center text-xs text-gray-600 font-mono">[{i}]</div>
        ))}
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-4 text-xs">
        <LegendItem color={COLORS.default} label="Default" />
        <LegendItem color={COLORS.comparing} label="Comparing" />
        <LegendItem color={COLORS.highlight} label="Swapping" />
        <LegendItem color={COLORS.sorted} label="Sorted" />
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// LINKED LIST VISUALIZER
// ═══════════════════════════════════════
function LinkedListVisualizer({ data }) {
  const nodes = data?.initial_state || [1, 2, 3, 4, 5]
  const [highlightIdx, setHighlightIdx] = useState(-1)
  const [traversing, setTraversing] = useState(false)
  const intervalRef = useRef(null)

  function startTraversal() {
    if (traversing) {
      clearInterval(intervalRef.current)
      setTraversing(false)
      setHighlightIdx(-1)
      return
    }
    setTraversing(true)
    let i = 0
    intervalRef.current = setInterval(() => {
      if (i >= nodes.length) {
        clearInterval(intervalRef.current)
        setTraversing(false)
        setHighlightIdx(-1)
        return
      }
      setHighlightIdx(i)
      i++
    }, 600)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Linked List Visualization</h4>
        <button
          onClick={startTraversal}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium transition-all"
        >
          {traversing ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
          {traversing ? 'Stop' : 'Traverse'}
        </button>
      </div>

      <div className="flex items-center gap-0 overflow-x-auto py-8 px-4 bg-gray-900 rounded-lg border border-gray-800">
        <div className="text-xs text-gray-500 mr-3 flex-shrink-0">HEAD →</div>
        {nodes.map((val, i) => (
          <div key={i} className="flex items-center flex-shrink-0">
            <div
              className={`w-16 h-16 rounded-lg border-2 flex flex-col items-center justify-center transition-all duration-300
                ${i === highlightIdx
                  ? 'border-yellow-400 bg-yellow-500/10 scale-110 shadow-lg shadow-yellow-500/20'
                  : i < highlightIdx
                    ? 'border-emerald-500 bg-emerald-500/10'
                    : 'border-indigo-500/50 bg-gray-800'
                }`}
            >
              <span className="font-mono font-bold text-lg">{val}</span>
              <div className="text-xs text-gray-500 border-t border-gray-700 w-full text-center mt-1 pt-0.5">
                next
              </div>
            </div>
            {i < nodes.length - 1 && (
              <div className="flex items-center px-1">
                <div className={`w-6 h-0.5 transition-colors duration-300 ${
                  i < highlightIdx ? 'bg-emerald-500' : 'bg-gray-600'
                }`} />
                <div className={`w-0 h-0 border-t-4 border-b-4 border-l-6 border-t-transparent border-b-transparent transition-colors duration-300 ${
                  i < highlightIdx ? 'border-l-emerald-500' : 'border-l-gray-600'
                }`} style={{ borderLeftWidth: '8px' }} />
              </div>
            )}
          </div>
        ))}
        <div className="text-xs text-gray-500 ml-3 flex-shrink-0">→ NULL</div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// BINARY TREE VISUALIZER
// ═══════════════════════════════════════
function TreeVisualizer({ data }) {
  const treeValues = data?.initial_state || [10, 5, 15, 3, 7, 12, 20]
  const [visitedNodes, setVisitedNodes] = useState(new Set())
  const [currentNode, setCurrentNode] = useState(-1)
  const [traversalOrder, setTraversalOrder] = useState([])
  const [traversing, setTraversing] = useState(false)
  const [traversalType, setTraversalType] = useState('inorder')
  const intervalRef = useRef(null)

  function getTraversalOrder(type) {
    // Build tree structure from array
    const order = []
    function inorder(i) {
      if (i >= treeValues.length || treeValues[i] === null) return
      inorder(2 * i + 1)
      order.push(i)
      inorder(2 * i + 2)
    }
    function preorder(i) {
      if (i >= treeValues.length || treeValues[i] === null) return
      order.push(i)
      preorder(2 * i + 1)
      preorder(2 * i + 2)
    }
    function levelorder() {
      for (let i = 0; i < treeValues.length; i++) {
        if (treeValues[i] !== null) order.push(i)
      }
    }

    if (type === 'inorder') inorder(0)
    else if (type === 'preorder') preorder(0)
    else levelorder()
    return order
  }

  function startTraversal() {
    if (traversing) {
      clearInterval(intervalRef.current)
      setTraversing(false)
      return
    }

    const order = getTraversalOrder(traversalType)
    setTraversalOrder(order)
    setVisitedNodes(new Set())
    setCurrentNode(-1)
    setTraversing(true)

    let i = 0
    intervalRef.current = setInterval(() => {
      if (i >= order.length) {
        clearInterval(intervalRef.current)
        setTraversing(false)
        setCurrentNode(-1)
        return
      }
      setCurrentNode(order[i])
      setVisitedNodes(prev => new Set([...prev, order[i]]))
      i++
    }, 700)
  }

  // Calculate positions for tree rendering
  const levels = Math.ceil(Math.log2(treeValues.length + 1))
  const width = 500
  const levelHeight = 70

  function getNodePos(index) {
    const level = Math.floor(Math.log2(index + 1))
    const posInLevel = index - (Math.pow(2, level) - 1)
    const nodesInLevel = Math.pow(2, level)
    const spacing = width / (nodesInLevel + 1)
    return {
      x: spacing * (posInLevel + 1),
      y: level * levelHeight + 30,
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Binary Tree Visualization</h4>
        <div className="flex items-center gap-2">
          <select
            value={traversalType}
            onChange={e => setTraversalType(e.target.value)}
            className="px-2 py-1 bg-gray-800 border border-gray-700 rounded text-xs text-gray-300"
          >
            <option value="inorder">Inorder</option>
            <option value="preorder">Preorder</option>
            <option value="levelorder">Level-order</option>
          </select>
          <button
            onClick={startTraversal}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium transition-all"
          >
            {traversing ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {traversing ? 'Stop' : 'Traverse'}
          </button>
        </div>
      </div>

      <div className="bg-gray-900 rounded-lg border border-gray-800 p-4 overflow-x-auto">
        <svg width={width} height={levels * levelHeight + 40} className="mx-auto">
          {/* Edges */}
          {treeValues.map((val, i) => {
            if (i === 0 || val === null) return null
            const parentIdx = Math.floor((i - 1) / 2)
            const parent = getNodePos(parentIdx)
            const child = getNodePos(i)
            const visited = visitedNodes.has(i) && visitedNodes.has(parentIdx)
            return (
              <line
                key={`edge-${i}`}
                x1={parent.x} y1={parent.y}
                x2={child.x} y2={child.y}
                stroke={visited ? COLORS.visited : '#374151'}
                strokeWidth={2}
                className="transition-colors duration-300"
              />
            )
          })}
          {/* Nodes */}
          {treeValues.map((val, i) => {
            if (val === null) return null
            const pos = getNodePos(i)
            const isCurrent = i === currentNode
            const isVisited = visitedNodes.has(i)
            const fill = isCurrent ? COLORS.current : isVisited ? COLORS.visited : COLORS.default
            return (
              <g key={`node-${i}`}>
                <circle
                  cx={pos.x} cy={pos.y} r={20}
                  fill={`${fill}30`} stroke={fill} strokeWidth={2}
                  className="transition-all duration-300"
                />
                {isCurrent && (
                  <circle
                    cx={pos.x} cy={pos.y} r={24}
                    fill="none" stroke={COLORS.current} strokeWidth={1}
                    opacity={0.5}
                    className="animate-ping"
                  />
                )}
                <text
                  x={pos.x} y={pos.y + 5}
                  textAnchor="middle" fill="white"
                  className="text-sm font-mono font-bold"
                >
                  {val}
                </text>
              </g>
            )
          })}
        </svg>
      </div>

      {/* Traversal order display */}
      {traversalOrder.length > 0 && (
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-gray-500">{traversalType} order:</span>
          {traversalOrder.map((nodeIdx, i) => (
            <span
              key={i}
              className={`px-2 py-0.5 rounded text-xs font-mono transition-all
                ${visitedNodes.has(nodeIdx) ? 'bg-emerald-500/20 text-emerald-400' : 'bg-gray-800 text-gray-500'}`}
            >
              {treeValues[nodeIdx]}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

// ═══════════════════════════════════════
// GRAPH VISUALIZER
// ═══════════════════════════════════════
function GraphVisualizer({ data }) {
  const nodeCount = 6
  const edges = data?.edges || [[0,1],[0,2],[1,3],[2,3],[2,4],[3,5],[4,5]]
  const [visited, setVisited] = useState(new Set())
  const [current, setCurrent] = useState(-1)
  const [traversing, setTraversing] = useState(false)
  const intervalRef = useRef(null)

  // Arrange nodes in a circle
  const cx = 200, cy = 160, r = 120
  const positions = Array.from({ length: nodeCount }, (_, i) => ({
    x: cx + r * Math.cos((2 * Math.PI * i) / nodeCount - Math.PI / 2),
    y: cy + r * Math.sin((2 * Math.PI * i) / nodeCount - Math.PI / 2),
  }))

  function bfs() {
    if (traversing) {
      clearInterval(intervalRef.current)
      setTraversing(false)
      return
    }
    setVisited(new Set())
    setCurrent(-1)
    setTraversing(true)

    // Build adjacency list
    const adj = Array.from({ length: nodeCount }, () => [])
    edges.forEach(([u, v]) => {
      adj[u].push(v)
      adj[v].push(u)
    })

    const queue = [0]
    const seen = new Set([0])
    const order = [0]
    while (queue.length) {
      const node = queue.shift()
      for (const nb of adj[node]) {
        if (!seen.has(nb)) {
          seen.add(nb)
          queue.push(nb)
          order.push(nb)
        }
      }
    }

    let i = 0
    intervalRef.current = setInterval(() => {
      if (i >= order.length) {
        clearInterval(intervalRef.current)
        setTraversing(false)
        setCurrent(-1)
        return
      }
      setCurrent(order[i])
      setVisited(prev => new Set([...prev, order[i]]))
      i++
    }, 600)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Graph Visualization</h4>
        <button
          onClick={bfs}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium transition-all"
        >
          {traversing ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
          {traversing ? 'Stop' : 'BFS Traversal'}
        </button>
      </div>

      <div className="bg-gray-900 rounded-lg border border-gray-800 p-4 overflow-x-auto">
        <svg width={400} height={320} className="mx-auto">
          {/* Edges */}
          {edges.map(([u, v], i) => (
            <line
              key={`edge-${i}`}
              x1={positions[u].x} y1={positions[u].y}
              x2={positions[v].x} y2={positions[v].y}
              stroke={visited.has(u) && visited.has(v) ? COLORS.visited : '#374151'}
              strokeWidth={2}
              className="transition-colors duration-300"
            />
          ))}
          {/* Nodes */}
          {positions.map((pos, i) => {
            const isCur = i === current
            const isVis = visited.has(i)
            const fill = isCur ? COLORS.current : isVis ? COLORS.visited : COLORS.default
            return (
              <g key={`node-${i}`}>
                <circle
                  cx={pos.x} cy={pos.y} r={22}
                  fill={`${fill}30`} stroke={fill} strokeWidth={2}
                  className="transition-all duration-300"
                />
                <text x={pos.x} y={pos.y + 5} textAnchor="middle" fill="white" className="text-sm font-mono font-bold">
                  {i}
                </text>
              </g>
            )
          })}
        </svg>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// STACK VISUALIZER
// ═══════════════════════════════════════
function StackVisualizer({ data }) {
  const [stack, setStack] = useState(data?.initial_state || [])
  const [input, setInput] = useState('')

  function push() {
    if (input.trim()) {
      setStack(prev => [...prev, input.trim()])
      setInput('')
    }
  }

  function pop() {
    setStack(prev => prev.slice(0, -1))
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Stack Visualization (LIFO)</h4>
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && push()}
            placeholder="Value"
            className="w-20 px-2 py-1 bg-gray-800 border border-gray-700 rounded text-sm text-white"
          />
          <button onClick={push} className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 rounded text-xs font-medium">
            Push
          </button>
          <button onClick={pop} disabled={!stack.length} className="px-3 py-1 bg-red-600 hover:bg-red-500 disabled:opacity-30 rounded text-xs font-medium">
            Pop
          </button>
        </div>
      </div>

      <div className="bg-gray-900 rounded-lg border border-gray-800 p-6 flex flex-col items-center">
        <div className="text-xs text-gray-500 mb-2">← TOP</div>
        <div className="flex flex-col-reverse items-center gap-1 min-h-32">
          {stack.map((val, i) => (
            <div
              key={i}
              className={`w-32 h-10 flex items-center justify-center rounded border-2 font-mono font-bold text-sm transition-all animate-slide-up
                ${i === stack.length - 1
                  ? 'border-yellow-400 bg-yellow-500/10 text-yellow-400'
                  : 'border-indigo-500/50 bg-gray-800 text-gray-300'}`}
            >
              {val}
            </div>
          ))}
          {stack.length === 0 && (
            <div className="text-gray-600 text-sm italic">Empty Stack</div>
          )}
        </div>
        <div className="text-xs text-gray-500 mt-2">BOTTOM →</div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// SORTING VISUALIZER (Interactive)
// ═══════════════════════════════════════
function SortingVisualizer({ data }) {
  const initial = data?.initial_state || [38, 27, 43, 3, 9, 82, 10, 45, 17, 63]
  const [values, setValues] = useState([...initial])
  const [highlights, setHighlights] = useState({})
  const [animating, setAnimating] = useState(false)
  const [algorithm, setAlgorithm] = useState('bubble')
  const intervalRef = useRef(null)

  function reset() {
    clearInterval(intervalRef.current)
    setAnimating(false)
    setValues([...initial])
    setHighlights({})
  }

  // Same as ArrayVisualizer sort animation
  function animate() {
    if (animating) { reset(); return }
    const steps = []
    const a = [...initial]
    for (let i = 0; i < a.length; i++) {
      for (let j = 0; j < a.length - i - 1; j++) {
        steps.push({ comparing: [j, j + 1], values: [...a] })
        if (a[j] > a[j + 1]) {
          ;[a[j], a[j + 1]] = [a[j + 1], a[j]]
          steps.push({ swapping: [j, j + 1], values: [...a] })
        }
      }
    }
    setAnimating(true)
    let s = 0
    intervalRef.current = setInterval(() => {
      if (s >= steps.length) { clearInterval(intervalRef.current); setAnimating(false); return }
      const st = steps[s]
      setValues(st.values)
      const h = {}
      if (st.comparing) { h[st.comparing[0]] = 'comparing'; h[st.comparing[1]] = 'comparing' }
      if (st.swapping) { h[st.swapping[0]] = 'highlight'; h[st.swapping[1]] = 'highlight' }
      setHighlights(h)
      s++
    }, 150)
  }

  const maxVal = Math.max(...values, 1)

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Sorting Visualization</h4>
        <div className="flex items-center gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700">
            <RotateCcw className="w-4 h-4 text-gray-400" />
          </button>
          <button onClick={animate}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium"
          >
            {animating ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {animating ? 'Stop' : 'Sort'}
          </button>
        </div>
      </div>

      <div className="flex items-end gap-1 h-40 px-4 py-2 bg-gray-900 rounded-lg border border-gray-800">
        {values.map((val, i) => {
          const color = highlights[i] === 'comparing' ? COLORS.comparing
            : highlights[i] === 'highlight' ? COLORS.highlight
            : COLORS.default
          return (
            <div key={i} className="flex-1 flex flex-col items-center gap-1 transition-all duration-100">
              <div
                className="w-full rounded-t transition-all duration-100"
                style={{ height: `${(val / maxVal) * 130}px`, backgroundColor: color }}
              />
              <span className="text-xs text-gray-600 font-mono">{val}</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// TWO POINTERS VISUALIZER
// ═══════════════════════════════════════
function TwoPointersVisualizer({ data }) {
  const arr = data?.initial_state || [1, 3, 5, 7, 9, 11, 15, 18]
  const target = data?.target || 20
  const [left, setLeft] = useState(0)
  const [right, setRight] = useState(arr.length - 1)
  const [running, setRunning] = useState(false)
  const [found, setFound] = useState(null)
  const [message, setMessage] = useState(`Find two numbers that sum to ${target}`)
  const intervalRef = useRef(null)

  function start() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    setLeft(0); setRight(arr.length - 1); setFound(null)
    setMessage(`Find two numbers that sum to ${target}`)
    setRunning(true)
    let l = 0, r = arr.length - 1
    intervalRef.current = setInterval(() => {
      if (l >= r) { clearInterval(intervalRef.current); setRunning(false); setMessage('No pair found'); return }
      const sum = arr[l] + arr[r]
      if (sum === target) {
        setLeft(l); setRight(r); setFound([l, r])
        setMessage(`Found! arr[${l}] + arr[${r}] = ${arr[l]} + ${arr[r]} = ${target}`)
        clearInterval(intervalRef.current); setRunning(false); return
      } else if (sum < target) {
        setMessage(`${arr[l]} + ${arr[r]} = ${sum} < ${target} → move left pointer right`)
        l++; setLeft(l)
      } else {
        setMessage(`${arr[l]} + ${arr[r]} = ${sum} > ${target} → move right pointer left`)
        r--; setRight(r)
      }
    }, 900)
  }

  function reset() { clearInterval(intervalRef.current); setRunning(false); setLeft(0); setRight(arr.length - 1); setFound(null); setMessage(`Find two numbers that sum to ${target}`) }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Two Pointers — Pair Sum</h4>
        <div className="flex gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700"><RotateCcw className="w-4 h-4 text-gray-400" /></button>
          <button onClick={start} className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium">
            {running ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {running ? 'Pause' : 'Animate'}
          </button>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-sm text-center text-gray-300">{message}</div>
      <div className="flex items-end justify-center gap-2 py-6 px-4 bg-gray-900 rounded-lg border border-gray-800 min-h-[140px]">
        {arr.map((val, i) => {
          const isLeft = i === left
          const isRight = i === right
          const isFound = found && (i === found[0] || i === found[1])
          const bg = isFound ? COLORS.found : isLeft ? COLORS.pointer1 : isRight ? COLORS.pointer2 : COLORS.default
          return (
            <div key={i} className="flex flex-col items-center gap-2 transition-all duration-300">
              {isLeft && <span className="text-xs font-bold text-red-400 animate-bounce">L</span>}
              {isRight && !isLeft && <span className="text-xs font-bold text-blue-400 animate-bounce">R</span>}
              {!isLeft && !isRight && <span className="text-xs text-transparent">.</span>}
              <div className="w-12 h-12 rounded-lg flex items-center justify-center font-mono font-bold text-white transition-all duration-300"
                style={{ backgroundColor: `${bg}${isFound ? '' : '80'}`, border: `2px solid ${bg}`, transform: (isLeft || isRight) ? 'scale(1.15)' : 'scale(1)', boxShadow: isFound ? `0 0 20px ${bg}60` : 'none' }}>
                {val}
              </div>
              <span className="text-xs text-gray-600 font-mono">[{i}]</span>
            </div>
          )
        })}
      </div>
      <div className="flex gap-4 text-xs">
        <LegendItem color={COLORS.pointer1} label="Left Pointer" />
        <LegendItem color={COLORS.pointer2} label="Right Pointer" />
        <LegendItem color={COLORS.found} label="Found!" />
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// SLIDING WINDOW VISUALIZER
// ═══════════════════════════════════════
function SlidingWindowVisualizer({ data }) {
  const arr = data?.initial_state || [2, 1, 5, 1, 3, 2, 8, 4, 3]
  const k = data?.window_size || 3
  const [windowStart, setWindowStart] = useState(0)
  const [running, setRunning] = useState(false)
  const [maxSum, setMaxSum] = useState(0)
  const [maxStart, setMaxStart] = useState(0)
  const [currentSum, setCurrentSum] = useState(0)
  const [message, setMessage] = useState(`Find max sum subarray of size ${k}`)
  const intervalRef = useRef(null)

  function start() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    // Initialize
    let sum = arr.slice(0, k).reduce((a, b) => a + b, 0)
    let best = sum, bestIdx = 0
    setWindowStart(0); setCurrentSum(sum); setMaxSum(sum); setMaxStart(0); setRunning(true)
    setMessage(`Window [0..${k - 1}]: sum = ${sum}`)
    let ws = 0
    intervalRef.current = setInterval(() => {
      ws++
      if (ws + k > arr.length) { clearInterval(intervalRef.current); setRunning(false); setMessage(`Max sum = ${best} at index ${bestIdx}`); setWindowStart(bestIdx); return }
      sum = sum - arr[ws - 1] + arr[ws + k - 1]
      setWindowStart(ws); setCurrentSum(sum)
      setMessage(`Slide: -${arr[ws - 1]} +${arr[ws + k - 1]} → sum = ${sum}`)
      if (sum > best) { best = sum; bestIdx = ws; setMaxSum(sum); setMaxStart(ws) }
    }, 800)
  }

  function reset() { clearInterval(intervalRef.current); setRunning(false); setWindowStart(0); setCurrentSum(0); setMaxSum(0); setMaxStart(0); setMessage(`Find max sum subarray of size ${k}`) }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Sliding Window — Max Sum (k={k})</h4>
        <div className="flex gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700"><RotateCcw className="w-4 h-4 text-gray-400" /></button>
          <button onClick={start} className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium">
            {running ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {running ? 'Pause' : 'Animate'}
          </button>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-sm text-center text-gray-300">{message}</div>
      <div className="relative flex items-end justify-center gap-1 py-8 px-4 bg-gray-900 rounded-lg border border-gray-800 min-h-[180px]">
        {arr.map((val, i) => {
          const inWindow = i >= windowStart && i < windowStart + k
          const maxVal = Math.max(...arr, 1)
          return (
            <div key={i} className="flex flex-col items-center gap-1 transition-all duration-300" style={{ flex: 1 }}>
              <div className="w-full rounded-t-md transition-all duration-300"
                style={{
                  height: `${(val / maxVal) * 100}px`,
                  backgroundColor: inWindow ? COLORS.window : COLORS.default,
                  opacity: inWindow ? 1 : 0.4,
                  boxShadow: inWindow ? `0 0 12px ${COLORS.window}40` : 'none',
                }} />
              <span className={`text-xs font-mono transition-colors ${inWindow ? 'text-purple-300 font-bold' : 'text-gray-600'}`}>{val}</span>
              <span className="text-xs text-gray-700 font-mono">[{i}]</span>
            </div>
          )
        })}
      </div>
      <div className="flex justify-between text-xs">
        <span className="text-gray-500">Current sum: <span className="text-purple-400 font-bold">{currentSum}</span></span>
        <span className="text-gray-500">Best sum: <span className="text-emerald-400 font-bold">{maxSum}</span></span>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// BINARY SEARCH VISUALIZER
// ═══════════════════════════════════════
function BinarySearchVisualizer({ data }) {
  const arr = data?.initial_state || [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
  const target = data?.target || 23
  const [lo, setLo] = useState(0)
  const [hi, setHi] = useState(arr.length - 1)
  const [mid, setMid] = useState(-1)
  const [running, setRunning] = useState(false)
  const [foundIdx, setFoundIdx] = useState(-1)
  const [message, setMessage] = useState(`Search for ${target} in sorted array`)
  const intervalRef = useRef(null)

  function start() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    let l = 0, r = arr.length - 1
    setLo(l); setHi(r); setMid(-1); setFoundIdx(-1); setRunning(true)
    intervalRef.current = setInterval(() => {
      if (l > r) { clearInterval(intervalRef.current); setRunning(false); setMessage(`${target} not found!`); return }
      const m = Math.floor((l + r) / 2)
      setMid(m); setLo(l); setHi(r)
      if (arr[m] === target) {
        setFoundIdx(m); setMessage(`Found ${target} at index ${m}!`)
        clearInterval(intervalRef.current); setRunning(false); return
      } else if (arr[m] < target) {
        setMessage(`arr[${m}]=${arr[m]} < ${target} → search right half`)
        l = m + 1
      } else {
        setMessage(`arr[${m}]=${arr[m]} > ${target} → search left half`)
        r = m - 1
      }
    }, 1000)
  }

  function reset() { clearInterval(intervalRef.current); setRunning(false); setLo(0); setHi(arr.length - 1); setMid(-1); setFoundIdx(-1); setMessage(`Search for ${target} in sorted array`) }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Binary Search — Target: {target}</h4>
        <div className="flex gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700"><RotateCcw className="w-4 h-4 text-gray-400" /></button>
          <button onClick={start} className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium">
            {running ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {running ? 'Pause' : 'Search'}
          </button>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-sm text-center text-gray-300">{message}</div>
      <div className="flex items-center justify-center gap-1 py-6 px-4 bg-gray-900 rounded-lg border border-gray-800">
        {arr.map((val, i) => {
          const isLo = i === lo
          const isHi = i === hi
          const isMid = i === mid
          const isFound = i === foundIdx
          const inRange = i >= lo && i <= hi
          const bg = isFound ? COLORS.found : isMid ? COLORS.current : isLo ? COLORS.pointer1 : isHi ? COLORS.pointer2 : inRange ? COLORS.default : '#374151'
          return (
            <div key={i} className="flex flex-col items-center gap-1 transition-all duration-300">
              <span className="text-xs font-bold h-4" style={{ color: isLo ? COLORS.pointer1 : isHi ? COLORS.pointer2 : isMid ? COLORS.current : 'transparent' }}>
                {isLo && 'lo'}{isHi && 'hi'}{isMid && !isLo && !isHi && 'mid'}
              </span>
              <div className="w-11 h-11 rounded-lg flex items-center justify-center font-mono text-sm font-bold text-white transition-all duration-300"
                style={{
                  backgroundColor: `${bg}${isFound || isMid ? '' : inRange ? '60' : '30'}`,
                  border: `2px solid ${bg}`,
                  transform: isMid || isFound ? 'scale(1.2)' : 'scale(1)',
                  boxShadow: isFound ? `0 0 20px ${COLORS.found}60` : isMid ? `0 0 12px ${COLORS.current}40` : 'none',
                }}>
                {val}
              </div>
              <span className="text-xs text-gray-700 font-mono">[{i}]</span>
            </div>
          )
        })}
      </div>
      <div className="flex gap-4 text-xs">
        <LegendItem color={COLORS.pointer1} label="Low" />
        <LegendItem color={COLORS.pointer2} label="High" />
        <LegendItem color={COLORS.current} label="Mid" />
        <LegendItem color={COLORS.found} label="Found" />
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// HASH MAP VISUALIZER
// ═══════════════════════════════════════
function HashMapVisualizer({ data }) {
  const entries = data?.entries || [['apple', 5], ['banana', 3], ['cherry', 8], ['date', 2], ['elderberry', 7]]
  const bucketCount = 7
  const [buckets, setBuckets] = useState(Array.from({ length: bucketCount }, () => []))
  const [currentEntry, setCurrentEntry] = useState(-1)
  const [running, setRunning] = useState(false)
  const [message, setMessage] = useState('Watch how keys are hashed into buckets')
  const [hashCalc, setHashCalc] = useState('')
  const intervalRef = useRef(null)

  function simpleHash(key) {
    let h = 0
    for (let c of String(key)) h = (h * 31 + c.charCodeAt(0)) % bucketCount
    return h
  }

  function start() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    setBuckets(Array.from({ length: bucketCount }, () => [])); setCurrentEntry(-1); setRunning(true)
    let idx = 0
    const newBuckets = Array.from({ length: bucketCount }, () => [])
    intervalRef.current = setInterval(() => {
      if (idx >= entries.length) { clearInterval(intervalRef.current); setRunning(false); setMessage('All entries inserted!'); setHashCalc(''); return }
      const [key, val] = entries[idx]
      const bucket = simpleHash(key)
      setHashCalc(`hash("${key}") % ${bucketCount} = ${bucket}`)
      setMessage(`Insert "${key}": ${val} → bucket ${bucket}`)
      newBuckets[bucket] = [...newBuckets[bucket], { key, val }]
      setBuckets(newBuckets.map(b => [...b]))
      setCurrentEntry(bucket)
      idx++
    }, 1200)
  }

  function reset() { clearInterval(intervalRef.current); setRunning(false); setBuckets(Array.from({ length: bucketCount }, () => [])); setCurrentEntry(-1); setMessage('Watch how keys are hashed into buckets'); setHashCalc('') }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Hash Map — Bucket Hashing</h4>
        <div className="flex gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700"><RotateCcw className="w-4 h-4 text-gray-400" /></button>
          <button onClick={start} className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium">
            {running ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {running ? 'Pause' : 'Insert All'}
          </button>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-sm text-center text-gray-300">{message}</div>
      {hashCalc && <div className="text-center text-xs text-purple-400 font-mono">{hashCalc}</div>}
      <div className="space-y-1.5 bg-gray-900 rounded-lg border border-gray-800 p-4">
        {buckets.map((bucket, i) => (
          <div key={i} className="flex items-center gap-2">
            <span className={`w-8 h-8 rounded flex items-center justify-center text-xs font-mono font-bold transition-all duration-300 ${
              i === currentEntry ? 'bg-yellow-500/20 text-yellow-400 ring-2 ring-yellow-400/50' : 'bg-gray-800 text-gray-500'
            }`}>{i}</span>
            <div className="flex-1 flex items-center gap-1 min-h-[32px]">
              {bucket.length === 0 ? (
                <span className="text-xs text-gray-700 italic">empty</span>
              ) : bucket.map((entry, j) => (
                <div key={j} className="flex items-center">
                  {j > 0 && <span className="text-gray-600 mx-0.5">→</span>}
                  <span className="px-2 py-1 rounded text-xs font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 animate-slide-up">
                    {entry.key}:{entry.val}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// QUEUE VISUALIZER
// ═══════════════════════════════════════
function QueueVisualizer({ data }) {
  const [queue, setQueue] = useState(data?.initial_state || [])
  const [input, setInput] = useState('')
  const [lastAction, setLastAction] = useState('')

  function enqueue() {
    if (!input.trim()) return
    setQueue(prev => [...prev, input.trim()])
    setLastAction(`Enqueued "${input.trim()}" at rear`)
    setInput('')
  }

  function dequeue() {
    if (!queue.length) return
    setLastAction(`Dequeued "${queue[0]}" from front`)
    setQueue(prev => prev.slice(1))
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Queue Visualization (FIFO)</h4>
        <div className="flex items-center gap-2">
          <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && enqueue()} placeholder="Value" className="w-20 px-2 py-1 bg-gray-800 border border-gray-700 rounded text-sm text-white" />
          <button onClick={enqueue} className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 rounded text-xs font-medium">Enqueue</button>
          <button onClick={dequeue} disabled={!queue.length} className="px-3 py-1 bg-red-600 hover:bg-red-500 disabled:opacity-30 rounded text-xs font-medium">Dequeue</button>
        </div>
      </div>
      {lastAction && <div className="p-2 rounded bg-gray-900 border border-gray-800 text-xs text-center text-gray-400">{lastAction}</div>}
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
        <div className="flex items-center justify-center gap-1 min-h-[60px]">
          <span className="text-xs text-emerald-400 font-bold mr-2">FRONT →</span>
          {queue.length === 0 ? (
            <span className="text-gray-600 text-sm italic">Empty Queue</span>
          ) : queue.map((val, i) => (
            <div key={i} className={`w-14 h-14 flex items-center justify-center rounded-lg border-2 font-mono font-bold text-sm transition-all animate-slide-up
              ${i === 0 ? 'border-emerald-400 bg-emerald-500/10 text-emerald-400' :
                i === queue.length - 1 ? 'border-blue-400 bg-blue-500/10 text-blue-400' :
                'border-indigo-500/50 bg-gray-800 text-gray-300'}`}
            >
              {val}
            </div>
          ))}
          <span className="text-xs text-blue-400 font-bold ml-2">← REAR</span>
        </div>
      </div>
      <div className="flex gap-4 text-xs">
        <LegendItem color={COLORS.found} label="Front (Dequeue)" />
        <LegendItem color={COLORS.pointer2} label="Rear (Enqueue)" />
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// HEAP / PRIORITY QUEUE VISUALIZER
// ═══════════════════════════════════════
function HeapVisualizer({ data }) {
  const [heap, setHeap] = useState(data?.initial_state || [])
  const [highlightIdx, setHighlightIdx] = useState(-1)
  const [running, setRunning] = useState(false)
  const [message, setMessage] = useState('Min-Heap: parent ≤ children. Insert values to see bubbling.')
  const [input, setInput] = useState('')
  const intervalRef = useRef(null)

  function insert(val) {
    const num = parseInt(val)
    if (isNaN(num)) return
    const h = [...heap, num]
    setHeap(h); setInput('')
    // Animate bubble up
    let i = h.length - 1
    setHighlightIdx(i); setMessage(`Inserted ${num}. Bubbling up...`)
    setRunning(true)
    const bubbleUp = () => {
      if (i <= 0) { setRunning(false); setHighlightIdx(-1); setMessage('Heap property restored!'); return }
      const parent = Math.floor((i - 1) / 2)
      if (h[parent] > h[i]) {
        ;[h[parent], h[i]] = [h[i], h[parent]]
        setHeap([...h]); setHighlightIdx(parent)
        setMessage(`Swap ${h[i]} ↔ ${h[parent]}: child < parent`)
        i = parent
        setTimeout(bubbleUp, 600)
      } else {
        setRunning(false); setHighlightIdx(-1); setMessage('Heap property satisfied!')
      }
    }
    setTimeout(bubbleUp, 400)
  }

  function extractMin() {
    if (heap.length === 0) return
    const h = [...heap]
    const min = h[0]
    h[0] = h[h.length - 1]; h.pop()
    setHeap([...h]); setMessage(`Extracted min: ${min}. Bubbling down...`)
    setRunning(true)
    let i = 0
    const bubbleDown = () => {
      const left = 2 * i + 1, right = 2 * i + 2
      let smallest = i
      if (left < h.length && h[left] < h[smallest]) smallest = left
      if (right < h.length && h[right] < h[smallest]) smallest = right
      if (smallest !== i) {
        ;[h[i], h[smallest]] = [h[smallest], h[i]]
        setHeap([...h]); setHighlightIdx(smallest)
        setMessage(`Swap ${h[smallest]} ↔ ${h[i]}`)
        i = smallest
        setTimeout(bubbleDown, 600)
      } else {
        setRunning(false); setHighlightIdx(-1); setMessage('Heap property restored!')
      }
    }
    setTimeout(bubbleDown, 400)
  }

  function autoFill() {
    const vals = [15, 10, 20, 8, 12, 25, 5, 3]
    let i = 0
    const h = []
    intervalRef.current = setInterval(() => {
      if (i >= vals.length) { clearInterval(intervalRef.current); return }
      h.push(vals[i])
      // Simple heapify up
      let j = h.length - 1
      while (j > 0) { const p = Math.floor((j - 1) / 2); if (h[p] > h[j]) { [h[p], h[j]] = [h[j], h[p]]; j = p } else break }
      setHeap([...h]); setMessage(`Inserted ${vals[i]}`)
      i++
    }, 500)
  }

  const width = 400, levelH = 60
  function getPos(idx) {
    const level = Math.floor(Math.log2(idx + 1))
    const pos = idx - (Math.pow(2, level) - 1)
    const count = Math.pow(2, level)
    return { x: (width / (count + 1)) * (pos + 1), y: level * levelH + 30 }
  }
  const levels = heap.length > 0 ? Math.floor(Math.log2(heap.length)) + 1 : 1

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Min-Heap / Priority Queue</h4>
        <div className="flex items-center gap-2">
          <input type="number" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && insert(input)} placeholder="Value" className="w-16 px-2 py-1 bg-gray-800 border border-gray-700 rounded text-sm text-white" />
          <button onClick={() => insert(input)} disabled={running} className="px-2 py-1 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-30 rounded text-xs font-medium">Insert</button>
          <button onClick={extractMin} disabled={running || !heap.length} className="px-2 py-1 bg-red-600 hover:bg-red-500 disabled:opacity-30 rounded text-xs font-medium">Extract Min</button>
          <button onClick={autoFill} disabled={running} className="px-2 py-1 bg-purple-600 hover:bg-purple-500 disabled:opacity-30 rounded text-xs font-medium">Auto Fill</button>
        </div>
      </div>
      <div className="p-2 rounded bg-gray-900 border border-gray-800 text-xs text-center text-gray-400">{message}</div>
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-4 overflow-x-auto">
        {heap.length === 0 ? (
          <div className="text-center text-gray-600 py-8">Insert values to build the heap</div>
        ) : (
          <svg width={width} height={levels * levelH + 30} className="mx-auto">
            {heap.map((_, i) => {
              if (i === 0) return null
              const parent = Math.floor((i - 1) / 2)
              const p = getPos(parent), c = getPos(i)
              return <line key={`e-${i}`} x1={p.x} y1={p.y} x2={c.x} y2={c.y} stroke="#374151" strokeWidth={2} />
            })}
            {heap.map((val, i) => {
              const pos = getPos(i)
              const isCur = i === highlightIdx
              const fill = isCur ? COLORS.current : i === 0 ? COLORS.found : COLORS.default
              return (
                <g key={`n-${i}`}>
                  <circle cx={pos.x} cy={pos.y} r={18} fill={`${fill}30`} stroke={fill} strokeWidth={2} className="transition-all duration-300" />
                  {isCur && <circle cx={pos.x} cy={pos.y} r={22} fill="none" stroke={COLORS.current} strokeWidth={1} opacity={0.5} />}
                  <text x={pos.x} y={pos.y + 5} textAnchor="middle" fill="white" className="text-xs font-mono font-bold">{val}</text>
                </g>
              )
            })}
          </svg>
        )}
      </div>
      <div className="flex items-center gap-1 text-xs text-gray-600 font-mono">
        Array: [{heap.join(', ')}]
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// DYNAMIC PROGRAMMING VISUALIZER
// ═══════════════════════════════════════
function DPVisualizer({ data }) {
  const [mode, setMode] = useState(data?.mode || 'fibonacci')
  const n = data?.n || 8
  const [dp, setDp] = useState(Array(n + 1).fill(null))
  const [currentIdx, setCurrentIdx] = useState(-1)
  const [running, setRunning] = useState(false)
  const [message, setMessage] = useState('Watch the DP table fill step by step')
  const intervalRef = useRef(null)

  function startFibonacci() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    const table = Array(n + 1).fill(null)
    table[0] = 0; table[1] = 1
    setDp([...table]); setCurrentIdx(1); setRunning(true)
    setMessage('Fibonacci: dp[0]=0, dp[1]=1')
    let i = 2
    intervalRef.current = setInterval(() => {
      if (i > n) { clearInterval(intervalRef.current); setRunning(false); setMessage(`Done! fib(${n}) = ${table[n]}`); return }
      table[i] = table[i - 1] + table[i - 2]
      setDp([...table]); setCurrentIdx(i)
      setMessage(`dp[${i}] = dp[${i - 1}] + dp[${i - 2}] = ${table[i - 1]} + ${table[i - 2]} = ${table[i]}`)
      i++
    }, 800)
  }

  function startClimbingStairs() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    const table = Array(n + 1).fill(null)
    table[0] = 1; table[1] = 1
    setDp([...table]); setCurrentIdx(1); setRunning(true)
    setMessage('Climbing Stairs: dp[0]=1, dp[1]=1')
    let i = 2
    intervalRef.current = setInterval(() => {
      if (i > n) { clearInterval(intervalRef.current); setRunning(false); setMessage(`Ways to climb ${n} stairs = ${table[n]}`); return }
      table[i] = table[i - 1] + table[i - 2]
      setDp([...table]); setCurrentIdx(i)
      setMessage(`dp[${i}] = dp[${i - 1}] + dp[${i - 2}] = ${table[i - 1]} + ${table[i - 2]} = ${table[i]}`)
      i++
    }, 800)
  }

  function reset() { clearInterval(intervalRef.current); setRunning(false); setDp(Array(n + 1).fill(null)); setCurrentIdx(-1); setMessage('Watch the DP table fill step by step') }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Dynamic Programming — Table Filling</h4>
        <div className="flex gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700"><RotateCcw className="w-4 h-4 text-gray-400" /></button>
          <button onClick={startFibonacci} disabled={running} className="px-2 py-1 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 rounded-lg text-xs font-medium">Fibonacci</button>
          <button onClick={startClimbingStairs} disabled={running} className="px-2 py-1 bg-purple-600 hover:bg-purple-500 disabled:opacity-30 rounded-lg text-xs font-medium">Climbing Stairs</button>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-sm text-center text-gray-300 font-mono">{message}</div>
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-4 overflow-x-auto">
        {/* Index row */}
        <div className="flex justify-center gap-1 mb-1">
          {dp.map((_, i) => <div key={i} className="w-14 text-center text-xs text-gray-600 font-mono">i={i}</div>)}
        </div>
        {/* Values */}
        <div className="flex justify-center gap-1">
          {dp.map((val, i) => {
            const isCurrent = i === currentIdx
            const isFilled = val !== null
            const isDependency = (i === currentIdx - 1 || i === currentIdx - 2) && currentIdx >= 2
            return (
              <div key={i} className={`w-14 h-14 rounded-lg flex items-center justify-center font-mono text-sm font-bold transition-all duration-300 border-2 ${
                isCurrent ? 'border-yellow-400 bg-yellow-500/15 text-yellow-400 scale-110 shadow-lg shadow-yellow-500/20' :
                isDependency ? 'border-purple-400 bg-purple-500/10 text-purple-300' :
                isFilled ? 'border-indigo-500/50 bg-indigo-500/10 text-indigo-300' :
                'border-gray-700 bg-gray-800/50 text-gray-600'
              }`}>
                {val !== null ? val : '?'}
              </div>
            )
          })}
        </div>
        {/* Arrows showing dependencies */}
        {currentIdx >= 2 && (
          <div className="flex justify-center gap-1 mt-1">
            {dp.map((_, i) => (
              <div key={i} className="w-14 text-center text-xs">
                {i === currentIdx - 1 && <span className="text-purple-400">↗</span>}
                {i === currentIdx - 2 && <span className="text-purple-400">↗</span>}
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="flex gap-4 text-xs">
        <LegendItem color={COLORS.dp_current} label="Computing" />
        <LegendItem color="#8b5cf6" label="Dependencies" />
        <LegendItem color={COLORS.dp_filled} label="Computed" />
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// RECURSION / BACKTRACKING VISUALIZER
// ═══════════════════════════════════════
function RecursionVisualizer({ data }) {
  const [callStack, setCallStack] = useState([])
  const [running, setRunning] = useState(false)
  const [message, setMessage] = useState('Watch the recursive call stack for factorial(5)')
  const [result, setResult] = useState(null)
  const intervalRef = useRef(null)

  function startFactorial() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    setCallStack([]); setResult(null); setRunning(true)
    const n = 5
    // Build the sequence of stack operations
    const ops = []
    for (let i = n; i >= 0; i--) ops.push({ action: 'push', frame: `factorial(${i})`, value: i })
    for (let i = 0; i <= n; i++) ops.push({ action: 'pop', frame: `factorial(${i})`, returnVal: i === 0 ? 1 : null })

    let idx = 0
    const stack = []
    let retVal = 1
    intervalRef.current = setInterval(() => {
      if (idx >= ops.length) { clearInterval(intervalRef.current); setRunning(false); setResult(retVal); setMessage(`factorial(${n}) = ${retVal}`); return }
      const op = ops[idx]
      if (op.action === 'push') {
        stack.push({ name: op.frame, status: 'waiting' })
        setCallStack([...stack]); setMessage(`Call: ${op.frame}`)
      } else {
        const top = stack[stack.length - 1]
        if (stack.length > 0) {
          retVal = op.returnVal !== null ? 1 : retVal * (stack.length)
          top.status = 'returning'
          top.returnVal = retVal
          setCallStack([...stack]); setMessage(`Return: ${top.name} → ${retVal}`)
          setTimeout(() => { stack.pop(); setCallStack([...stack]) }, 350)
        }
      }
      idx++
    }, 700)
  }

  function startFibRecursion() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    setCallStack([]); setResult(null); setRunning(true)
    const calls = []
    function fib(n, depth) {
      calls.push({ action: 'push', frame: `fib(${n})`, depth })
      if (n <= 1) { calls.push({ action: 'pop', frame: `fib(${n})`, returnVal: n, depth }); return n }
      const a = fib(n - 1, depth + 1)
      const b = fib(n - 2, depth + 1)
      calls.push({ action: 'pop', frame: `fib(${n})`, returnVal: a + b, depth })
      return a + b
    }
    fib(5, 0)

    let idx = 0
    const stack = []
    intervalRef.current = setInterval(() => {
      if (idx >= calls.length) { clearInterval(intervalRef.current); setRunning(false); setMessage('fib(5) = 5. Notice the repeated subproblems — this is why DP is better!'); setResult(5); return }
      const op = calls[idx]
      if (op.action === 'push') {
        stack.push({ name: op.frame, status: 'computing', depth: op.depth })
        setCallStack([...stack]); setMessage(`Call: ${op.frame}`)
      } else {
        if (stack.length > 0) {
          stack[stack.length - 1].status = 'returning'
          stack[stack.length - 1].returnVal = op.returnVal
          setCallStack([...stack]); setMessage(`Return: ${op.frame} → ${op.returnVal}`)
          setTimeout(() => { stack.pop(); setCallStack([...stack]) }, 200)
        }
      }
      idx++
    }, 350)
  }

  function reset() { clearInterval(intervalRef.current); setRunning(false); setCallStack([]); setResult(null); setMessage('Watch the recursive call stack') }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Recursion — Call Stack</h4>
        <div className="flex gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700"><RotateCcw className="w-4 h-4 text-gray-400" /></button>
          <button onClick={startFactorial} disabled={running} className="px-2 py-1 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 rounded-lg text-xs font-medium">Factorial(5)</button>
          <button onClick={startFibRecursion} disabled={running} className="px-2 py-1 bg-purple-600 hover:bg-purple-500 disabled:opacity-30 rounded-lg text-xs font-medium">Fib(5)</button>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-sm text-center text-gray-300">{message}</div>
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-4 min-h-[200px]">
        <div className="flex flex-col-reverse items-center gap-1">
          {callStack.length === 0 && <div className="text-gray-600 text-sm py-8">Click a button to visualize recursion</div>}
          {callStack.map((frame, i) => (
            <div key={i} className={`w-56 px-4 py-2 rounded-lg border-2 text-sm font-mono flex justify-between items-center transition-all animate-slide-up ${
              frame.status === 'returning' ? 'border-emerald-400 bg-emerald-500/10 text-emerald-400' :
              i === callStack.length - 1 ? 'border-yellow-400 bg-yellow-500/10 text-yellow-400' :
              'border-indigo-500/50 bg-gray-800 text-gray-300'
            }`}>
              <span>{frame.name}</span>
              {frame.returnVal !== undefined && <span className="text-xs bg-emerald-500/20 px-1.5 py-0.5 rounded">→ {frame.returnVal}</span>}
            </div>
          ))}
        </div>
        {callStack.length > 0 && <div className="text-center text-xs text-gray-600 mt-2">↑ TOP OF STACK</div>}
      </div>
      {result !== null && <div className="text-center text-sm text-emerald-400 font-bold">Result: {result}</div>}
    </div>
  )
}

// ═══════════════════════════════════════
// GREEDY ALGORITHM VISUALIZER
// ═══════════════════════════════════════
function GreedyVisualizer({ data }) {
  const coins = data?.coins || [25, 10, 5, 1]
  const target = data?.target || 67
  const [remaining, setRemaining] = useState(target)
  const [selected, setSelected] = useState([])
  const [running, setRunning] = useState(false)
  const [message, setMessage] = useState(`Coin Change: Make ${target}¢ with fewest coins`)
  const intervalRef = useRef(null)

  function start() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    setRemaining(target); setSelected([]); setRunning(true)
    let rem = target
    let coinIdx = 0
    const sel = []
    intervalRef.current = setInterval(() => {
      if (rem === 0 || coinIdx >= coins.length) {
        clearInterval(intervalRef.current); setRunning(false)
        setMessage(`Done! Used ${sel.length} coins: ${sel.join(' + ')} = ${target}¢`)
        return
      }
      if (coins[coinIdx] <= rem) {
        sel.push(coins[coinIdx])
        rem -= coins[coinIdx]
        setSelected([...sel]); setRemaining(rem)
        setMessage(`Take ${coins[coinIdx]}¢ → remaining: ${rem}¢`)
      } else {
        coinIdx++
        setMessage(`${coins[coinIdx - 1]}¢ too large, try next denomination`)
      }
    }, 600)
  }

  function reset() { clearInterval(intervalRef.current); setRunning(false); setRemaining(target); setSelected([]); setMessage(`Coin Change: Make ${target}¢ with fewest coins`) }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Greedy — Coin Change</h4>
        <div className="flex gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700"><RotateCcw className="w-4 h-4 text-gray-400" /></button>
          <button onClick={start} className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium">
            {running ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {running ? 'Pause' : 'Solve'}
          </button>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-sm text-center text-gray-300">{message}</div>
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
        <div className="flex justify-center gap-3 mb-4">
          {coins.map((c, i) => (
            <div key={i} className="w-14 h-14 rounded-full border-2 border-yellow-500/50 bg-yellow-500/10 flex items-center justify-center text-yellow-400 font-bold text-sm">{c}¢</div>
          ))}
        </div>
        <div className="text-center text-xs text-gray-500 mb-3">Remaining: <span className="text-white font-bold text-base">{remaining}¢</span></div>
        <div className="flex justify-center flex-wrap gap-1 min-h-[40px]">
          {selected.map((c, i) => (
            <div key={i} className="w-10 h-10 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 text-xs font-bold animate-slide-up">{c}</div>
          ))}
        </div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// BIT MANIPULATION VISUALIZER
// ═══════════════════════════════════════
function BitManipVisualizer({ data }) {
  const [valueA, setValueA] = useState(data?.a || 13)
  const [valueB, setValueB] = useState(data?.b || 7)
  const [op, setOp] = useState('AND')

  const result = op === 'AND' ? valueA & valueB : op === 'OR' ? valueA | valueB : op === 'XOR' ? valueA ^ valueB : op === 'NOT' ? ~valueA & 0xFF : valueA << 1

  function toBin(n) { return (n >>> 0).toString(2).padStart(8, '0') }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">Bit Manipulation</h4>
        <div className="flex gap-1">
          {['AND', 'OR', 'XOR', 'NOT', 'LSHIFT'].map(o => (
            <button key={o} onClick={() => setOp(o)} className={`px-2 py-1 rounded text-xs font-medium ${op === o ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}>{o}</button>
          ))}
        </div>
      </div>
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-4 font-mono text-sm space-y-3">
        <div className="flex items-center gap-3">
          <span className="text-gray-500 w-8">A:</span>
          <div className="flex gap-0.5">{toBin(valueA).split('').map((b, i) => <span key={i} className={`w-7 h-7 flex items-center justify-center rounded ${b === '1' ? 'bg-indigo-500/30 text-indigo-300' : 'bg-gray-800 text-gray-600'}`}>{b}</span>)}</div>
          <span className="text-gray-500">= {valueA}</span>
          <input type="number" value={valueA} onChange={e => setValueA(parseInt(e.target.value) || 0)} className="w-14 px-1 py-0.5 bg-gray-800 border border-gray-700 rounded text-xs text-white" />
        </div>
        {op !== 'NOT' && op !== 'LSHIFT' && (
          <div className="flex items-center gap-3">
            <span className="text-gray-500 w-8">B:</span>
            <div className="flex gap-0.5">{toBin(valueB).split('').map((b, i) => <span key={i} className={`w-7 h-7 flex items-center justify-center rounded ${b === '1' ? 'bg-purple-500/30 text-purple-300' : 'bg-gray-800 text-gray-600'}`}>{b}</span>)}</div>
            <span className="text-gray-500">= {valueB}</span>
            <input type="number" value={valueB} onChange={e => setValueB(parseInt(e.target.value) || 0)} className="w-14 px-1 py-0.5 bg-gray-800 border border-gray-700 rounded text-xs text-white" />
          </div>
        )}
        <div className="border-t border-gray-700 pt-2 flex items-center gap-3">
          <span className="text-yellow-400 w-8">{op}:</span>
          <div className="flex gap-0.5">{toBin(result).split('').map((b, i) => <span key={i} className={`w-7 h-7 flex items-center justify-center rounded ${b === '1' ? 'bg-emerald-500/30 text-emerald-300' : 'bg-gray-800 text-gray-600'}`}>{b}</span>)}</div>
          <span className="text-emerald-400 font-bold">= {result}</span>
        </div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════
// STRING OPERATIONS VISUALIZER
// ═══════════════════════════════════════
function StringVisualizer({ data }) {
  const str = data?.initial_state || 'abcabcbb'
  const [windowStart, setWindowStart] = useState(0)
  const [windowEnd, setWindowEnd] = useState(0)
  const [charSet, setCharSet] = useState(new Set())
  const [running, setRunning] = useState(false)
  const [maxLen, setMaxLen] = useState(0)
  const [message, setMessage] = useState('Longest Substring Without Repeating Characters')
  const intervalRef = useRef(null)

  function start() {
    if (running) { clearInterval(intervalRef.current); setRunning(false); return }
    setWindowStart(0); setWindowEnd(0); setCharSet(new Set()); setMaxLen(0)
    setRunning(true)
    let ws = 0, we = 0, best = 0
    const seen = new Set()
    intervalRef.current = setInterval(() => {
      if (we >= str.length) { clearInterval(intervalRef.current); setRunning(false); setMessage(`Done! Max length = ${best}`); return }
      if (!seen.has(str[we])) {
        seen.add(str[we])
        setCharSet(new Set(seen))
        const len = we - ws + 1
        if (len > best) { best = len; setMaxLen(best) }
        setMessage(`Add '${str[we]}' → window "${str.substring(ws, we + 1)}" (len=${len})`)
        we++; setWindowEnd(we)
      } else {
        setMessage(`'${str[we]}' repeated! Shrink: remove '${str[ws]}'`)
        seen.delete(str[ws])
        setCharSet(new Set(seen))
        ws++; setWindowStart(ws)
      }
    }, 600)
  }

  function reset() { clearInterval(intervalRef.current); setRunning(false); setWindowStart(0); setWindowEnd(0); setCharSet(new Set()); setMaxLen(0); setMessage('Longest Substring Without Repeating Characters') }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-gray-400">String — Longest Unique Substring</h4>
        <div className="flex gap-2">
          <button onClick={reset} className="p-1.5 rounded bg-gray-800 hover:bg-gray-700"><RotateCcw className="w-4 h-4 text-gray-400" /></button>
          <button onClick={start} className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-xs font-medium">
            {running ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {running ? 'Pause' : 'Animate'}
          </button>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-gray-900 border border-gray-800 text-sm text-center text-gray-300">{message}</div>
      <div className="flex justify-center gap-1 py-6 bg-gray-900 rounded-lg border border-gray-800">
        {str.split('').map((ch, i) => {
          const inWindow = i >= windowStart && i < windowEnd
          return (
            <div key={i} className={`w-10 h-10 rounded-lg flex items-center justify-center font-mono font-bold text-lg transition-all duration-200 ${
              inWindow ? 'bg-purple-500/20 text-purple-300 border-2 border-purple-500/50 scale-110' : 'bg-gray-800 text-gray-500 border border-gray-700'
            }`}>
              {ch}
            </div>
          )
        })}
      </div>
      <div className="flex justify-between text-xs">
        <span className="text-gray-500">Current set: {`{${[...charSet].join(', ')}}`}</span>
        <span className="text-gray-500">Max length: <span className="text-emerald-400 font-bold">{maxLen}</span></span>
      </div>
    </div>
  )
}

// ── Helper Components ──
function LegendItem({ color, label }) {
  return (
    <div className="flex items-center gap-1.5">
      <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: color }} />
      <span className="text-gray-400">{label}</span>
    </div>
  )
}
