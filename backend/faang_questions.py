"""
FAANG 75 - The Ultimate Interview Crash Course Question Bank.

75 most-asked coding problems that cover 90%+ of DSA patterns tested at
Google, Meta, Amazon, Apple, Netflix, Microsoft, and top-tier startups.

Organized by PATTERN (not topic) so you learn to recognize and reuse
the same mental framework across seemingly different problems.
"""

# ─────────────────────────────────────────────
# PATTERN CATALOG  (15 patterns, 75 problems)
# ─────────────────────────────────────────────

FAANG_PATTERNS = {
    # ── PHASE 1: Foundation Patterns ──────────
    "two_pointers": {
        "name": "Two Pointers",
        "emoji": "👉👈",
        "phase": 1,
        "phase_name": "Foundation Patterns",
        "order": 1,
        "difficulty": "easy",
        "estimated_hours": 4,
        "story": (
            "Imagine you're at a bookshelf looking for two books whose combined page count "
            "equals exactly 500. Instead of checking every pair (which takes forever), you "
            "put one finger at the thinnest book and another at the thickest. If the total "
            "is too big, move the right finger left; too small, move the left finger right. "
            "Two pointers is that elegant dance — two markers walking toward each other (or "
            "in the same direction) to shrink the search space from O(n^2) to O(n)."
        ),
        "intuition": "When the input is sorted (or can be sorted), use two markers to eliminate possibilities from both ends.",
        "template": (
            "def two_pointer(arr, target):\n"
            "    left, right = 0, len(arr) - 1\n"
            "    while left < right:\n"
            "        curr = arr[left] + arr[right]\n"
            "        if curr == target:\n"
            "            return [left, right]\n"
            "        elif curr < target:\n"
            "            left += 1\n"
            "        else:\n"
            "            right -= 1\n"
            "    return []"
        ),
        "when_to_use": [
            "Array is sorted or can be sorted",
            "Need to find a pair/triplet with a target sum",
            "Remove duplicates in-place",
            "Palindrome checks",
            "Merging two sorted arrays",
        ],
        "complexity": {"time": "O(n)", "space": "O(1)"},
    },

    "sliding_window": {
        "name": "Sliding Window",
        "emoji": "🪟",
        "phase": 1,
        "phase_name": "Foundation Patterns",
        "order": 2,
        "difficulty": "easy",
        "estimated_hours": 4,
        "story": (
            "Picture yourself on a train looking through a window. As the train moves, "
            "the scenery in the window changes — some things slide out on the left while "
            "new things appear on the right. That's a sliding window: you maintain a "
            "'window' of elements and slide it across the array. Instead of recalculating "
            "everything from scratch each time, you just update what entered and what left. "
            "This turns O(n*k) brute force into O(n) magic."
        ),
        "intuition": "When you need the best/longest/shortest contiguous subarray or substring, slide a window and track your answer.",
        "template": (
            "def sliding_window(arr, k):\n"
            "    window_sum = sum(arr[:k])\n"
            "    best = window_sum\n"
            "    for i in range(k, len(arr)):\n"
            "        window_sum += arr[i] - arr[i - k]  # slide\n"
            "        best = max(best, window_sum)\n"
            "    return best\n"
            "\n"
            "# Variable-size window:\n"
            "def variable_window(s):\n"
            "    left = 0\n"
            "    seen = set()\n"
            "    best = 0\n"
            "    for right in range(len(s)):\n"
            "        while s[right] in seen:\n"
            "            seen.remove(s[left])\n"
            "            left += 1\n"
            "        seen.add(s[right])\n"
            "        best = max(best, right - left + 1)\n"
            "    return best"
        ),
        "when_to_use": [
            "Find longest/shortest subarray with a condition",
            "Substring with at most K distinct characters",
            "Maximum sum subarray of size K",
            "Any 'contiguous' subarray/substring problem",
        ],
        "complexity": {"time": "O(n)", "space": "O(k)"},
    },

    "hash_map": {
        "name": "Hash Map",
        "emoji": "🗺️",
        "phase": 1,
        "phase_name": "Foundation Patterns",
        "order": 3,
        "difficulty": "easy",
        "estimated_hours": 3,
        "story": (
            "Think of a hash map as your personal assistant with a perfect memory. "
            "You hand them items and ask 'have you seen this before?' — they answer "
            "instantly, no matter how many items they've memorized. While brute force "
            "searches take O(n) to find something, a hash map does it in O(1). "
            "It's the Swiss Army knife of DSA — the single most versatile pattern "
            "you'll ever learn. When in doubt, reach for a hash map."
        ),
        "intuition": "Trade space for time. Store what you've seen so you can answer 'does X exist?' in O(1).",
        "template": (
            "def hash_map_pattern(arr, target):\n"
            "    seen = {}  # value -> index\n"
            "    for i, num in enumerate(arr):\n"
            "        complement = target - num\n"
            "        if complement in seen:\n"
            "            return [seen[complement], i]\n"
            "        seen[num] = i\n"
            "    return []"
        ),
        "when_to_use": [
            "Need O(1) lookup for 'have I seen this?'",
            "Counting frequency of elements",
            "Finding pairs/complements",
            "Grouping anagrams or similar items",
            "Two Sum pattern (target - current)",
        ],
        "complexity": {"time": "O(n)", "space": "O(n)"},
    },

    "binary_search": {
        "name": "Binary Search",
        "emoji": "🔍",
        "phase": 1,
        "phase_name": "Foundation Patterns",
        "order": 4,
        "difficulty": "medium",
        "estimated_hours": 5,
        "story": (
            "Remember the number guessing game? 'I'm thinking of a number 1-100.' "
            "You wouldn't guess 1, 2, 3… You'd say 50, then 25 or 75, cutting the "
            "range in half each time. That's binary search — the art of halving. "
            "But it's not just for sorted arrays. Any time you have a monotonic "
            "condition (all falses then all trues), you can binary search the "
            "boundary. This insight unlocks 'search on answer' — one of the most "
            "powerful interview techniques."
        ),
        "intuition": "If you can answer 'is X too big or too small?', you can binary search it. Halving = O(log n).",
        "template": (
            "def binary_search(arr, target):\n"
            "    lo, hi = 0, len(arr) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return -1\n"
            "\n"
            "# Search on answer:\n"
            "def search_on_answer(lo, hi, is_feasible):\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if is_feasible(mid):\n"
            "            hi = mid\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "    return lo"
        ),
        "when_to_use": [
            "Sorted array search",
            "'Find minimum X such that…' (search on answer)",
            "Rotated sorted array problems",
            "Finding boundaries (first/last occurrence)",
            "Problems where O(n) is too slow and data is monotonic",
        ],
        "complexity": {"time": "O(log n)", "space": "O(1)"},
    },

    # ── PHASE 2: Core Data Structures ─────────
    "stack": {
        "name": "Stack (Monotonic)",
        "emoji": "📚",
        "phase": 2,
        "phase_name": "Core Data Structures",
        "order": 5,
        "difficulty": "medium",
        "estimated_hours": 4,
        "story": (
            "A stack of plates at a buffet: you can only add or remove from the top. "
            "Simple, right? But here's where it gets powerful — a MONOTONIC stack keeps "
            "elements in sorted order. Imagine a bouncer at a club who kicks out anyone "
            "shorter than the new person arriving. This lets you find the 'next greater "
            "element' for every item in O(n). It's the secret weapon for temperature "
            "problems, histogram areas, and stock span questions."
        ),
        "intuition": "When you need the 'next greater/smaller' element, or need to match brackets, think stack.",
        "template": (
            "def next_greater(arr):\n"
            "    n = len(arr)\n"
            "    result = [-1] * n\n"
            "    stack = []  # indices, monotonically decreasing values\n"
            "    for i in range(n):\n"
            "        while stack and arr[i] > arr[stack[-1]]:\n"
            "            idx = stack.pop()\n"
            "            result[idx] = arr[i]\n"
            "        stack.append(i)\n"
            "    return result"
        ),
        "when_to_use": [
            "Next greater/smaller element",
            "Valid parentheses / bracket matching",
            "Largest rectangle in histogram",
            "Daily temperatures / stock span",
            "Expression evaluation",
        ],
        "complexity": {"time": "O(n)", "space": "O(n)"},
    },

    "linked_list": {
        "name": "Linked List",
        "emoji": "🔗",
        "phase": 2,
        "phase_name": "Core Data Structures",
        "order": 6,
        "difficulty": "medium",
        "estimated_hours": 4,
        "story": (
            "Think of a conga line at a party — each person holds the shoulders of "
            "the person in front. To find someone, you start at the front and walk "
            "through. To insert someone, you just change who's holding whom. "
            "Linked list problems are really about pointer manipulation — the 'fast "
            "and slow' pointer trick (tortoise and hare) is pure genius. One pointer "
            "moves twice as fast; when it reaches the end, the slow pointer is at "
            "the middle. If there's a cycle, they'll eventually meet."
        ),
        "intuition": "Draw it out. Use dummy nodes to simplify edge cases. Fast/slow pointers solve cycle and midpoint problems.",
        "template": (
            "def reverse_linked_list(head):\n"
            "    prev, curr = None, head\n"
            "    while curr:\n"
            "        nxt = curr.next\n"
            "        curr.next = prev\n"
            "        prev = curr\n"
            "        curr = nxt\n"
            "    return prev\n"
            "\n"
            "def find_middle(head):\n"
            "    slow = fast = head\n"
            "    while fast and fast.next:\n"
            "        slow = slow.next\n"
            "        fast = fast.next.next\n"
            "    return slow"
        ),
        "when_to_use": [
            "Reverse a linked list (iterative or recursive)",
            "Detect cycle (Floyd's tortoise & hare)",
            "Find middle element",
            "Merge two sorted lists",
            "Remove Nth node from end",
        ],
        "complexity": {"time": "O(n)", "space": "O(1)"},
    },

    "tree_traversal": {
        "name": "Trees (BFS/DFS)",
        "emoji": "🌳",
        "phase": 2,
        "phase_name": "Core Data Structures",
        "order": 7,
        "difficulty": "medium",
        "estimated_hours": 6,
        "story": (
            "Think of a family tree. DFS is like following one branch all the way "
            "to the youngest descendant before backtracking — depth first. BFS is "
            "like taking a family photo at each generation — breadth first, level by "
            "level. Most tree problems boil down to: 'What question do I ask each "
            "node, and do I go depth-first or breadth-first?' DFS uses recursion "
            "(the call stack), BFS uses a queue. If you can solve tree problems, "
            "you can solve 30% of all interview questions."
        ),
        "intuition": "For each node, think: what info do I need from my left and right children? That's your recursion.",
        "template": (
            "# DFS - recursive\n"
            "def dfs(node):\n"
            "    if not node:\n"
            "        return 0  # base case\n"
            "    left = dfs(node.left)\n"
            "    right = dfs(node.right)\n"
            "    return 1 + max(left, right)  # combine\n"
            "\n"
            "# BFS - level order\n"
            "from collections import deque\n"
            "def bfs(root):\n"
            "    if not root:\n"
            "        return []\n"
            "    queue = deque([root])\n"
            "    levels = []\n"
            "    while queue:\n"
            "        level = []\n"
            "        for _ in range(len(queue)):\n"
            "            node = queue.popleft()\n"
            "            level.append(node.val)\n"
            "            if node.left:  queue.append(node.left)\n"
            "            if node.right: queue.append(node.right)\n"
            "        levels.append(level)\n"
            "    return levels"
        ),
        "when_to_use": [
            "Tree depth, height, diameter",
            "Level-order traversal",
            "Validate BST",
            "Path sum problems",
            "Lowest common ancestor",
            "Serialize / deserialize tree",
        ],
        "complexity": {"time": "O(n)", "space": "O(h) DFS / O(w) BFS"},
    },

    "heap": {
        "name": "Heap / Priority Queue",
        "emoji": "⛰️",
        "phase": 2,
        "phase_name": "Core Data Structures",
        "order": 8,
        "difficulty": "medium",
        "estimated_hours": 3,
        "story": (
            "Imagine a hospital ER where the sickest patients are always treated "
            "first, regardless of arrival order. That's a priority queue backed by "
            "a heap. A min-heap always gives you the smallest element in O(1), and "
            "lets you insert/remove in O(log n). The trick for 'Top K' problems: "
            "use a min-heap of size K. Every element competes to stay in the top K. "
            "When the heap overflows, the smallest (least worthy) gets kicked out. "
            "At the end, everything in the heap is your answer."
        ),
        "intuition": "'Top K' or 'Kth largest' = heap. 'Median' = two heaps. 'Merge K sorted' = heap.",
        "template": (
            "import heapq\n"
            "\n"
            "# Top K elements\n"
            "def top_k(arr, k):\n"
            "    return heapq.nlargest(k, arr)\n"
            "\n"
            "# Kth largest (min-heap of size k)\n"
            "def kth_largest(arr, k):\n"
            "    heap = arr[:k]\n"
            "    heapq.heapify(heap)\n"
            "    for num in arr[k:]:\n"
            "        if num > heap[0]:\n"
            "            heapq.heapreplace(heap, num)\n"
            "    return heap[0]\n"
            "\n"
            "# Merge K sorted lists\n"
            "def merge_k(lists):\n"
            "    heap = []\n"
            "    for i, lst in enumerate(lists):\n"
            "        if lst:\n"
            "            heapq.heappush(heap, (lst[0], i, 0))\n"
            "    result = []\n"
            "    while heap:\n"
            "        val, li, idx = heapq.heappop(heap)\n"
            "        result.append(val)\n"
            "        if idx + 1 < len(lists[li]):\n"
            "            heapq.heappush(heap, (lists[li][idx+1], li, idx+1))\n"
            "    return result"
        ),
        "when_to_use": [
            "Top K / Kth largest or smallest",
            "Merge K sorted lists/arrays",
            "Running median (two heaps)",
            "Task scheduling with priorities",
            "Dijkstra's shortest path",
        ],
        "complexity": {"time": "O(n log k)", "space": "O(k)"},
    },

    # ── PHASE 3: Graph & Search ───────────────
    "graph_bfs_dfs": {
        "name": "Graph BFS/DFS",
        "emoji": "🕸️",
        "phase": 3,
        "phase_name": "Graph & Search",
        "order": 9,
        "difficulty": "medium",
        "estimated_hours": 6,
        "story": (
            "Imagine you're in a maze. DFS is like always turning left — you go as "
            "deep as you can before backtracking. BFS is like a flood — water spreads "
            "to all neighboring cells at the same time, level by level. In interviews, "
            "graphs appear as grids, social networks, and dependency chains. The trick "
            "is recognizing: 'Is this really a graph problem?' Islands in a grid? Graph. "
            "Friend of a friend? Graph. Can I reach X from Y? Graph. Then pick BFS for "
            "shortest path, DFS for exploring all paths."
        ),
        "intuition": "BFS = shortest path (unweighted). DFS = explore all / connected components. Grid = implicit graph.",
        "template": (
            "from collections import deque\n"
            "\n"
            "# BFS on grid\n"
            "def bfs_grid(grid, start):\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    queue = deque([start])\n"
            "    visited = {start}\n"
            "    while queue:\n"
            "        r, c = queue.popleft()\n"
            "        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:\n"
            "            nr, nc = r+dr, c+dc\n"
            "            if 0<=nr<rows and 0<=nc<cols and (nr,nc) not in visited and grid[nr][nc]==1:\n"
            "                visited.add((nr,nc))\n"
            "                queue.append((nr,nc))\n"
            "    return visited\n"
            "\n"
            "# DFS - connected components\n"
            "def count_components(graph, n):\n"
            "    visited = set()\n"
            "    count = 0\n"
            "    def dfs(node):\n"
            "        visited.add(node)\n"
            "        for nei in graph[node]:\n"
            "            if nei not in visited:\n"
            "                dfs(nei)\n"
            "    for i in range(n):\n"
            "        if i not in visited:\n"
            "            dfs(i)\n"
            "            count += 1\n"
            "    return count"
        ),
        "when_to_use": [
            "Number of islands / connected components",
            "Shortest path in unweighted graph (BFS)",
            "Detect cycle in graph",
            "Clone graph",
            "Word ladder / transformation",
            "Rotting oranges (multi-source BFS)",
        ],
        "complexity": {"time": "O(V + E)", "space": "O(V)"},
    },

    "backtracking": {
        "name": "Backtracking",
        "emoji": "🔙",
        "phase": 3,
        "phase_name": "Graph & Search",
        "order": 10,
        "difficulty": "medium",
        "estimated_hours": 5,
        "story": (
            "Remember those choose-your-own-adventure books? You pick a path, and if "
            "it leads to a dead end, you go back and try a different choice. That's "
            "backtracking — systematic trial and error. You build a solution piece by "
            "piece: CHOOSE an option, EXPLORE further, and if it fails, UNCHOOSE "
            "(undo) and try the next option. It's how you generate all permutations, "
            "combinations, subsets, and solve puzzles like N-Queens and Sudoku."
        ),
        "intuition": "Choose -> Explore -> Unchoose. Draw the decision tree — each branch is a choice, each leaf is a solution.",
        "template": (
            "def backtrack(candidates, path, result):\n"
            "    if is_solution(path):  # base case\n"
            "        result.append(path[:])  # copy!\n"
            "        return\n"
            "    for i, choice in enumerate(candidates):\n"
            "        if not is_valid(choice, path):  # prune\n"
            "            continue\n"
            "        path.append(choice)              # choose\n"
            "        backtrack(candidates[i+1:], path, result)  # explore\n"
            "        path.pop()                       # unchoose"
        ),
        "when_to_use": [
            "'Generate all' combinations/permutations/subsets",
            "Constraint satisfaction (N-Queens, Sudoku)",
            "Word search in grid",
            "Palindrome partitioning",
            "Problems with 'try all possibilities'",
        ],
        "complexity": {"time": "O(2^n) or O(n!)", "space": "O(n)"},
    },

    "trie": {
        "name": "Trie (Prefix Tree)",
        "emoji": "🌲",
        "phase": 3,
        "phase_name": "Graph & Search",
        "order": 11,
        "difficulty": "medium",
        "estimated_hours": 3,
        "story": (
            "Open your phone and start typing 'hel'. Instantly, it suggests 'hello', "
            "'help', 'helmet'. How? A trie — a tree where each branch is a letter. "
            "Words sharing prefixes share branches. To check if 'hello' exists, you "
            "walk h→e→l→l→o down the tree. It's like a dictionary organized so every "
            "prefix lookup is O(length of word), not O(n * length). Tries are essential "
            "for autocomplete, spell-check, and word games."
        ),
        "intuition": "Prefix-based search? Dictionary of words? Starts-with queries? Build a trie.",
        "template": (
            "class TrieNode:\n"
            "    def __init__(self):\n"
            "        self.children = {}\n"
            "        self.is_end = False\n"
            "\n"
            "class Trie:\n"
            "    def __init__(self):\n"
            "        self.root = TrieNode()\n"
            "\n"
            "    def insert(self, word):\n"
            "        node = self.root\n"
            "        for ch in word:\n"
            "            if ch not in node.children:\n"
            "                node.children[ch] = TrieNode()\n"
            "            node = node.children[ch]\n"
            "        node.is_end = True\n"
            "\n"
            "    def search(self, word):\n"
            "        node = self.root\n"
            "        for ch in word:\n"
            "            if ch not in node.children:\n"
            "                return False\n"
            "            node = node.children[ch]\n"
            "        return node.is_end\n"
            "\n"
            "    def starts_with(self, prefix):\n"
            "        node = self.root\n"
            "        for ch in prefix:\n"
            "            if ch not in node.children:\n"
            "                return False\n"
            "            node = node.children[ch]\n"
            "        return True"
        ),
        "when_to_use": [
            "Prefix-based search / autocomplete",
            "Word dictionary with starts_with",
            "Word search II (trie + backtracking)",
            "Longest common prefix",
            "Counting distinct substrings",
        ],
        "complexity": {"time": "O(L) per operation", "space": "O(N * L)"},
    },

    # ── PHASE 4: Advanced Patterns ────────────
    "dp_1d": {
        "name": "Dynamic Programming (1D)",
        "emoji": "🧮",
        "phase": 4,
        "phase_name": "Advanced Patterns",
        "order": 12,
        "difficulty": "hard",
        "estimated_hours": 8,
        "story": (
            "DP is just 'smart recursion with a notebook'. Imagine climbing stairs — "
            "to reach step 5, you can come from step 4 or step 3. So ways(5) = "
            "ways(4) + ways(3). Without DP you'd recompute ways(3) millions of times. "
            "With DP, you write each answer in your notebook and never solve it twice. "
            "The secret: every DP problem is a recursive problem where subproblems "
            "overlap. Find the recurrence, define your dp array, fill it up, done. "
            "Start with 1D DP — one array, one variable changes."
        ),
        "intuition": "Define dp[i] = answer to subproblem of size i. Find the recurrence: dp[i] = f(dp[i-1], dp[i-2], ...).",
        "template": (
            "# Climbing stairs\n"
            "def dp_1d(n):\n"
            "    if n <= 2:\n"
            "        return n\n"
            "    dp = [0] * (n + 1)\n"
            "    dp[1], dp[2] = 1, 2\n"
            "    for i in range(3, n + 1):\n"
            "        dp[i] = dp[i-1] + dp[i-2]\n"
            "    return dp[n]\n"
            "\n"
            "# Space-optimized\n"
            "def dp_1d_optimized(n):\n"
            "    if n <= 2:\n"
            "        return n\n"
            "    prev2, prev1 = 1, 2\n"
            "    for i in range(3, n + 1):\n"
            "        prev2, prev1 = prev1, prev2 + prev1\n"
            "    return prev1"
        ),
        "when_to_use": [
            "Fibonacci-style recurrences (climbing stairs, house robber)",
            "Coin change / minimum cost",
            "Longest increasing subsequence",
            "Maximum subarray",
            "Word break",
            "'Can I reach…' / 'How many ways…' / 'What's the minimum…'",
        ],
        "complexity": {"time": "O(n) to O(n^2)", "space": "O(n) or O(1)"},
    },

    "dp_2d": {
        "name": "Dynamic Programming (2D)",
        "emoji": "📊",
        "phase": 4,
        "phase_name": "Advanced Patterns",
        "order": 13,
        "difficulty": "hard",
        "estimated_hours": 6,
        "story": (
            "2D DP is like filling in a spreadsheet where each cell depends on its "
            "neighbors. Think of edit distance — how many edits to turn 'kitten' into "
            "'sitting'? You build a grid where dp[i][j] = cost to match the first i "
            "characters of word1 with first j characters of word2. Each cell looks at "
            "the cell above, to the left, and diagonally — choosing the minimum. "
            "When you have TWO sequences or a grid, think 2D DP."
        ),
        "intuition": "Two strings/sequences → 2D table. Grid path problems → 2D table. dp[i][j] uses dp[i-1][j], dp[i][j-1], etc.",
        "template": (
            "# Edit distance\n"
            "def dp_2d(word1, word2):\n"
            "    m, n = len(word1), len(word2)\n"
            "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
            "    for i in range(m + 1):\n"
            "        dp[i][0] = i\n"
            "    for j in range(n + 1):\n"
            "        dp[0][j] = j\n"
            "    for i in range(1, m + 1):\n"
            "        for j in range(1, n + 1):\n"
            "            if word1[i-1] == word2[j-1]:\n"
            "                dp[i][j] = dp[i-1][j-1]\n"
            "            else:\n"
            "                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\n"
            "    return dp[m][n]"
        ),
        "when_to_use": [
            "Two strings → longest common subsequence, edit distance",
            "Grid path counting / minimum path sum",
            "Knapsack variants (0/1 knapsack)",
            "Interleaving strings",
            "Regular expression matching",
        ],
        "complexity": {"time": "O(m * n)", "space": "O(m * n)"},
    },

    "greedy": {
        "name": "Greedy",
        "emoji": "🤑",
        "phase": 4,
        "phase_name": "Advanced Patterns",
        "order": 14,
        "difficulty": "medium",
        "estimated_hours": 4,
        "story": (
            "Greedy is the 'common sense' algorithm. At each step, make the locally "
            "best choice and never look back. Like a hungry person at a buffet who "
            "always picks the most delicious dish available — no planning, no regret. "
            "The catch: greedy only works when local optima lead to global optima. "
            "Interval scheduling? Sort by end time, always pick the earliest-ending "
            "non-overlapping interval. It feels too simple, but it's provably optimal."
        ),
        "intuition": "Sort the input smartly, then make the best choice at each step. Prove it works by exchange argument.",
        "template": (
            "# Interval scheduling\n"
            "def greedy_intervals(intervals):\n"
            "    intervals.sort(key=lambda x: x[1])  # sort by end\n"
            "    count = 0\n"
            "    end = float('-inf')\n"
            "    for start, finish in intervals:\n"
            "        if start >= end:\n"
            "            count += 1\n"
            "            end = finish\n"
            "    return count\n"
            "\n"
            "# Jump game\n"
            "def can_jump(nums):\n"
            "    max_reach = 0\n"
            "    for i, jump in enumerate(nums):\n"
            "        if i > max_reach:\n"
            "            return False\n"
            "        max_reach = max(max_reach, i + jump)\n"
            "    return True"
        ),
        "when_to_use": [
            "Interval scheduling / merging intervals",
            "Jump game variants",
            "Task assignment / meeting rooms",
            "Gas station (circular tour)",
            "Problems where sorting + one pass gives optimal answer",
        ],
        "complexity": {"time": "O(n log n)", "space": "O(1)"},
    },

    "intervals": {
        "name": "Intervals",
        "emoji": "📐",
        "phase": 4,
        "phase_name": "Advanced Patterns",
        "order": 15,
        "difficulty": "medium",
        "estimated_hours": 3,
        "story": (
            "Think of a calendar — meetings are intervals [start, end]. When do they "
            "overlap? Can you fit a new meeting in? How many rooms do you need? "
            "Interval problems are everywhere: scheduling, time ranges, ranges on a "
            "number line. The master key: SORT by start time. Then walk through and "
            "check: does the current interval overlap with the previous? If yes, merge "
            "or count. If no, move on. This 'sort then sweep' pattern handles 90% of "
            "interval problems."
        ),
        "intuition": "Sort by start. Compare current interval's start with previous interval's end. Overlap if start < prev_end.",
        "template": (
            "def merge_intervals(intervals):\n"
            "    intervals.sort(key=lambda x: x[0])\n"
            "    merged = [intervals[0]]\n"
            "    for start, end in intervals[1:]:\n"
            "        if start <= merged[-1][1]:  # overlap\n"
            "            merged[-1][1] = max(merged[-1][1], end)\n"
            "        else:\n"
            "            merged.append([start, end])\n"
            "    return merged\n"
            "\n"
            "# Minimum meeting rooms\n"
            "import heapq\n"
            "def min_rooms(intervals):\n"
            "    intervals.sort()\n"
            "    heap = []  # end times\n"
            "    for start, end in intervals:\n"
            "        if heap and heap[0] <= start:\n"
            "            heapq.heapreplace(heap, end)\n"
            "        else:\n"
            "            heapq.heappush(heap, end)\n"
            "    return len(heap)"
        ),
        "when_to_use": [
            "Merge overlapping intervals",
            "Insert interval into sorted list",
            "Meeting rooms (min rooms needed)",
            "Non-overlapping intervals",
            "Interval intersection / union",
        ],
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
    },
}


# ─────────────────────────────────────────────
# THE FAANG 75 QUESTION BANK
# ─────────────────────────────────────────────

FAANG_QUESTIONS = [
    # ── Two Pointers (5 problems) ──
    {"id": 1,  "title": "Two Sum II - Input Array Is Sorted", "leetcode": 167, "difficulty": "medium", "pattern": "two_pointers",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": True,
     "why": "The pure two-pointer gateway problem. Sorted input = two pointers."},
    {"id": 2,  "title": "3Sum", "leetcode": 15, "difficulty": "medium", "pattern": "two_pointers",
     "companies": ["Meta", "Google", "Amazon", "Apple"], "is_blind75": True,
     "why": "Extends two pointers with a loop. Teaches duplicate handling — an interview favorite."},
    {"id": 3,  "title": "Container With Most Water", "leetcode": 11, "difficulty": "medium", "pattern": "two_pointers",
     "companies": ["Amazon", "Google", "Meta", "Microsoft"], "is_blind75": True,
     "why": "Greedy two-pointer reasoning. You learn WHY moving the shorter line is always safe."},
    {"id": 4,  "title": "Trapping Rain Water", "leetcode": 42, "difficulty": "hard", "pattern": "two_pointers",
     "companies": ["Google", "Amazon", "Meta", "Goldman Sachs"], "is_blind75": True,
     "why": "The boss-level two-pointer problem. If you can solve this, you've mastered the pattern."},
    {"id": 5,  "title": "Valid Palindrome", "leetcode": 125, "difficulty": "easy", "pattern": "two_pointers",
     "companies": ["Meta", "Microsoft", "Amazon"], "is_blind75": True,
     "why": "Warm-up. Opposite-direction pointers filtering non-alphanumeric characters."},

    # ── Sliding Window (5 problems) ──
    {"id": 6,  "title": "Best Time to Buy and Sell Stock", "leetcode": 121, "difficulty": "easy", "pattern": "sliding_window",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "Track min so far, compute max profit. Simplest sliding window concept."},
    {"id": 7,  "title": "Longest Substring Without Repeating Characters", "leetcode": 3, "difficulty": "medium", "pattern": "sliding_window",
     "companies": ["Amazon", "Google", "Meta", "Apple", "Microsoft"], "is_blind75": True,
     "why": "THE classic variable-size sliding window. Shrink from left when you see a repeat."},
    {"id": 8,  "title": "Longest Repeating Character Replacement", "leetcode": 424, "difficulty": "medium", "pattern": "sliding_window",
     "companies": ["Google", "Amazon"], "is_blind75": True,
     "why": "Advanced window: window_size - max_freq <= k. Teaches the 'can I keep this window?' question."},
    {"id": 9,  "title": "Minimum Window Substring", "leetcode": 76, "difficulty": "hard", "pattern": "sliding_window",
     "companies": ["Meta", "Google", "Amazon", "Microsoft"], "is_blind75": True,
     "why": "Hard but massively asked. Expand right, shrink left. The sliding window master problem."},
    {"id": 10, "title": "Permutation in String", "leetcode": 567, "difficulty": "medium", "pattern": "sliding_window",
     "companies": ["Microsoft", "Amazon"], "is_blind75": False,
     "why": "Fixed-size window with frequency matching. Bridges to anagram problems."},

    # ── Hash Map (5 problems) ──
    {"id": 11, "title": "Two Sum", "leetcode": 1, "difficulty": "easy", "pattern": "hash_map",
     "companies": ["Amazon", "Google", "Meta", "Apple", "Microsoft"], "is_blind75": True,
     "why": "The #1 most asked interview question. complement = target - num. Store in map."},
    {"id": 12, "title": "Group Anagrams", "leetcode": 49, "difficulty": "medium", "pattern": "hash_map",
     "companies": ["Amazon", "Meta", "Google"], "is_blind75": True,
     "why": "Sorted string as key. Teaches creative hash key design."},
    {"id": 13, "title": "Top K Frequent Elements", "leetcode": 347, "difficulty": "medium", "pattern": "hash_map",
     "companies": ["Amazon", "Meta", "Google", "Apple"], "is_blind75": True,
     "why": "Count frequencies with map, then bucket sort or heap. Versatile problem."},
    {"id": 14, "title": "Longest Consecutive Sequence", "leetcode": 128, "difficulty": "medium", "pattern": "hash_map",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": True,
     "why": "Set for O(1) lookup. Only start counting from sequence starts. Clever O(n)."},
    {"id": 15, "title": "Valid Anagram", "leetcode": 242, "difficulty": "easy", "pattern": "hash_map",
     "companies": ["Amazon", "Microsoft", "Meta"], "is_blind75": True,
     "why": "Frequency counting 101. Counter comparison or sort."},

    # ── Binary Search (5 problems) ──
    {"id": 16, "title": "Binary Search", "leetcode": 704, "difficulty": "easy", "pattern": "binary_search",
     "companies": ["Amazon", "Microsoft"], "is_blind75": False,
     "why": "The foundation. Get the template in your bones: lo, hi, mid."},
    {"id": 17, "title": "Search in Rotated Sorted Array", "leetcode": 33, "difficulty": "medium", "pattern": "binary_search",
     "companies": ["Meta", "Google", "Amazon", "Microsoft"], "is_blind75": True,
     "why": "Top interview classic. Binary search with a twist — which half is sorted?"},
    {"id": 18, "title": "Find Minimum in Rotated Sorted Array", "leetcode": 153, "difficulty": "medium", "pattern": "binary_search",
     "companies": ["Amazon", "Google", "Meta"], "is_blind75": True,
     "why": "Rotated array variant. Compare mid with right boundary."},
    {"id": 19, "title": "Koko Eating Bananas", "leetcode": 875, "difficulty": "medium", "pattern": "binary_search",
     "companies": ["Google", "Amazon"], "is_blind75": False,
     "why": "The 'search on answer' paradigm. Binary search over the answer space."},
    {"id": 20, "title": "Median of Two Sorted Arrays", "leetcode": 4, "difficulty": "hard", "pattern": "binary_search",
     "companies": ["Google", "Amazon", "Meta", "Apple"], "is_blind75": True,
     "why": "Hard but legendary. Binary search on partition. Ultimate BS mastery."},

    # ── Stack (5 problems) ──
    {"id": 21, "title": "Valid Parentheses", "leetcode": 20, "difficulty": "easy", "pattern": "stack",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "Stack 101. Push open, pop for close, check match."},
    {"id": 22, "title": "Min Stack", "leetcode": 155, "difficulty": "medium", "pattern": "stack",
     "companies": ["Amazon", "Microsoft", "Google"], "is_blind75": True,
     "why": "Design problem. Track minimum alongside main stack."},
    {"id": 23, "title": "Daily Temperatures", "leetcode": 739, "difficulty": "medium", "pattern": "stack",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": False,
     "why": "Monotonic stack in action. 'Next warmer day' = next greater element."},
    {"id": 24, "title": "Largest Rectangle in Histogram", "leetcode": 84, "difficulty": "hard", "pattern": "stack",
     "companies": ["Google", "Amazon", "Microsoft"], "is_blind75": True,
     "why": "The hardest stack problem. Monotonic stack to find left/right boundaries."},
    {"id": 25, "title": "Evaluate Reverse Polish Notation", "leetcode": 150, "difficulty": "medium", "pattern": "stack",
     "companies": ["Amazon", "Microsoft"], "is_blind75": True,
     "why": "Classic stack application. Process operators by popping operands."},

    # ── Linked List (5 problems) ──
    {"id": 26, "title": "Reverse Linked List", "leetcode": 206, "difficulty": "easy", "pattern": "linked_list",
     "companies": ["Amazon", "Microsoft", "Google", "Meta"], "is_blind75": True,
     "why": "The fundamental linked list operation. prev/curr/next dance."},
    {"id": 27, "title": "Merge Two Sorted Lists", "leetcode": 21, "difficulty": "easy", "pattern": "linked_list",
     "companies": ["Amazon", "Microsoft", "Meta"], "is_blind75": True,
     "why": "Dummy node technique. Foundation for merge sort on lists."},
    {"id": 28, "title": "Linked List Cycle", "leetcode": 141, "difficulty": "easy", "pattern": "linked_list",
     "companies": ["Amazon", "Microsoft", "Google"], "is_blind75": True,
     "why": "Floyd's tortoise and hare. Fast/slow pointers."},
    {"id": 29, "title": "Remove Nth Node From End of List", "leetcode": 19, "difficulty": "medium", "pattern": "linked_list",
     "companies": ["Meta", "Amazon", "Google"], "is_blind75": True,
     "why": "Two pointers with gap. Advance fast N steps first."},
    {"id": 30, "title": "LRU Cache", "leetcode": 146, "difficulty": "medium", "pattern": "linked_list",
     "companies": ["Amazon", "Meta", "Google", "Microsoft", "Apple"], "is_blind75": True,
     "why": "Top design question. Hash map + doubly linked list."},

    # ── Trees (7 problems) ──
    {"id": 31, "title": "Invert Binary Tree", "leetcode": 226, "difficulty": "easy", "pattern": "tree_traversal",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": True,
     "why": "Simple recursion. Swap left and right children. Builds DFS intuition."},
    {"id": 32, "title": "Maximum Depth of Binary Tree", "leetcode": 104, "difficulty": "easy", "pattern": "tree_traversal",
     "companies": ["Amazon", "Microsoft", "Google"], "is_blind75": True,
     "why": "1 + max(left, right). The quintessential tree recursion."},
    {"id": 33, "title": "Same Tree", "leetcode": 100, "difficulty": "easy", "pattern": "tree_traversal",
     "companies": ["Amazon", "Microsoft"], "is_blind75": True,
     "why": "Simultaneous recursive traversal of two trees."},
    {"id": 34, "title": "Binary Tree Level Order Traversal", "leetcode": 102, "difficulty": "medium", "pattern": "tree_traversal",
     "companies": ["Meta", "Amazon", "Google", "Microsoft"], "is_blind75": True,
     "why": "BFS on a tree with queue. Process level by level."},
    {"id": 35, "title": "Validate Binary Search Tree", "leetcode": 98, "difficulty": "medium", "pattern": "tree_traversal",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "Pass valid range (min, max) down. Tests understanding of BST property."},
    {"id": 36, "title": "Lowest Common Ancestor of BST", "leetcode": 235, "difficulty": "medium", "pattern": "tree_traversal",
     "companies": ["Meta", "Amazon", "Microsoft"], "is_blind75": True,
     "why": "If p and q are on different sides, current node is LCA. Elegant."},
    {"id": 37, "title": "Binary Tree Maximum Path Sum", "leetcode": 124, "difficulty": "hard", "pattern": "tree_traversal",
     "companies": ["Meta", "Google", "Amazon"], "is_blind75": True,
     "why": "Hard DFS. At each node: max path through it vs best so far. Global variable trick."},

    # ── Heap (3 problems) ──
    {"id": 38, "title": "Kth Largest Element in an Array", "leetcode": 215, "difficulty": "medium", "pattern": "heap",
     "companies": ["Meta", "Amazon", "Google", "Microsoft"], "is_blind75": True,
     "why": "Min-heap of size K. Or quickselect. Both are critical to know."},
    {"id": 39, "title": "Merge K Sorted Lists", "leetcode": 23, "difficulty": "hard", "pattern": "heap",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "Heap to always get the smallest head. Merges K lists in O(n log k)."},
    {"id": 40, "title": "Find Median from Data Stream", "leetcode": 295, "difficulty": "hard", "pattern": "heap",
     "companies": ["Amazon", "Google", "Meta", "Microsoft"], "is_blind75": True,
     "why": "Two heaps: max-heap for lower half, min-heap for upper half. Brilliant design."},

    # ── Graph BFS/DFS (7 problems) ──
    {"id": 41, "title": "Number of Islands", "leetcode": 200, "difficulty": "medium", "pattern": "graph_bfs_dfs",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "THE gateway graph problem. DFS to sink islands. Count components."},
    {"id": 42, "title": "Clone Graph", "leetcode": 133, "difficulty": "medium", "pattern": "graph_bfs_dfs",
     "companies": ["Meta", "Google", "Amazon"], "is_blind75": True,
     "why": "DFS + hash map to track cloned nodes. Deep copy pattern."},
    {"id": 43, "title": "Pacific Atlantic Water Flow", "leetcode": 417, "difficulty": "medium", "pattern": "graph_bfs_dfs",
     "companies": ["Google", "Amazon"], "is_blind75": True,
     "why": "Reverse thinking: BFS from ocean inward. Intersection of two reachability sets."},
    {"id": 44, "title": "Course Schedule", "leetcode": 207, "difficulty": "medium", "pattern": "graph_bfs_dfs",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "Cycle detection in directed graph. Topological sort. Massively asked."},
    {"id": 45, "title": "Rotting Oranges", "leetcode": 994, "difficulty": "medium", "pattern": "graph_bfs_dfs",
     "companies": ["Amazon", "Google", "Meta"], "is_blind75": False,
     "why": "Multi-source BFS. All rotten oranges start simultaneously."},
    {"id": 46, "title": "Word Ladder", "leetcode": 127, "difficulty": "hard", "pattern": "graph_bfs_dfs",
     "companies": ["Amazon", "Google", "Meta"], "is_blind75": True,
     "why": "BFS for shortest transformation. Words as nodes, edges = 1 char diff."},
    {"id": 47, "title": "Graph Valid Tree", "leetcode": 261, "difficulty": "medium", "pattern": "graph_bfs_dfs",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": True,
     "why": "Tree = connected + no cycle + n-1 edges. Union-Find or DFS."},

    # ── Backtracking (5 problems) ──
    {"id": 48, "title": "Subsets", "leetcode": 78, "difficulty": "medium", "pattern": "backtracking",
     "companies": ["Meta", "Amazon", "Google"], "is_blind75": True,
     "why": "Backtracking 101. Include or exclude each element."},
    {"id": 49, "title": "Combination Sum", "leetcode": 39, "difficulty": "medium", "pattern": "backtracking",
     "companies": ["Amazon", "Meta", "Google"], "is_blind75": True,
     "why": "Choose-Explore-Unchoose with repetition allowed."},
    {"id": 50, "title": "Permutations", "leetcode": 46, "difficulty": "medium", "pattern": "backtracking",
     "companies": ["Meta", "Google", "Amazon", "Microsoft"], "is_blind75": True,
     "why": "Generate all orderings. Swap-based or used-set approach."},
    {"id": 51, "title": "Word Search", "leetcode": 79, "difficulty": "medium", "pattern": "backtracking",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "Grid backtracking. Mark visited, explore 4 directions, unmark."},
    {"id": 52, "title": "N-Queens", "leetcode": 51, "difficulty": "hard", "pattern": "backtracking",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": False,
     "why": "The ultimate backtracking challenge. Constraint pruning at its finest."},

    # ── Trie (3 problems) ──
    {"id": 53, "title": "Implement Trie (Prefix Tree)", "leetcode": 208, "difficulty": "medium", "pattern": "trie",
     "companies": ["Google", "Amazon", "Microsoft"], "is_blind75": True,
     "why": "Build the data structure from scratch. Insert, search, startsWith."},
    {"id": 54, "title": "Design Add and Search Words", "leetcode": 211, "difficulty": "medium", "pattern": "trie",
     "companies": ["Meta", "Google", "Amazon"], "is_blind75": True,
     "why": "Trie + DFS for wildcard '.' matching. Combines two patterns."},
    {"id": 55, "title": "Word Search II", "leetcode": 212, "difficulty": "hard", "pattern": "trie",
     "companies": ["Amazon", "Google", "Meta"], "is_blind75": True,
     "why": "Trie + backtracking on grid. The ultimate trie problem."},

    # ── DP 1D (8 problems) ──
    {"id": 56, "title": "Climbing Stairs", "leetcode": 70, "difficulty": "easy", "pattern": "dp_1d",
     "companies": ["Amazon", "Google", "Microsoft"], "is_blind75": True,
     "why": "dp[i] = dp[i-1] + dp[i-2]. The 'Hello World' of DP."},
    {"id": 57, "title": "House Robber", "leetcode": 198, "difficulty": "medium", "pattern": "dp_1d",
     "companies": ["Amazon", "Google", "Microsoft"], "is_blind75": True,
     "why": "dp[i] = max(dp[i-1], dp[i-2] + nums[i]). Classic 'take or skip'."},
    {"id": 58, "title": "Coin Change", "leetcode": 322, "difficulty": "medium", "pattern": "dp_1d",
     "companies": ["Amazon", "Google", "Meta", "Microsoft"], "is_blind75": True,
     "why": "BFS or DP. dp[amount] = min coins needed. Tests DP foundations."},
    {"id": 59, "title": "Longest Increasing Subsequence", "leetcode": 300, "difficulty": "medium", "pattern": "dp_1d",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": True,
     "why": "O(n^2) DP or O(n log n) with binary search. Multi-technique problem."},
    {"id": 60, "title": "Word Break", "leetcode": 139, "difficulty": "medium", "pattern": "dp_1d",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "dp[i] = can we segment s[:i]? Check all previous valid positions."},
    {"id": 61, "title": "Maximum Subarray", "leetcode": 53, "difficulty": "medium", "pattern": "dp_1d",
     "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple"], "is_blind75": True,
     "why": "Kadane's algorithm. dp[i] = max(nums[i], dp[i-1] + nums[i])."},
    {"id": 62, "title": "Decode Ways", "leetcode": 91, "difficulty": "medium", "pattern": "dp_1d",
     "companies": ["Google", "Meta", "Amazon"], "is_blind75": True,
     "why": "Like climbing stairs but with constraints. Tests careful edge handling."},
    {"id": 63, "title": "Maximum Product Subarray", "leetcode": 152, "difficulty": "medium", "pattern": "dp_1d",
     "companies": ["Amazon", "Google", "Meta"], "is_blind75": True,
     "why": "Track both max and min (negatives can flip). Elegant twist on Kadane's."},

    # ── DP 2D (5 problems) ──
    {"id": 64, "title": "Unique Paths", "leetcode": 62, "difficulty": "medium", "pattern": "dp_2d",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": True,
     "why": "dp[i][j] = dp[i-1][j] + dp[i][j-1]. Grid DP fundamentals."},
    {"id": 65, "title": "Longest Common Subsequence", "leetcode": 1143, "difficulty": "medium", "pattern": "dp_2d",
     "companies": ["Google", "Amazon"], "is_blind75": True,
     "why": "Two-string DP classic. Match → diagonal + 1, else max(left, up)."},
    {"id": 66, "title": "Edit Distance", "leetcode": 72, "difficulty": "medium", "pattern": "dp_2d",
     "companies": ["Google", "Amazon", "Meta"], "is_blind75": False,
     "why": "Insert, delete, replace operations. The 'textbook' 2D DP problem."},
    {"id": 67, "title": "Coin Change 2", "leetcode": 518, "difficulty": "medium", "pattern": "dp_2d",
     "companies": ["Amazon", "Google"], "is_blind75": False,
     "why": "Unbounded knapsack. Count combinations (not permutations)."},
    {"id": 68, "title": "Target Sum", "leetcode": 494, "difficulty": "medium", "pattern": "dp_2d",
     "companies": ["Meta", "Google", "Amazon"], "is_blind75": False,
     "why": "Subset sum variant. 0/1 knapsack with +/- choices."},

    # ── Greedy (4 problems) ──
    {"id": 69, "title": "Jump Game", "leetcode": 55, "difficulty": "medium", "pattern": "greedy",
     "companies": ["Amazon", "Google", "Meta"], "is_blind75": True,
     "why": "Track max reachable index. Pure greedy."},
    {"id": 70, "title": "Jump Game II", "leetcode": 45, "difficulty": "medium", "pattern": "greedy",
     "companies": ["Amazon", "Google"], "is_blind75": False,
     "why": "Min jumps to reach end. BFS / greedy with current range."},
    {"id": 71, "title": "Gas Station", "leetcode": 134, "difficulty": "medium", "pattern": "greedy",
     "companies": ["Amazon", "Google", "Microsoft"], "is_blind75": False,
     "why": "Circular tour. If total gas >= total cost, solution exists. Find start."},
    {"id": 72, "title": "Hand of Straights", "leetcode": 846, "difficulty": "medium", "pattern": "greedy",
     "companies": ["Google", "Amazon"], "is_blind75": False,
     "why": "Sort + greedy grouping. Practical greedy reasoning."},

    # ── Intervals (3 problems) ──
    {"id": 73, "title": "Merge Intervals", "leetcode": 56, "difficulty": "medium", "pattern": "intervals",
     "companies": ["Amazon", "Meta", "Google", "Microsoft"], "is_blind75": True,
     "why": "THE interval problem. Sort by start, merge overlapping."},
    {"id": 74, "title": "Non-overlapping Intervals", "leetcode": 435, "difficulty": "medium", "pattern": "intervals",
     "companies": ["Amazon", "Google", "Meta"], "is_blind75": True,
     "why": "Min removals for no overlap = n - max non-overlapping. Greedy by end time."},
    {"id": 75, "title": "Meeting Rooms II", "leetcode": 253, "difficulty": "medium", "pattern": "intervals",
     "companies": ["Amazon", "Meta", "Google", "Microsoft", "Apple"], "is_blind75": True,
     "why": "Min rooms needed. Sweep line or min-heap approach."},
]


# ─────────────────────────────────────────────
# PHASES WITH MOTIVATION
# ─────────────────────────────────────────────

FAANG_PHASES = {
    1: {
        "name": "Foundation Patterns",
        "tagline": "Build Your Weapons",
        "description": "These 4 patterns are your bread and butter. They appear in 40%+ of all interview questions. Master them and you already have a huge advantage.",
        "motivation_start": "Every FAANG engineer started exactly where you are right now. These patterns will become second nature — let's go!",
        "motivation_complete": "You've built the foundation. These 4 patterns alone can solve hundreds of LeetCode problems. You're already ahead of 60% of candidates!",
        "estimated_days": 5,
        "patterns": ["two_pointers", "sliding_window", "hash_map", "binary_search"],
    },
    2: {
        "name": "Core Data Structures",
        "tagline": "Know Your Tools",
        "description": "Stacks, linked lists, trees, and heaps — the building blocks interviewers love to test. These problems test your ability to choose and implement the right data structure.",
        "motivation_start": "Phase 1 gave you patterns; Phase 2 gives you mastery of the data structures underneath. This is where things click.",
        "motivation_complete": "You now command the core data structures that power tech. Trees alone cover 20% of interview questions. Incredible progress!",
        "estimated_days": 6,
        "patterns": ["stack", "linked_list", "tree_traversal", "heap"],
    },
    3: {
        "name": "Graph & Search",
        "tagline": "Navigate Any Maze",
        "description": "Graphs are everywhere in disguise: grids, social networks, dependencies. Backtracking generates all possibilities. Tries power search. This phase teaches you to explore.",
        "motivation_start": "If Phase 1 was learning to walk and Phase 2 was learning to run, Phase 3 is learning to fly. Graphs open up a whole new dimension.",
        "motivation_complete": "Graph problems no longer scare you. You can see the graph hidden inside any problem. You're in the top 20% of candidates now!",
        "estimated_days": 5,
        "patterns": ["graph_bfs_dfs", "backtracking", "trie"],
    },
    4: {
        "name": "Advanced Patterns",
        "tagline": "The Final Boss",
        "description": "Dynamic Programming, Greedy, and Intervals — the patterns that separate good candidates from great ones. DP is the most feared topic, but we'll make it intuitive with stories and templates.",
        "motivation_start": "This is the final stretch. DP is the Mount Everest of interviews — and you're about to summit it. Every problem you solve here is a massive confidence boost.",
        "motivation_complete": "YOU DID IT. You've conquered all 15 patterns and 75 problems. You are interview-ready for any FAANG company. Go crush it!",
        "estimated_days": 7,
        "patterns": ["dp_1d", "dp_2d", "greedy", "intervals"],
    },
}


# ─────────────────────────────────────────────
# MILESTONES & ACHIEVEMENTS
# ─────────────────────────────────────────────

MILESTONES = [
    {"id": "first_blood",     "name": "First Blood",          "description": "Solve your first FAANG 75 problem",            "threshold": 1,  "emoji": "🩸"},
    {"id": "getting_started", "name": "Getting Started",      "description": "Solve 5 problems",                             "threshold": 5,  "emoji": "🚀"},
    {"id": "double_digits",   "name": "Double Digits",        "description": "Solve 10 problems",                            "threshold": 10, "emoji": "🔟"},
    {"id": "quarter_way",     "name": "Quarter Way",          "description": "Solve 19 problems — 25% complete!",            "threshold": 19, "emoji": "🏁"},
    {"id": "halfway_hero",    "name": "Halfway Hero",         "description": "Solve 38 problems — 50% complete!",            "threshold": 38, "emoji": "⚡"},
    {"id": "three_quarters",  "name": "Almost There",         "description": "Solve 56 problems — 75% complete!",            "threshold": 56, "emoji": "🔥"},
    {"id": "home_stretch",    "name": "Home Stretch",         "description": "Solve 65 problems — the finish line is near!", "threshold": 65, "emoji": "🏃"},
    {"id": "faang_ready",     "name": "FAANG Ready",          "description": "Solve all 75 problems. You're ready.",         "threshold": 75, "emoji": "👑"},
    {"id": "phase_1_done",    "name": "Foundation Master",    "description": "Complete all Phase 1 problems",                "threshold": -1, "emoji": "🧱"},
    {"id": "phase_2_done",    "name": "Structure Master",     "description": "Complete all Phase 2 problems",                "threshold": -2, "emoji": "🏗️"},
    {"id": "phase_3_done",    "name": "Graph Navigator",      "description": "Complete all Phase 3 problems",                "threshold": -3, "emoji": "🗺️"},
    {"id": "phase_4_done",    "name": "DP Conqueror",         "description": "Complete all Phase 4 problems",                "threshold": -4, "emoji": "🏆"},
    {"id": "pattern_master",  "name": "Pattern Master",       "description": "Solve 3+ problems in a single pattern",       "threshold": -5, "emoji": "🎯"},
    {"id": "streak_3",        "name": "On Fire",              "description": "3-day solving streak",                         "threshold": -6, "emoji": "🔥"},
    {"id": "streak_7",        "name": "Unstoppable",          "description": "7-day solving streak",                         "threshold": -7, "emoji": "💪"},
]


# ─────────────────────────────────────────────
# MOTIVATIONAL QUOTES
# ─────────────────────────────────────────────

MOTIVATION_QUOTES = [
    {"quote": "The best time to start was yesterday. The second best time is now.", "context": "starting"},
    {"quote": "You don't have to be great to start, but you have to start to be great.", "context": "starting"},
    {"quote": "Every expert was once a beginner.", "context": "struggling"},
    {"quote": "The pain you feel today is the strength you feel tomorrow.", "context": "struggling"},
    {"quote": "It's not about being the smartest — it's about being the most prepared.", "context": "struggling"},
    {"quote": "Consistency beats intensity. 1 problem a day > 10 problems once a week.", "context": "consistency"},
    {"quote": "You're not competing with others. You're competing with the version of you that didn't start.", "context": "comparison"},
    {"quote": "The difference between a junior and senior engineer is the number of patterns they've internalized.", "context": "patterns"},
    {"quote": "Think of each problem as a rep at the gym. Every rep makes you stronger.", "context": "practice"},
    {"quote": "FAANG engineers aren't geniuses — they're people who practiced the right problems.", "context": "faang"},
    {"quote": "You're closer than you think. Keep going.", "context": "progress"},
    {"quote": "The interviewer isn't looking for perfection. They're looking for clear thinking.", "context": "interview"},
    {"quote": "Stuck on a problem? That feeling IS the learning happening.", "context": "stuck"},
    {"quote": "Pattern recognition is a skill. Every problem you solve adds to your pattern library.", "context": "patterns"},
    {"quote": "You've already done the hardest part — you showed up and started.", "context": "progress"},
]


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_questions_by_pattern(pattern_key: str) -> list:
    """Get all questions for a specific pattern."""
    return [q for q in FAANG_QUESTIONS if q["pattern"] == pattern_key]


def get_questions_by_phase(phase: int) -> list:
    """Get all questions in a phase."""
    phase_patterns = FAANG_PHASES[phase]["patterns"]
    return [q for q in FAANG_QUESTIONS if q["pattern"] in phase_patterns]


def get_question_by_id(question_id: int) -> dict:
    """Get a specific question by ID."""
    for q in FAANG_QUESTIONS:
        if q["id"] == question_id:
            return q
    return None


def get_pattern_info(pattern_key: str) -> dict:
    """Get full pattern information."""
    return FAANG_PATTERNS.get(pattern_key)


def get_readiness_score(solved_ids: list) -> dict:
    """Calculate interview readiness score based on solved problems."""
    total = len(FAANG_QUESTIONS)
    solved = len(solved_ids)
    percentage = round((solved / total) * 100) if total > 0 else 0

    # Pattern coverage
    pattern_coverage = {}
    for pattern_key in FAANG_PATTERNS:
        pattern_qs = get_questions_by_pattern(pattern_key)
        pattern_solved = [q for q in pattern_qs if q["id"] in solved_ids]
        pattern_coverage[pattern_key] = {
            "total": len(pattern_qs),
            "solved": len(pattern_solved),
            "percentage": round((len(pattern_solved) / len(pattern_qs)) * 100) if pattern_qs else 0,
        }

    # Phase completion
    phase_completion = {}
    for phase_num, phase_info in FAANG_PHASES.items():
        phase_qs = get_questions_by_phase(phase_num)
        phase_solved = [q for q in phase_qs if q["id"] in solved_ids]
        phase_completion[phase_num] = {
            "total": len(phase_qs),
            "solved": len(phase_solved),
            "percentage": round((len(phase_solved) / len(phase_qs)) * 100) if phase_qs else 0,
            "complete": len(phase_solved) == len(phase_qs),
        }

    # Readiness level
    if percentage >= 95:
        level = "FAANG Ready"
        emoji = "👑"
    elif percentage >= 75:
        level = "Strong Candidate"
        emoji = "💪"
    elif percentage >= 50:
        level = "Getting There"
        emoji = "📈"
    elif percentage >= 25:
        level = "Building Foundation"
        emoji = "🧱"
    else:
        level = "Just Starting"
        emoji = "🌱"

    # Earned milestones
    earned = []
    for m in MILESTONES:
        if m["threshold"] > 0 and solved >= m["threshold"]:
            earned.append(m)
        elif m["threshold"] == -1 and phase_completion.get(1, {}).get("complete"):
            earned.append(m)
        elif m["threshold"] == -2 and phase_completion.get(2, {}).get("complete"):
            earned.append(m)
        elif m["threshold"] == -3 and phase_completion.get(3, {}).get("complete"):
            earned.append(m)
        elif m["threshold"] == -4 and phase_completion.get(4, {}).get("complete"):
            earned.append(m)

    return {
        "total_problems": total,
        "solved": solved,
        "percentage": percentage,
        "readiness_level": level,
        "readiness_emoji": emoji,
        "pattern_coverage": pattern_coverage,
        "phase_completion": phase_completion,
        "milestones_earned": earned,
        "milestones_total": len(MILESTONES),
    }
