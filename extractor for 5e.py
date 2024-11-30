from bs4 import BeautifulSoup
import re
from collections import Counter


def parse_html_chat(file_path):
    # Read and parse the HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Initialize data structure
    rolls_data = {}
    total_rolls_found = 0  # For debugging purposes

    # Locate all roll messages
    messages = soup.find_all("div", class_="sheet-rolltemplate-rolls")
    print(f"Debug: Total roll messages found: {len(messages)}")  # Debug

    for message in messages:
        # Extract the character's name
        character_name = message.find("span", class_="sheet-charactername")
        if character_name:
            character_name = character_name.get_text().strip()
        else:
            continue

        # Initialize data for the character if not already present
        if character_name not in rolls_data:
            rolls_data[character_name] = {
                "rolls": [],
                "critsuccess": 0,
                "critfail": 0,
                "distribution": Counter({i: 0 for i in range(1, 21)})
            }

        # Debug: Print character name being processed
        print(f"Debug: Processing rolls for {character_name}")  # Debug

        # Extract roll elements within the message
        roll_elements = message.find_all("span", class_="inlinerollresult")
        for roll in roll_elements:
            title = roll.get("title", "")
            roll_classes = roll.get("class", [])  # Get the class attribute as a list

            # Debug: Print raw roll attributes for inspection
            print(f"Debug: Roll title: {title}")
            print(f"Debug: Roll classes: {roll_classes}")

            # Check for d20 roll
            if "Rolling 1d20cs20cf1" in title:
                roll_value_match = re.search(r'class="basicdiceroll(?: critsuccess | critfail )?">(.*?)<', title)
                crit_success = "fullcrit" in roll_classes
                crit_fail = "fullfail" in roll_classes

                if roll_value_match:
                    try:
                        roll_value = int(roll_value_match.group(1))
                        rolls_data[character_name]["rolls"].append(roll_value)
                        rolls_data[character_name]["distribution"][roll_value] += 1
                        total_rolls_found += 1

                        # Count critical successes and failures
                        if crit_success:
                            rolls_data[character_name]["critsuccess"] += 1
                            print(f"Debug: Critical Success detected for {character_name}: {roll_value}")
                        if crit_fail:
                            rolls_data[character_name]["critfail"] += 1
                            print(f"Debug: Critical Fail detected for {character_name}: {roll_value}")
                    except ValueError:
                        print(f"Debug: Invalid roll value encountered: {roll_value_match.group(1)}")
                else:
                    print(f"Debug: No valid roll value found in title: {title}")

    print(f"Debug: Total d20 rolls captured across all characters: {total_rolls_found}")  # Debug
    return rolls_data


def calculate_statistics(data):
    stats = {}
    for character_name, character_data in data.items():
        rolls = character_data["rolls"]
        total_rolls = len(rolls)
        average_roll = sum(rolls) / total_rolls if total_rolls > 0 else 0
        stats[character_name] = {
            "Total Rolls": total_rolls,
            "Average Roll": average_roll,
            "Crit Success": character_data["critsuccess"],
            "Crit Fail": character_data["critfail"],
            "Distribution": character_data["distribution"]
        }
    return stats


def display_statistics(stats):
    # Sort stats by Total Rolls in descending order
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['Total Rolls'], reverse=True)

    # Print the header
    headers = ["Character", "Total Rolls", "Average Roll", "Crit Success", "Crit Fail"] + [str(i) for i in range(1, 21)]
    print("\t".join(headers))

    # Print sorted stats
    for character_name, character_stats in sorted_stats:
        row = [
                  character_name,
                  str(character_stats["Total Rolls"]),
                  f"{character_stats['Average Roll']:.2f}",
                  str(character_stats["Crit Success"]),
                  str(character_stats["Crit Fail"]),
              ] + [str(character_stats["Distribution"][i]) for i in range(1, 21)]
        print("\t".join(row))


# Main Program
if __name__ == "__main__":
    file_path = "Chat Log for Cursed.html"  # Replace with your file
    try:
        all_characters_data = parse_html_chat(file_path)
        stats = calculate_statistics(all_characters_data)
        display_statistics(stats)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
