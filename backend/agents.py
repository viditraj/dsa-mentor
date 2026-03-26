"""AI Agents for DSA Mentor - Roadmap, Teaching, Assessment, and Visualization agents."""
import asyncio
import json
import os
import re
from typing import Optional

from llm_client import get_llm_client


def _repair_and_parse_json(raw: str) -> dict:
    """Attempt to parse JSON from LLM output, repairing common issues.

    LLMs frequently produce JSON with:
      - Markdown code fences around the JSON
      - Unescaped newlines/tabs inside string values
      - Triple-quoted strings (Python-style '''/\"\"\") instead of JSON strings
      - Trailing commas before } or ]
      - Control characters

    Returns the parsed dict or raises on failure.
    """
    text = raw.strip()

    # Strip markdown code fences
    fence_match = re.match(r'^```(?:json)?\s*\n?(.*?)\n?\s*```$', text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    # First try: direct parse (fast path)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Replace triple-quoted strings (Python-style) with proper JSON strings.
    # LLMs sometimes output '''...''' or \"\"\"...\"\"\" for multi-line values.
    def _replace_triple_quotes(t):
        for delim in ("'''", '"""'):
            while delim in t:
                start = t.find(delim)
                end = t.find(delim, start + 3)
                if end == -1:
                    break
                inner = t[start + 3:end]
                # Escape the inner content for JSON
                escaped = inner.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                t = t[:start] + '"' + escaped + '"' + t[end + 3:]
        return t

    text = _replace_triple_quotes(text)

    # Try again after triple-quote fix
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fix unescaped control chars inside JSON string values.
    # Walk the string tracking whether we're inside a JSON string literal,
    # and escape any raw newlines/tabs/control chars found inside strings.
    repaired_chars = []
    in_string = False
    i = 0
    while i < len(text):
        ch = text[i]
        if in_string:
            if ch == '\\':
                # Emit the backslash and the next char as-is (it's an escape sequence)
                repaired_chars.append(ch)
                if i + 1 < len(text):
                    i += 1
                    repaired_chars.append(text[i])
                i += 1
                continue
            if ch == '"':
                in_string = False
                repaired_chars.append(ch)
                i += 1
                continue
            # Escape raw control characters that break JSON
            if ch == '\n':
                repaired_chars.append('\\n')
                i += 1
                continue
            if ch == '\r':
                repaired_chars.append('\\r')
                i += 1
                continue
            if ch == '\t':
                repaired_chars.append('\\t')
                i += 1
                continue
            if ord(ch) < 0x20:
                repaired_chars.append(f'\\u{ord(ch):04x}')
                i += 1
                continue
            repaired_chars.append(ch)
        else:
            if ch == '"':
                in_string = True
            repaired_chars.append(ch)
        i += 1

    repaired = ''.join(repaired_chars)

    # Remove trailing commas before } or ]
    repaired = re.sub(r',\s*([}\]])', r'\1', repaired)

    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        pass

    # Last try: extract the largest JSON object from the text
    json_blocks = []
    depth = 0
    start = -1
    in_str = False
    esc = False
    for idx, c in enumerate(repaired):
        if esc:
            esc = False
            continue
        if c == '\\' and in_str:
            esc = True
            continue
        if c == '"' and not esc:
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == '{':
            if depth == 0:
                start = idx
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0 and start >= 0:
                json_blocks.append(repaired[start:idx + 1])
                start = -1

    if json_blocks:
        candidate = max(json_blocks, key=len)
        return json.loads(candidate)

    # Give up — raise with original error
    return json.loads(text)


async def _call_llm(system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
    """Call the LLM with given prompts.
    
    Runs the synchronous LLM client in a thread pool for async compat.
    """
    try:
        client = get_llm_client()
    except Exception as e:
        print(f"[DSA Mentor] LLM client initialization failed: {e}")
        return _fallback_response(user_prompt)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        # Run synchronous LLM call in a thread pool to keep async
        loop = asyncio.get_event_loop()
        if json_mode:
            result = await loop.run_in_executor(None, client.chat_json, messages)
        else:
            result = await loop.run_in_executor(None, client.chat, messages)
        return result
    except Exception as e:
        print(f"[DSA Mentor] LLM call failed: {e}")
        return _fallback_response(user_prompt)


def _fallback_response(prompt: str) -> str:
    """Provide intelligent fallback when LLM is unavailable."""
    return json.dumps({
        "response": "AI features require an LLM provider to be configured. "
                     "Please set LLM_PROVIDER to 'nvidia' or 'ollama' and provide the necessary API keys. "
                     "Meanwhile, the app works with the built-in DSA curriculum and visualizations!",
        "visualization": None,
        "code_example": None,
        "follow_up_questions": []
    })


# ═══════════════════════════════════════
# ROADMAP AGENT
# ═══════════════════════════════════════

ROADMAP_SYSTEM_PROMPT = """You are an expert DSA interview coach. Your role is to create personalized 
learning roadmaps based on the user's experience level, available time, and target timeline.

Consider:
- Current skill level and what they already know
- Time available per day for practice
- Target interview date
- Which companies they're targeting (FAANG has different focus than startups)
- Learning pace adaptation based on performance

Output a JSON object with adaptive recommendations."""


async def generate_adaptive_roadmap(user_profile: dict, current_stats: dict = None) -> dict:
    """Generate or adapt a personalized DSA roadmap."""
    prompt = f"""Create a personalized DSA learning roadmap for:
- Name: {user_profile.get('name', 'Student')}
- Experience: {user_profile.get('experience_level', 'beginner')}
- Daily hours: {user_profile.get('daily_hours', 2)}
- Target company: {user_profile.get('target_company', 'Any tech company')}
- Target date: {user_profile.get('target_date', 'No specific date')}
- Preferred language: {user_profile.get('preferred_language', 'python')}
"""
    if current_stats:
        prompt += f"""
Current Progress:
- Problems solved: {current_stats.get('total_problems_solved', 0)}
- Weak areas: {current_stats.get('weak_areas', [])}
- Strong areas: {current_stats.get('strong_areas', [])}
- Learning pace: {current_stats.get('learning_pace', 'normal')}
- Topics completed: {current_stats.get('topics_completed', 0)}

Adapt the roadmap based on their progress. Speed up topics they're good at, spend more time on weak areas.
"""
    prompt += """
Return a JSON with:
{
    "total_days": number,
    "daily_hours_recommended": number,
    "adjustments": ["list of specific adjustments made"],
    "focus_areas": ["priority topics to focus on"],
    "skip_suggestions": ["topics that can be condensed based on experience"],
    "motivational_message": "personalized encouragement"
}"""

    try:
        result = await _call_llm(ROADMAP_SYSTEM_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "total_days": 90,
            "daily_hours_recommended": 2,
            "adjustments": [],
            "focus_areas": ["arrays", "trees", "dynamic_programming"],
            "skip_suggestions": [],
            "motivational_message": "Let's master DSA together! Consistency is key."
        }


# ═══════════════════════════════════════
# TEACHING AGENT
# ═══════════════════════════════════════

TEACHING_SYSTEM_PROMPT = """You are a world-class DSA teacher who explains complex algorithms 
with clarity, intuition, and visual thinking. You write comprehensive, textbook-quality lessons
that are engaging and thorough. You use:

1. Real-world analogies to build deep intuition
2. Step-by-step visual walkthroughs with concrete examples
3. Multiple code examples in the user's preferred language
4. Comparison tables between different approaches
5. Common pitfalls, edge cases, and interview tips
6. Pattern recognition across similar problems

Your explanations should be LONG and DETAILED — at least 1500-2000 words for the explanation field.
Use markdown formatting extensively: headers, bold, code blocks, bullet lists, numbered lists, tables.
Include real interview context and practical problem-solving strategies."""


async def teach_concept(topic: str, subtopic: str = None, language: str = "python") -> dict:
    """Generate a comprehensive teaching lesson for a DSA concept."""
    prompt = f"""Teach me about: {topic}
{f'Specifically: {subtopic}' if subtopic else ''}
Language: {language}

Provide a COMPREHENSIVE, DETAILED lesson. The explanation field must be LONG and THOROUGH (1500+ words).

The "explanation" field should be a COMPLETE markdown document containing ALL of the following sections:

## What is [Topic]?
Clear definition, real-world analogy, and intuitive explanation of the concept.

## Why is it Important?
Why this matters in interviews, real-world applications, which companies test this heavily.

## Core Concepts
Break down the fundamental building blocks. Define key terms. Use bullet points.

## How it Works (Visual Walkthrough)
Walk through a concrete example step-by-step using text-based visualization.
Show the state at each step. Use formatted tables or diagrams where helpful.
Example: for arrays show index states, for trees show node traversal order.

## Implementation
Provide well-commented code with explanation of each part.
Use ```{language} code blocks.

## Complexity Analysis
Detailed time and space complexity with clear reasoning WHY (not just stating O(n)).
Include best case, worst case, and average case where applicable.
Use a comparison table if multiple approaches exist:
| Approach | Time | Space | When to Use |

## Variations & Related Techniques
List 3-5 variations of this technique (e.g., for Two Pointers: same-direction, opposite-direction, fast/slow).
Explain when each variation applies.

## Common Mistakes & Pitfalls
List 4-6 specific mistakes students make, with examples of wrong vs correct code when applicable.

## Interview Tips & Pattern Recognition
When you see ___ in a problem, think of this technique.
List 3-5 "trigger words" or patterns that signal this approach.
Mention 3-5 specific LeetCode problems that use this pattern.

## Practice Strategy
Suggested order of problems to practice (easy → medium → hard).
How much time to spend. What to do when stuck.

Return as JSON:
{{
    "title": "topic title",
    "analogy": "one-line real-world analogy",
    "explanation": "VERY LONG comprehensive markdown document with ALL sections above (1500+ words)",
    "walkthrough_steps": [
        {{"step": 1, "description": "what happens", "state": "current state of data structure", "highlight": "what to focus on"}}
    ],
    "code": "primary implementation code (clean, well-commented)",
    "complexity": {{"time": "O(?) — each of the n elements ... (brief explanation)", "space": "O(?) — ... (brief explanation)"}},
    "variations": ["variation 1 with brief description", "variation 2 with brief description"],
    "common_mistakes": ["mistake 1 with explanation", "mistake 2 with explanation"],
    "practice_tips": ["tip 1", "tip 2", "tip 3"],
    "interview_problems": ["Two Sum (Easy)", "3Sum (Medium)", "Container With Most Water (Medium)"],
    "visualization_type": "which visualization to show (array, tree, graph, stack, etc.)",
    "visualization_data": {{"initial_state": [], "operations": []}}
}}"""

    try:
        result = await _call_llm(TEACHING_SYSTEM_PROMPT, prompt, json_mode=True)
        print(f"[teach_concept] LLM returned {len(result)} chars, starts with: {result[:200]}")
        parsed = _repair_and_parse_json(result)
        # Validate that we got the expected structure
        if "explanation" not in parsed or len(parsed.get("explanation", "")) < 50:
            print(f"[teach_concept] LLM response missing 'explanation' field or too short, keys: {list(parsed.keys())}")
            return _default_lesson(topic)
        return parsed
    except json.JSONDecodeError as e:
        print(f"[teach_concept] JSON parse failed: {e}")
        print(f"[teach_concept] Raw response: {result[:500] if result else 'EMPTY'}")
        # Try to extract JSON from markdown fences
        import re
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group(1))
                if "explanation" in parsed:
                    return parsed
            except Exception:
                pass
        return _default_lesson(topic)
    except Exception as e:
        print(f"[teach_concept] Unexpected error: {type(e).__name__}: {e}")
        return _default_lesson(topic)


def _default_lesson(topic: str) -> dict:
    """Default lesson when AI is unavailable."""
    return {
        "title": topic,
        "analogy": "Think of it as organizing items in the most efficient way possible.",
        "explanation": f"# {topic}\n\nThis is a fundamental concept in Data Structures and Algorithms. "
                       f"Understanding {topic} is crucial for technical interviews.",
        "walkthrough_steps": [
            {"step": 1, "description": "Initialize the data structure", "state": "Empty", "highlight": "Setup"},
            {"step": 2, "description": "Process the input", "state": "Processing", "highlight": "Core logic"},
            {"step": 3, "description": "Return the result", "state": "Done", "highlight": "Output"},
        ],
        "code": f"# {topic} implementation\n# Enable AI for detailed code examples",
        "complexity": {"time": "Varies", "space": "Varies"},
        "variations": [],
        "common_mistakes": [],
        "practice_tips": ["Practice with simple examples first", "Trace through the algorithm by hand"],
        "visualization_type": "array",
        "visualization_data": {"initial_state": [5, 3, 8, 1, 9, 2, 7], "operations": []}
    }


# ═══════════════════════════════════════
# ASSESSMENT AGENT
# ═══════════════════════════════════════

ASSESSMENT_SYSTEM_PROMPT = """You are a senior software engineer at a top tech company who reviews 
code during technical interviews. You provide:

1. Constructive, encouraging feedback
2. Specific suggestions for improvement
3. Pattern recognition tips
4. Time/space complexity analysis
5. Edge cases the solution might miss

Be supportive but thorough. Highlight what they did well AND what needs work."""


async def review_solution(problem_title: str, code: str, language: str = "python",
                          time_taken: int = None) -> dict:
    """Review a user's solution and provide detailed feedback."""
    prompt = f"""Review this solution for "{problem_title}":

```{language}
{code}
```

Time taken: {f'{time_taken} minutes' if time_taken else 'Not recorded'}

Provide:
1. Correctness assessment
2. Time and space complexity
3. What was done well
4. Areas for improvement
5. A cleaner/optimal solution if theirs isn't optimal
6. Edge cases they might have missed
7. Score out of 10

Return as JSON:
{{
    "score": number (1-10),
    "is_correct": boolean,
    "time_complexity": "O(?)",
    "space_complexity": "O(?)",
    "strengths": ["what they did well"],
    "improvements": ["specific improvements"],
    "optimal_solution": "optimal code if different",
    "edge_cases": ["missed edge cases"],
    "pattern_tips": ["pattern recognition advice"],
    "summary": "encouraging overall feedback"
}}"""

    try:
        result = await _call_llm(ASSESSMENT_SYSTEM_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "score": 5,
            "is_correct": True,
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "strengths": ["Solution submitted successfully"],
            "improvements": ["Enable AI for detailed code review"],
            "optimal_solution": None,
            "edge_cases": [],
            "pattern_tips": [],
            "summary": "Enable AI features for comprehensive code review."
        }


# ═══════════════════════════════════════
# HINT AGENT
# ═══════════════════════════════════════

async def get_progressive_hint(problem_title: str, problem_description: str,
                                hint_level: int = 1) -> dict:
    """Provide progressive hints (1=subtle, 2=medium, 3=detailed)."""
    prompt = f"""Problem: {problem_title}
Description: {problem_description}

Provide a level {hint_level} hint (1=subtle nudge, 2=approach hint, 3=detailed strategy):

Return as JSON:
{{
    "hint": "the hint text",
    "thinking_questions": ["questions to guide their thinking"],
    "related_pattern": "the algorithmic pattern this problem uses",
    "next_hint_available": {str(hint_level < 3).lower()}
}}"""

    try:
        result = await _call_llm(TEACHING_SYSTEM_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        hints = {
            1: "Think about what data structure would allow O(1) lookups.",
            2: "Consider using a hash map to store values you've already seen.",
            3: "Iterate through the array. For each element, check if target - element exists in your hash map."
        }
        return {
            "hint": hints.get(hint_level, hints[1]),
            "thinking_questions": ["What's the brute force approach?", "Can you trade space for time?"],
            "related_pattern": "hash_map_lookup",
            "next_hint_available": hint_level < 3
        }


# ═══════════════════════════════════════
# BRIDGE LESSON AGENT (Concept Connector)
# ═══════════════════════════════════════

BRIDGE_SYSTEM_PROMPT = """You are a DSA concept connector. Your job is to explain how two DSA topics 
are related and why learning one is essential before the other.

Write bridge lessons that:
1. Start with a brief reminder of the prerequisite concept
2. Show the EXACT connection — how the prerequisite is used/extended
3. Give a concrete code example showing the bridge
4. End with "Now you're ready for..." 

Keep it concise (200-400 words). Use markdown formatting.
Make the student feel like everything connects naturally, not randomly."""


async def generate_bridge_lesson(
    from_topic: str,
    to_topic: str,
    dependency_explanation: str = None,
    user_level: str = "beginner",
) -> dict:
    """Generate a bridge lesson connecting two related topics.
    
    Explains WHY topic B requires knowledge of topic A.
    """
    context = ""
    if dependency_explanation:
        context = f"\nKnown connection: {dependency_explanation}"

    prompt = f"""Generate a bridge lesson connecting these DSA topics:

PREREQUISITE (already learned): {from_topic}
NEXT TOPIC (about to learn): {to_topic}
Student level: {user_level}
{context}

Return as JSON:
{{
    "title": "Bridge: [from] → [to]",
    "hook": "One sentence showing why this connection matters",
    "recap": "Quick 2-3 sentence recap of the prerequisite topic",
    "connection": "Detailed explanation of how these topics connect (the 'aha!' moment)",
    "code_example": {{
        "language": "python",
        "code": "Short code showing the bridge concept",
        "explanation": "What this code demonstrates"
    }},
    "ready_message": "Now you're ready for [to_topic] because..."
}}"""

    try:
        result = await _call_llm(BRIDGE_SYSTEM_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "title": f"Bridge: {from_topic} → {to_topic}",
            "hook": f"Understanding {from_topic} is the key to mastering {to_topic}.",
            "recap": f"You've already learned {from_topic}. Let's see how it connects to what's next.",
            "connection": dependency_explanation or f"{from_topic} provides the foundation that {to_topic} builds upon.",
            "code_example": None,
            "ready_message": f"Now you're ready for {to_topic} because you understand {from_topic}!"
        }


# ═══════════════════════════════════════
# REVIEW CARD AGENT (Spaced Repetition Helper)
# ═══════════════════════════════════════

REVIEW_SYSTEM_PROMPT = """You are a flashcard/review quiz generator for DSA concepts.
Generate concise review questions that test understanding, not just memorization.
Focus on:
- Time/space complexity reasoning
- When to use which pattern
- Edge cases and gotchas
- Comparison between similar concepts"""


async def generate_review_question(card_title: str, card_content: dict) -> dict:
    """Generate a review question for a spaced repetition card."""
    card_type = card_content.get("card_type", "concept")

    prompt = f"""Generate a review question for this DSA concept:

Topic: {card_title}
Type: {card_type}
Details: {json.dumps(card_content)}

Return as JSON:
{{
    "question": "The review question",
    "hint": "A small hint if they're stuck",
    "answer": "The expected answer",
    "difficulty_rating": "easy|medium|hard",
    "follow_up": "A deeper follow-up question"
}}"""

    try:
        result = await _call_llm(REVIEW_SYSTEM_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "question": f"Explain the key concept behind {card_title} and when you'd use it.",
            "hint": "Think about time/space complexity and common use cases.",
            "answer": f"Review the key concepts of {card_title}.",
            "difficulty_rating": "medium",
            "follow_up": f"Can you code a basic example of {card_title}?"
        }


# ═══════════════════════════════════════
# CHAT AGENT (General DSA Q&A)
# ═══════════════════════════════════════

CHAT_SYSTEM_PROMPT = """You are DSA Mentor, an AI tutor specializing in Data Structures and Algorithms 
for technical interview preparation. You help students:

1. Understand DSA concepts deeply with intuition and analogies
2. Solve LeetCode problems with guided thinking
3. Recognize patterns across problems
4. Build problem-solving frameworks
5. Prepare for behavioral + technical interview questions

Rules:
- ALWAYS give detailed, thorough explanations (at least 3-5 paragraphs for concept questions)
- Use clear, beginner-friendly language with intuition and analogies
- Include visual descriptions (describe what data structures look like)
- Show step-by-step reasoning with examples
- Provide Python code examples in markdown code blocks (```python)
- Use encouraging, supportive tone
- Format responses in clear markdown with headers, bullet points, and code blocks
- NEVER respond with just a single line or a code snippet alone — always explain the concept first

If the user provides context about a specific problem they're working on, tailor your answer to that problem.
If asked about code, explain WHY it works, not just WHAT it does."""


async def chat_with_mentor(message: str, context: str = None) -> dict:
    """General DSA Q&A chat with the AI mentor."""
    prompt = message
    if context:
        prompt = f"Context: {context}\n\nQuestion: {message}"

    try:
        result = await _call_llm(CHAT_SYSTEM_PROMPT, prompt)
        return {
            "response": result,
            "visualization": None,
            "code_example": None,
            "follow_up_questions": []
        }
    except Exception:
        return {
            "response": "I'm here to help with DSA! Enable the AI features by setting your OpenAI API key "
                        "for personalized mentoring. Meanwhile, explore the roadmap and practice problems!",
            "visualization": None,
            "code_example": None,
            "follow_up_questions": [
                "How do I approach Two Sum?",
                "Explain BFS vs DFS",
                "What is dynamic programming?"
            ]
        }


# ═══════════════════════════════════════
# DAILY PLAN GENERATOR
# ═══════════════════════════════════════

async def generate_daily_plan(user_profile: dict, day_number: int, current_topic: dict,
                               stats: dict = None, review_problems: list = None) -> dict:
    """Generate a personalized daily learning plan."""
    prompt = f"""Generate a daily DSA study plan for Day {day_number}:

Student: {user_profile.get('name', 'Student')}
Level: {user_profile.get('experience_level', 'beginner')}
Available time: {user_profile.get('daily_hours', 2)} hours
Current topic: {current_topic.get('name', 'Arrays')}

{f"Learning pace: {stats.get('learning_pace', 'normal')}" if stats else ""}
{f"Weak areas: {stats.get('weak_areas', [])}" if stats else ""}
{f"Problems to review: {review_problems}" if review_problems else ""}

Return as JSON:
{{
    "greeting": "personalized daily greeting",
    "concept_lesson": {{
        "title": "today's concept",
        "summary": "brief overview",
        "key_points": ["main takeaways"],
        "estimated_time_minutes": 30
    }},
    "warm_up": {{
        "description": "Quick 5-min warm up exercise",
        "example": "a simple example to solve mentally"
    }},
    "study_plan": [
        {{"time": "0-30 min", "activity": "Learn concept", "details": "..."}},
        {{"time": "30-60 min", "activity": "Solve easy problem", "details": "..."}},
        {{"time": "60-90 min", "activity": "Solve medium problem", "details": "..."}},
        {{"time": "90-120 min", "activity": "Review and reflect", "details": "..."}}
    ],
    "motivation": "encouraging message for the day"
}}"""

    try:
        result = await _call_llm(TEACHING_SYSTEM_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "greeting": f"Welcome to Day {day_number}! Let's learn something amazing today.",
            "concept_lesson": {
                "title": current_topic.get("name", "DSA Fundamentals"),
                "summary": "Today we'll dive deep into this topic with examples and practice.",
                "key_points": current_topic.get("key_concepts", ["Understanding the basics"]),
                "estimated_time_minutes": 30
            },
            "warm_up": {
                "description": "Quick mental exercise: What's the time complexity of accessing an array element by index?",
                "example": "Answer: O(1) - Direct memory access using base address + offset"
            },
            "study_plan": [
                {"time": "0-30 min", "activity": "Learn concept", "details": "Read the lesson and watch visualizations"},
                {"time": "30-60 min", "activity": "Solve easy problem", "details": "Start with the easiest problem"},
                {"time": "60-90 min", "activity": "Solve medium problem", "details": "Challenge yourself"},
                {"time": "90-120 min", "activity": "Review and reflect", "details": "Review solutions and take notes"}
            ],
            "motivation": "Every expert was once a beginner. Keep going! 🚀"
        }


# ═══════════════════════════════════════
# PATTERN ANALYSIS AGENT
# ═══════════════════════════════════════

PATTERN_ANALYSIS_PROMPT = """You are a DSA pattern recognition expert. You analyze code to identify
which algorithmic patterns the student used, and compare them to the optimal pattern.
Be specific about pattern names: two_pointers, sliding_window, hash_map, binary_search,
bfs, dfs, backtracking, dp_linear, dp_grid, monotonic_stack, greedy, union_find,
topological_sort, trie, heap_top_k."""


async def analyze_code_pattern(
    problem_title: str,
    code: str,
    language: str = "python",
    known_optimal_pattern: str = None,
) -> dict:
    """AI analyzes submitted code to identify which pattern the student used."""
    optimal_hint = ""
    if known_optimal_pattern:
        optimal_hint = f"\nThe optimal pattern for this problem is: {known_optimal_pattern}"

    prompt = f"""Analyze this code submitted for "{problem_title}":

```{language}
{code}
```
{optimal_hint}

Identify:
1. What pattern(s) the student actually used
2. Whether it matches the optimal pattern
3. The time/space complexity of their approach
4. Specific "When you see X, think Y" advice for this problem type

Return as JSON:
{{
    "detected_pattern": "pattern_key the student used (e.g. two_pointers, hash_map)",
    "detected_pattern_name": "Human readable name",
    "is_optimal_pattern": true/false,
    "optimal_pattern": "the optimal pattern_key",
    "optimal_pattern_name": "Human readable name of optimal",
    "student_complexity": {{"time": "O(?)", "space": "O(?)"}},
    "optimal_complexity": {{"time": "O(?)", "space": "O(?)"}},
    "pattern_match_explanation": "Why their pattern works or doesn't",
    "when_you_see_think": {{
        "cue": "When you see [X in this problem]...",
        "pattern": "think [Y pattern]",
        "reason": "because [Z]"
    }},
    "improvement_tips": ["specific tips to improve their approach"],
    "related_problems": ["other problems that use the same optimal pattern"]
}}"""

    try:
        result = await _call_llm(PATTERN_ANALYSIS_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "detected_pattern": "unknown",
            "detected_pattern_name": "Could not detect",
            "is_optimal_pattern": False,
            "optimal_pattern": known_optimal_pattern or "unknown",
            "optimal_pattern_name": known_optimal_pattern or "Unknown",
            "student_complexity": {"time": "Unknown", "space": "Unknown"},
            "optimal_complexity": {"time": "Unknown", "space": "Unknown"},
            "pattern_match_explanation": "Enable AI for detailed pattern analysis.",
            "when_you_see_think": {
                "cue": f"When you see a problem like {problem_title}...",
                "pattern": f"think {known_optimal_pattern or 'about which pattern fits'}",
                "reason": "Practice pattern recognition by studying the problem constraints."
            },
            "improvement_tips": ["Review the pattern catalog for this problem type"],
            "related_problems": [],
        }


# ═══════════════════════════════════════
# AI PROBLEM SOLVER AGENT
# ═══════════════════════════════════════

AI_SOLVE_SYSTEM_PROMPT = """You are an expert DSA tutor who helps students truly understand coding problems.
Your role is to provide a comprehensive walkthrough that teaches problem-solving thinking, not just give the answer.
Be encouraging, clear, and thorough. Use simple analogies when helpful.
Format your response with proper markdown headings and code blocks."""


async def solve_problem_with_ai(
    problem_title: str,
    problem_description: str = "",
    difficulty: str = "medium",
    patterns: list = None,
) -> dict:
    """Provide a complete AI walkthrough for solving a problem."""
    prompt = f"""Provide a comprehensive walkthrough for this coding problem:

Problem: {problem_title}
Description: {problem_description or 'Standard LeetCode problem'}
Difficulty: {difficulty}
Known Patterns: {', '.join(patterns) if patterns else 'Not specified'}

Create a detailed teaching walkthrough with these exact sections:

1. **Understanding the Problem** - Explain what the problem is really asking. Break down the input/output. Give a real-world analogy if helpful.

2. **How to Think About It** - What questions should the student ask themselves? What observations are key? What pattern does this problem match and why?

3. **Approach & Strategy** - Describe the algorithm step by step in plain English BEFORE showing any code. Explain WHY this approach works.

4. **Step-by-Step Walkthrough** - Walk through a concrete example with the algorithm, showing each step of the process visually (use text-based visualization).

5. **Implementation** - Provide clean, well-commented Python solution code.

6. **Complexity Analysis** - Time and space complexity with clear explanation of WHY.

7. **Common Mistakes** - What pitfalls should students watch out for?

8. **Follow-up Variations** - How would the approach change for related problems?

Return as JSON:
{{
    "problem_understanding": "markdown text explaining the problem clearly",
    "thinking_process": "markdown text on how to think about this problem",
    "approach": "markdown text describing the algorithm strategy",
    "walkthrough": "markdown text with step-by-step example walkthrough",
    "solution_code": "clean Python solution code only (no markdown fences)",
    "time_complexity": "O(?)",
    "space_complexity": "O(?)",
    "complexity_explanation": "why these complexities",
    "common_mistakes": ["mistake 1", "mistake 2"],
    "follow_up": ["variation 1", "variation 2"],
    "key_insight": "the single most important insight for this problem"
}}"""

    try:
        result = await _call_llm(AI_SOLVE_SYSTEM_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "problem_understanding": f"**{problem_title}** is a {difficulty} level problem. Enable AI features for a comprehensive walkthrough.",
            "thinking_process": "Start by understanding the input/output constraints, then identify which DSA pattern applies.",
            "approach": "Analyze the problem constraints to determine the optimal approach.",
            "walkthrough": "Enable AI for a detailed step-by-step walkthrough with examples.",
            "solution_code": f"# Solution for {problem_title}\n# Enable AI features for the complete solution\npass",
            "time_complexity": "Depends on approach",
            "space_complexity": "Depends on approach",
            "complexity_explanation": "Enable AI for detailed complexity analysis.",
            "common_mistakes": ["Not considering edge cases", "Overlooking time complexity requirements"],
            "follow_up": ["Try solving with a different approach", "Consider the follow-up constraints"],
            "key_insight": "Enable AI features for the key insight.",
        }


# ═══════════════════════════════════════
# TEST CASE GENERATOR AGENT
# ═══════════════════════════════════════

TEST_CASE_PROMPT = """You are a test case generator for coding interview problems.
Generate comprehensive test cases including edge cases.
Each test case must have clear input and expected output.
Make test cases runnable in Python."""


async def generate_test_cases(
    problem_title: str,
    problem_description: str = "",
    difficulty: str = "medium",
) -> dict:
    """Generate test cases for a problem, including edge cases."""
    prompt = f"""Generate test cases for this coding problem:

Problem: {problem_title}
Description: {problem_description or 'Standard LeetCode problem'}
Difficulty: {difficulty}

Generate 5-8 test cases covering:
1. Basic/simple case
2. Standard case
3. Edge case (empty input, single element)
4. Large input boundary
5. Tricky/corner case

Return as JSON:
{{
    "function_name": "the function name to call (e.g. twoSum, maxProfit)",
    "test_cases": [
        {{
            "name": "descriptive name",
            "input": "Python expression for input (e.g. [2,7,11,15], 9)",
            "expected": "Python expression for expected output",
            "explanation": "why this test case matters",
            "is_edge_case": true/false
        }}
    ],
    "runner_code": "Complete Python test runner code that defines the solution function signature and runs all test cases, printing PASS/FAIL for each"
}}"""

    try:
        result = await _call_llm(TEST_CASE_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "function_name": "solution",
            "test_cases": [
                {
                    "name": "Basic case",
                    "input": "[]",
                    "expected": "[]",
                    "explanation": "Test with basic input",
                    "is_edge_case": False,
                },
                {
                    "name": "Empty input",
                    "input": "[]",
                    "expected": "[]",
                    "explanation": "Edge case: empty input",
                    "is_edge_case": True,
                },
            ],
            "runner_code": f"# Test runner for {problem_title}\n# Enable AI for auto-generated test cases\nprint('PASS: placeholder')",
        }


# ═══════════════════════════════════════
# FAANG PATTERN STORY AGENT
# ═══════════════════════════════════════

PATTERN_STORY_PROMPT = """You are a world-class DSA teacher who explains algorithmic patterns through
vivid stories, real-world analogies, and intuition. You make complex patterns feel obvious.

Your style:
1. Start with a real-world story that perfectly mirrors the pattern
2. Build intuition BEFORE showing any code — make the student "get it" conceptually
3. Show the pattern template with line-by-line explanation
4. Walk through 2-3 problems that use this pattern, showing how the SAME template solves them all
5. End with a "Pattern Recognition Cheat Sheet" — when you see X, think this pattern

Be encouraging, conversational, and make the student feel like they're having an "aha!" moment.
Use markdown formatting with headers, bold, code blocks, bullet points."""


async def teach_pattern_story(pattern_key: str, pattern_info: dict, language: str = "python") -> dict:
    """Generate an immersive story-based lesson for a FAANG pattern."""
    prompt = f"""Teach the "{pattern_info['name']}" pattern through an engaging story.

Pattern info:
- Name: {pattern_info['name']}
- Story hook: {pattern_info['story']}
- Intuition: {pattern_info['intuition']}
- When to use: {', '.join(pattern_info['when_to_use'])}
- Complexity: Time {pattern_info['complexity']['time']}, Space {pattern_info['complexity']['space']}

Template code:
```{language}
{pattern_info['template']}
```

Create a COMPREHENSIVE lesson (2000+ words) covering:

1. **The Story** — An engaging real-world analogy that makes the pattern click
2. **The "Aha!" Moment** — The core insight that makes this pattern work
3. **The Template** — Line-by-line breakdown of the reusable code template
4. **Pattern in Action** — Walk through 3 concrete problems using this pattern
5. **Recognition Guide** — "When you see ___, think {pattern_info['name']}"
6. **Common Pitfalls** — Mistakes students make with this pattern
7. **Variations** — Different flavors of this pattern

Return as JSON:
{{
    "title": "Mastering {pattern_info['name']}",
    "story": "The full engaging story (500+ words)",
    "aha_moment": "The single most important insight in 1-2 sentences",
    "template_breakdown": "Line-by-line template explanation in markdown",
    "problems_walkthrough": "Walking through 3 problems with the pattern (markdown)",
    "recognition_guide": [
        {{"trigger": "When you see...", "think": "Think of {pattern_info['name']} because..."}}
    ],
    "common_pitfalls": ["pitfall 1 with explanation", "pitfall 2 with explanation"],
    "variations": ["variation name: brief description"],
    "motivation": "An encouraging message about mastering this pattern"
}}"""

    try:
        result = await _call_llm(PATTERN_STORY_PROMPT, prompt, json_mode=True)
        return _repair_and_parse_json(result)
    except Exception:
        return {
            "title": f"Mastering {pattern_info['name']}",
            "story": pattern_info["story"],
            "aha_moment": pattern_info["intuition"],
            "template_breakdown": f"```{language}\n{pattern_info['template']}\n```\n\nThis is the core template for the {pattern_info['name']} pattern.",
            "problems_walkthrough": f"Practice the problems in the {pattern_info['name']} section to see this pattern in action.",
            "recognition_guide": [
                {"trigger": use, "think": f"Think of {pattern_info['name']}"}
                for use in pattern_info["when_to_use"][:3]
            ],
            "common_pitfalls": ["Off-by-one errors in boundary conditions", "Forgetting to handle empty input"],
            "variations": [],
            "motivation": f"Every problem you solve with {pattern_info['name']} makes you stronger. You've got this!"
        }


async def get_faang_question_walkthrough(question: dict, language: str = "python") -> dict:
    """Generate a focused walkthrough for a FAANG 75 question."""
    prompt = f"""Provide a focused, interview-style walkthrough for this FAANG interview question:

Problem: {question['title']} (LeetCode #{question['leetcode']})
Difficulty: {question['difficulty']}
Pattern: {question['pattern']}
Why it's asked: {question['why']}
Companies: {', '.join(question['companies'])}

Create an interview-focused walkthrough. Imagine you're coaching someone who has 30 minutes
to solve this in an actual FAANG interview. Start by clearly explaining the problem so the
reader understands what they need to solve before diving into approaches.

Return as JSON:
{{
    "problem_title": "{question['title']}",
    "difficulty": "{question['difficulty']}",
    "pattern_used": "{question['pattern']}",
    "problem_explanation": "Clear explanation of the problem statement in markdown. Include: what the input is, what the output should be, the constraints, and 1-2 concrete examples with input/output. Make sure the reader fully understands the problem before moving on.",
    "interviewer_expects": "What the interviewer is really testing with this problem",
    "brute_force": "Brief brute force approach and why it's not good enough",
    "optimal_approach": "Step-by-step optimal approach in plain English",
    "key_insight": "The single 'aha!' moment that unlocks the solution",
    "solution_code": "Clean, well-commented {language} solution",
    "dry_run": "Walk through a concrete example step by step",
    "complexity": {{"time": "O(?)", "space": "O(?)"}},
    "follow_up_questions": ["What the interviewer might ask as follow-up"],
    "interview_tips": ["How to communicate your thinking", "Edge cases to mention"]
}}"""

    result = None
    try:
        result = await _call_llm(AI_SOLVE_SYSTEM_PROMPT, prompt, json_mode=True)
        parsed = _repair_and_parse_json(result)
        # Normalize fields: LLMs sometimes return nested objects where strings
        # are expected. Convert dicts to readable markdown strings.
        for key in ("problem_explanation", "brute_force", "optimal_approach",
                     "key_insight", "dry_run", "interviewer_expects"):
            val = parsed.get(key)
            if isinstance(val, dict):
                parts = []
                for k, v in val.items():
                    label = k.replace("_", " ").title()
                    if isinstance(v, dict):
                        v = ", ".join(f"**{sk}**: {sv}" for sk, sv in v.items())
                    parts.append(f"**{label}:** {v}")
                parsed[key] = "\n\n".join(parts)
            elif isinstance(val, list):
                parsed[key] = "\n".join(f"- {item}" for item in val)
        # Normalize solution_code: may arrive as {language, code} dict
        sc = parsed.get("solution_code")
        if isinstance(sc, dict):
            code = sc.get("code", sc.get("solution", ""))
            lang = sc.get("language", language)
            parsed["solution_code"] = f"```{lang}\n{code.strip()}\n```" if code else ""
        parsed["ai_generated"] = True
        return parsed
    except Exception as e:
        print(f"[FAANG Walkthrough] Failed to parse LLM response: {e}")
        return {
            "ai_generated": False,
            "ai_error": str(e),
            "problem_title": question["title"],
            "difficulty": question["difficulty"],
            "pattern_used": question["pattern"],
            "problem_explanation": f"**{question['title']}** (LeetCode #{question['leetcode']})\n\nEnable AI for a detailed problem explanation with examples.",
            "interviewer_expects": f"Understanding of the {question['pattern']} pattern and clean implementation.",
            "brute_force": "The brute force approach is usually O(n^2). Enable AI for detailed analysis.",
            "optimal_approach": f"Use the {question['pattern']} pattern for an optimal solution.",
            "key_insight": question["why"],
            "solution_code": f"# {question['title']}\n# Enable AI for the complete solution\npass",
            "dry_run": "Enable AI for a step-by-step walkthrough.",
            "complexity": {"time": "Varies", "space": "Varies"},
            "follow_up_questions": ["Can you optimize the space complexity?", "What if the input is very large?"],
            "interview_tips": ["Talk through your approach before coding", "Mention edge cases"],
        }
