"""DSA Knowledge Base - Comprehensive curriculum data for roadmap generation."""

DSA_CURRICULUM = {
    "foundations": {
        "order": 1,
        "topics": [
            {
                "name": "Big-O Notation & Complexity Analysis",
                "category": "foundations",
                "difficulty": "easy",
                "estimated_days": 2,
                "key_concepts": ["Time complexity", "Space complexity", "Best/Worst/Average case", "Amortized analysis"],
                "common_patterns": ["Analyzing loops", "Recursive complexity", "Space-time tradeoffs"],
                "problems": [
                    {"title": "Running Sum of 1d Array", "leetcode_number": 1480, "difficulty": "easy"},
                ]
            },
        ]
    },
    "arrays_strings": {
        "order": 2,
        "topics": [
            {
                "name": "Arrays - Basics & Traversal",
                "category": "arrays_strings",
                "difficulty": "easy",
                "estimated_days": 3,
                "key_concepts": ["Array indexing", "Traversal patterns", "In-place operations", "Prefix sums"],
                "common_patterns": ["Linear scan", "Prefix sum", "Kadane's algorithm"],
                "problems": [
                    {"title": "Two Sum", "leetcode_number": 1, "difficulty": "easy"},
                    {"title": "Best Time to Buy and Sell Stock", "leetcode_number": 121, "difficulty": "easy"},
                    {"title": "Maximum Subarray", "leetcode_number": 53, "difficulty": "medium"},
                    {"title": "Product of Array Except Self", "leetcode_number": 238, "difficulty": "medium"},
                    {"title": "Contains Duplicate", "leetcode_number": 217, "difficulty": "easy"},
                ]
            },
            {
                "name": "Two Pointers Technique",
                "category": "arrays_strings",
                "difficulty": "easy",
                "estimated_days": 3,
                "key_concepts": ["Left-right pointers", "Fast-slow pointers", "Sorted array patterns"],
                "common_patterns": ["Two pointers converging", "Two pointers same direction", "Three pointers"],
                "problems": [
                    {"title": "Valid Palindrome", "leetcode_number": 125, "difficulty": "easy"},
                    {"title": "Two Sum II - Input Array Is Sorted", "leetcode_number": 167, "difficulty": "medium"},
                    {"title": "3Sum", "leetcode_number": 15, "difficulty": "medium"},
                    {"title": "Container With Most Water", "leetcode_number": 11, "difficulty": "medium"},
                    {"title": "Trapping Rain Water", "leetcode_number": 42, "difficulty": "hard"},
                ]
            },
            {
                "name": "Sliding Window",
                "category": "arrays_strings",
                "difficulty": "medium",
                "estimated_days": 3,
                "key_concepts": ["Fixed window", "Variable window", "Window shrinking condition"],
                "common_patterns": ["Fixed size window", "Longest/shortest subarray", "Character frequency window"],
                "problems": [
                    {"title": "Maximum Average Subarray I", "leetcode_number": 643, "difficulty": "easy"},
                    {"title": "Longest Substring Without Repeating Characters", "leetcode_number": 3, "difficulty": "medium"},
                    {"title": "Minimum Window Substring", "leetcode_number": 76, "difficulty": "hard"},
                    {"title": "Permutation in String", "leetcode_number": 567, "difficulty": "medium"},
                    {"title": "Sliding Window Maximum", "leetcode_number": 239, "difficulty": "hard"},
                ]
            },
            {
                "name": "String Manipulation",
                "category": "arrays_strings",
                "difficulty": "medium",
                "estimated_days": 3,
                "key_concepts": ["String building", "Anagram detection", "Palindromes", "Pattern matching"],
                "common_patterns": ["Character frequency", "String comparison", "StringBuilder patterns"],
                "problems": [
                    {"title": "Valid Anagram", "leetcode_number": 242, "difficulty": "easy"},
                    {"title": "Longest Palindromic Substring", "leetcode_number": 5, "difficulty": "medium"},
                    {"title": "Group Anagrams", "leetcode_number": 49, "difficulty": "medium"},
                    {"title": "Longest Common Prefix", "leetcode_number": 14, "difficulty": "easy"},
                    {"title": "String to Integer (atoi)", "leetcode_number": 8, "difficulty": "medium"},
                ]
            },
        ]
    },
    "hashing": {
        "order": 3,
        "topics": [
            {
                "name": "Hash Maps & Hash Sets",
                "category": "hashing",
                "difficulty": "easy",
                "estimated_days": 3,
                "key_concepts": ["Hash functions", "Collision handling", "Frequency counting", "Lookup optimization"],
                "common_patterns": ["Frequency map", "Two-pass hash", "Complement lookup"],
                "problems": [
                    {"title": "Two Sum", "leetcode_number": 1, "difficulty": "easy"},
                    {"title": "Longest Consecutive Sequence", "leetcode_number": 128, "difficulty": "medium"},
                    {"title": "Top K Frequent Elements", "leetcode_number": 347, "difficulty": "medium"},
                    {"title": "Valid Sudoku", "leetcode_number": 36, "difficulty": "medium"},
                    {"title": "Encode and Decode Strings", "leetcode_number": 271, "difficulty": "medium"},
                ]
            },
        ]
    },
    "linked_lists": {
        "order": 4,
        "topics": [
            {
                "name": "Singly Linked Lists",
                "category": "linked_lists",
                "difficulty": "easy",
                "estimated_days": 3,
                "key_concepts": ["Node structure", "Traversal", "Insertion", "Deletion", "Reversal"],
                "common_patterns": ["Dummy head", "Runner technique", "In-place reversal"],
                "problems": [
                    {"title": "Reverse Linked List", "leetcode_number": 206, "difficulty": "easy"},
                    {"title": "Merge Two Sorted Lists", "leetcode_number": 21, "difficulty": "easy"},
                    {"title": "Linked List Cycle", "leetcode_number": 141, "difficulty": "easy"},
                    {"title": "Remove Nth Node From End of List", "leetcode_number": 19, "difficulty": "medium"},
                    {"title": "Reorder List", "leetcode_number": 143, "difficulty": "medium"},
                ]
            },
            {
                "name": "Advanced Linked Lists",
                "category": "linked_lists",
                "difficulty": "medium",
                "estimated_days": 2,
                "key_concepts": ["Doubly linked lists", "Circular lists", "Skip lists", "LRU Cache"],
                "common_patterns": ["Merge sort on lists", "Floyd's cycle detection", "Multi-level lists"],
                "problems": [
                    {"title": "Add Two Numbers", "leetcode_number": 2, "difficulty": "medium"},
                    {"title": "Copy List with Random Pointer", "leetcode_number": 138, "difficulty": "medium"},
                    {"title": "LRU Cache", "leetcode_number": 146, "difficulty": "medium"},
                    {"title": "Merge k Sorted Lists", "leetcode_number": 23, "difficulty": "hard"},
                ]
            },
        ]
    },
    "stacks_queues": {
        "order": 5,
        "topics": [
            {
                "name": "Stacks",
                "category": "stacks_queues",
                "difficulty": "easy",
                "estimated_days": 3,
                "key_concepts": ["LIFO principle", "Monotonic stack", "Expression evaluation", "Parentheses matching"],
                "common_patterns": ["Monotonic stack", "Next greater element", "Stack for parsing"],
                "problems": [
                    {"title": "Valid Parentheses", "leetcode_number": 20, "difficulty": "easy"},
                    {"title": "Min Stack", "leetcode_number": 155, "difficulty": "medium"},
                    {"title": "Daily Temperatures", "leetcode_number": 739, "difficulty": "medium"},
                    {"title": "Largest Rectangle in Histogram", "leetcode_number": 84, "difficulty": "hard"},
                    {"title": "Evaluate Reverse Polish Notation", "leetcode_number": 150, "difficulty": "medium"},
                ]
            },
            {
                "name": "Queues & Deques",
                "category": "stacks_queues",
                "difficulty": "medium",
                "estimated_days": 2,
                "key_concepts": ["FIFO principle", "Circular queue", "Priority queue basics", "Deque operations"],
                "common_patterns": ["BFS with queue", "Sliding window with deque", "Task scheduling"],
                "problems": [
                    {"title": "Implement Queue using Stacks", "leetcode_number": 232, "difficulty": "easy"},
                    {"title": "Sliding Window Maximum", "leetcode_number": 239, "difficulty": "hard"},
                    {"title": "Design Circular Queue", "leetcode_number": 622, "difficulty": "medium"},
                ]
            },
        ]
    },
    "trees": {
        "order": 6,
        "topics": [
            {
                "name": "Binary Trees - Traversals",
                "category": "trees",
                "difficulty": "easy",
                "estimated_days": 3,
                "key_concepts": ["Inorder", "Preorder", "Postorder", "Level-order", "DFS vs BFS"],
                "common_patterns": ["Recursive traversal", "Iterative with stack", "Level-order with queue"],
                "problems": [
                    {"title": "Binary Tree Inorder Traversal", "leetcode_number": 94, "difficulty": "easy"},
                    {"title": "Maximum Depth of Binary Tree", "leetcode_number": 104, "difficulty": "easy"},
                    {"title": "Invert Binary Tree", "leetcode_number": 226, "difficulty": "easy"},
                    {"title": "Same Tree", "leetcode_number": 100, "difficulty": "easy"},
                    {"title": "Binary Tree Level Order Traversal", "leetcode_number": 102, "difficulty": "medium"},
                ]
            },
            {
                "name": "Binary Search Trees",
                "category": "trees",
                "difficulty": "medium",
                "estimated_days": 3,
                "key_concepts": ["BST property", "Search/Insert/Delete", "Validation", "Balancing concepts"],
                "common_patterns": ["BST validation", "Inorder gives sorted", "Successor/Predecessor"],
                "problems": [
                    {"title": "Validate Binary Search Tree", "leetcode_number": 98, "difficulty": "medium"},
                    {"title": "Lowest Common Ancestor of a BST", "leetcode_number": 235, "difficulty": "medium"},
                    {"title": "Kth Smallest Element in a BST", "leetcode_number": 230, "difficulty": "medium"},
                    {"title": "Serialize and Deserialize BST", "leetcode_number": 449, "difficulty": "medium"},
                ]
            },
            {
                "name": "Advanced Tree Problems",
                "category": "trees",
                "difficulty": "hard",
                "estimated_days": 3,
                "key_concepts": ["Tree DP", "Path problems", "Diameter", "Tries"],
                "common_patterns": ["Path sum patterns", "Tree serialization", "Morris traversal"],
                "problems": [
                    {"title": "Binary Tree Maximum Path Sum", "leetcode_number": 124, "difficulty": "hard"},
                    {"title": "Diameter of Binary Tree", "leetcode_number": 543, "difficulty": "easy"},
                    {"title": "Construct Binary Tree from Preorder and Inorder Traversal", "leetcode_number": 105, "difficulty": "medium"},
                    {"title": "Implement Trie (Prefix Tree)", "leetcode_number": 208, "difficulty": "medium"},
                    {"title": "Word Search II", "leetcode_number": 212, "difficulty": "hard"},
                ]
            },
        ]
    },
    "heaps": {
        "order": 7,
        "topics": [
            {
                "name": "Heaps & Priority Queues",
                "category": "heaps",
                "difficulty": "medium",
                "estimated_days": 3,
                "key_concepts": ["Min/Max heap", "Heapify", "Heap sort", "K-way problems"],
                "common_patterns": ["Top K elements", "K-way merge", "Two heaps for median"],
                "problems": [
                    {"title": "Kth Largest Element in an Array", "leetcode_number": 215, "difficulty": "medium"},
                    {"title": "Top K Frequent Elements", "leetcode_number": 347, "difficulty": "medium"},
                    {"title": "Find Median from Data Stream", "leetcode_number": 295, "difficulty": "hard"},
                    {"title": "Merge k Sorted Lists", "leetcode_number": 23, "difficulty": "hard"},
                    {"title": "Task Scheduler", "leetcode_number": 621, "difficulty": "medium"},
                ]
            },
        ]
    },
    "graphs": {
        "order": 8,
        "topics": [
            {
                "name": "Graph Representations & BFS/DFS",
                "category": "graphs",
                "difficulty": "medium",
                "estimated_days": 4,
                "key_concepts": ["Adjacency list", "Adjacency matrix", "BFS", "DFS", "Connected components"],
                "common_patterns": ["Grid BFS/DFS", "Island counting", "Flood fill"],
                "problems": [
                    {"title": "Number of Islands", "leetcode_number": 200, "difficulty": "medium"},
                    {"title": "Clone Graph", "leetcode_number": 133, "difficulty": "medium"},
                    {"title": "Pacific Atlantic Water Flow", "leetcode_number": 417, "difficulty": "medium"},
                    {"title": "Course Schedule", "leetcode_number": 207, "difficulty": "medium"},
                    {"title": "Rotting Oranges", "leetcode_number": 994, "difficulty": "medium"},
                ]
            },
            {
                "name": "Topological Sort & Advanced Graphs",
                "category": "graphs",
                "difficulty": "hard",
                "estimated_days": 3,
                "key_concepts": ["Topological ordering", "Cycle detection", "Union-Find", "Shortest paths"],
                "common_patterns": ["Kahn's algorithm", "DFS topological sort", "Union-Find with rank"],
                "problems": [
                    {"title": "Course Schedule II", "leetcode_number": 210, "difficulty": "medium"},
                    {"title": "Alien Dictionary", "leetcode_number": 269, "difficulty": "hard"},
                    {"title": "Graph Valid Tree", "leetcode_number": 261, "difficulty": "medium"},
                    {"title": "Number of Connected Components in an Undirected Graph", "leetcode_number": 323, "difficulty": "medium"},
                    {"title": "Redundant Connection", "leetcode_number": 684, "difficulty": "medium"},
                ]
            },
            {
                "name": "Shortest Path Algorithms",
                "category": "graphs",
                "difficulty": "hard",
                "estimated_days": 3,
                "key_concepts": ["Dijkstra's", "Bellman-Ford", "Floyd-Warshall", "A*"],
                "common_patterns": ["Weighted BFS", "Priority queue BFS", "Multi-source BFS"],
                "problems": [
                    {"title": "Network Delay Time", "leetcode_number": 743, "difficulty": "medium"},
                    {"title": "Cheapest Flights Within K Stops", "leetcode_number": 787, "difficulty": "medium"},
                    {"title": "Swim in Rising Water", "leetcode_number": 778, "difficulty": "hard"},
                ]
            },
        ]
    },
    "binary_search": {
        "order": 9,
        "topics": [
            {
                "name": "Binary Search Patterns",
                "category": "binary_search",
                "difficulty": "medium",
                "estimated_days": 3,
                "key_concepts": ["Classic binary search", "Search space reduction", "Rotated arrays", "Search on answer"],
                "common_patterns": ["Left/Right boundary", "Search on answer", "Peak finding"],
                "problems": [
                    {"title": "Binary Search", "leetcode_number": 704, "difficulty": "easy"},
                    {"title": "Search in Rotated Sorted Array", "leetcode_number": 33, "difficulty": "medium"},
                    {"title": "Find Minimum in Rotated Sorted Array", "leetcode_number": 153, "difficulty": "medium"},
                    {"title": "Search a 2D Matrix", "leetcode_number": 74, "difficulty": "medium"},
                    {"title": "Koko Eating Bananas", "leetcode_number": 875, "difficulty": "medium"},
                    {"title": "Median of Two Sorted Arrays", "leetcode_number": 4, "difficulty": "hard"},
                ]
            },
        ]
    },
    "recursion_backtracking": {
        "order": 10,
        "topics": [
            {
                "name": "Recursion Fundamentals",
                "category": "recursion_backtracking",
                "difficulty": "medium",
                "estimated_days": 2,
                "key_concepts": ["Base cases", "Recursive decomposition", "Call stack", "Memoization intro"],
                "common_patterns": ["Divide and conquer", "Generate all possibilities", "Tree recursion"],
                "problems": [
                    {"title": "Pow(x, n)", "leetcode_number": 50, "difficulty": "medium"},
                    {"title": "Climbing Stairs", "leetcode_number": 70, "difficulty": "easy"},
                    {"title": "Fibonacci Number", "leetcode_number": 509, "difficulty": "easy"},
                ]
            },
            {
                "name": "Backtracking",
                "category": "recursion_backtracking",
                "difficulty": "medium",
                "estimated_days": 4,
                "key_concepts": ["Choice-constraint-goal framework", "Pruning", "State management"],
                "common_patterns": ["Subsets/Combinations", "Permutations", "Grid backtracking"],
                "problems": [
                    {"title": "Subsets", "leetcode_number": 78, "difficulty": "medium"},
                    {"title": "Combination Sum", "leetcode_number": 39, "difficulty": "medium"},
                    {"title": "Permutations", "leetcode_number": 46, "difficulty": "medium"},
                    {"title": "Word Search", "leetcode_number": 79, "difficulty": "medium"},
                    {"title": "N-Queens", "leetcode_number": 51, "difficulty": "hard"},
                    {"title": "Palindrome Partitioning", "leetcode_number": 131, "difficulty": "medium"},
                ]
            },
        ]
    },
    "dynamic_programming": {
        "order": 11,
        "topics": [
            {
                "name": "1D Dynamic Programming",
                "category": "dynamic_programming",
                "difficulty": "medium",
                "estimated_days": 4,
                "key_concepts": ["Optimal substructure", "Overlapping subproblems", "Top-down vs Bottom-up", "State definition"],
                "common_patterns": ["Linear DP", "Decision at each step", "Min/Max optimization"],
                "problems": [
                    {"title": "Climbing Stairs", "leetcode_number": 70, "difficulty": "easy"},
                    {"title": "House Robber", "leetcode_number": 198, "difficulty": "medium"},
                    {"title": "Coin Change", "leetcode_number": 322, "difficulty": "medium"},
                    {"title": "Longest Increasing Subsequence", "leetcode_number": 300, "difficulty": "medium"},
                    {"title": "Word Break", "leetcode_number": 139, "difficulty": "medium"},
                    {"title": "Decode Ways", "leetcode_number": 91, "difficulty": "medium"},
                ]
            },
            {
                "name": "2D Dynamic Programming",
                "category": "dynamic_programming",
                "difficulty": "hard",
                "estimated_days": 4,
                "key_concepts": ["Grid DP", "Two sequence DP", "Knapsack variants", "Interval DP"],
                "common_patterns": ["Grid path counting", "LCS/Edit distance", "0/1 Knapsack"],
                "problems": [
                    {"title": "Unique Paths", "leetcode_number": 62, "difficulty": "medium"},
                    {"title": "Longest Common Subsequence", "leetcode_number": 1143, "difficulty": "medium"},
                    {"title": "Edit Distance", "leetcode_number": 72, "difficulty": "medium"},
                    {"title": "Target Sum", "leetcode_number": 494, "difficulty": "medium"},
                    {"title": "Interleaving String", "leetcode_number": 97, "difficulty": "medium"},
                    {"title": "Burst Balloons", "leetcode_number": 312, "difficulty": "hard"},
                ]
            },
        ]
    },
    "greedy": {
        "order": 12,
        "topics": [
            {
                "name": "Greedy Algorithms",
                "category": "greedy",
                "difficulty": "medium",
                "estimated_days": 3,
                "key_concepts": ["Greedy choice property", "Interval scheduling", "Activity selection", "Proof of correctness"],
                "common_patterns": ["Sort and greedy", "Interval merging", "Jump game pattern"],
                "problems": [
                    {"title": "Jump Game", "leetcode_number": 55, "difficulty": "medium"},
                    {"title": "Jump Game II", "leetcode_number": 45, "difficulty": "medium"},
                    {"title": "Gas Station", "leetcode_number": 134, "difficulty": "medium"},
                    {"title": "Hand of Straights", "leetcode_number": 846, "difficulty": "medium"},
                    {"title": "Merge Intervals", "leetcode_number": 56, "difficulty": "medium"},
                    {"title": "Non-overlapping Intervals", "leetcode_number": 435, "difficulty": "medium"},
                ]
            },
        ]
    },
    "advanced": {
        "order": 13,
        "topics": [
            {
                "name": "Bit Manipulation",
                "category": "advanced",
                "difficulty": "medium",
                "estimated_days": 2,
                "key_concepts": ["Bitwise operators", "Bit masking", "XOR properties", "Counting bits"],
                "common_patterns": ["Single number pattern", "Bit masking for subsets", "Power of two"],
                "problems": [
                    {"title": "Single Number", "leetcode_number": 136, "difficulty": "easy"},
                    {"title": "Number of 1 Bits", "leetcode_number": 191, "difficulty": "easy"},
                    {"title": "Counting Bits", "leetcode_number": 338, "difficulty": "easy"},
                    {"title": "Reverse Bits", "leetcode_number": 190, "difficulty": "easy"},
                    {"title": "Sum of Two Integers", "leetcode_number": 371, "difficulty": "medium"},
                ]
            },
            {
                "name": "Math & Geometry",
                "category": "advanced",
                "difficulty": "medium",
                "estimated_days": 2,
                "key_concepts": ["Modular arithmetic", "Matrix operations", "Geometry basics", "Number theory"],
                "common_patterns": ["Matrix rotation", "Spiral traversal", "GCD/LCM"],
                "problems": [
                    {"title": "Rotate Image", "leetcode_number": 48, "difficulty": "medium"},
                    {"title": "Spiral Matrix", "leetcode_number": 54, "difficulty": "medium"},
                    {"title": "Set Matrix Zeroes", "leetcode_number": 73, "difficulty": "medium"},
                    {"title": "Happy Number", "leetcode_number": 202, "difficulty": "easy"},
                ]
            },
            {
                "name": "Intervals & Sweep Line",
                "category": "advanced",
                "difficulty": "medium",
                "estimated_days": 2,
                "key_concepts": ["Interval merging", "Interval intersection", "Sweep line technique"],
                "common_patterns": ["Sort by start", "Meeting rooms pattern", "Skyline problem"],
                "problems": [
                    {"title": "Merge Intervals", "leetcode_number": 56, "difficulty": "medium"},
                    {"title": "Insert Interval", "leetcode_number": 57, "difficulty": "medium"},
                    {"title": "Meeting Rooms II", "leetcode_number": 253, "difficulty": "medium"},
                ]
            },
        ]
    },
    "system_design_patterns": {
        "order": 14,
        "topics": [
            {
                "name": "Design Data Structures",
                "category": "system_design_patterns",
                "difficulty": "hard",
                "estimated_days": 3,
                "key_concepts": ["LRU/LFU Cache", "HashMap + LinkedList", "Circular buffer", "Trie applications"],
                "common_patterns": ["Combine data structures", "Amortized operations", "Iterator pattern"],
                "problems": [
                    {"title": "LRU Cache", "leetcode_number": 146, "difficulty": "medium"},
                    {"title": "LFU Cache", "leetcode_number": 460, "difficulty": "hard"},
                    {"title": "Design Twitter", "leetcode_number": 355, "difficulty": "medium"},
                    {"title": "Design Add and Search Words Data Structure", "leetcode_number": 211, "difficulty": "medium"},
                ]
            },
        ]
    },
}

# Concept lessons for the teaching agent
CONCEPT_LESSONS = {
    "arrays_basics": {
        "title": "Arrays - The Foundation of DSA",
        "sections": [
            {
                "heading": "What is an Array?",
                "content": "An array is a contiguous block of memory that stores elements of the same type. Each element is accessible by its index in O(1) time.",
                "visualization": "array_basic"
            },
            {
                "heading": "Key Operations & Complexity",
                "content": "Access: O(1) | Search: O(n) | Insert at end: O(1) amortized | Insert at index: O(n) | Delete: O(n)",
                "visualization": "array_operations"
            },
            {
                "heading": "Common Patterns",
                "content": "1. Two Pointers: Use two indices moving towards each other or in the same direction\n2. Sliding Window: Maintain a window of elements that satisfies a condition\n3. Prefix Sum: Precompute cumulative sums for range queries in O(1)",
                "visualization": "array_patterns"
            },
        ]
    },
    "linked_list_basics": {
        "title": "Linked Lists - Dynamic Memory Mastery",
        "sections": [
            {
                "heading": "Singly Linked List",
                "content": "A linked list is a sequence of nodes where each node contains data and a pointer to the next node. Unlike arrays, linked lists allow O(1) insertion/deletion at known positions.",
                "visualization": "linked_list_basic"
            },
            {
                "heading": "Key Operations",
                "content": "Access: O(n) | Search: O(n) | Insert at head: O(1) | Insert at tail: O(1) with tail pointer | Delete: O(1) if node known",
                "visualization": "linked_list_operations"
            },
        ]
    },
    "binary_tree_basics": {
        "title": "Binary Trees - Hierarchical Data",
        "sections": [
            {
                "heading": "Tree Structure",
                "content": "A binary tree is a hierarchical data structure where each node has at most two children. The topmost node is the root.",
                "visualization": "binary_tree_basic"
            },
            {
                "heading": "Tree Traversals",
                "content": "Inorder (Left-Root-Right): Gives sorted order for BST\nPreorder (Root-Left-Right): Used for serialization\nPostorder (Left-Right-Root): Used for deletion\nLevel-order: BFS with queue",
                "visualization": "tree_traversals"
            },
        ]
    },
    "graph_basics": {
        "title": "Graphs - Networks & Connections",
        "sections": [
            {
                "heading": "Graph Representations",
                "content": "Adjacency List: Space O(V+E), good for sparse graphs\nAdjacency Matrix: Space O(V²), good for dense graphs\nEdge List: Simple but less efficient for lookups",
                "visualization": "graph_representations"
            },
            {
                "heading": "BFS vs DFS",
                "content": "BFS explores level by level using a queue - best for shortest path in unweighted graphs\nDFS explores as deep as possible using a stack/recursion - best for connectivity, cycles, topological sort",
                "visualization": "bfs_vs_dfs"
            },
        ]
    },
    "dp_basics": {
        "title": "Dynamic Programming - Optimal Substructure",
        "sections": [
            {
                "heading": "When to Use DP",
                "content": "1. Optimal substructure: Solution can be built from solutions to subproblems\n2. Overlapping subproblems: Same subproblems solved multiple times\n3. Usually asks for min/max, count, or existence",
                "visualization": "dp_decision_tree"
            },
            {
                "heading": "Top-Down vs Bottom-Up",
                "content": "Top-Down (Memoization): Start from the original problem, cache results\nBottom-Up (Tabulation): Start from smallest subproblems, build up\nBoth have same time complexity, bottom-up often has better constant factors",
                "visualization": "dp_approaches"
            },
        ]
    },
}

# Pattern-based problem categorization for spaced repetition
PROBLEM_PATTERNS = {
    "two_pointers": {
        "description": "Use two pointers to traverse data structure efficiently",
        "when_to_use": "Sorted arrays, finding pairs, palindromes, linked list problems",
        "template": "Initialize left=0, right=len-1. While left < right, make decisions based on condition.",
    },
    "sliding_window": {
        "description": "Maintain a window that slides over data to find optimal subarray/substring",
        "when_to_use": "Contiguous subarray/substring problems, fixed or variable window size",
        "template": "Expand right boundary. When condition violated, shrink left boundary.",
    },
    "binary_search": {
        "description": "Divide search space in half each iteration",
        "when_to_use": "Sorted data, search space can be halved, monotonic function",
        "template": "lo, hi = bounds. While lo < hi: mid = (lo+hi)//2, adjust based on condition.",
    },
    "bfs": {
        "description": "Explore nodes level by level using a queue",
        "when_to_use": "Shortest path (unweighted), level-order traversal, multi-source problems",
        "template": "Queue with starting nodes. Process level by level, mark visited.",
    },
    "dfs": {
        "description": "Explore as deep as possible before backtracking",
        "when_to_use": "Connected components, cycle detection, path finding, tree problems",
        "template": "Stack/recursion. Mark visited, explore all neighbors recursively.",
    },
    "backtracking": {
        "description": "Build solution incrementally, abandon paths that can't lead to solution",
        "when_to_use": "Generate all valid combinations/permutations, constraint satisfaction",
        "template": "Choose -> Explore -> Unchoose. Prune invalid branches early.",
    },
    "dp_linear": {
        "description": "Build optimal solution from left to right",
        "when_to_use": "Sequence problems with optimal substructure, counting paths",
        "template": "dp[i] = best solution ending at/using first i elements. Base case dp[0].",
    },
    "dp_grid": {
        "description": "DP on 2D grid, typically filling table cell by cell",
        "when_to_use": "Two sequences (LCS, edit distance), grid paths, knapsack",
        "template": "dp[i][j] depends on dp[i-1][j], dp[i][j-1], dp[i-1][j-1].",
    },
    "monotonic_stack": {
        "description": "Stack maintaining monotonic order for next greater/smaller element",
        "when_to_use": "Next greater element, histogram problems, stock span",
        "template": "Process elements, pop stack while condition met, push current.",
    },
    "union_find": {
        "description": "Track connected components efficiently with path compression and rank",
        "when_to_use": "Dynamic connectivity, cycle detection in undirected graphs, grouping",
        "template": "Find with path compression, Union by rank. Track component count.",
    },
    "topological_sort": {
        "description": "Linear ordering of vertices in a DAG",
        "when_to_use": "Dependency resolution, course scheduling, build order",
        "template": "Kahn's: BFS from nodes with 0 in-degree. DFS: Reverse post-order.",
    },
    "heap_top_k": {
        "description": "Use heap to efficiently find K largest/smallest elements",
        "when_to_use": "Top K elements, K-way merge, running median",
        "template": "Min-heap of size K for top K largest. Max-heap for top K smallest.",
    },
}
