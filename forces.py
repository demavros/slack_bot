import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from forces_stat import forces_stat

def get_forces():
    # codeforces bot
    load_dotenv()
    force_token=os.environ['CODEFORCES_TOKEN']
    force_client = slack.WebClient(token=force_token)
    COACHES_ID = os.environ['COACHES_ID']
    STUDENTS_ID = os.environ['STUDENTS_2024_ID']
    TEST_ID = os.getenv('TEST_ID')
    ALL_ID = os.environ['ALL_ID']
    BASE_PATH = os.environ['BASE_PATH']

    coaches = []
    with open(f"{BASE_PATH}/usernames/codeforces/coaches.txt", "r") as f:
        coaches = [c.strip() for c in f if c.strip()]
    
    students_2024 = []
    with open(f"{BASE_PATH}/usernames/codeforces/students-2024.txt", "r") as f:
        students_2024 = [s.strip() for s in f if s.strip()]

    students_2025 = []
    with open(f"{BASE_PATH}/usernames/codeforces/students-2025.txt", "r") as f:
        students_2025 = [s.strip() for s in f if s.strip()]

    all_users = list(set(coaches + students_2024 + students_2025))

    force_users = {
        "coaches": 
        {
            "users": coaches,
            "channel_id": COACHES_ID,
        },
        "students-2024": 
        {
            "users": students_2024,
            "channel_id": STUDENTS_ID
        },

        "students-2025": 
        {
            "users": students_2025,
            "channel_id": STUDENTS_ID
        },
        "all": 
        {
            "users": all_users,
            "channel_id": ALL_ID
        }
    }

    return force_users, force_client, forces_stat
