import { useState } from 'react'
import { executeCode, runTestCases, analyzeComplexity } from '../api/client'
import { Play, FlaskConical, Gauge, CheckCircle2, XCircle, Clock, AlertTriangle } from 'lucide-react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import ReactMarkdown from 'react-markdown'

const LANGS = [
  { id: 'python', name: 'Python 3' },
  { id: 'javascript', name: 'JavaScript' },
  { id: 'java', name: 'Java' },
  { id: 'cpp', name: 'C++' },
]

export default function CodeRunnerPage({ userId, user }) {
  const [code, setCode] = useState('def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n    return []\n\n# Test\nprint(two_sum([2, 7, 11, 15], 9))')
  const [lang, setLang] = useState('python')
  const [stdin, setStdin] = useState('')
  const [output, setOutput] = useState(null)
  const [testResults, setTestResults] = useState(null)
  const [complexity, setComplexity] = useState(null)
  const [loading, setLoading] = useState('')
  const [testCasesInput, setTestCasesInput] = useState(JSON.stringify([
    { name: "Basic case", input: "[2,7,11,15], 9", expected: "[0, 1]" },
    { name: "Last pair", input: "[3,2,4], 6", expected: "[1, 2]" },
    { name: "Duplicates", input: "[3,3], 6", expected: "[0, 1]", is_edge_case: true },
  ], null, 2))
  const [fnName, setFnName] = useState('two_sum')
  const [activeTab, setActiveTab] = useState('run')

  const handleRun = async () => {
    setLoading('run'); setOutput(null)
    try { const r = await executeCode({ code, language: lang, stdin }); setOutput(r) } catch (e) { setOutput({ error: e.message, passed: false }) }
    setLoading('')
  }

  const handleTest = async () => {
    setLoading('test'); setTestResults(null)
    try {
      const tc = JSON.parse(testCasesInput)
      const r = await runTestCases({ code, language: lang, test_cases: tc, function_name: fnName || null })
      setTestResults(r)
    } catch (e) { setTestResults({ error: e.message }) }
    setLoading('')
  }

  const handleComplexity = async () => {
    setLoading('complexity'); setComplexity(null)
    try { const r = await analyzeComplexity({ code, language: lang }); setComplexity(r) } catch (e) { setComplexity({ error: e.message }) }
    setLoading('')
  }

  const Tab = ({ id, label, icon: Icon }) => (
    <button onClick={() => setActiveTab(id)} className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-t-lg transition-colors ${activeTab === id ? 'bg-gray-800 text-white border-b-2 border-indigo-500' : 'text-gray-400 hover:text-gray-200'}`}><Icon className="w-4 h-4" />{label}</button>
  )

  return (
    <div className="space-y-4">
      <div><h1 className="text-3xl font-bold gradient-text">Code Runner</h1><p className="text-gray-400 mt-1">Execute code, run tests, and analyze complexity</p></div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Editor */}
        <div className="bg-gray-800/60 rounded-xl border border-gray-700 flex flex-col">
          <div className="flex items-center justify-between p-3 border-b border-gray-700">
            <select value={lang} onChange={e => setLang(e.target.value)} className="bg-gray-700 rounded px-3 py-1.5 text-sm border border-gray-600">{LANGS.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}</select>
            <div className="flex gap-2">
              <button onClick={handleRun} disabled={!!loading} className="flex items-center gap-1.5 px-3 py-1.5 bg-green-600 rounded-lg text-sm hover:bg-green-500 disabled:opacity-50"><Play className="w-4 h-4" />{loading === 'run' ? 'Running...' : 'Run'}</button>
              <button onClick={handleComplexity} disabled={!!loading} className="flex items-center gap-1.5 px-3 py-1.5 bg-purple-600 rounded-lg text-sm hover:bg-purple-500 disabled:opacity-50"><Gauge className="w-4 h-4" />{loading === 'complexity' ? 'Analyzing...' : 'Analyze O(n)'}</button>
            </div>
          </div>
          <textarea value={code} onChange={e => setCode(e.target.value)} spellCheck={false} className="flex-1 min-h-[400px] bg-transparent p-4 font-mono text-sm text-green-300 resize-none outline-none" />
        </div>
        {/* Results */}
        <div className="bg-gray-800/60 rounded-xl border border-gray-700 flex flex-col">
          <div className="flex border-b border-gray-700">
            <Tab id="run" label="Output" icon={Play} />
            <Tab id="test" label="Tests" icon={FlaskConical} />
            <Tab id="complexity" label="Complexity" icon={Gauge} />
          </div>
          <div className="flex-1 p-4 overflow-y-auto min-h-[400px]">
            {activeTab === 'run' && (<div>
              {output ? (<div className="space-y-3">
                <div className="flex items-center gap-2">{output.passed ? <CheckCircle2 className="w-5 h-5 text-green-400" /> : <XCircle className="w-5 h-5 text-red-400" />}<span className="text-sm font-medium">{output.error || (output.passed ? 'Success' : 'Error')}</span>{output.execution_time_ms != null && <span className="text-xs text-gray-400 ml-auto"><Clock className="w-3 h-3 inline mr-1" />{output.execution_time_ms}ms</span>}</div>
                {output.stdout && <div><p className="text-xs text-gray-400 mb-1">stdout</p><pre className="bg-gray-900 rounded-lg p-3 text-sm text-green-300 overflow-x-auto">{output.stdout}</pre></div>}
                {output.stderr && <div><p className="text-xs text-gray-400 mb-1">stderr</p><pre className="bg-gray-900 rounded-lg p-3 text-sm text-red-300 overflow-x-auto">{output.stderr}</pre></div>}
              </div>) : <p className="text-gray-500 text-sm">Click Run to execute your code</p>}
              <div className="mt-4"><label className="text-xs text-gray-400 block mb-1">stdin (optional)</label><textarea value={stdin} onChange={e => setStdin(e.target.value)} rows={2} className="w-full bg-gray-900 rounded-lg p-3 text-sm font-mono text-white border border-gray-700 resize-none" placeholder="Input data..." /></div>
            </div>)}
            {activeTab === 'test' && (<div className="space-y-4">
              <div><label className="text-xs text-gray-400 block mb-1">Function Name</label><input value={fnName} onChange={e => setFnName(e.target.value)} className="w-full bg-gray-900 rounded-lg px-3 py-2 text-sm font-mono text-white border border-gray-700" placeholder="e.g. two_sum" /></div>
              <div><label className="text-xs text-gray-400 block mb-1">Test Cases (JSON)</label><textarea value={testCasesInput} onChange={e => setTestCasesInput(e.target.value)} rows={8} className="w-full bg-gray-900 rounded-lg p-3 text-sm font-mono text-white border border-gray-700 resize-none" /></div>
              <button onClick={handleTest} disabled={!!loading} className="w-full py-2 bg-indigo-600 rounded-lg text-sm hover:bg-indigo-500 disabled:opacity-50 flex items-center justify-center gap-2"><FlaskConical className="w-4 h-4" />{loading === 'test' ? 'Running Tests...' : 'Run Tests'}</button>
              {testResults && !testResults.error && (<div className="space-y-2">
                <div className="flex items-center gap-4 p-3 bg-gray-900 rounded-lg">
                  <span className={`text-2xl font-bold ${testResults.all_passed ? 'text-green-400' : 'text-amber-400'}`}>{testResults.passed}/{testResults.total}</span>
                  <span className="text-sm text-gray-400">tests passed</span>
                </div>
                {testResults.results?.map((r, i) => (
                  <div key={i} className={`p-3 rounded-lg border ${r.passed ? 'bg-green-500/10 border-green-500/20' : 'bg-red-500/10 border-red-500/20'}`}>
                    <div className="flex items-center gap-2 mb-1">{r.passed ? <CheckCircle2 className="w-4 h-4 text-green-400" /> : <XCircle className="w-4 h-4 text-red-400" />}<span className="text-sm font-medium">{r.name}</span>{r.is_edge_case && <span className="text-xs bg-amber-500/20 text-amber-400 px-1.5 py-0.5 rounded">edge</span>}<span className="text-xs text-gray-400 ml-auto">{r.execution_time_ms}ms</span></div>
                    {!r.passed && <div className="text-xs mt-1 space-y-0.5"><p className="text-gray-400">Expected: <span className="text-green-400">{r.expected}</span></p><p className="text-gray-400">Got: <span className="text-red-400">{r.actual || '(empty)'}</span></p>{r.error && <p className="text-red-400">{r.error}</p>}</div>}
                  </div>
                ))}
              </div>)}
              {testResults?.error && <p className="text-red-400 text-sm">{testResults.error}</p>}
            </div>)}
            {activeTab === 'complexity' && (<div>
              {complexity && !complexity.error ? (<div className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-gray-900 rounded-lg p-4 text-center"><p className="text-xs text-gray-400 mb-1">Time</p><p className="text-2xl font-bold text-indigo-400">{complexity.time_complexity}</p></div>
                  <div className="bg-gray-900 rounded-lg p-4 text-center"><p className="text-xs text-gray-400 mb-1">Space</p><p className="text-2xl font-bold text-emerald-400">{complexity.space_complexity}</p></div>
                </div>
                {complexity.is_optimal != null && <div className={`p-3 rounded-lg ${complexity.is_optimal ? 'bg-green-500/10 border border-green-500/20' : 'bg-amber-500/10 border border-amber-500/20'}`}><p className="text-sm">{complexity.is_optimal ? 'Your solution is optimal!' : 'There may be a more optimal approach.'}</p></div>}
                {complexity.analysis && <div className="space-y-3">
                  {complexity.analysis.summary && <p className="text-sm text-gray-300">{complexity.analysis.summary}</p>}
                  {complexity.analysis.line_by_line?.map((l, i) => <div key={i} className="flex gap-3 p-2 bg-gray-900/50 rounded text-xs"><span className="text-indigo-400 font-mono whitespace-nowrap">L{l.lines}</span><span className="text-gray-300 flex-1">{l.description}</span><span className="text-amber-400">{l.contribution}</span></div>)}
                </div>}
                {complexity.optimization_suggestions?.length > 0 && <div><h4 className="text-sm font-semibold text-amber-400 mb-2">Optimization Suggestions</h4>{complexity.optimization_suggestions.map((s, i) => <div key={i} className="p-3 bg-gray-900 rounded-lg text-sm mb-2"><p className="text-gray-300">{s.current} → {s.achievable}</p><p className="text-gray-400 text-xs mt-1">{s.how}</p></div>)}</div>}
              </div>) : complexity?.error ? <p className="text-red-400 text-sm">{complexity.error}</p> : <p className="text-gray-500 text-sm">Click "Analyze O(n)" to analyze your code's complexity</p>}
            </div>)}
          </div>
        </div>
      </div>
    </div>
  )
}
