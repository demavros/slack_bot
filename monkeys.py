import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from monkey_stat import monkey_stat

def get_monkeys():
    # monkeytype bot
    load_dotenv()
    monkey_token=os.getenv('MONKEYS_TOKEN')
    monkey_client = slack.WebClient(token=monkey_token)

    COACHES_ID = os.getenv('COACHES_ID')
    STUDENTS_ID = os.getenv('STUDENTS_2024_ID')
    TEST_ID = os.getenv('TEST_ID')
    ALL_ID = os.environ['ALL_ID']
    BASE_PATH = os.getenv('BASE_PATH')

    coaches = []
    with open(f"{BASE_PATH}/usernames/monkeytype/coaches.txt", "r") as f:
        coaches = [c.strip() for c in f if c.strip()]
    
    students_2024 = []
    with open(f"{BASE_PATH}/usernames/monkeytype/students-2024.txt", "r") as f:
        students_2024 = [s.strip() for s in f if s.strip()]
    
    students_2025 = []
    with open(f"{BASE_PATH}/usernames/monkeytype/students-2025.txt", "r") as f:
        students_2025 = [s.strip() for s in f if s.strip()]

    all_users = list(set(coaches + students_2024 + students_2025))

    monkey_users = {
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
        "all": {
            "users": all_users,
            "channel_id": ALL_ID 
        }
    }

    return monkey_users, monkey_client, monkey_stat
