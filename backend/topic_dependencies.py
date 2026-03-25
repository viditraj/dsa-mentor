"""Topic Dependency Graph for the Skill Tree visualization.

Each topic has explicit prerequisites showing WHY you learn things in order.
This powers both the visual skill tree and the bridge lesson generation.
"""

# Maps topic name → list of prerequisite topic names
# This is the "edges" of the skill tree graph
TOPIC_DEPENDENCIES = {
    # ── Foundations (no prereqs) ──
    "Big-O Notation & Complexity Analysis": [],

    # ── Arrays & Strings ──
    "Arrays - Basics & Traversal": ["Big-O Notation & Complexity Analysis"],
    "Two Pointers Technique": ["Arrays - Basics & Traversal"],
    "Sliding Window": ["Arrays - Basics & Traversal", "Two Pointers Technique"],
    "String Manipulation": ["Arrays - Basics & Traversal"],

    # ── Hashing ──
    "Hash Maps & Hash Sets": ["Arrays - Basics & Traversal"],

    # ── Linked Lists ──
    "Singly Linked Lists": ["Big-O Notation & Complexity Analysis"],
    "Advanced Linked Lists": ["Singly Linked Lists", "Two Pointers Technique"],

    # ── Stacks & Queues ──
    "Stacks": ["Arrays - Basics & Traversal", "Singly Linked Lists"],
    "Queues & Deques": ["Arrays - Basics & Traversal", "Singly Linked Lists"],

    # ── Trees ──
    "Binary Trees - Traversals": ["Stacks", "Queues & Deques"],
    "Binary Search Trees": ["Binary Trees - Traversals", "Binary Search Patterns"],
    "Advanced Tree Problems": ["Binary Search Trees", "Recursion Fundamentals"],

    # ── Heaps ──
    "Heaps & Priority Queues": ["Binary Trees - Traversals", "Arrays - Basics & Traversal"],

    # ── Graphs ──
    "Graph Representations & BFS/DFS": ["Queues & Deques", "Stacks", "Hash Maps & Hash Sets"],
    "Topological Sort & Advanced Graphs": ["Graph Representations & BFS/DFS"],
    "Shortest Path Algorithms": ["Graph Representations & BFS/DFS", "Heaps & Priority Queues"],

    # ── Binary Search ──
    "Binary Search Patterns": ["Arrays - Basics & Traversal"],

    # ── Recursion & Backtracking ──
    "Recursion Fundamentals": ["Stacks", "Big-O Notation & Complexity Analysis"],
    "Backtracking": ["Recursion Fundamentals"],

    # ── Dynamic Programming ──
    "1D Dynamic Programming": ["Recursion Fundamentals", "Arrays - Basics & Traversal"],
    "2D Dynamic Programming": ["1D Dynamic Programming"],

    # ── Greedy ──
    "Greedy Algorithms": ["Arrays - Basics & Traversal", "Binary Search Patterns"],

    # ── Advanced ──
    "Bit Manipulation": ["Arrays - Basics & Traversal"],
    "Math & Geometry": ["Arrays - Basics & Traversal"],
    "Intervals & Sweep Line": ["Arrays - Basics & Traversal", "Greedy Algorithms"],

    # ── Design ──
    "Design Data Structures": ["Hash Maps & Hash Sets", "Advanced Linked Lists", "Heaps & Priority Queues"],
}

# Connection explanations: why does topic B require topic A?
# Used by bridge lesson AI to explain connections
DEPENDENCY_EXPLANATIONS = {
    ("Big-O Notation & Complexity Analysis", "Arrays - Basics & Traversal"):
        "You need Big-O to analyze WHY array operations have different costs — O(1) access vs O(n) search.",

    ("Arrays - Basics & Traversal", "Two Pointers Technique"):
        "Two pointers is a pattern that works ON arrays. You must understand array indexing and traversal first.",

    ("Arrays - Basics & Traversal", "Sliding Window"):
        "Sliding window maintains a subarray — you need array basics to understand how windows move across elements.",

    ("Two Pointers Technique", "Sliding Window"):
        "Sliding window IS a form of two pointers! The left and right boundaries of the window are two pointers moving in the same direction.",

    ("Arrays - Basics & Traversal", "Hash Maps & Hash Sets"):
        "Hash maps solve many array problems more efficiently (Two Sum: O(n²)→O(n)). Understanding array patterns shows you why hashing is powerful.",

    ("Singly Linked Lists", "Advanced Linked Lists"):
        "Advanced patterns like LRU Cache combine linked lists with hash maps. You must master basic node operations first.",

    ("Two Pointers Technique", "Advanced Linked Lists"):
        "Floyd's cycle detection and the runner technique ARE two-pointer patterns applied to linked lists.",

    ("Arrays - Basics & Traversal", "Stacks"):
        "Stacks are often implemented using arrays. Understanding push/pop is like array append/pop.",

    ("Singly Linked Lists", "Stacks"):
        "Stacks can also be implemented as linked lists. Node-based thinking helps with stack internals.",

    ("Stacks", "Binary Trees - Traversals"):
        "Iterative tree traversals USE a stack. DFS on trees is essentially stack-based exploration.",

    ("Queues & Deques", "Binary Trees - Traversals"):
        "Level-order (BFS) traversal uses a queue. Understanding FIFO is essential for BFS on trees.",

    ("Binary Trees - Traversals", "Binary Search Trees"):
        "BSTs are binary trees with the sorted property. You need traversal skills to validate and search BSTs.",

    ("Binary Search Patterns", "Binary Search Trees"):
        "BST search IS binary search on a tree structure. The same halving principle applies.",

    ("Binary Search Trees", "Advanced Tree Problems"):
        "Advanced problems combine BST properties with recursion (path sums, diameter, serialization).",

    ("Binary Trees - Traversals", "Heaps & Priority Queues"):
        "Heaps ARE complete binary trees stored in arrays. Tree intuition helps understand heap operations.",

    ("Queues & Deques", "Graph Representations & BFS/DFS"):
        "BFS on graphs uses queues — exactly like level-order on trees, but with visited set.",

    ("Stacks", "Graph Representations & BFS/DFS"):
        "DFS on graphs uses stacks (or recursion). Same principle as tree DFS but with cycle handling.",

    ("Hash Maps & Hash Sets", "Graph Representations & BFS/DFS"):
        "Adjacency lists use hash maps. Visited sets use hash sets. Graphs rely heavily on hashing.",

    ("Graph Representations & BFS/DFS", "Topological Sort & Advanced Graphs"):
        "Topological sort IS a modified DFS/BFS on directed graphs. You need graph traversal mastery.",

    ("Graph Representations & BFS/DFS", "Shortest Path Algorithms"):
        "Dijkstra's is BFS with a priority queue. Understanding BFS is the foundation for shortest paths.",

    ("Heaps & Priority Queues", "Shortest Path Algorithms"):
        "Dijkstra's algorithm uses a min-heap to always process the nearest unvisited node.",

    ("Stacks", "Recursion Fundamentals"):
        "Recursion uses the call STACK. Understanding stack frames helps you trace and debug recursive code.",

    ("Recursion Fundamentals", "Backtracking"):
        "Backtracking IS recursion with a choice→explore→unchoose pattern. Master recursion first.",

    ("Recursion Fundamentals", "1D Dynamic Programming"):
        "DP starts as recursion + memoization. You convert recursive solutions to DP tables.",

    ("1D Dynamic Programming", "2D Dynamic Programming"):
        "2D DP extends the same principles to two dimensions (grids, two sequences).",

    ("Arrays - Basics & Traversal", "Greedy Algorithms"):
        "Many greedy problems operate on arrays (intervals, jump games). Array manipulation is essential.",

    ("Binary Search Patterns", "Greedy Algorithms"):
        "Some greedy problems use binary search to find optimal thresholds (search on answer).",

    ("Hash Maps & Hash Sets", "Design Data Structures"):
        "LRU Cache = HashMap + Doubly Linked List. Design problems combine data structures.",

    ("Advanced Linked Lists", "Design Data Structures"):
        "LRU/LFU caches use doubly linked lists for O(1) removal. You need linked list mastery.",

    ("Heaps & Priority Queues", "Design Data Structures"):
        "Design Twitter uses heaps for merge-k-sorted-feeds. Many designs need priority queues.",

    ("Greedy Algorithms", "Intervals & Sweep Line"):
        "Interval problems use greedy sorting strategies. The greedy choice drives interval decisions.",
}

# Visual layout hints for skill tree rendering
# x, y positions (normalized 0-100) for each topic node
SKILL_TREE_LAYOUT = {
    "Big-O Notation & Complexity Analysis":     {"x": 50, "y": 5,  "tier": 0},
    "Arrays - Basics & Traversal":              {"x": 35, "y": 15, "tier": 1},
    "Singly Linked Lists":                      {"x": 65, "y": 15, "tier": 1},
    "Two Pointers Technique":                   {"x": 20, "y": 25, "tier": 2},
    "String Manipulation":                      {"x": 40, "y": 25, "tier": 2},
    "Hash Maps & Hash Sets":                    {"x": 55, "y": 25, "tier": 2},
    "Binary Search Patterns":                   {"x": 10, "y": 35, "tier": 2},
    "Sliding Window":                           {"x": 25, "y": 35, "tier": 3},
    "Advanced Linked Lists":                    {"x": 70, "y": 30, "tier": 3},
    "Stacks":                                   {"x": 40, "y": 40, "tier": 3},
    "Queues & Deques":                          {"x": 55, "y": 40, "tier": 3},
    "Recursion Fundamentals":                   {"x": 30, "y": 48, "tier": 4},
    "Binary Trees - Traversals":                {"x": 48, "y": 50, "tier": 4},
    "Heaps & Priority Queues":                  {"x": 65, "y": 50, "tier": 4},
    "Bit Manipulation":                         {"x": 10, "y": 50, "tier": 4},
    "Math & Geometry":                          {"x": 85, "y": 50, "tier": 4},
    "Binary Search Trees":                      {"x": 45, "y": 60, "tier": 5},
    "Graph Representations & BFS/DFS":          {"x": 60, "y": 60, "tier": 5},
    "Backtracking":                             {"x": 25, "y": 60, "tier": 5},
    "1D Dynamic Programming":                   {"x": 15, "y": 65, "tier": 5},
    "Greedy Algorithms":                        {"x": 80, "y": 60, "tier": 5},
    "Advanced Tree Problems":                   {"x": 40, "y": 70, "tier": 6},
    "Topological Sort & Advanced Graphs":       {"x": 55, "y": 72, "tier": 6},
    "Shortest Path Algorithms":                 {"x": 70, "y": 72, "tier": 6},
    "2D Dynamic Programming":                   {"x": 15, "y": 75, "tier": 6},
    "Intervals & Sweep Line":                   {"x": 85, "y": 72, "tier": 6},
    "Design Data Structures":                   {"x": 50, "y": 85, "tier": 7},
}

# Category colors for the skill tree
CATEGORY_COLORS = {
    "foundations": "#6366f1",        # indigo
    "arrays_strings": "#3b82f6",    # blue
    "hashing": "#8b5cf6",           # violet
    "linked_lists": "#ec4899",      # pink
    "stacks_queues": "#f59e0b",     # amber
    "trees": "#10b981",             # emerald
    "heaps": "#14b8a6",             # teal
    "graphs": "#ef4444",            # red
    "binary_search": "#06b6d4",     # cyan
    "recursion_backtracking": "#f97316",  # orange
    "dynamic_programming": "#a855f7",     # purple
    "greedy": "#84cc16",            # lime
    "advanced": "#64748b",          # slate
    "system_design_patterns": "#e11d48",  # rose
}
