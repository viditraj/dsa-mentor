"""Code Execution API routes — run code and test cases."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from code_executor import async_execute_code, async_run_test_cases

router = APIRouter()


class ExecuteCodeRequest(BaseModel):
    code: str
    language: str = "python"
    stdin: str = ""
    timeout: Optional[int] = None


class RunTestsRequest(BaseModel):
    code: str
    language: str = "python"
    test_cases: list[dict]
    function_name: Optional[str] = None


@router.post("/execute")
async def execute_code(req: ExecuteCodeRequest):
    """Execute code and return output."""
    result = await async_execute_code(
        code=req.code,
        language=req.language,
        stdin_data=req.stdin,
        timeout=req.timeout,
    )
    return result


@router.post("/run-tests")
async def run_tests(req: RunTestsRequest):
    """Run code against test cases and return results."""
    if not req.test_cases:
        raise HTTPException(status_code=400, detail="No test cases provided")
    result = await async_run_test_cases(
        code=req.code,
        language=req.language,
        test_cases=req.test_cases,
        function_name=req.function_name,
    )
    return result


@router.get("/languages")
async def supported_languages():
    """List supported programming languages."""
    return {
        "languages": [
            {"id": "python", "name": "Python 3", "extension": ".py"},
            {"id": "javascript", "name": "JavaScript (Node.js)", "extension": ".js"},
            {"id": "java", "name": "Java", "extension": ".java"},
            {"id": "cpp", "name": "C++17", "extension": ".cpp"},
        ]
    }
