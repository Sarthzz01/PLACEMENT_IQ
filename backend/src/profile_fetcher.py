"""
PlacementIQ - External Profile Fetcher Module
Extracts competitive programming and developer metrics from user profile links
(LeetCode, GitHub, HackerRank, etc.) to automatically populate student profile records.
"""

import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

def extract_leetcode_username(val: str) -> str:
    """Extract username from LeetCode URL or handle."""
    if not val:
        return ""
    val = val.strip().rstrip('/')
    # Patterns:
    # https://leetcode.com/u/neal_wu/
    # https://leetcode.com/neal_wu/
    # leetcode.com/u/neal_wu
    m = re.search(r'leetcode\.com/(?:u/)?([a-zA-Z0-9_\-]+)', val, re.IGNORECASE)
    if m:
        return m.group(1)
    cleaned = re.sub(r'^https?://', '', val).strip('/')
    if '/' not in cleaned:
        return cleaned
    return cleaned.split('/')[-1]

def extract_github_username(val: str) -> str:
    """Extract username from GitHub URL or handle."""
    if not val:
        return ""
    val = val.strip().rstrip('/')
    # Pattern: https://github.com/torvalds/
    m = re.search(r'github\.com/([a-zA-Z0-9_\-]+)', val, re.IGNORECASE)
    if m:
        return m.group(1)
    cleaned = re.sub(r'^https?://', '', val).strip('/')
    if '/' not in cleaned:
        return cleaned
    return cleaned.split('/')[-1]

def extract_hackerrank_username(val: str) -> str:
    """Extract username from HackerRank URL or handle."""
    if not val:
        return ""
    val = val.strip().rstrip('/')
    m = re.search(r'hackerrank\.com/(?:profile/)?([a-zA-Z0-9_\-]+)', val, re.IGNORECASE)
    if m:
        return m.group(1)
    cleaned = re.sub(r'^https?://', '', val).strip('/')
    if '/' not in cleaned:
        return cleaned
    return cleaned.split('/')[-1]

def fetch_leetcode_stats(url_or_username: str) -> Optional[Dict[str, Any]]:
    """Fetch live LeetCode stats via GraphQL endpoint with fallback."""
    username = extract_leetcode_username(url_or_username)
    if not username:
        return None

    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            profile {
                realName
                ranking
                reputation
            }
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Primary attempt: LeetCode official GraphQL API
    try:
        req = urllib.request.Request(
            'https://leetcode.com/graphql',
            data=json.dumps({'query': query, 'variables': {'username': username}}).encode('utf-8'),
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=7) as res:
            resp_data = json.loads(res.read().decode('utf-8'))
            matched = resp_data.get("data", {}).get("matchedUser")
            if matched:
                stats = matched.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
                total = 0
                easy, med, hard = 0, 0, 0
                for item in stats:
                    d = item.get("difficulty")
                    cnt = item.get("count", 0)
                    if d == "All":
                        total = cnt
                    elif d == "Easy":
                        easy = cnt
                    elif d == "Medium":
                        med = cnt
                    elif d == "Hard":
                        hard = cnt
                return {
                    "username": username,
                    "total_solved": total,
                    "easy_solved": easy,
                    "medium_solved": med,
                    "hard_solved": hard,
                    "ranking": matched.get("profile", {}).get("ranking"),
                    "source": "LeetCode GraphQL",
                    "success": True
                }
    except Exception as e:
        pass

    # Secondary attempt: Public LeetCode proxy API
    try:
        req = urllib.request.Request(
            f'https://leetcode-stats-api.herokuapp.com/{username}',
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=7) as res:
            data = json.loads(res.read().decode('utf-8'))
            if data.get("status") == "success":
                return {
                    "username": username,
                    "total_solved": int(data.get("totalSolved", 0)),
                    "easy_solved": int(data.get("easySolved", 0)),
                    "medium_solved": int(data.get("mediumSolved", 0)),
                    "hard_solved": int(data.get("hardSolved", 0)),
                    "ranking": data.get("ranking"),
                    "source": "LeetCode Stats Proxy",
                    "success": True
                }
    except Exception:
        pass

    return None

def fetch_github_stats(url_or_username: str) -> Optional[Dict[str, Any]]:
    """Fetch live GitHub metrics via public REST API."""
    username = extract_github_username(url_or_username)
    if not username:
        return None

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) PlacementIQ-Academic-System'
    }

    try:
        req = urllib.request.Request(
            f'https://api.github.com/users/{username}',
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=7) as res:
            data = json.loads(res.read().decode('utf-8'))
            return {
                "username": username,
                "name": data.get("name") or username,
                "public_repos": int(data.get("public_repos", 0)),
                "followers": int(data.get("followers", 0)),
                "public_gists": int(data.get("public_gists", 0)),
                "avatar_url": data.get("avatar_url", ""),
                "bio": data.get("bio", ""),
                "source": "GitHub REST API",
                "success": True
            }
    except Exception as e:
        return None

def fetch_external_profile_stats(
    github_url: str = "",
    leetcode_url: str = "",
    hackerrank_url: str = ""
) -> Dict[str, Any]:
    """
    Coordinates multi-platform profile fetching and packages updates
    for student profile synchronization.
    """
    res = {
        "success": False,
        "github": None,
        "leetcode": None,
        "extracted_values": {},
        "messages": []
    }

    if github_url and github_url.strip():
        gh_data = fetch_github_stats(github_url)
        if gh_data and gh_data.get("success"):
            res["github"] = gh_data
            repos = gh_data["public_repos"]
            res["extracted_values"]["github_repos"] = repos
            res["extracted_values"]["github_repos_count"] = repos
            res["messages"].append(f"GitHub: Verified @{gh_data['username']} ({repos} public repositories)")
        else:
            res["messages"].append(f"GitHub: Could not verify account for '{github_url}'")

    if leetcode_url and leetcode_url.strip():
        lc_data = fetch_leetcode_stats(leetcode_url)
        if lc_data and lc_data.get("success"):
            res["leetcode"] = lc_data
            solved = lc_data["total_solved"]
            res["extracted_values"]["leetcode_questions_solved"] = solved
            res["extracted_values"]["leetcode_problems_solved"] = solved
            # Also calculate DSA problems solved boost if appropriate
            res["extracted_values"]["dsa_questions_solved"] = solved
            res["extracted_values"]["dsa_problems_solved"] = solved
            
            # Coding skill score estimation based on LeetCode questions solved
            # 0-50 -> 40-60, 50-150 -> 60-80, 150-300+ -> 80-98
            est_coding_score = min(98, round(50 + (solved * 0.15) + (lc_data['hard_solved'] * 1.5)))
            res["extracted_values"]["coding_skill_score"] = max(55, est_coding_score)
            
            res["messages"].append(
                f"LeetCode: Verified @{lc_data['username']} ({solved} problems solved: "
                f"{lc_data['easy_solved']} Easy, {lc_data['medium_solved']} Med, {lc_data['hard_solved']} Hard)"
            )
        else:
            res["messages"].append(f"LeetCode: Could not verify account for '{leetcode_url}'")

    if res["github"] or res["leetcode"]:
        res["success"] = True

    return res
