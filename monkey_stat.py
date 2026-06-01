import requests
import asyncio

async def monkey_stat(usernames, 
                msg="\nTo appear on the leaderboard, please `reply to this message with your Monkeytype username`. Congratulations to everyone who has already submitted their usernames—keep up the great work and keep improving your typing speed! `Happy Typing!` ⌨️ \n"
    ):
    users_data = []
    leaderboard = []
    leaderboard.append("Username        | wpm | acc | secs|")
    leaderboard.append("----------------|-----|-----|-----|")  
    for username in usernames:
        max_retries = 3
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            try:
                response = requests.api.get(f"https://api.monkeytype.com/users/{username}/profile", timeout=20)
                response.raise_for_status()  # Raise exception for bad status codes
                
                data = response.json()
                name = data['data']['name']
                bests = data['data']['personalBests']['time']

                max_s = 0
                acc = 0
                tm = 0

                for t, values in bests.items():
                    if int(t) < 30: continue
                    for val in values:
                        speed = val['wpm']
                        if speed > max_s:
                            max_s = speed
                            acc = val['acc']
                            tm = t
                users_data.append((name, round(max_s), round(acc), tm))
                success = True
            
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 5 * (2 ** (retry_count - 1))  # Exponential backoff: 5, 10, 20 seconds
                        print(f"Rate limited (429) for {username}. Retry {retry_count}/{max_retries}. Waiting {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"Error: Rate limited (429) for {username}. Max retries exceeded.")
                else:
                    print(f"Error: HTTP error for {username}: {e}")
                    break
            except requests.exceptions.Timeout:
                print(f"Error: Request timeout for username: {username}")
                break
            except requests.exceptions.ConnectionError as e:
                print(f"Error: Connection error for {username}: {e}")
                break
            except requests.exceptions.RequestException as e:
                print(f"Error: Request failed for {username}: {e}")
                break
            except (KeyError, IndexError, TypeError) as e:
                print(f"Error: Failed to parse data for {username}: {e}")
                break
            except Exception as e:
                print(f"Error: Unexpected error for {username}: {e}")
                break
        
        # Add delay between requests to avoid rate limiting
        await asyncio.sleep(3)

    # Sort users by typing speed in descending order for ranking
    sorted_users = sorted(users_data, key=lambda x: (x[1], x[2]), reverse=True)
    # Add each user's data to the leaderboard
    for rank, user in enumerate(sorted_users, start=1):
        username, speed, accuracy, time_taken = user
        row = f"{rank:<2} {username[:12]:<12} | {speed:<3} | {accuracy:<3} | {time_taken:<4}|"
        leaderboard.append(row)

    result = "🏆      `TYPING SPEED LEADERBOARD`      🏆\n\n"
    result += "```\n" 
    result += "\n".join(leaderboard)
    result += "\n```\n"
    result += msg
    
    # Split into chunks if exceeding 2000 character limit
    if len(result) <= 2000:
        return result
    
    # Split while keeping code blocks intact
    messages = []
    lines = leaderboard[:]  # Copy leaderboard lines
    
    # First message: header + first batch of rows
    current_msg = "🏆      `TYPING SPEED LEADERBOARD`      🏆\n\n```\n"
    current_msg += "\n".join(lines[:2])  # Add header lines
    
    for line in lines[2:]:
        test_msg = current_msg + "\n" + line + "\n```"
        if len(test_msg) <= 1900:  # Leave room for closing ```
            current_msg += "\n" + line
        else:
            # Current message is full, close it and start a new one
            current_msg += "\n```"
            messages.append(current_msg)
            current_msg = "```\n" + line
    
    # Close the last message
    current_msg += "\n```\n" + msg
    messages.append(current_msg)
    
    return messages
