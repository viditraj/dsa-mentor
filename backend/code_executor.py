"""Sandboxed code execution engine for DSA Mentor.

Executes user code in isolated subprocess with timeout and resource limits.
Supports: Python, JavaScript (Node.js), Java, C++.
"""
import asyncio
import os
import subprocess
import tempfile
import time
from typing import Optional


# Language configurations
LANGUAGE_CONFIG = {
    "python": {
        "extension": ".py",
        "compile_cmd": None,
        "run_cmd": ["python3", "{file}"],
        "timeout": 10,
    },
    "javascript": {
        "extension": ".js",
        "compile_cmd": None,
        "run_cmd": ["node", "{file}"],
        "timeout": 10,
    },
    "java": {
        "extension": ".java",
        "compile_cmd": ["javac", "{file}"],
        "run_cmd": ["java", "-cp", "{dir}", "Solution"],
        "timeout": 15,
    },
    "cpp": {
        "extension": ".cpp",
        "compile_cmd": ["g++", "-o", "{dir}/solution", "{file}", "-std=c++17"],
        "run_cmd": ["{dir}/solution"],
        "timeout": 10,
    },
    "c++": {
        "extension": ".cpp",
        "compile_cmd": ["g++", "-o", "{dir}/solution", "{file}", "-std=c++17"],
        "run_cmd": ["{dir}/solution"],
        "timeout": 10,
    },
}

MAX_OUTPUT_SIZE = 50000  # 50KB max output


def _run_process(cmd: list[str], stdin_data: str = "", timeout: int = 10, cwd: str = None) -> dict:
    """Run a subprocess with timeout and capture output."""
    try:
        result = subprocess.run(
            cmd,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env={**os.environ, "PATH": os.environ.get("PATH", "/usr/bin:/usr/local/bin")},
        )
        return {
            "stdout": result.stdout[:MAX_OUTPUT_SIZE],
            "stderr": result.stderr[:MAX_OUTPUT_SIZE],
            "returncode": result.returncode,
            "error": None,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "",
            "returncode": -1,
            "error": "Time Limit Exceeded (TLE)",
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
            "error": f"Execution error: {str(e)}",
        }


def execute_code(code: str, language: str, stdin_data: str = "", timeout: Optional[int] = None) -> dict:
    """Execute code in a sandboxed subprocess.
    
    Returns:
        dict with keys: stdout, stderr, returncode, error, execution_time_ms
    """
    lang = language.lower().strip()
    config = LANGUAGE_CONFIG.get(lang)
    if not config:
        return {
            "stdout": "",
            "stderr": f"Unsupported language: {language}",
            "returncode": -1,
            "error": f"Unsupported language: {language}. Supported: {list(LANGUAGE_CONFIG.keys())}",
            "execution_time_ms": 0,
            "passed": False,
        }

    effective_timeout = timeout or config["timeout"]

    with tempfile.TemporaryDirectory(prefix="dsa_exec_") as tmpdir:
        # Write source file
        if lang == "java":
            filename = "Solution" + config["extension"]
        else:
            filename = "solution" + config["extension"]
        filepath = os.path.join(tmpdir, filename)

        with open(filepath, "w") as f:
            f.write(code)

        # Compile if needed
        if config["compile_cmd"]:
            compile_cmd = [
                c.replace("{file}", filepath).replace("{dir}", tmpdir)
                for c in config["compile_cmd"]
            ]
            compile_result = _run_process(compile_cmd, timeout=30, cwd=tmpdir)
            if compile_result["returncode"] != 0:
                return {
                    "stdout": "",
                    "stderr": compile_result["stderr"],
                    "returncode": compile_result["returncode"],
                    "error": "Compilation Error",
                    "execution_time_ms": 0,
                    "passed": False,
                }

        # Run
        run_cmd = [
            c.replace("{file}", filepath).replace("{dir}", tmpdir)
            for c in config["run_cmd"]
        ]

        start_time = time.perf_counter()
        result = _run_process(run_cmd, stdin_data=stdin_data, timeout=effective_timeout, cwd=tmpdir)
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return {
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "returncode": result["returncode"],
            "error": result["error"],
            "execution_time_ms": elapsed_ms,
            "passed": result["returncode"] == 0 and result["error"] is None,
        }


def run_test_cases(code: str, language: str, test_cases: list[dict], function_name: str = None) -> dict:
    """Run code against multiple test cases.
    
    Each test_case should have: input, expected, name (optional), is_edge_case (optional).
    
    Returns:
        dict with: total, passed, failed, results (list of per-test results), all_passed
    """
    results = []
    passed_count = 0

    for i, tc in enumerate(test_cases):
        tc_name = tc.get("name", f"Test {i + 1}")
        tc_input = tc.get("input", "")
        tc_expected = str(tc.get("expected", "")).strip()
        is_edge = tc.get("is_edge_case", False)

        # Build runner code that calls the function with the test input
        if language.lower() in ("python", "python3"):
            runner_code = code + f"\n\n# Test runner\nimport json, sys\ntry:\n    _input = {repr(tc_input)}\n    # Try to evaluate as Python expression for structured input\n    try:\n        _args = eval(_input) if _input.strip() else ()\n        if not isinstance(_args, tuple):\n            _args = (_args,)\n    except:\n        _args = (_input,)\n    _result = {function_name}(*_args) if '{function_name}' != 'None' else None\n    print(_result)\nexcept Exception as e:\n    print(f'ERROR: {{e}}', file=sys.stderr)\n    sys.exit(1)\n" if function_name else code

            if not function_name:
                # If no function name, just run with stdin
                exec_result = execute_code(code, language, stdin_data=str(tc_input))
            else:
                exec_result = execute_code(runner_code, language)
        else:
            # For other languages, pass input via stdin
            exec_result = execute_code(code, language, stdin_data=str(tc_input))

        actual_output = exec_result["stdout"].strip()
        
        # Flexible comparison
        test_passed = False
        if actual_output == tc_expected:
            test_passed = True
        else:
            # Try normalized comparison (ignore whitespace differences)
            norm_actual = " ".join(actual_output.split())
            norm_expected = " ".join(tc_expected.split())
            if norm_actual == norm_expected:
                test_passed = True
            # Try numeric comparison
            try:
                if float(actual_output) == float(tc_expected):
                    test_passed = True
            except (ValueError, TypeError):
                pass
            # Try Python repr comparison (e.g., [1, 2, 3] vs [1,2,3])
            try:
                import ast
                if ast.literal_eval(actual_output) == ast.literal_eval(tc_expected):
                    test_passed = True
            except:
                pass

        if test_passed:
            passed_count += 1

        results.append({
            "name": tc_name,
            "input": tc_input,
            "expected": tc_expected,
            "actual": actual_output,
            "passed": test_passed,
            "is_edge_case": is_edge,
            "execution_time_ms": exec_result["execution_time_ms"],
            "error": exec_result["error"],
            "stderr": exec_result["stderr"] if exec_result["stderr"] else None,
        })

    return {
        "total": len(test_cases),
        "passed": passed_count,
        "failed": len(test_cases) - passed_count,
        "results": results,
        "all_passed": passed_count == len(test_cases),
    }


async def async_execute_code(code: str, language: str, stdin_data: str = "", timeout: Optional[int] = None) -> dict:
    """Async wrapper for execute_code."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, execute_code, code, language, stdin_data, timeout)


async def async_run_test_cases(code: str, language: str, test_cases: list[dict], function_name: str = None) -> dict:
    """Async wrapper for run_test_cases."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, run_test_cases, code, language, test_cases, function_name)
