import { useState } from 'react'
import { executeCode, runTestCases, analyzeComplexity } from '../api/client'
import { Play, FlaskConical, Gauge, CheckCircle2, XCircle, Clock, Loader2, ChevronDown, ChevronUp } from 'lucide-react'

/**
 * Reusable backend code executor panel.
 * Props:
 *   code       – (string) current code from parent
 *   language   – (string) 'python' | 'javascript' | 'java' | 'cpp'
 *   compact    – (bool)   collapsible mode
 */
export default function CodeExecutor({ code, language = 'python', compact = false }) {
  const [open, setOpen] = useState(!compact)
  const [activeTab, setActiveTab] = useState('run')
  const [loading, setLoading] = useState('')
  const [output, setOutput] = useState(null)
  const [stdin, setStdin] = useState('')
  const [testResults, setTestResults] = useState(null)
  const [complexity, setComplexity] = useState(null)
  const [testCasesInput, setTestCasesInput] = useState('')
  const [fnName, setFnName] = useState('')

  const handleRun = async () => {
    if (!code?.trim()) return
    setLoading('run'); setOutput(null)
    try { setOutput(await executeCode({ code, language, stdin })) } catch (e) { setOutput({ error: e.message }) }
    setLoading('')
  }

  const handleTest = async () => {
    if (!code?.trim()) return
    setLoading('test'); setTestResults(null)
    try {
      const tc = JSON.parse(testCasesInput || '[]')
      setTestResults(await runTestCases({ code, language, test_cases: tc, function_name: fnName || null }))
    } catch (e) { setTestResults({ error: e.message }) }
    setLoading('')
  }

  const handleComplexity = async () => {
    if (!code?.trim()) return
    setLoading('complexity'); setComplexity(null)
    try { setComplexity(await analyzeComplexity({ code, language })) } catch (e) { setComplexity({ error: e.message }) }
    setLoading('')
  }

  if (compact && !open) {
    return (
      <button onClick={() => setOpen(true)} className="w-full glass-card rounded-xl p-3 flex items-center justify-center gap-2 text-sm text-green-400 hover:text-green-300 hover:border-green-500/40 transition-all group">
        <Play className="w-4 h-4 group-hover:scale-110 transition-transform" />
        Run Code on Server
      </button>
    )
  }

  const Tab = ({ id, label, icon: Icon }) => (
    <button onClick={() => setActiveTab(id)} className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${activeTab === id ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-gray-200'}`}><Icon className="w-3.5 h-3.5" />{label}</button>
  )

  return (
    <div className="glass-card rounded-xl overflow-hidden border border-gray-800">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800 bg-gray-900/60">
        <div className="flex items-center gap-2">
          <Play className="w-4 h-4 text-green-400" />
          <span className="text-xs font-medium text-gray-400">Code Executor</span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleRun} disabled={!!loading || !code?.trim()} className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-green-600 hover:bg-green-500 text-white text-xs font-medium disabled:opacity-40 transition-colors">
            {loading === 'run' ? <Loader2 className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3" />}Run
          </button>
          <button onClick={handleComplexity} disabled={!!loading || !code?.trim()} className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-purple-600/80 hover:bg-purple-500 text-white text-xs font-medium disabled:opacity-40 transition-colors">
            {loading === 'complexity' ? <Loader2 className="w-3 h-3 animate-spin" /> : <Gauge className="w-3 h-3" />}O(n)
          </button>
          {compact && <button onClick={() => setOpen(false)} className="p-1 rounded hover:bg-gray-800 text-gray-500 hover:text-gray-300"><ChevronUp className="w-3.5 h-3.5" /></button>}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 px-3 py-2 border-b border-gray-800">
        <Tab id="run" label="Output" icon={Play} />
        <Tab id="test" label="Tests" icon={FlaskConical} />
        <Tab id="complexity" label="Complexity" icon={Gauge} />
      </div>

      <div className="p-3 max-h-64 overflow-y-auto">
        {activeTab === 'run' && (
          <div>
            {output ? (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  {output.error ? <XCircle className="w-4 h-4 text-red-400" /> : output.passed ? <CheckCircle2 className="w-4 h-4 text-green-400" /> : <XCircle className="w-4 h-4 text-red-400" />}
                  <span className="text-xs font-medium">{output.error || (output.passed ? 'Success' : 'Error')}</span>
                  {output.execution_time_ms != null && <span className="text-[10px] text-gray-400 ml-auto"><Clock className="w-3 h-3 inline mr-0.5" />{output.execution_time_ms}ms</span>}
                </div>
                {output.stdout && <pre className="bg-gray-900 rounded-lg p-2.5 text-xs text-green-300 overflow-x-auto">{output.stdout}</pre>}
                {output.stderr && <pre className="bg-gray-900 rounded-lg p-2.5 text-xs text-red-300 overflow-x-auto">{output.stderr}</pre>}
              </div>
            ) : <p className="text-gray-500 text-xs">Click Run to execute your code on the server</p>}
            <div className="mt-3"><label className="text-[10px] text-gray-500 block mb-0.5">stdin</label><textarea value={stdin} onChange={e => setStdin(e.target.value)} rows={2} className="w-full bg-gray-900 rounded-lg p-2 text-xs font-mono text-white border border-gray-700 resize-none" placeholder="Input..." /></div>
          </div>
        )}

        {activeTab === 'test' && (
          <div className="space-y-3">
            <div><label className="text-[10px] text-gray-500 block mb-0.5">Function Name</label><input value={fnName} onChange={e => setFnName(e.target.value)} className="w-full bg-gray-900 rounded-lg px-2.5 py-1.5 text-xs font-mono text-white border border-gray-700" placeholder="e.g. two_sum" /></div>
            <div><label className="text-[10px] text-gray-500 block mb-0.5">Test Cases (JSON)</label><textarea value={testCasesInput} onChange={e => setTestCasesInput(e.target.value)} rows={5} className="w-full bg-gray-900 rounded-lg p-2 text-xs font-mono text-white border border-gray-700 resize-none" placeholder='[{"name":"basic","input":"[2,7],9","expected":"[0,1]"}]' /></div>
            <button onClick={handleTest} disabled={!!loading} className="w-full py-1.5 bg-indigo-600 rounded-lg text-xs hover:bg-indigo-500 disabled:opacity-50 flex items-center justify-center gap-1.5"><FlaskConical className="w-3 h-3" />{loading === 'test' ? 'Running...' : 'Run Tests'}</button>
            {testResults && !testResults.error && (
              <div className="space-y-1.5">
                <div className="flex items-center gap-3 p-2 bg-gray-900 rounded-lg">
                  <span className={`text-lg font-bold ${testResults.all_passed ? 'text-green-400' : 'text-amber-400'}`}>{testResults.passed}/{testResults.total}</span>
                  <span className="text-xs text-gray-400">passed</span>
                </div>
                {testResults.results?.map((r, i) => (
                  <div key={i} className={`p-2 rounded-lg border text-xs ${r.passed ? 'bg-green-500/10 border-green-500/20' : 'bg-red-500/10 border-red-500/20'}`}>
                    <div className="flex items-center gap-1.5">{r.passed ? <CheckCircle2 className="w-3 h-3 text-green-400" /> : <XCircle className="w-3 h-3 text-red-400" />}<span className="font-medium">{r.name}</span></div>
                    {!r.passed && <div className="mt-1 text-[10px]"><p>Expected: <span className="text-green-400">{r.expected}</span></p><p>Got: <span className="text-red-400">{r.actual || '(empty)'}</span></p></div>}
                  </div>
                ))}
              </div>
            )}
            {testResults?.error && <p className="text-red-400 text-xs">{testResults.error}</p>}
          </div>
        )}

        {activeTab === 'complexity' && (
          <div>
            {complexity && !complexity.error ? (
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-gray-900 rounded-lg p-3 text-center"><p className="text-[10px] text-gray-400 mb-0.5">Time</p><p className="text-lg font-bold text-indigo-400">{complexity.time_complexity}</p></div>
                  <div className="bg-gray-900 rounded-lg p-3 text-center"><p className="text-[10px] text-gray-400 mb-0.5">Space</p><p className="text-lg font-bold text-emerald-400">{complexity.space_complexity}</p></div>
                </div>
                {complexity.is_optimal != null && <div className={`p-2 rounded-lg text-xs ${complexity.is_optimal ? 'bg-green-500/10 border border-green-500/20' : 'bg-amber-500/10 border border-amber-500/20'}`}>{complexity.is_optimal ? 'Your solution is optimal!' : 'There may be a more optimal approach.'}</div>}
                {complexity.analysis?.summary && <p className="text-xs text-gray-300">{complexity.analysis.summary}</p>}
                {complexity.optimization_suggestions?.length > 0 && (
                  <div>{complexity.optimization_suggestions.map((s, i) => <div key={i} className="p-2 bg-gray-900 rounded-lg text-xs mb-1"><p className="text-gray-300">{s.current} → {s.achievable}</p><p className="text-gray-500 text-[10px] mt-0.5">{s.how}</p></div>)}</div>
                )}
              </div>
            ) : complexity?.error ? <p className="text-red-400 text-xs">{complexity.error}</p> : <p className="text-gray-500 text-xs">Click O(n) to analyze complexity</p>}
          </div>
        )}
      </div>
    </div>
  )
}
