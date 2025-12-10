import json
from typing import Dict, Any, Optional

import requests

CF_USER_INFO = "https://codeforces.com/api/user.info"
CF_USER_RATING = "https://codeforces.com/api/user.rating"
CF_USER_STATUS = "https://codeforces.com/api/user.status"


def fetch_codeforces_profile(handle: str, max_submission_sample: int = 1000) -> Dict[str, Any]:
    """
    Fetch minimal, normalized Codeforces profile info for a handle.
    Returns a dict with keys we support for snapshots.
    """
    result: Dict[str, Any] = {"platform": "codeforces", "handle": handle}

    # 1) user.info -> basic rating & maxRating
    r_info = requests.get(CF_USER_INFO, params={"handles": handle}, timeout=10)
    if r_info.ok:
        info_json = r_info.json()
        if info_json.get("status") == "OK":
            user = info_json["result"][0]
            result["rating"] = user.get("rating")
            result["max_rating"] = user.get("maxRating") or user.get("max_rating")
            result["handle"] = user.get("handle")
        else:
            result["error"] = info_json.get("comment", "Failed to fetch user.info")
    else:
        result["error"] = f"HTTP {r_info.status_code} from user.info"

    # 2) user.rating -> list of rating changes (for contests_played)
    r_rating = requests.get(CF_USER_RATING, params={"handle": handle}, timeout=10)
    if r_rating.ok:
        rating_json = r_rating.json()
        if rating_json.get("status") == "OK":
            ratings = rating_json.get("result", [])
            result["contests_played"] = len(ratings)
            # optionally extract latest rating if missing
            if ratings:
                last = ratings[-1]
                # last is dict with 'newRating'
                result.setdefault("rating", last.get("newRating"))
                # compute max_rating from ratings if missing
                max_r = max((entry.get("newRating", 0) for entry in ratings), default=None)
                if max_r:
                    result["max_rating"] = result.get("max_rating") or max_r
        else:
            # keep silent; contest info optional
            pass

    # 3) user.status (submissions) -> optional: approximate unique solved problems
    # This can be heavy; we'll fetch up to a sample limit. Count unique problem ids with verdict == 'OK'
    try:
        r_status = requests.get(CF_USER_STATUS, params={"handle": handle}, timeout=10)
        if r_status.ok:
            status_json = r_status.json()
            if status_json.get("status") == "OK":
                submissions = status_json.get("result", [])
                solved_set = set()
                for s in submissions:
                    if s.get("verdict") == "OK":
                        problem = s.get("problem", {})
                        contestId = problem.get("contestId")
                        index = problem.get("index")
                        if contestId and index:
                            solved_set.add(f"{contestId}-{index}")
                        else:
                            # fallback: name
                            solved_set.add(problem.get("name"))
                result["total_solved"] = len(solved_set)
            else:
                # skip counting if API returns non-OK
                pass
    except Exception:
        # avoid failing the whole call for submissions issues
        pass

    result["raw_data"] = json.dumps(result)  # we keep normalized dict as raw_data for debugging
    return result
