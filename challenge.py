import os
import sys
import requests
import time

LICHESS_API_URL = "https://lichess.org/api/challenge"
# Read token from environment
TOKEN = os.getenv("LICHESS_KEY")

if not TOKEN:
    print("Error: LICHESS_KEY is not set in environment.")
    sys.exit(1)

# Remove surrounding quotes if present
TOKEN = TOKEN.strip().strip('"').strip("'")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def send_challenge(username, time_control, mode):
    payload = {
        "rated": (mode.lower() == "rated"),
        "clock": {
            "limit": time_control[0] * 60,  # minutes → seconds
            "increment": time_control[1]
        },
        "color": "random"
    }
    url = f"{LICHESS_API_URL}/{username}"
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        print(f"✅ Challenge sent to {username} ({time_control[0]}+{time_control[1]} {mode})")
    else:
        print(f"❌ Failed to challenge {username}: {response.status_code} {response.text}")

def main():
    if len(sys.argv) < 5:
        print("Usage: python challenge.py <player_id> <number_of_games> <minutes>+<increment> <mode>")
        print("Example: python challenge.py maggicoder16 3 3+2 rated")
        sys.exit(1)

    player_id = sys.argv[1]
    num_games = int(sys.argv[2])
    time_str = sys.argv[3]
    mode = sys.argv[4]

    try:
        minutes, increment = map(int, time_str.split("+"))
    except ValueError:
        print("Error: Time control must be in format <minutes>+<increment>, e.g., 5+0")
        sys.exit(1)

    for i in range(num_games):
        print(f"📨 Sending challenge {i+1}/{num_games}...")
        send_challenge(player_id, (minutes, increment), mode)
        time.sleep(3)  # delay to avoid API spam

if __name__ == "__main__":
    main()
