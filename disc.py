import os
import discord
from dotenv import load_dotenv
from forces_stat import forces_stat

load_dotenv()
ALU_CHANNEL_ID = int(os.getenv('ALU_CHANNEL_ID'))
class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        alu_2026 = []
        BASE_PATH = os.getenv("BASE_PATH")
        with open(f"{BASE_PATH}/usernames/codeforces/alu-2026.txt", "r") as f:
            alu_2026 = [s.strip() for s in f]
        all_users = list(set(alu_2026))
        msg="\n🏆 **Qualification Round Incoming!** To advance to the next phase (starting April 12th), reach a Codeforces rating of **1000 by April 9th, 2359 (UTC+2)**. Aim for 3–5 contests over the next month—consistency matters more than perfection! No cap on qualifiers, and we're here to help everyone hit the bar. `Let's go! 💪🚀`\n"
        message = forces_stat(usernames=all_users, msg=msg)
        channel = client.get_channel(ALU_CHANNEL_ID)
        if channel:
            print(f"channel: {channel}")
            await channel.send(message)
        await self.close()

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(f'{TOKEN}')
