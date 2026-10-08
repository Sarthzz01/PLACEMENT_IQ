import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def test_fetch_external_stats():
    print("1. Testing POST /api/student/fetch-external-stats...")
    payload = {
        "github_url": "https://github.com/torvalds",
        "leetcode_url": "https://leetcode.com/u/neal_wu/"
    }
    req = urllib.request.Request(
        f"{BASE_URL}/api/student/fetch-external-stats",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as res:
        data = json.loads(res.read().decode("utf-8"))
        assert data.get("success") is True, f"Fetch failed: {data}"
        assert data.get("github", {}).get("public_repos") >= 1, "Missing GitHub repos"
        assert data.get("leetcode", {}).get("total_solved") >= 1, "Missing LeetCode solved"
        print(f"   -> Success! GitHub repos: {data['github']['public_repos']}, LeetCode solved: {data['leetcode']['total_solved']}")
        return data

def test_profile_save_and_retrieve(fetch_res):
    print("2. Testing POST /api/student/profile with fetched metrics & URLs...")
    test_email = "aarav.sharma@college.edu"
    profile_data = {
        "name": "Aarav Sharma",
        "email": test_email,
        "age": 21,
        "branch": "CSE",
        "cgpa": 8.7,
        "github_url": "https://github.com/torvalds",
        "leetcode_url": "https://leetcode.com/u/neal_wu/",
        "portfolio_url": "https://aarav-portfolio.dev",
        "github_repos": fetch_res["extracted_values"]["github_repos"],
        "github_repos_count": fetch_res["extracted_values"]["github_repos_count"],
        "leetcode_questions_solved": fetch_res["extracted_values"]["leetcode_questions_solved"],
        "leetcode_problems_solved": fetch_res["extracted_values"]["leetcode_problems_solved"],
        "dsa_questions_solved": fetch_res["extracted_values"]["dsa_questions_solved"],
        "coding_skill_score": fetch_res["extracted_values"]["coding_skill_score"]
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/api/student/profile",
        data=json.dumps({"email": test_email, "data": profile_data}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as res:
        save_resp = json.loads(res.read().decode("utf-8"))
        assert save_resp.get("status") == "success", f"Save failed: {save_resp}"
        print(f"   -> Saved successfully: {save_resp}")

    print("3. Testing GET /api/student/profile/{email} to verify persistence...")
    req_get = urllib.request.Request(f"{BASE_URL}/api/student/profile/{test_email}")
    with urllib.request.urlopen(req_get, timeout=10) as res:
        get_resp = json.loads(res.read().decode("utf-8"))
        p = get_resp.get("profile", {})
        assert p.get("github_url") == "https://github.com/torvalds", f"GitHub URL mismatch: {p.get('github_url')}"
        assert p.get("leetcode_url") == "https://leetcode.com/u/neal_wu/", f"LeetCode URL mismatch: {p.get('leetcode_url')}"
        assert p.get("github_repos") == fetch_res["extracted_values"]["github_repos"], "Repo count mismatch"
        assert p.get("leetcode_questions_solved") == fetch_res["extracted_values"]["leetcode_questions_solved"], "LeetCode count mismatch"
        print("   -> Retrieved profile verified:")
        print(f"      - LeetCode URL: {p.get('leetcode_url')}")
        print(f"      - LeetCode Solved: {p.get('leetcode_questions_solved')}")
        print(f"      - GitHub URL: {p.get('github_url')}")
        print(f"      - GitHub Repos: {p.get('github_repos')}")

def test_admin_student_directory():
    print("4. Testing GET /api/admin/students to check admin visibility...")
    req = urllib.request.Request(f"{BASE_URL}/api/admin/students")
    with urllib.request.urlopen(req, timeout=10) as res:
        data = json.loads(res.read().decode("utf-8"))
        students = data.get("students", [])
        aarav = next((s for s in students if s.get("email") == "aarav.sharma@college.edu"), None)
        assert aarav is not None, "Aarav not found in students directory"
        assert aarav.get("leetcode_url") == "https://leetcode.com/u/neal_wu/", "Aarav missing leetcode_url in directory"
        print(f"   -> Admin directory verified candidate: {aarav.get('name')} | LC: {aarav.get('leetcode_url')} | GH: {aarav.get('github_url')}")

if __name__ == "__main__":
    fetch_res = test_fetch_external_stats()
    test_profile_save_and_retrieve(fetch_res)
    test_admin_student_directory()
    print("\nALL LIVE STATS & LINK INTEGRATION TESTS PASSED PERFECTLY!")
