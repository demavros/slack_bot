import asyncio
from datetime import datetime
from monkeys import get_monkeys
from forces import get_forces

async def main():
    current_day = datetime.now().strftime("%A")

    monkeys_days = "Tuesday, Thursday, Saturday, Monday"
    if current_day in monkeys_days:
        users, client, stat =  get_monkeys()
    else:
        users, client, stat = get_forces() 

    for user, value in users.items():
        if user == 'all':
            result = await stat(usernames=value['users'])
            # Handle both string and list of messages
            if isinstance(result, list):
                result_string = "\n".join(result)
            else:
                result_string = result
            try:
                client.chat_postMessage(channel=value['channel_id'], text=result_string)
            except Exception as e:
                print(f"Error sending message to {value['channel_id']}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
