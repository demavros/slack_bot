import requests
import asyncio

async def forces_stat(usernames, msg="\nTo appear on the leaderboard, please `reply to this message with your codeforces username`. Congratulations to everyone who has already submitted their usernames—keep up the great work and keep improving your Coding and Math skills! `Happy Coding!` 👩‍💻👨‍💻\n"):
    users_data = []
    leaderboard = []
#   leaderboard.append("Username       | wpm | acc | secs|")
    leaderboard.append("Username       | rating  | rank    |")
    leaderboard.append("---------------|---------|---------|")  

    for username in usernames:
        rating = 0
        ranking = "None"
        try:
            url = f"https://codeforces.com/api/user.info?handles={username}"
            response = requests.get(url, timeout=20)
            response.raise_for_status()  # Raise exception for bad status codes
            
            data = response.json()
            if data["status"] == "OK":
                user_info = data["result"][0]
                rating = user_info.get("rating", 0)
                ranking = user_info.get("rank", "None")
            else:
                print(f"Error: API returned non-OK status for {username}")
                continue
            
            users_data.append((username, rating, ranking))
        
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"Error: Rate limited (429) for {username}. Waiting 5 seconds before retry...")
                await asyncio.sleep(5)
            else:
                print(f"Error: HTTP error for {username}: {e}")
        except requests.exceptions.Timeout:
            print(f"Error: Request timeout for username: {username}")
        except requests.exceptions.ConnectionError as e:
            print(f"Error: Connection error for {username}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: Request failed for {username}: {e}")
        except (KeyError, IndexError) as e:
            print(f"Error: Failed to parse data for {username}: {e}")
        except Exception as e:
            print(f"Error: Unexpected error for {username}: {e}")
        
        # Add delay between requests to avoid rate limiting
        await asyncio.sleep(1)

    # Sort users by typing speed in descending order for ranking
    sorted_users = sorted(users_data, key=lambda x: x[1], reverse=True)
    # Add each user's data to the leaderboard
    for rank, user in enumerate(sorted_users, start=1):
        name, rating, ranking = user
        if rating == 0 : rating = "Unrated"
        row = f"{rank:<2} {name[:11]:<11} | {rating:<7} | {ranking[:8]:<7} |"
        leaderboard.append(row)

    result = "👨‍💻   🏆   `CODEFORCES LEADERBOARD`   🏆   👩‍💻\n\n"
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
    current_msg = "👨‍💻   🏆   `CODEFORCES LEADERBOARD`   🏆   👩‍💻\n\n```\n"
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
