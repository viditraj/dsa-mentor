"""Pattern Recognition Engine — comprehensive DSA pattern data and matching."""

# ── Full pattern catalog with recognition cues ──
PATTERNS = {
    "two_pointers": {
        "name": "Two Pointers",
        "emoji": "👉👈",
        "description": "Use two pointers to traverse a data structure from different positions.",
        "when_to_use": [
            "Sorted array with pair/triplet lookup",
            "Palindrome checking",
            "Removing duplicates in-place",
            "Container with most water / trapping rain",
            "Linked list cycle or intersection",
        ],
        "recognition_cues": [
            "Array is sorted (or can be sorted)",
            "Need to find pair/triplet that satisfies a condition",
            "Asked to do something in-place with O(1) space",
            "Two ends converging toward the middle",
            "Fast and slow pointer scenario (linked list)",
        ],
        "template": """def two_pointer(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        # check condition
        if condition_met(arr[left], arr[right]):
            return result
        elif need_bigger:
            left += 1
        else:
            right -= 1""",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "related_patterns": ["sliding_window", "binary_search"],
        "example_problems": ["Two Sum II", "3Sum", "Container With Most Water", "Trapping Rain Water"],
    },
    "sliding_window": {
        "name": "Sliding Window",
        "emoji": "🪟",
        "description": "Maintain a window of elements that slides across the array to find optimal subarray/substring.",
        "when_to_use": [
            "Longest/shortest subarray with a constraint",
            "Substring problems (anagrams, permutations)",
            "Maximum sum subarray of size K",
            "Problems asking about contiguous elements",
        ],
        "recognition_cues": [
            "Problem mentions 'subarray' or 'substring'",
            "Asks for longest/shortest contiguous sequence",
            "Constraint on the window (sum, distinct chars, etc.)",
            "Fixed or variable window size",
        ],
        "template": """def sliding_window(arr, k):
    left = 0
    window_state = {}  # track window contents
    best = 0
    for right in range(len(arr)):
        # expand: add arr[right] to window
        update_window(window_state, arr[right])
        # shrink: while window invalid
        while window_invalid(window_state):
            remove_from_window(window_state, arr[left])
            left += 1
        best = max(best, right - left + 1)
    return best""",
        "time_complexity": "O(n)",
        "space_complexity": "O(k) where k = window content",
        "related_patterns": ["two_pointers", "hash_map"],
        "example_problems": ["Longest Substring Without Repeating Characters", "Minimum Window Substring", "Sliding Window Maximum"],
    },
    "hash_map": {
        "name": "Hash Map / Frequency Count",
        "emoji": "🗂️",
        "description": "Use a hash map for O(1) lookups, frequency counting, or complement finding.",
        "when_to_use": [
            "O(1) lookup needed (complement, seen before?)",
            "Counting frequency of elements",
            "Grouping by some key",
            "Finding duplicates or unique elements",
        ],
        "recognition_cues": [
            "'Find if target - x exists' → complement lookup",
            "Need to count occurrences",
            "Group anagrams or similar items",
            "Problem has O(n²) brute force → hash map gives O(n)",
        ],
        "template": """def hash_map_pattern(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i""",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "related_patterns": ["two_pointers", "sliding_window"],
        "example_problems": ["Two Sum", "Group Anagrams", "Top K Frequent Elements"],
    },
    "binary_search": {
        "name": "Binary Search",
        "emoji": "🔍",
        "description": "Divide search space in half each step. Works on sorted data or monotonic functions.",
        "when_to_use": [
            "Sorted array search",
            "Search on answer (minimize/maximize)",
            "Rotated sorted array",
            "Finding boundary (first/last occurrence)",
        ],
        "recognition_cues": [
            "Array is sorted",
            "'Find minimum X such that condition is true'",
            "Problem has monotonic property (if X works, X+1 works too)",
            "O(log n) time hint or requirement",
        ],
        "template": """def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1  # or lo for insertion point""",
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "related_patterns": ["two_pointers"],
        "example_problems": ["Binary Search", "Search in Rotated Sorted Array", "Koko Eating Bananas"],
    },
    "bfs": {
        "name": "BFS (Breadth-First Search)",
        "emoji": "🌊",
        "description": "Explore nodes level by level using a queue. Best for shortest path in unweighted graphs.",
        "when_to_use": [
            "Shortest path in unweighted graph/grid",
            "Level-order traversal of tree",
            "Multi-source BFS (rotting oranges)",
            "Finding nearest X in grid",
        ],
        "recognition_cues": [
            "'Shortest' or 'minimum steps' in unweighted graph",
            "Grid/matrix traversal ('how many moves to reach X')",
            "Level by level processing",
            "Multiple starting points spreading simultaneously",
        ],
        "template": """from collections import deque
def bfs(graph, start):
    queue = deque([start])
    visited = {start}
    level = 0
    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        level += 1""",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "related_patterns": ["dfs", "topological_sort"],
        "example_problems": ["Number of Islands", "Rotting Oranges", "Word Ladder"],
    },
    "dfs": {
        "name": "DFS (Depth-First Search)",
        "emoji": "🏊",
        "description": "Explore as deep as possible before backtracking. Uses stack or recursion.",
        "when_to_use": [
            "Connected components / flood fill",
            "Cycle detection",
            "Path finding (all paths, any path)",
            "Tree problems (height, diameter, path sum)",
        ],
        "recognition_cues": [
            "Tree traversal or tree property questions",
            "'Find all paths' or 'does a path exist'",
            "Connected components counting",
            "Grid flood fill",
        ],
        "template": """def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)""",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V) for recursion stack",
        "related_patterns": ["bfs", "backtracking"],
        "example_problems": ["Clone Graph", "Number of Islands", "Pacific Atlantic Water Flow"],
    },
    "backtracking": {
        "name": "Backtracking",
        "emoji": "🔙",
        "description": "Build solution incrementally, abandon (backtrack) invalid paths early.",
        "when_to_use": [
            "Generate all combinations / permutations / subsets",
            "Constraint satisfaction (N-Queens, Sudoku)",
            "Partition problems",
            "Word search in grid",
        ],
        "recognition_cues": [
            "'Generate all possible...' or 'find all valid...'",
            "Decision tree with constraints",
            "Combinatorial explosion → need pruning",
            "Choose → Explore → Unchoose pattern",
        ],
        "template": """def backtrack(candidates, path, result):
    if is_valid_solution(path):
        result.append(path[:])
        return
    for i, candidate in enumerate(candidates):
        if not is_valid(candidate):
            continue
        path.append(candidate)  # choose
        backtrack(candidates[i+1:], path, result)  # explore
        path.pop()  # unchoose""",
        "time_complexity": "O(2^n) or O(n!)",
        "space_complexity": "O(n) recursion depth",
        "related_patterns": ["dfs", "dp_linear"],
        "example_problems": ["Subsets", "Permutations", "N-Queens", "Combination Sum"],
    },
    "dp_linear": {
        "name": "1D Dynamic Programming",
        "emoji": "📊",
        "description": "Build optimal solution step by step, using previous results.",
        "when_to_use": [
            "Optimization (min cost, max profit)",
            "Counting (number of ways)",
            "Sequence problems (LIS, word break)",
            "Decision at each step (take or skip)",
        ],
        "recognition_cues": [
            "'Minimum/maximum' or 'number of ways'",
            "Each decision depends on previous decisions",
            "Overlapping subproblems (same computation repeated)",
            "Can define state: dp[i] = best answer using first i elements",
        ],
        "template": """def dp_linear(nums):
    n = len(nums)
    dp = [0] * (n + 1)
    dp[0] = base_case
    for i in range(1, n + 1):
        dp[i] = best(dp[i-1] + ..., dp[i-2] + ..., ...)
    return dp[n]""",
        "time_complexity": "O(n) or O(n²)",
        "space_complexity": "O(n), often optimizable to O(1)",
        "related_patterns": ["dp_grid", "greedy"],
        "example_problems": ["Climbing Stairs", "House Robber", "Coin Change", "Longest Increasing Subsequence"],
    },
    "dp_grid": {
        "name": "2D Dynamic Programming",
        "emoji": "🧮",
        "description": "DP on 2D table — typically two sequences or grid paths.",
        "when_to_use": [
            "Two strings comparison (LCS, edit distance)",
            "Grid path counting/optimization",
            "Knapsack variants (subset sum, partition)",
            "Interval DP (matrix chain, burst balloons)",
        ],
        "recognition_cues": [
            "Two sequences/strings being compared",
            "Grid with movement constraints",
            "Knapsack-like: items with weight and value",
            "dp[i][j] depends on dp[i-1][j], dp[i][j-1], dp[i-1][j-1]",
        ],
        "template": """def dp_grid(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]""",
        "time_complexity": "O(m × n)",
        "space_complexity": "O(m × n), optimizable to O(n)",
        "related_patterns": ["dp_linear", "backtracking"],
        "example_problems": ["Longest Common Subsequence", "Edit Distance", "Unique Paths"],
    },
    "monotonic_stack": {
        "name": "Monotonic Stack",
        "emoji": "📚",
        "description": "Stack maintaining elements in sorted order for next greater/smaller element queries.",
        "when_to_use": [
            "Next greater/smaller element",
            "Histogram problems (largest rectangle)",
            "Stock span / daily temperatures",
            "Sliding window maximum (with deque variant)",
        ],
        "recognition_cues": [
            "'Next greater element' or 'previous smaller element'",
            "Need to maintain relative order while finding bounds",
            "Histogram or skyline-like problems",
            "O(n) solution replaces O(n²) brute force",
        ],
        "template": """def monotonic_stack(arr):
    stack = []  # indices
    result = [-1] * len(arr)
    for i in range(len(arr)):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            result[idx] = arr[i]  # next greater
        stack.append(i)
    return result""",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "related_patterns": ["sliding_window", "two_pointers"],
        "example_problems": ["Daily Temperatures", "Largest Rectangle in Histogram", "Next Greater Element"],
    },
    "greedy": {
        "name": "Greedy",
        "emoji": "🤑",
        "description": "Make locally optimal choice at each step, hoping for global optimum.",
        "when_to_use": [
            "Interval scheduling / merging",
            "Activity selection",
            "Jump game variants",
            "Huffman coding / optimal merge",
        ],
        "recognition_cues": [
            "Sorting + making one pass gives optimal",
            "Interval problems (merge, non-overlapping)",
            "Can prove greedy choice is always safe",
            "'Can you reach the end?' type problems",
        ],
        "template": """def greedy_interval(intervals):
    intervals.sort(key=lambda x: x[1])  # sort by end time
    count = 0
    end = float('-inf')
    for start, finish in intervals:
        if start >= end:
            count += 1
            end = finish
    return count""",
        "time_complexity": "O(n log n) due to sorting",
        "space_complexity": "O(1)",
        "related_patterns": ["dp_linear", "binary_search"],
        "example_problems": ["Jump Game", "Merge Intervals", "Non-overlapping Intervals"],
    },
    "union_find": {
        "name": "Union-Find (Disjoint Set)",
        "emoji": "🔗",
        "description": "Track connected components efficiently with path compression and union by rank.",
        "when_to_use": [
            "Dynamic connectivity queries",
            "Cycle detection in undirected graphs",
            "Grouping / clustering",
            "Kruskal's MST",
        ],
        "recognition_cues": [
            "'Are X and Y connected?'",
            "Build connections incrementally",
            "Count number of groups/components",
            "Undirected graph cycle detection",
        ],
        "template": """class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True""",
        "time_complexity": "O(α(n)) ≈ O(1) amortized per operation",
        "space_complexity": "O(n)",
        "related_patterns": ["dfs", "bfs"],
        "example_problems": ["Number of Connected Components", "Redundant Connection", "Graph Valid Tree"],
    },
    "topological_sort": {
        "name": "Topological Sort",
        "emoji": "📐",
        "description": "Linear ordering of vertices in a DAG where u comes before v for every edge (u,v).",
        "when_to_use": [
            "Dependency resolution (course schedule)",
            "Build order / compilation order",
            "Detecting cycles in directed graph",
            "Longest path in DAG",
        ],
        "recognition_cues": [
            "Dependencies between tasks",
            "'Order in which to do things'",
            "Directed acyclic graph (DAG)",
            "Course prerequisites pattern",
        ],
        "template": """from collections import deque
def topological_sort(graph, n):
    in_degree = [0] * n
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    queue = deque(i for i in range(n) if in_degree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == n else []  # empty = cycle""",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "related_patterns": ["bfs", "dfs"],
        "example_problems": ["Course Schedule", "Course Schedule II", "Alien Dictionary"],
    },
    "trie": {
        "name": "Trie (Prefix Tree)",
        "emoji": "🌳",
        "description": "Tree structure for efficient prefix-based string operations.",
        "when_to_use": [
            "Autocomplete / prefix search",
            "Word dictionary with startsWith",
            "Word search in grid (multiple words)",
            "Longest common prefix",
        ],
        "recognition_cues": [
            "Multiple string lookups with common prefixes",
            "'Starts with' queries",
            "Dictionary of words + search patterns",
            "XOR-based problems (binary trie)",
        ],
        "template": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True""",
        "time_complexity": "O(L) per operation, L = word length",
        "space_complexity": "O(total characters)",
        "related_patterns": ["dfs", "backtracking"],
        "example_problems": ["Implement Trie", "Word Search II", "Design Add and Search Words"],
    },
    "heap_top_k": {
        "name": "Heap / Top-K",
        "emoji": "⛰️",
        "description": "Use heap (priority queue) for efficient K-largest/smallest or streaming median.",
        "when_to_use": [
            "Top K / Kth largest element",
            "K-way merge (merge K sorted lists)",
            "Running median (two heaps)",
            "Priority-based scheduling",
        ],
        "recognition_cues": [
            "'Kth largest' or 'top K' in problem title",
            "Merge multiple sorted sequences",
            "'Median' of streaming data",
            "Need repeated min/max extraction",
        ],
        "template": """import heapq
def top_k(nums, k):
    # Min-heap of size k for top K largest
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap""",
        "time_complexity": "O(n log k)",
        "space_complexity": "O(k)",
        "related_patterns": ["binary_search", "greedy"],
        "example_problems": ["Kth Largest Element", "Top K Frequent Elements", "Find Median from Data Stream"],
    },
}

# Map problem names to their primary and secondary patterns
PROBLEM_PATTERN_MAP = {
    "Two Sum": {"primary": "hash_map", "secondary": ["two_pointers"]},
    "Two Sum II": {"primary": "two_pointers", "secondary": ["binary_search"]},
    "3Sum": {"primary": "two_pointers", "secondary": ["hash_map"]},
    "Container With Most Water": {"primary": "two_pointers", "secondary": []},
    "Trapping Rain Water": {"primary": "two_pointers", "secondary": ["monotonic_stack"]},
    "Longest Substring Without Repeating Characters": {"primary": "sliding_window", "secondary": ["hash_map"]},
    "Minimum Window Substring": {"primary": "sliding_window", "secondary": ["hash_map"]},
    "Longest Consecutive Sequence": {"primary": "hash_map", "secondary": []},
    "Top K Frequent Elements": {"primary": "heap_top_k", "secondary": ["hash_map"]},
    "Valid Sudoku": {"primary": "hash_map", "secondary": []},
    "Reverse Linked List": {"primary": "two_pointers", "secondary": []},
    "Merge Two Sorted Lists": {"primary": "two_pointers", "secondary": []},
    "Linked List Cycle": {"primary": "two_pointers", "secondary": []},
    "Remove Nth Node From End of List": {"primary": "two_pointers", "secondary": []},
    "Valid Parentheses": {"primary": "monotonic_stack", "secondary": []},
    "Min Stack": {"primary": "monotonic_stack", "secondary": []},
    "Daily Temperatures": {"primary": "monotonic_stack", "secondary": []},
    "Largest Rectangle in Histogram": {"primary": "monotonic_stack", "secondary": []},
    "Binary Tree Inorder Traversal": {"primary": "dfs", "secondary": []},
    "Maximum Depth of Binary Tree": {"primary": "dfs", "secondary": ["bfs"]},
    "Invert Binary Tree": {"primary": "dfs", "secondary": ["bfs"]},
    "Binary Tree Level Order Traversal": {"primary": "bfs", "secondary": []},
    "Validate Binary Search Tree": {"primary": "dfs", "secondary": []},
    "Lowest Common Ancestor of a BST": {"primary": "dfs", "secondary": ["binary_search"]},
    "Kth Smallest Element in a BST": {"primary": "dfs", "secondary": ["heap_top_k"]},
    "Binary Tree Maximum Path Sum": {"primary": "dfs", "secondary": ["dp_linear"]},
    "Implement Trie (Prefix Tree)": {"primary": "trie", "secondary": []},
    "Word Search II": {"primary": "trie", "secondary": ["backtracking", "dfs"]},
    "Kth Largest Element in an Array": {"primary": "heap_top_k", "secondary": ["binary_search"]},
    "Find Median from Data Stream": {"primary": "heap_top_k", "secondary": []},
    "Task Scheduler": {"primary": "heap_top_k", "secondary": ["greedy"]},
    "Number of Islands": {"primary": "dfs", "secondary": ["bfs", "union_find"]},
    "Clone Graph": {"primary": "bfs", "secondary": ["dfs"]},
    "Pacific Atlantic Water Flow": {"primary": "dfs", "secondary": ["bfs"]},
    "Course Schedule": {"primary": "topological_sort", "secondary": ["dfs"]},
    "Course Schedule II": {"primary": "topological_sort", "secondary": []},
    "Rotting Oranges": {"primary": "bfs", "secondary": []},
    "Graph Valid Tree": {"primary": "union_find", "secondary": ["dfs"]},
    "Redundant Connection": {"primary": "union_find", "secondary": []},
    "Network Delay Time": {"primary": "bfs", "secondary": ["heap_top_k"]},
    "Binary Search": {"primary": "binary_search", "secondary": []},
    "Search in Rotated Sorted Array": {"primary": "binary_search", "secondary": []},
    "Find Minimum in Rotated Sorted Array": {"primary": "binary_search", "secondary": []},
    "Koko Eating Bananas": {"primary": "binary_search", "secondary": []},
    "Median of Two Sorted Arrays": {"primary": "binary_search", "secondary": []},
    "Subsets": {"primary": "backtracking", "secondary": []},
    "Combination Sum": {"primary": "backtracking", "secondary": []},
    "Permutations": {"primary": "backtracking", "secondary": []},
    "Word Search": {"primary": "backtracking", "secondary": ["dfs"]},
    "N-Queens": {"primary": "backtracking", "secondary": []},
    "Climbing Stairs": {"primary": "dp_linear", "secondary": []},
    "House Robber": {"primary": "dp_linear", "secondary": []},
    "Coin Change": {"primary": "dp_linear", "secondary": []},
    "Longest Increasing Subsequence": {"primary": "dp_linear", "secondary": ["binary_search"]},
    "Word Break": {"primary": "dp_linear", "secondary": ["trie"]},
    "Unique Paths": {"primary": "dp_grid", "secondary": []},
    "Longest Common Subsequence": {"primary": "dp_grid", "secondary": []},
    "Edit Distance": {"primary": "dp_grid", "secondary": []},
    "Target Sum": {"primary": "dp_grid", "secondary": ["backtracking"]},
    "Jump Game": {"primary": "greedy", "secondary": ["dp_linear"]},
    "Jump Game II": {"primary": "greedy", "secondary": ["bfs"]},
    "Gas Station": {"primary": "greedy", "secondary": []},
    "Merge Intervals": {"primary": "greedy", "secondary": []},
    "Non-overlapping Intervals": {"primary": "greedy", "secondary": []},
    "Single Number": {"primary": "hash_map", "secondary": []},
    "LRU Cache": {"primary": "hash_map", "secondary": []},
    "Rotate Image": {"primary": "two_pointers", "secondary": []},
    "Spiral Matrix": {"primary": "two_pointers", "secondary": []},
}


def get_pattern_for_problem(problem_title: str) -> dict:
    """Get pattern info for a specific problem."""
    mapping = PROBLEM_PATTERN_MAP.get(problem_title, None)
    if not mapping:
        return {"primary": None, "secondary": [], "patterns": {}}

    primary_key = mapping["primary"]
    primary = PATTERNS.get(primary_key, {})
    secondary = [PATTERNS.get(k, {}) for k in mapping.get("secondary", []) if k in PATTERNS]

    return {
        "primary": {**primary, "key": primary_key},
        "secondary": [{"key": k, **PATTERNS.get(k, {})} for k in mapping.get("secondary", [])],
    }


def get_all_patterns() -> list:
    """Get all patterns as a list for the frontend."""
    return [
        {"key": key, **pattern}
        for key, pattern in PATTERNS.items()
    ]


def match_patterns_to_problem(problem_title: str, problem_description: str = "") -> list:
    """Heuristic pattern matching based on problem title/description keywords."""
    text = f"{problem_title} {problem_description}".lower()

    keyword_map = {
        "two_pointers": ["two pointer", "sorted array", "palindrome", "in-place", "container", "water"],
        "sliding_window": ["substring", "subarray", "window", "contiguous", "consecutive"],
        "hash_map": ["frequency", "count", "sum", "duplicate", "anagram", "group"],
        "binary_search": ["sorted", "search", "rotated", "minimum in", "koko", "median of two"],
        "bfs": ["shortest path", "level order", "rotting", "nearest", "minimum steps"],
        "dfs": ["depth", "path sum", "connected", "island", "flood", "tree"],
        "backtracking": ["permutation", "combination", "subset", "generate all", "n-queen", "word search"],
        "dp_linear": ["climbing", "robber", "coin", "longest increasing", "word break", "decode"],
        "dp_grid": ["unique path", "edit distance", "common subsequence", "knapsack", "target sum"],
        "monotonic_stack": ["next greater", "temperature", "histogram", "stock span"],
        "greedy": ["jump game", "interval", "merge interval", "gas station", "activity"],
        "union_find": ["connected component", "redundant", "valid tree", "union"],
        "topological_sort": ["course schedule", "prerequisite", "build order", "alien dictionary"],
        "trie": ["prefix", "trie", "autocomplete", "word search ii"],
        "heap_top_k": ["kth largest", "top k", "median", "merge k", "priority"],
    }

    matches = []
    for pattern_key, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            matches.append((pattern_key, score))

    matches.sort(key=lambda x: x[1], reverse=True)
    return [{"key": k, "score": s, **PATTERNS[k]} for k, s in matches[:3]]
