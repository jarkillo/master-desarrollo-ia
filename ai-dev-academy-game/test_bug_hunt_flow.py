"""Test Bug Hunt complete flow end-to-end."""
import sys

import requests


def test_bug_hunt_flow():
    """Test complete Bug Hunt game flow."""
    base_url = "http://localhost:8000/api/minigames/bug-hunt"

    print("=" * 60)
    print("BUG HUNT END-TO-END TEST")
    print("=" * 60)
    print()

    # Test 1: Start game
    print("TEST 1: Start Bug Hunt game")
    print("-" * 40)
    try:
        response = requests.post(
            f"{base_url}/start",
            json={"player_id": 1, "difficulty": "easy"},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        print(f"[OK] Status: {response.status_code}")
        print(f"[OK] Session ID: {data['session_id']}")
        print(f"[OK] Title: {data['title']}")
        print(f"[OK] Template: {data['template_id']}")
        print(f"[OK] Bugs to find: {data['bugs_count']}")
        print(f"[OK] Max XP: {data['max_xp']}")
        print(f"[OK] Difficulty: {data['difficulty']}")
        print()

        session_id = data['session_id']
        template_id = data['template_id']

    except Exception as e:
        print(f"[FAIL] {e}")
        return False

    # Test 2: Submit game
    print("TEST 2: Submit answers")
    print("-" * 40)
    try:
        # Submit with correct answer for bug_001 (line 4)
        found_lines = [4] if template_id == "bug_001" else [1]

        response = requests.post(
            f"{base_url}/submit",
            json={
                "session_id": session_id,
                "player_id": 1,
                "found_bug_lines": found_lines,
                "time_seconds": 45.2
            },
            timeout=5
        )
        response.raise_for_status()
        result = response.json()

        print(f"[OK] Status: {response.status_code}")
        print(f"[OK] Score: {result['score']}")
        print(f"[OK] XP Earned: {result['xp_earned']}")
        print(f"[OK] Bugs found: {result['bugs_found']}/{result['bugs_total']}")
        print(f"[OK] Accuracy: {result['accuracy']:.1f}%")
        print(f"[OK] Perfect game: {result['is_perfect']}")
        print()

    except Exception as e:
        print(f"[FAIL] {e}")
        return False

    # Test 3: Leaderboard
    print("TEST 3: Get leaderboard")
    print("-" * 40)
    try:
        response = requests.get(
            f"{base_url}/leaderboard",
            params={"limit": 5},
            timeout=5
        )
        response.raise_for_status()
        board = response.json()

        print(f"[OK] Status: {response.status_code}")
        print(f"[OK] Total entries: {board['total_entries']}")
        if board['entries']:
            top = board['entries'][0]
            print(f"[OK] Top player: {top['username']} with score {top['score']}")
        print()

    except Exception as e:
        print(f"[FAIL] {e}")
        return False

    # Test 4: Player stats
    print("TEST 4: Get player stats")
    print("-" * 40)
    try:
        response = requests.get(
            f"{base_url}/stats/1",
            timeout=5
        )
        response.raise_for_status()
        stats = response.json()

        print(f"[OK] Status: {response.status_code}")
        print(f"[OK] Total games: {stats['total_games_played']}")
        print(f"[OK] Total bugs found: {stats['total_bugs_found']}")
        print(f"[OK] Best score: {stats['best_score']}")
        print(f"[OK] Average accuracy: {stats['average_accuracy']:.1f}%")
        print()

    except Exception as e:
        print(f"[FAIL] {e}")
        return False

    print("=" * 60)
    print("[SUCCESS] ALL TESTS PASSED - BUG HUNT IS FULLY FUNCTIONAL")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        success = test_bug_hunt_flow()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
