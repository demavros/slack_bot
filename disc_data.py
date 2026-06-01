import os
import discord
from dotenv import load_dotenv
from forces_stat import forces_stat

load_dotenv()
ALU_CHANNEL_ID = int(os.getenv('ALU_CHANNEL_ID'))
RWCO_CHANNEL_ID = int(os.getenv('RwCO_CHANNEL_ID'))
# EtIO_CHANNEL_ID= int(os.getenv('EtIO_CHANNEL_ID'))

# Define users with their associated channel IDs
CF_DATA = {
    'rwco_2026': {
        'channel_id': RWCO_CHANNEL_ID,
        'file': 'usernames/codeforces/rwco.txt',
        'usernames': [],
        'msg': "\nTo appear on the leaderboard, please `reply to this message with your codeforces username`. Congratulations to everyone who has already submitted their usernames—keep up the great work and keep improving your Programming and Math skills! `Happy Learning!` 👩‍💻👨‍💻\n"
    },
    'alu_2026': {
        'channel_id': ALU_CHANNEL_ID,
        'file': 'usernames/codeforces/alu.txt',
        'usernames': [],
        'msg': "\nTo appear on the leaderboard, please `reply to this message with your codeforces username`. Congratulations to everyone who has already submitted their usernames—keep up the great work and keep improving your Programming and Math skills! `Happy Learning!` 👩‍💻👨‍💻\n", 
    },
    # 'etio_2026': {
    #     'channel_id': EtIO_CHANNEL_ID,
    #     'file': 'usernames/codeforces/etio-2026.txt',
    #     'usernames': [],
    #     'msg': "\nTo appear on the leaderboard, please `reply to this message with your codeforces username`. Congratulations to everyone who has already submitted their usernames—keep up the great work and keep improving your Programming and Math skills! `Happy Learning!` 👩‍💻👨‍💻\n", 
    # }
}

MK_DATA = {
    'rwco_2026': {
        'channel_id': RWCO_CHANNEL_ID,
        'file': 'usernames/monkeytype/rwco.txt',
        'usernames': [],
        'msg': "\nTo appear on the leaderboard, please `reply to this message with your Monkeytype username`. Congratulations to everyone who has already submitted their usernames—keep up the great work and keep improving your typing speed! `Happy Typing!` ⌨️ \n"
    },
    'alu_2026': {
        'channel_id': ALU_CHANNEL_ID,
        'file': 'usernames/monkeytype/alu.txt',
        'usernames': [],
        'msg': "\nTo appear on the leaderboard, please `reply to this message with your Monkeytype username`. Congratulations to everyone who has already submitted their usernames—keep up the great work and keep improving your typing speed! `Happy Typing!` ⌨️ \n"
    },
    # 'etio_2026': {
    #     'channel_id': EtIO_CHANNEL_ID,
    #     'file': 'usernames/monkeytype/rwco-2026.txt',
    #     'usernames': [],
    #     'msg': ""
    # }
}

class Client(discord.Client):
    def __init__(self, users_data, func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_data = users_data
        self.func = func
    
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        BASE_PATH = os.getenv("BASE_PATH")
        
        # Read usernames from files
        for group_name, group_data in self.users_data.items():
            file_path = f"{BASE_PATH}/{group_data['file']}"
            with open(file_path, "r") as f:
                group_data['usernames'] = [s.strip() for s in f if s.strip()]
        
        # Process and send messages to each group
        for group_name, group_data in self.users_data.items():
            all_users = list(set(group_data['usernames']))
            msg=group_data['msg']
            messages = await self.func(usernames=all_users, msg=msg)
            channel = self.get_channel(group_data['channel_id'])
            if channel:
                print(f"channel: {channel}")
                # Handle both single message (string) and multiple messages (list)
                if isinstance(messages, str):
                    messages = [messages]
                for message in messages:
                    await channel.send(message)
        
        await self.close()

def run_disc(data, func):
    intents = discord.Intents.default()
    intents.message_content = True
    client = Client(users_data=data, func=func, intents=intents)
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(f'{TOKEN}')
