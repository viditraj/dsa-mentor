"""Fetch and cache real LeetCode problem descriptions."""
import re
import asyncio
import logging
from html import unescape

import httpx

logger = logging.getLogger(__name__)

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

QUERY = """
query questionContent($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    content
    difficulty
    exampleTestcaseList
  }
}
"""

# ── In-memory cache ──
_cache: dict[str, str] = {}


def _title_to_slug(title: str) -> str:
    """Convert problem title to LeetCode URL slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def _html_to_text(html: str) -> str:
    """Convert LeetCode HTML description to clean readable text."""
    if not html:
        return ""
    text = html
    # Convert common HTML elements
    text = re.sub(r"<p>", "\n", text)
    text = re.sub(r"</p>", "", text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<strong>|<b>", "**", text)
    text = re.sub(r"</strong>|</b>", "**", text)
    text = re.sub(r"<em>|<i>", "_", text)
    text = re.sub(r"</em>|</i>", "_", text)
    text = re.sub(r"<code>", "`", text)
    text = re.sub(r"</code>", "`", text)
    text = re.sub(r"<sup>", "^", text)
    text = re.sub(r"</sup>", "", text)
    text = re.sub(r"<sub>", "_", text)
    text = re.sub(r"</sub>", "", text)
    text = re.sub(r"</?ul>", "\n", text)
    text = re.sub(r"<li>", "• ", text)
    text = re.sub(r"</li>", "\n", text)
    text = re.sub(r"<pre>", "\n```\n", text)
    text = re.sub(r"</pre>", "\n```\n", text)
    # Remove all remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text


async def fetch_leetcode_description(title: str, leetcode_number: int = None) -> str:
    """Fetch problem description from LeetCode's public GraphQL API."""
    slug = _title_to_slug(title)
    cache_key = slug

    if cache_key in _cache:
        return _cache[cache_key]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                LEETCODE_GRAPHQL,
                json={
                    "query": QUERY,
                    "variables": {"titleSlug": slug},
                },
                headers={
                    "Content-Type": "application/json",
                    "Referer": f"https://leetcode.com/problems/{slug}/",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                },
            )

            if resp.status_code == 200:
                data = resp.json()
                question = data.get("data", {}).get("question")
                if question and question.get("content"):
                    description = _html_to_text(question["content"])
                    _cache[cache_key] = description
                    logger.info(f"Fetched description for '{title}' from LeetCode")
                    return description

        logger.warning(f"No description returned for '{title}' (slug: {slug})")
    except Exception as e:
        logger.warning(f"Failed to fetch description for '{title}': {e}")

    # Return fallback from local cache
    fallback = LOCAL_DESCRIPTIONS.get(leetcode_number) or LOCAL_DESCRIPTIONS.get(title)
    if fallback:
        _cache[cache_key] = fallback
        return fallback

    return ""


async def get_problem_description(title: str, leetcode_number: int = None) -> str:
    """Get description: try local cache first, then fetch from LeetCode."""
    # Check local descriptions first (instant)
    desc = LOCAL_DESCRIPTIONS.get(leetcode_number) or LOCAL_DESCRIPTIONS.get(title)
    if desc:
        return desc

    # Try fetching from LeetCode
    return await fetch_leetcode_description(title, leetcode_number)


# ═══════════════════════════════════════════
# LOCAL DESCRIPTIONS CACHE
# Real problem descriptions for all curriculum problems
# ═══════════════════════════════════════════

LOCAL_DESCRIPTIONS = {
    # ── Arrays & Basics ──
    1: (
        "Given an array of integers `nums` and an integer `target`, return "
        "indices of the two numbers such that they add up to `target`.\n\n"
        "You may assume that each input would have exactly one solution, "
        "and you may not use the same element twice.\n\n"
        "You can return the answer in any order.\n\n"
        "**Example 1:**\n"
        "Input: nums = [2,7,11,15], target = 9\n"
        "Output: [0,1]\n"
        "Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].\n\n"
        "**Example 2:**\n"
        "Input: nums = [3,2,4], target = 6\n"
        "Output: [1,2]\n\n"
        "**Constraints:**\n"
        "• 2 <= nums.length <= 10^4\n"
        "• -10^9 <= nums[i] <= 10^9\n"
        "• -10^9 <= target <= 10^9\n"
        "• Only one valid answer exists."
    ),

    121: (
        "You are given an array `prices` where `prices[i]` is the price of a given "
        "stock on the ith day.\n\n"
        "You want to maximize your profit by choosing a single day to buy one stock "
        "and choosing a different day in the future to sell that stock.\n\n"
        "Return the maximum profit you can achieve from this transaction. "
        "If you cannot achieve any profit, return 0.\n\n"
        "**Example 1:**\n"
        "Input: prices = [7,1,5,3,6,4]\n"
        "Output: 5\n"
        "Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.\n\n"
        "**Example 2:**\n"
        "Input: prices = [7,6,4,3,1]\n"
        "Output: 0\n"
        "Explanation: No transactions, max profit = 0.\n\n"
        "**Constraints:**\n"
        "• 1 <= prices.length <= 10^5\n"
        "• 0 <= prices[i] <= 10^4"
    ),

    53: (
        "Given an integer array `nums`, find the subarray with the largest sum, "
        "and return its sum.\n\n"
        "**Example 1:**\n"
        "Input: nums = [-2,1,-3,4,-1,2,1,-5,4]\n"
        "Output: 6\n"
        "Explanation: The subarray [4,-1,2,1] has the largest sum 6.\n\n"
        "**Example 2:**\n"
        "Input: nums = [5,4,-1,7,8]\n"
        "Output: 23\n"
        "Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 10^5\n"
        "• -10^4 <= nums[i] <= 10^4\n\n"
        "**Follow up:** If you have figured out the O(n) solution, try coding another "
        "solution using the divide and conquer approach, which is more subtle."
    ),

    238: (
        "Given an integer array `nums`, return an array `answer` such that `answer[i]` "
        "is equal to the product of all the elements of `nums` except `nums[i]`.\n\n"
        "The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.\n\n"
        "You must write an algorithm that runs in O(n) time and without using the division operation.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,2,3,4]\n"
        "Output: [24,12,8,6]\n\n"
        "**Example 2:**\n"
        "Input: nums = [-1,1,0,-3,3]\n"
        "Output: [0,0,9,0,0]\n\n"
        "**Constraints:**\n"
        "• 2 <= nums.length <= 10^5\n"
        "• -30 <= nums[i] <= 30\n"
        "• The product of any prefix or suffix of nums fits in a 32-bit integer."
    ),

    217: (
        "Given an integer array `nums`, return `true` if any value appears at least "
        "twice in the array, and return `false` if every element is distinct.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,2,3,1]\n"
        "Output: true\n\n"
        "**Example 2:**\n"
        "Input: nums = [1,2,3,4]\n"
        "Output: false\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 10^5\n"
        "• -10^9 <= nums[i] <= 10^9"
    ),

    1480: (
        "Given an array `nums`. We define a running sum of an array as "
        "`runningSum[i] = sum(nums[0]...nums[i])`.\n\n"
        "Return the running sum of `nums`.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,2,3,4]\n"
        "Output: [1,3,6,10]\n"
        "Explanation: Running sum is [1, 1+2, 1+2+3, 1+2+3+4].\n\n"
        "**Example 2:**\n"
        "Input: nums = [3,1,2,10,1]\n"
        "Output: [3,4,6,16,17]\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 1000\n"
        "• -10^6 <= nums[i] <= 10^6"
    ),

    # ── Two Pointers ──
    125: (
        "A phrase is a palindrome if, after converting all uppercase letters into "
        "lowercase letters and removing all non-alphanumeric characters, it reads "
        "the same forward and backward.\n\n"
        "Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.\n\n"
        "**Example 1:**\n"
        "Input: s = \"A man, a plan, a canal: Panama\"\n"
        "Output: true\n"
        "Explanation: \"amanaplanacanalpanama\" is a palindrome.\n\n"
        "**Example 2:**\n"
        "Input: s = \"race a car\"\n"
        "Output: false\n\n"
        "**Constraints:**\n"
        "• 1 <= s.length <= 2 * 10^5\n"
        "• s consists only of printable ASCII characters."
    ),

    167: (
        "Given a 1-indexed array of integers `numbers` that is already sorted in "
        "non-decreasing order, find two numbers such that they add up to a specific "
        "`target` number.\n\n"
        "Return the indices of the two numbers (1-indexed) as an integer array `[index1, index2]`.\n\n"
        "You may not use the same element twice. The solution must use only constant extra space.\n\n"
        "**Example 1:**\n"
        "Input: numbers = [2,7,11,15], target = 9\n"
        "Output: [1,2]\n\n"
        "**Constraints:**\n"
        "• 2 <= numbers.length <= 3 * 10^4\n"
        "• -1000 <= numbers[i] <= 1000\n"
        "• numbers is sorted in non-decreasing order.\n"
        "• Exactly one solution exists."
    ),

    15: (
        "Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` "
        "such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\n"
        "Notice that the solution set must not contain duplicate triplets.\n\n"
        "**Example 1:**\n"
        "Input: nums = [-1,0,1,2,-1,-4]\n"
        "Output: [[-1,-1,2],[-1,0,1]]\n\n"
        "**Example 2:**\n"
        "Input: nums = [0,1,1]\n"
        "Output: []\n\n"
        "**Constraints:**\n"
        "• 3 <= nums.length <= 3000\n"
        "• -10^5 <= nums[i] <= 10^5"
    ),

    11: (
        "You are given an integer array `height` of length `n`. There are `n` vertical "
        "lines drawn such that the two endpoints of the ith line are `(i, 0)` and `(i, height[i])`.\n\n"
        "Find two lines that together with the x-axis form a container, such that the container "
        "contains the most water.\n\n"
        "Return the maximum amount of water a container can store.\n\n"
        "**Example 1:**\n"
        "Input: height = [1,8,6,2,5,4,8,3,7]\n"
        "Output: 49\n\n"
        "**Constraints:**\n"
        "• n == height.length\n"
        "• 2 <= n <= 10^5\n"
        "• 0 <= height[i] <= 10^4"
    ),

    42: (
        "Given `n` non-negative integers representing an elevation map where the width of each "
        "bar is 1, compute how much water it can trap after raining.\n\n"
        "**Example 1:**\n"
        "Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]\n"
        "Output: 6\n"
        "Explanation: The above elevation map is represented by [0,1,0,2,1,0,1,3,2,1,2,1]. "
        "In this case, 6 units of rain water are being trapped.\n\n"
        "**Constraints:**\n"
        "• n == height.length\n"
        "• 1 <= n <= 2 * 10^4\n"
        "• 0 <= height[i] <= 10^5"
    ),

    # ── Sliding Window ──
    3: (
        "Given a string `s`, find the length of the longest substring without repeating characters.\n\n"
        "**Example 1:**\n"
        "Input: s = \"abcabcbb\"\n"
        "Output: 3\n"
        "Explanation: The answer is \"abc\", with length 3.\n\n"
        "**Example 2:**\n"
        "Input: s = \"bbbbb\"\n"
        "Output: 1\n"
        "Explanation: The answer is \"b\", with length 1.\n\n"
        "**Constraints:**\n"
        "• 0 <= s.length <= 5 * 10^4\n"
        "• s consists of English letters, digits, symbols and spaces."
    ),

    76: (
        "Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum "
        "window substring of `s` such that every character in `t` (including duplicates) is included "
        "in the window. If there is no such substring, return the empty string \"\".\n\n"
        "**Example 1:**\n"
        "Input: s = \"ADOBECODEBANC\", t = \"ABC\"\n"
        "Output: \"BANC\"\n"
        "Explanation: The minimum window substring \"BANC\" includes 'A', 'B', and 'C' from string t.\n\n"
        "**Constraints:**\n"
        "• m == s.length, n == t.length\n"
        "• 1 <= m, n <= 10^5\n"
        "• s and t consist of uppercase and lowercase English letters.\n\n"
        "**Follow up:** Could you find an algorithm that runs in O(m + n) time?"
    ),

    424: (
        "You are given a string `s` and an integer `k`. You can choose any character of the string "
        "and change it to any other uppercase English character. You can perform this operation at most "
        "`k` times.\n\n"
        "Return the length of the longest substring containing the same letter you can get after "
        "performing the above operations.\n\n"
        "**Example 1:**\n"
        "Input: s = \"ABAB\", k = 2\n"
        "Output: 4\n"
        "Explanation: Replace the two 'A's with two 'B's or vice versa.\n\n"
        "**Example 2:**\n"
        "Input: s = \"AABABBA\", k = 1\n"
        "Output: 4\n\n"
        "**Constraints:**\n"
        "• 1 <= s.length <= 10^5\n"
        "• s consists of only uppercase English letters.\n"
        "• 0 <= k <= s.length"
    ),

    567: (
        "Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, "
        "or `false` otherwise.\n\n"
        "In other words, return `true` if one of `s1`'s permutations is the substring of `s2`.\n\n"
        "**Example 1:**\n"
        "Input: s1 = \"ab\", s2 = \"eidbaooo\"\n"
        "Output: true\n"
        "Explanation: s2 contains one permutation of s1 (\"ba\").\n\n"
        "**Example 2:**\n"
        "Input: s1 = \"ab\", s2 = \"eidboaoo\"\n"
        "Output: false\n\n"
        "**Constraints:**\n"
        "• 1 <= s1.length, s2.length <= 10^4\n"
        "• s1 and s2 consist of lowercase English letters."
    ),

    239: (
        "You are given an array of integers `nums` and an integer `k`. There is a sliding window "
        "of size `k` which is moving from the very left of the array to the very right. You can "
        "only see the `k` numbers in the window. Each time the sliding window moves right by one position.\n\n"
        "Return the max sliding window.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,3,-1,-3,5,3,6,7], k = 3\n"
        "Output: [3,3,5,5,6,7]\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 10^5\n"
        "• -10^4 <= nums[i] <= 10^4\n"
        "• 1 <= k <= nums.length"
    ),

    # ── Hash Maps & Sets ──
    49: (
        "Given an array of strings `strs`, group the anagrams together. You can return the "
        "answer in any order.\n\n"
        "An anagram is a word formed by rearranging the letters of a different word, using "
        "all the original letters exactly once.\n\n"
        "**Example 1:**\n"
        "Input: strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]\n"
        "Output: [[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]\n\n"
        "**Constraints:**\n"
        "• 1 <= strs.length <= 10^4\n"
        "• 0 <= strs[i].length <= 100\n"
        "• strs[i] consists of lowercase English letters."
    ),

    128: (
        "Given an unsorted array of integers `nums`, return the length of the longest "
        "consecutive elements sequence.\n\n"
        "You must write an algorithm that runs in O(n) time.\n\n"
        "**Example 1:**\n"
        "Input: nums = [100,4,200,1,3,2]\n"
        "Output: 4\n"
        "Explanation: The longest consecutive elements sequence is [1, 2, 3, 4], length 4.\n\n"
        "**Example 2:**\n"
        "Input: nums = [0,3,7,2,5,8,4,6,0,1]\n"
        "Output: 9\n\n"
        "**Constraints:**\n"
        "• 0 <= nums.length <= 10^5\n"
        "• -10^9 <= nums[i] <= 10^9"
    ),

    560: (
        "Given an array of integers `nums` and an integer `k`, return the total number of "
        "subarrays whose sum equals to `k`.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,1,1], k = 2\n"
        "Output: 2\n\n"
        "**Example 2:**\n"
        "Input: nums = [1,2,3], k = 3\n"
        "Output: 2\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 2 * 10^4\n"
        "• -1000 <= nums[i] <= 1000\n"
        "• -10^7 <= k <= 10^7"
    ),

    347: (
        "Given an integer array `nums` and an integer `k`, return the `k` most frequent "
        "elements. You may return the answer in any order.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,1,1,2,2,3], k = 2\n"
        "Output: [1,2]\n\n"
        "**Example 2:**\n"
        "Input: nums = [1], k = 1\n"
        "Output: [1]\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 10^5\n"
        "• -10^4 <= nums[i] <= 10^4\n"
        "• k is in the range [1, the number of unique elements in the array].\n\n"
        "**Follow up:** Your algorithm's time complexity must be better than O(n log n)."
    ),

    # ── Linked Lists ──
    206: (
        "Given the `head` of a singly linked list, reverse the list, and return the reversed list.\n\n"
        "**Example 1:**\n"
        "Input: head = [1,2,3,4,5]\n"
        "Output: [5,4,3,2,1]\n\n"
        "**Example 2:**\n"
        "Input: head = [1,2]\n"
        "Output: [2,1]\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the list is in the range [0, 5000].\n"
        "• -5000 <= Node.val <= 5000\n\n"
        "**Follow up:** A linked list can be reversed iteratively or recursively. "
        "Can you implement both?"
    ),

    141: (
        "Given `head`, the head of a linked list, determine if the linked list has a cycle in it.\n\n"
        "There is a cycle if there is some node in the list that can be reached again by continuously "
        "following the `next` pointer.\n\n"
        "Return `true` if there is a cycle, otherwise return `false`.\n\n"
        "**Example 1:**\n"
        "Input: head = [3,2,0,-4], pos = 1\n"
        "Output: true\n"
        "Explanation: There is a cycle where tail connects to the 1st node (0-indexed).\n\n"
        "**Constraints:**\n"
        "• The number of nodes is in the range [0, 10^4].\n"
        "• -10^5 <= Node.val <= 10^5\n\n"
        "**Follow up:** Can you solve it using O(1) memory?"
    ),

    21: (
        "You are given the heads of two sorted linked lists `list1` and `list2`.\n\n"
        "Merge the two lists into one sorted list. The list should be made by splicing together "
        "the nodes of the first two lists.\n\n"
        "Return the head of the merged linked list.\n\n"
        "**Example 1:**\n"
        "Input: list1 = [1,2,4], list2 = [1,3,4]\n"
        "Output: [1,1,2,3,4,4]\n\n"
        "**Constraints:**\n"
        "• The number of nodes in both lists is in the range [0, 50].\n"
        "• -100 <= Node.val <= 100\n"
        "• Both list1 and list2 are sorted in non-decreasing order."
    ),

    19: (
        "Given the `head` of a linked list, remove the nth node from the end of the list "
        "and return its head.\n\n"
        "**Example 1:**\n"
        "Input: head = [1,2,3,4,5], n = 2\n"
        "Output: [1,2,3,5]\n\n"
        "**Example 2:**\n"
        "Input: head = [1], n = 1\n"
        "Output: []\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the list is sz.\n"
        "• 1 <= sz <= 30\n"
        "• 0 <= Node.val <= 100\n"
        "• 1 <= n <= sz\n\n"
        "**Follow up:** Could you do this in one pass?"
    ),

    143: (
        "You are given the head of a singly linked-list: L0 → L1 → … → Ln-1 → Ln.\n\n"
        "Reorder the list to: L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …\n\n"
        "You may not modify the values in the list's nodes. Only nodes themselves may be changed.\n\n"
        "**Example 1:**\n"
        "Input: head = [1,2,3,4]\n"
        "Output: [1,4,2,3]\n\n"
        "**Example 2:**\n"
        "Input: head = [1,2,3,4,5]\n"
        "Output: [1,5,2,4,3]\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the list is in the range [1, 5 * 10^4].\n"
        "• 1 <= Node.val <= 1000"
    ),

    23: (
        "You are given an array of `k` linked-lists `lists`, each linked-list is sorted "
        "in ascending order.\n\n"
        "Merge all the linked-lists into one sorted linked-list and return it.\n\n"
        "**Example 1:**\n"
        "Input: lists = [[1,4,5],[1,3,4],[2,6]]\n"
        "Output: [1,1,2,3,4,4,5,6]\n\n"
        "**Constraints:**\n"
        "• k == lists.length\n"
        "• 0 <= k <= 10^4\n"
        "• 0 <= lists[i].length <= 500\n"
        "• -10^4 <= lists[i][j] <= 10^4\n"
        "• lists[i] is sorted in ascending order.\n"
        "• The sum of lists[i].length will not exceed 10^4."
    ),

    # ── Stacks ──
    20: (
        "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', "
        "determine if the input string is valid.\n\n"
        "An input string is valid if:\n"
        "• Open brackets must be closed by the same type of brackets.\n"
        "• Open brackets must be closed in the correct order.\n"
        "• Every close bracket has a corresponding open bracket of the same type.\n\n"
        "**Example 1:**\n"
        "Input: s = \"()\"\n"
        "Output: true\n\n"
        "**Example 2:**\n"
        "Input: s = \"()[]{}\"\n"
        "Output: true\n\n"
        "**Example 3:**\n"
        "Input: s = \"(]\"\n"
        "Output: false\n\n"
        "**Constraints:**\n"
        "• 1 <= s.length <= 10^4\n"
        "• s consists of parentheses only '()[]{}'."
    ),

    155: (
        "Design a stack that supports push, pop, top, and retrieving the minimum element "
        "in constant time.\n\n"
        "Implement the `MinStack` class:\n"
        "• `MinStack()` initializes the stack object.\n"
        "• `void push(int val)` pushes val onto the stack.\n"
        "• `void pop()` removes the element on the top of the stack.\n"
        "• `int top()` gets the top element of the stack.\n"
        "• `int getMin()` retrieves the minimum element in the stack.\n\n"
        "You must implement a solution with O(1) time complexity for each function.\n\n"
        "**Constraints:**\n"
        "• -2^31 <= val <= 2^31 - 1\n"
        "• Methods pop, top and getMin will always be called on non-empty stacks.\n"
        "• At most 3 * 10^4 calls will be made to push, pop, top, and getMin."
    ),

    150: (
        "You are given an array of strings `tokens` that represents an arithmetic expression "
        "in Reverse Polish Notation.\n\n"
        "Evaluate the expression. Return an integer that represents the value of the expression.\n\n"
        "**Example 1:**\n"
        "Input: tokens = [\"2\",\"1\",\"+\",\"3\",\"*\"]\n"
        "Output: 9\n"
        "Explanation: ((2 + 1) * 3) = 9\n\n"
        "**Constraints:**\n"
        "• 1 <= tokens.length <= 10^4\n"
        "• tokens[i] is either an operator or an integer in the range [-200, 200]."
    ),

    739: (
        "Given an array of integers `temperatures`, return an array `answer` such that "
        "`answer[i]` is the number of days you have to wait after the ith day to get a warmer "
        "temperature. If there is no future day for which this is possible, keep `answer[i] == 0`.\n\n"
        "**Example 1:**\n"
        "Input: temperatures = [73,74,75,71,69,72,76,73]\n"
        "Output: [1,1,4,2,1,1,0,0]\n\n"
        "**Example 2:**\n"
        "Input: temperatures = [30,60,90]\n"
        "Output: [1,1,0]\n\n"
        "**Constraints:**\n"
        "• 1 <= temperatures.length <= 10^5\n"
        "• 30 <= temperatures[i] <= 100"
    ),

    84: (
        "Given an array of integers `heights` representing the histogram's bar height where "
        "the width of each bar is 1, return the area of the largest rectangle in the histogram.\n\n"
        "**Example 1:**\n"
        "Input: heights = [2,1,5,6,2,3]\n"
        "Output: 10\n"
        "Explanation: The largest rectangle has an area of 10 units (5 and 6 tall, 2 wide).\n\n"
        "**Constraints:**\n"
        "• 1 <= heights.length <= 10^5\n"
        "• 0 <= heights[i] <= 10^4"
    ),

    # ── Binary Search ──
    704: (
        "Given an array of integers `nums` which is sorted in ascending order, and an integer "
        "`target`, write a function to search `target` in `nums`. If `target` exists, return its "
        "index. Otherwise, return -1.\n\n"
        "You must write an algorithm with O(log n) runtime complexity.\n\n"
        "**Example 1:**\n"
        "Input: nums = [-1,0,3,5,9,12], target = 9\n"
        "Output: 4\n"
        "Explanation: 9 exists in nums and its index is 4.\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 10^4\n"
        "• -10^4 < nums[i], target < 10^4\n"
        "• All the integers in nums are unique.\n"
        "• nums is sorted in ascending order."
    ),

    33: (
        "There is an integer array `nums` sorted in ascending order (with distinct values). "
        "Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot "
        "index `k`.\n\n"
        "Given the array `nums` after the possible rotation and an integer `target`, return the "
        "index of `target` if it is in `nums`, or -1 if it is not.\n\n"
        "You must write an algorithm with O(log n) runtime complexity.\n\n"
        "**Example 1:**\n"
        "Input: nums = [4,5,6,7,0,1,2], target = 0\n"
        "Output: 4\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 5000\n"
        "• -10^4 <= nums[i] <= 10^4\n"
        "• All values of nums are unique.\n"
        "• nums is an ascending array that is possibly rotated."
    ),

    153: (
        "Suppose an array of length `n` sorted in ascending order is rotated between 1 and `n` times. "
        "Given the sorted rotated array `nums` of unique elements, return the minimum element.\n\n"
        "You must write an algorithm that runs in O(log n) time.\n\n"
        "**Example 1:**\n"
        "Input: nums = [3,4,5,1,2]\n"
        "Output: 1\n"
        "Explanation: The original array was [1,2,3,4,5] rotated 3 times.\n\n"
        "**Constraints:**\n"
        "• n == nums.length\n"
        "• 1 <= n <= 5000\n"
        "• -5000 <= nums[i] <= 5000\n"
        "• All the integers of nums are unique."
    ),

    4: (
        "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return "
        "the median of the two sorted arrays.\n\n"
        "The overall run time complexity should be O(log (m+n)).\n\n"
        "**Example 1:**\n"
        "Input: nums1 = [1,3], nums2 = [2]\n"
        "Output: 2.00000\n"
        "Explanation: merged array = [1,2,3] and median is 2.\n\n"
        "**Example 2:**\n"
        "Input: nums1 = [1,2], nums2 = [3,4]\n"
        "Output: 2.50000\n"
        "Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.\n\n"
        "**Constraints:**\n"
        "• nums1.length == m, nums2.length == n\n"
        "• 0 <= m <= 1000, 0 <= n <= 1000\n"
        "• 1 <= m + n <= 2000\n"
        "• -10^6 <= nums1[i], nums2[i] <= 10^6"
    ),

    # ── Trees ──
    226: (
        "Given the `root` of a binary tree, invert the tree, and return its root.\n\n"
        "**Example 1:**\n"
        "Input: root = [4,2,7,1,3,6,9]\n"
        "Output: [4,7,2,9,6,3,1]\n\n"
        "**Example 2:**\n"
        "Input: root = [2,1,3]\n"
        "Output: [2,3,1]\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the tree is in the range [0, 100].\n"
        "• -100 <= Node.val <= 100"
    ),

    104: (
        "Given the `root` of a binary tree, return its maximum depth.\n\n"
        "A binary tree's maximum depth is the number of nodes along the longest path from "
        "the root node down to the farthest leaf node.\n\n"
        "**Example 1:**\n"
        "Input: root = [3,9,20,null,null,15,7]\n"
        "Output: 3\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the tree is in the range [0, 10^4].\n"
        "• -100 <= Node.val <= 100"
    ),

    100: (
        "Given the roots of two binary trees `p` and `q`, write a function to check if they "
        "are the same or not.\n\n"
        "Two binary trees are considered the same if they are structurally identical, and the "
        "nodes have the same value.\n\n"
        "**Example 1:**\n"
        "Input: p = [1,2,3], q = [1,2,3]\n"
        "Output: true\n\n"
        "**Constraints:**\n"
        "• The number of nodes in both trees is in the range [0, 100].\n"
        "• -10^4 <= Node.val <= 10^4"
    ),

    102: (
        "Given the `root` of a binary tree, return the level order traversal of its nodes' "
        "values. (i.e., from left to right, level by level).\n\n"
        "**Example 1:**\n"
        "Input: root = [3,9,20,null,null,15,7]\n"
        "Output: [[3],[9,20],[15,7]]\n\n"
        "**Example 2:**\n"
        "Input: root = [1]\n"
        "Output: [[1]]\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the tree is in the range [0, 2000].\n"
        "• -1000 <= Node.val <= 1000"
    ),

    230: (
        "Given the `root` of a binary search tree and an integer `k`, return the kth smallest "
        "value (1-indexed) of all the values of the nodes in the tree.\n\n"
        "**Example 1:**\n"
        "Input: root = [3,1,4,null,2], k = 1\n"
        "Output: 1\n\n"
        "**Example 2:**\n"
        "Input: root = [5,3,6,2,4,null,null,1], k = 3\n"
        "Output: 3\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the tree is n.\n"
        "• 1 <= k <= n <= 10^4\n"
        "• 0 <= Node.val <= 10^4"
    ),

    98: (
        "Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).\n\n"
        "A valid BST is defined as follows:\n"
        "• The left subtree of a node contains only nodes with keys less than the node's key.\n"
        "• The right subtree of a node contains only nodes with keys greater than the node's key.\n"
        "• Both the left and right subtrees must also be binary search trees.\n\n"
        "**Example 1:**\n"
        "Input: root = [2,1,3]\n"
        "Output: true\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the tree is in the range [1, 10^4].\n"
        "• -2^31 <= Node.val <= 2^31 - 1"
    ),

    105: (
        "Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder "
        "traversal of a binary tree and `inorder` is the inorder traversal of the same tree, "
        "construct and return the binary tree.\n\n"
        "**Example 1:**\n"
        "Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]\n"
        "Output: [3,9,20,null,null,15,7]\n\n"
        "**Constraints:**\n"
        "• 1 <= preorder.length <= 3000\n"
        "• inorder.length == preorder.length\n"
        "• -3000 <= preorder[i], inorder[i] <= 3000\n"
        "• preorder and inorder consist of unique values."
    ),

    124: (
        "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has "
        "an edge connecting them. A node can only appear in the sequence at most once. The path "
        "does not need to pass through the root.\n\n"
        "The path sum of a path is the sum of the node's values in the path.\n\n"
        "Given the `root` of a binary tree, return the maximum path sum of any non-empty path.\n\n"
        "**Example 1:**\n"
        "Input: root = [1,2,3]\n"
        "Output: 6\n"
        "Explanation: The optimal path is 2 -> 1 -> 3 with sum 2 + 1 + 3 = 6.\n\n"
        "**Constraints:**\n"
        "• The number of nodes in the tree is in the range [1, 3 * 10^4].\n"
        "• -1000 <= Node.val <= 1000"
    ),

    297: (
        "Design an algorithm to serialize and deserialize a binary tree. Serialization is the "
        "process of converting a data structure into a sequence of bits so that it can be stored "
        "or transmitted. Deserialization is the reverse process.\n\n"
        "Implement the `Codec` class:\n"
        "• `serialize(root)` Encodes a tree to a single string.\n"
        "• `deserialize(data)` Decodes your encoded data to tree.\n\n"
        "**Example 1:**\n"
        "Input: root = [1,2,3,null,null,4,5]\n"
        "Output: [1,2,3,null,null,4,5]\n\n"
        "**Constraints:**\n"
        "• The number of nodes is in the range [0, 10^4].\n"
        "• -1000 <= Node.val <= 1000"
    ),

    # ── Heaps ──
    215: (
        "Given an integer array `nums` and an integer `k`, return the kth largest element "
        "in the array.\n\n"
        "Note that it is the kth largest element in the sorted order, not the kth distinct element.\n\n"
        "Can you solve it without sorting?\n\n"
        "**Example 1:**\n"
        "Input: nums = [3,2,1,5,6,4], k = 2\n"
        "Output: 5\n\n"
        "**Example 2:**\n"
        "Input: nums = [3,2,3,1,2,4,5,5,6], k = 4\n"
        "Output: 4\n\n"
        "**Constraints:**\n"
        "• 1 <= k <= nums.length <= 10^5\n"
        "• -10^4 <= nums[i] <= 10^4"
    ),

    295: (
        "The median is the middle value in an ordered integer list. If the size of the list "
        "is even, the median is the mean of the two middle values.\n\n"
        "Implement the `MedianFinder` class:\n"
        "• `MedianFinder()` initializes the MedianFinder object.\n"
        "• `void addNum(int num)` adds the integer num to the data structure.\n"
        "• `double findMedian()` returns the median of all elements so far.\n\n"
        "**Example 1:**\n"
        "Input: [\"MedianFinder\",\"addNum\",\"addNum\",\"findMedian\",\"addNum\",\"findMedian\"]\n"
        "[[],[1],[2],[],[3],[]]\n"
        "Output: [null,null,null,1.5,null,2.0]\n\n"
        "**Constraints:**\n"
        "• -10^5 <= num <= 10^5\n"
        "• At most 5 * 10^4 calls will be made to addNum and findMedian."
    ),

    # ── Graphs ──
    200: (
        "Given an m x n 2D binary grid `grid` which represents a map of '1's (land) and '0's "
        "(water), return the number of islands.\n\n"
        "An island is surrounded by water and is formed by connecting adjacent lands "
        "horizontally or vertically.\n\n"
        "**Example 1:**\n"
        "Input: grid = [\n"
        "  [\"1\",\"1\",\"1\",\"1\",\"0\"],\n"
        "  [\"1\",\"1\",\"0\",\"1\",\"0\"],\n"
        "  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n"
        "  [\"0\",\"0\",\"0\",\"0\",\"0\"]\n"
        "]\n"
        "Output: 1\n\n"
        "**Constraints:**\n"
        "• m == grid.length, n == grid[i].length\n"
        "• 1 <= m, n <= 300\n"
        "• grid[i][j] is '0' or '1'."
    ),

    133: (
        "Given a reference of a node in a connected undirected graph, return a deep copy (clone) "
        "of the graph. Each node contains a value and a list of its neighbors.\n\n"
        "**Example 1:**\n"
        "Input: adjList = [[2,4],[1,3],[2,4],[1,3]]\n"
        "Output: [[2,4],[1,3],[2,4],[1,3]]\n\n"
        "**Constraints:**\n"
        "• The number of nodes is in the range [0, 100].\n"
        "• 1 <= Node.val <= 100\n"
        "• Node.val is unique for each node.\n"
        "• There are no repeated edges and no self-loops."
    ),

    207: (
        "There are a total of `numCourses` courses you have to take, labeled from 0 to "
        "`numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = "
        "[ai, bi]` indicates that you must take course bi first if you want to take course ai.\n\n"
        "Return `true` if you can finish all courses. Otherwise, return `false`.\n\n"
        "**Example 1:**\n"
        "Input: numCourses = 2, prerequisites = [[1,0]]\n"
        "Output: true\n"
        "Explanation: You take course 0 then course 1.\n\n"
        "**Example 2:**\n"
        "Input: numCourses = 2, prerequisites = [[1,0],[0,1]]\n"
        "Output: false\n"
        "Explanation: There is a cycle.\n\n"
        "**Constraints:**\n"
        "• 1 <= numCourses <= 2000\n"
        "• 0 <= prerequisites.length <= 5000"
    ),

    # ── Dynamic Programming ──
    70: (
        "You are climbing a staircase. It takes `n` steps to reach the top.\n\n"
        "Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb "
        "to the top?\n\n"
        "**Example 1:**\n"
        "Input: n = 2\n"
        "Output: 2\n"
        "Explanation: (1+1) and (2).\n\n"
        "**Example 2:**\n"
        "Input: n = 3\n"
        "Output: 3\n"
        "Explanation: (1+1+1), (1+2), and (2+1).\n\n"
        "**Constraints:**\n"
        "• 1 <= n <= 45"
    ),

    198: (
        "You are a professional robber planning to rob houses along a street. Each house has "
        "a certain amount of money stashed, but adjacent houses have security systems connected — "
        "if two adjacent houses are broken into on the same night, the police will be alerted.\n\n"
        "Given an integer array `nums` representing the amount of money of each house, return "
        "the maximum amount of money you can rob tonight without alerting the police.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,2,3,1]\n"
        "Output: 4\n"
        "Explanation: Rob house 1 (money=1) then house 3 (money=3). Total = 1 + 3 = 4.\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 100\n"
        "• 0 <= nums[i] <= 400"
    ),

    322: (
        "You are given an integer array `coins` representing coins of different denominations "
        "and an integer `amount` representing a total amount of money.\n\n"
        "Return the fewest number of coins needed to make up that amount. If that amount of "
        "money cannot be made up, return -1.\n\n"
        "You may assume you have an infinite number of each kind of coin.\n\n"
        "**Example 1:**\n"
        "Input: coins = [1,2,5], amount = 11\n"
        "Output: 3\n"
        "Explanation: 11 = 5 + 5 + 1\n\n"
        "**Example 2:**\n"
        "Input: coins = [2], amount = 3\n"
        "Output: -1\n\n"
        "**Constraints:**\n"
        "• 1 <= coins.length <= 12\n"
        "• 1 <= coins[i] <= 2^31 - 1\n"
        "• 0 <= amount <= 10^4"
    ),

    300: (
        "Given an integer array `nums`, return the length of the longest strictly increasing "
        "subsequence.\n\n"
        "**Example 1:**\n"
        "Input: nums = [10,9,2,5,3,7,101,18]\n"
        "Output: 4\n"
        "Explanation: The longest increasing subsequence is [2,3,7,101], length 4.\n\n"
        "**Example 2:**\n"
        "Input: nums = [0,1,0,3,2,3]\n"
        "Output: 4\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 2500\n"
        "• -10^4 <= nums[i] <= 10^4\n\n"
        "**Follow up:** Can you come up with an algorithm that runs in O(n log(n)) time?"
    ),

    # ── DP Grid ──
    62: (
        "There is a robot on an m x n grid. The robot is initially in the top-left corner "
        "(grid[0][0]). The robot tries to move to the bottom-right corner (grid[m-1][n-1]). "
        "The robot can only move either down or right at any point in time.\n\n"
        "Given the two integers `m` and `n`, return the number of possible unique paths that "
        "the robot can take to reach the bottom-right corner.\n\n"
        "**Example 1:**\n"
        "Input: m = 3, n = 7\n"
        "Output: 28\n\n"
        "**Constraints:**\n"
        "• 1 <= m, n <= 100"
    ),

    1143: (
        "Given two strings `text1` and `text2`, return the length of their longest common "
        "subsequence. If there is no common subsequence, return 0.\n\n"
        "A subsequence of a string is a new string generated from the original string with some "
        "characters (can be none) deleted without changing the relative order of the remaining "
        "characters.\n\n"
        "**Example 1:**\n"
        "Input: text1 = \"abcde\", text2 = \"ace\"\n"
        "Output: 3\n"
        "Explanation: The longest common subsequence is \"ace\".\n\n"
        "**Constraints:**\n"
        "• 1 <= text1.length, text2.length <= 1000\n"
        "• text1 and text2 consist of only lowercase English characters."
    ),

    # ── Backtracking ──
    78: (
        "Given an integer array `nums` of unique elements, return all possible subsets (the "
        "power set).\n\n"
        "The solution set must not contain duplicate subsets. Return the solution in any order.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,2,3]\n"
        "Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 10\n"
        "• -10 <= nums[i] <= 10\n"
        "• All the numbers of nums are unique."
    ),

    46: (
        "Given an array `nums` of distinct integers, return all the possible permutations. "
        "You can return the answer in any order.\n\n"
        "**Example 1:**\n"
        "Input: nums = [1,2,3]\n"
        "Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 6\n"
        "• -10 <= nums[i] <= 10\n"
        "• All the integers of nums are unique."
    ),

    39: (
        "Given an array of distinct integers `candidates` and a target integer `target`, return "
        "a list of all unique combinations of candidates where the chosen numbers sum to target. "
        "The same number may be chosen an unlimited number of times.\n\n"
        "**Example 1:**\n"
        "Input: candidates = [2,3,6,7], target = 7\n"
        "Output: [[2,2,3],[7]]\n\n"
        "**Constraints:**\n"
        "• 1 <= candidates.length <= 30\n"
        "• 2 <= candidates[i] <= 40\n"
        "• All elements of candidates are distinct.\n"
        "• 1 <= target <= 40"
    ),

    79: (
        "Given an m x n grid of characters `board` and a string `word`, return `true` if `word` "
        "exists in the grid.\n\n"
        "The word can be constructed from letters of sequentially adjacent cells, where adjacent "
        "cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.\n\n"
        "**Example 1:**\n"
        "Input: board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"ABCCED\"\n"
        "Output: true\n\n"
        "**Constraints:**\n"
        "• m == board.length, n == board[i].length\n"
        "• 1 <= m, n <= 6\n"
        "• 1 <= word.length <= 15"
    ),

    51: (
        "The n-queens puzzle is the problem of placing `n` queens on an n x n chessboard such "
        "that no two queens attack each other.\n\n"
        "Given an integer `n`, return all distinct solutions to the n-queens puzzle.\n\n"
        "Each solution contains a distinct board configuration where 'Q' and '.' indicate a queen "
        "and an empty space respectively.\n\n"
        "**Example 1:**\n"
        "Input: n = 4\n"
        "Output: [[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"],[\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]]\n\n"
        "**Constraints:**\n"
        "• 1 <= n <= 9"
    ),

    # ── Greedy ──
    55: (
        "You are given an integer array `nums`. You are initially positioned at the array's "
        "first index, and each element represents your maximum jump length at that position.\n\n"
        "Return `true` if you can reach the last index, or `false` otherwise.\n\n"
        "**Example 1:**\n"
        "Input: nums = [2,3,1,1,4]\n"
        "Output: true\n"
        "Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.\n\n"
        "**Example 2:**\n"
        "Input: nums = [3,2,1,0,4]\n"
        "Output: false\n\n"
        "**Constraints:**\n"
        "• 1 <= nums.length <= 10^4\n"
        "• 0 <= nums[i] <= 10^5"
    ),

    # ── Tries ──
    208: (
        "A trie (pronounced as \"try\") or prefix tree is a tree data structure used to "
        "efficiently store and retrieve keys in a dataset of strings.\n\n"
        "Implement the Trie class:\n"
        "• `Trie()` Initializes the trie object.\n"
        "• `void insert(String word)` Inserts the string word into the trie.\n"
        "• `boolean search(String word)` Returns true if word is in the trie.\n"
        "• `boolean startsWith(String prefix)` Returns true if there is a previously inserted "
        "string that has the prefix prefix.\n\n"
        "**Example 1:**\n"
        "Input: [\"Trie\",\"insert\",\"search\",\"search\",\"startsWith\",\"insert\",\"search\"]\n"
        "[[],[\"apple\"],[\"apple\"],[\"app\"],[\"app\"],[\"app\"],[\"app\"]]\n"
        "Output: [null,null,true,false,true,null,true]\n\n"
        "**Constraints:**\n"
        "• 1 <= word.length, prefix.length <= 2000\n"
        "• word and prefix consist only of lowercase English letters."
    ),

    # ── Union Find ──
    261: (
        "You have a graph of `n` nodes labeled from 0 to n-1. You are given an integer n and a "
        "list of `edges` where edges[i] = [ai, bi] indicates that there is an undirected edge "
        "between nodes ai and bi.\n\n"
        "Return `true` if the edges of the given graph make up a valid tree, and `false` otherwise.\n\n"
        "A valid tree has exactly n-1 edges and is fully connected with no cycles.\n\n"
        "**Example 1:**\n"
        "Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]\n"
        "Output: true\n\n"
        "**Constraints:**\n"
        "• 1 <= n <= 2000\n"
        "• 0 <= edges.length <= 5000\n"
        "• edges[i].length == 2"
    ),
}
