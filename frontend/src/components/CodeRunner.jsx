import { useState, useEffect, useRef, useCallback } from 'react'
import {
  Play, TestTube2, Loader2, CheckCircle2, XCircle,
  Download, Terminal, RotateCcw, ChevronDown, ChevronUp,
} from 'lucide-react'
import * as api from '../api/client'

/**
 * In-browser Python code runner using Pyodide.
 * Features: Run code, run test cases, show output / pass-fail.
 */

/* ─── Pyodide Loader ─── */
let pyodidePromise = null

function loadPyodide() {
  if (pyodidePromise) return pyodidePromise
  pyodidePromise = new Promise((resolve, reject) => {
    // Check if already loaded
    if (window.loadPyodide) {
      window.loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/' })
        .then(resolve)
        .catch(reject)
      return
    }
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js'
    script.onload = () => {
      window.loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/' })
        .then(resolve)
        .catch(reject)
    }
    script.onerror = () => reject(new Error('Failed to load Pyodide'))
    document.head.appendChild(script)
  })
  return pyodidePromise
}

/* ─── Code Runner Component ─── */
export default function CodeRunner({ code, problemTitle, problemDescription, difficulty }) {
  const [pyodide, setPyodide] = useState(null)
  const [pyLoading, setPyLoading] = useState(false)
  const [pyReady, setPyReady] = useState(false)
  const [output, setOutput] = useState('')
  const [running, setRunning] = useState(false)
  const [error, setError] = useState(null)

  // Test cases state
  const [testCases, setTestCases] = useState(null)
  const [testResults, setTestResults] = useState(null)
  const [testLoading, setTestLoading] = useState(false)
  const [runnerCode, setRunnerCode] = useState('')
  const [showTests, setShowTests] = useState(false)

  const outputRef = useRef(null)

  // Auto-scroll output
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight
    }
  }, [output])

  /* ─── Initialize Pyodide ─── */
  const initPyodide = useCallback(async () => {
    if (pyReady) return pyodide
    setPyLoading(true)
    try {
      const py = await loadPyodide()
      setPyodide(py)
      setPyReady(true)
      return py
    } catch (err) {
      setError('Failed to load Python runtime. Check your internet connection.')
      return null
    } finally {
      setPyLoading(false)
    }
  }, [pyReady, pyodide])

  /* ─── Run user code ─── */
  async function runCode() {
    if (!code.trim()) return
    setRunning(true)
    setOutput('')
    setError(null)

    const py = pyodide || await initPyodide()
    if (!py) {
      setRunning(false)
      return
    }

    try {
      // Run everything in a SINGLE runPython call for reliable stdout capture.
      // Indent user code inside a try block (try doesn't create a new scope).
      const indentedCode = code.split('\n').map(line => '    ' + line).join('\n')
      const wrappedScript = `
import sys as _sys
from io import StringIO as _StringIO

_captured_buf = _StringIO()
_old_stdout = _sys.stdout
_old_stderr = _sys.stderr
_sys.stdout = _captured_buf
_sys.stderr = _captured_buf

try:
${indentedCode}
except Exception as _e:
    print(f"Error: {_e}", file=_captured_buf)
finally:
    _sys.stdout = _old_stdout
    _sys.stderr = _old_stderr

_captured_buf.getvalue()
`
      const captured = py.runPython(wrappedScript)
      const result = (captured != null) ? String(captured) : ''

      if (result.trim()) {
        setOutput(result)
      } else {
        setOutput('✓ Code executed successfully (no output)\n\nTip: Add print() calls to see output, or use "Generate Tests" → "Run Tests" to test your solution with test cases.')
      }
    } catch (err) {
      // Reset stdout on unexpected error
      try { py.runPython('import sys; sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__') } catch(_) {}
      const msg = err.message || String(err)
      const cleaned = msg.replace(/PythonError: Traceback.*?\n/s, '').trim()
      setError(cleaned || msg)
      setOutput('')
    } finally {
      setRunning(false)
    }
  }

  /* ─── Generate test cases from AI ─── */
  async function loadTestCases() {
    setTestLoading(true)
    try {
      const data = await api.generateTestCases({
        problem_title: problemTitle,
        problem_description: problemDescription || '',
        difficulty: difficulty || 'medium',
      })
      setTestCases(data.test_cases || [])
      setRunnerCode(data.runner_code || '')
      setShowTests(true)
    } catch (err) {
      setError('Failed to generate test cases')
    } finally {
      setTestLoading(false)
    }
  }

  /* ─── Run test cases ─── */
  async function runTests() {
    if (!code.trim()) return
    setRunning(true)
    setError(null)
    setOutput('')
    setTestResults(null)

    const py = pyodide || await initPyodide()
    if (!py) {
      setRunning(false)
      return
    }

    try {
      // Step 1: Load user code into global scope (defines classes/functions)
      py.runPython(code)
    } catch (err) {
      const msg = err.message || String(err)
      setError('Error in your code:\n' + msg.replace(/PythonError: Traceback.*?\n/s, '').trim())
      setRunning(false)
      return
    }

    // Step 2: Run the test runner with stdout capture in a single call
    const testScript = `
import sys as _sys
from io import StringIO as _StringIO

_test_buf = _StringIO()
_old_out = _sys.stdout
_old_err = _sys.stderr
_sys.stdout = _test_buf
_sys.stderr = _test_buf

try:
${(runnerCode || 'print("No test runner available. Generate test cases first.")').split('\n').map(line => '    ' + line).join('\n')}
except Exception as _e:
    print(f"FAIL: Test runner error: {_e}")
finally:
    _sys.stdout = _old_out
    _sys.stderr = _old_err

_test_buf.getvalue()
`

    try {
      const result = py.runPython(testScript)
      const outputText = (result != null) ? String(result) : ''
      setOutput(outputText)

      // Parse pass/fail from output
      const lines = outputText.split('\n').filter(l => l.trim())
      const results = lines.map(line => {
        const isPassed = /PASS/i.test(line) && !/FAIL/i.test(line)
        const isFailed = /FAIL/i.test(line)
        return { line, passed: isPassed, failed: isFailed, neutral: !isPassed && !isFailed }
      })
      setTestResults(results)
    } catch (err) {
      const msg = err.message || String(err)
      setError(msg)
    } finally {
      setRunning(false)
    }
  }

  const passCount = testResults?.filter(r => r.passed).length || 0
  const failCount = testResults?.filter(r => r.failed).length || 0
  const totalTests = testResults?.filter(r => r.passed || r.failed).length || 0

  return (
    <div className="glass-card rounded-xl overflow-hidden border border-gray-800">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800 bg-gray-900/60">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-gray-400" />
          <span className="text-xs font-medium text-gray-400">Code Runner</span>
          {pyReady && (
            <span className="flex items-center gap-1 text-[10px] text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Python Ready
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {/* Generate Tests button */}
          <button
            onClick={loadTestCases}
            disabled={testLoading}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-purple-600/20 text-purple-300 hover:bg-purple-600/30 text-xs font-medium disabled:opacity-40 transition-colors"
          >
            {testLoading ? <Loader2 className="w-3 h-3 animate-spin" /> : <TestTube2 className="w-3 h-3" />}
            {testCases ? 'Regenerate Tests' : 'Generate Tests'}
          </button>

          {/* Run Tests button */}
          {testCases && (
            <button
              onClick={runTests}
              disabled={running || !code.trim()}
              className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-600/20 text-amber-300 hover:bg-amber-600/30 text-xs font-medium disabled:opacity-40 transition-colors"
            >
              {running ? <Loader2 className="w-3 h-3 animate-spin" /> : <TestTube2 className="w-3 h-3" />}
              Run Tests
            </button>
          )}

          {/* Run Code button */}
          <button
            onClick={runCode}
            disabled={running || !code.trim()}
            className="flex items-center gap-1 px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium disabled:opacity-40 transition-colors"
          >
            {running ? <Loader2 className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3" />}
            {pyLoading ? 'Loading Python...' : 'Run Code'}
          </button>
        </div>
      </div>

      {/* Test Cases List */}
      {showTests && testCases && testCases.length > 0 && (
        <div className="border-b border-gray-800">
          <button
            onClick={() => setShowTests(!showTests)}
            className="w-full flex items-center justify-between px-4 py-2 text-xs text-gray-400 hover:bg-gray-800/30"
          >
            <span className="font-medium">
              Test Cases ({testCases.length})
              {totalTests > 0 && (
                <span className="ml-2">
                  <span className="text-emerald-400">{passCount}✓</span>
                  {failCount > 0 && <span className="text-red-400 ml-1">{failCount}✗</span>}
                </span>
              )}
            </span>
            <ChevronUp className="w-3 h-3" />
          </button>
          <div className="px-4 pb-3 space-y-1.5 max-h-40 overflow-y-auto">
            {testCases.map((tc, i) => {
              const result = testResults?.find(r => r.line?.includes(tc.name))
              const passed = result?.passed
              const failed = result?.failed

              return (
                <div
                  key={i}
                  className={`flex items-center gap-2 p-2 rounded-lg text-xs ${
                    passed ? 'bg-emerald-500/10 border border-emerald-500/20' :
                    failed ? 'bg-red-500/10 border border-red-500/20' :
                    'bg-gray-800/30 border border-gray-800'
                  }`}
                >
                  {passed ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" /> :
                   failed ? <XCircle className="w-3.5 h-3.5 text-red-400 flex-shrink-0" /> :
                   <div className="w-3.5 h-3.5 rounded-full border border-gray-600 flex-shrink-0" />}
                  <div className="flex-1 min-w-0">
                    <span className={`font-medium ${
                      passed ? 'text-emerald-300' : failed ? 'text-red-300' : 'text-gray-300'
                    }`}>
                      {tc.name}
                    </span>
                    {tc.is_edge_case && (
                      <span className="ml-1.5 text-[9px] px-1 py-0.5 rounded bg-amber-500/15 text-amber-400">edge</span>
                    )}
                  </div>
                  <span className="text-gray-500 font-mono text-[10px] truncate max-w-[120px]">{tc.input}</span>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Output Panel */}
      {(output || error) && (
        <div className="border-t border-gray-800">
          <div className="flex items-center justify-between px-4 py-1.5 bg-gray-900/40">
            <span className="text-xs text-gray-500 font-medium">Output</span>
            <button
              onClick={() => { setOutput(''); setError(null); setTestResults(null) }}
              className="text-gray-600 hover:text-gray-400"
            >
              <RotateCcw className="w-3 h-3" />
            </button>
          </div>
          <div
            ref={outputRef}
            className="px-4 py-3 max-h-48 overflow-y-auto font-mono text-xs"
          >
            {error ? (
              <pre className="text-red-400 whitespace-pre-wrap">{error}</pre>
            ) : testResults ? (
              <div className="space-y-0.5">
                {testResults.map((r, i) => (
                  <div key={i} className={
                    r.passed ? 'text-emerald-400' :
                    r.failed ? 'text-red-400' :
                    'text-gray-400'
                  }>
                    {r.line}
                  </div>
                ))}
                {totalTests > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-800 font-semibold">
                    {failCount === 0 ? (
                      <span className="text-emerald-400">✓ All {passCount} tests passed!</span>
                    ) : (
                      <span className="text-amber-400">
                        {passCount}/{totalTests} tests passed ({failCount} failed)
                      </span>
                    )}
                  </div>
                )}
              </div>
            ) : (
              <pre className="text-gray-300 whitespace-pre-wrap">{output}</pre>
            )}
          </div>
        </div>
      )}

      {/* Empty state */}
      {!output && !error && (
        <div className="px-4 py-6 text-center">
          <Play className="w-8 h-8 text-gray-700 mx-auto mb-2" />
          <p className="text-xs text-gray-600">
            Click "Run Code" to execute your Python solution in the browser, or "Generate Tests" for auto test cases.
          </p>
        </div>
      )}
    </div>
  )
}
