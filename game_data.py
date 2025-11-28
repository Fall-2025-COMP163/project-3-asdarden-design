"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    
    if not os.path.exists(filename):
        raise MissingDataFileError("Quest file not found")

    quests = {}
    try:
        f = open(filename, "r")
        content = f.read()
        f.close()
    except:
        raise CorruptedDataError("Cannot read quest file")

    try:
        blocks = content.split("\n\n")
        for block in blocks:
            lines = block.split("\n")
            lines = [line for line in lines if line.strip() != ""]
            if not lines:
                continue
            quest = parse_quest_block(lines)
            validate_quest_data(quest)
            quests[quest["quest_id"]] = quest
    except InvalidDataFormatError:
        raise
    except:
        raise InvalidDataFormatError("Quest file format invalid")

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests

    if not os.path.exists(filename):
        raise MissingDataFileError("Item file not found")

    items = {}
    try:
        f = open(filename, "r")
        content = f.read()
        f.close()
    except:
        raise CorruptedDataError("Cannot read item file")

    try:
        blocks = content.split("\n\n")
        for block in blocks:
            lines = block.split("\n")
            lines = [line for line in lines if line.strip() != ""]
            if not lines:
                continue
            item = parse_item_block(lines)
            validate_item_data(item)
            items[item["item_id"]] = item
    except InvalidDataFormatError:
        raise
    except:
        raise InvalidDataFormatError("Item file format invalid")

    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    
    required = ["quest_id", "title", "description", "reward_xp",
                "reward_gold", "required_level", "prerequisite"]
    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError("Quest missing field: " + key)
    if type(quest_dict["reward_xp"]) != int or type(quest_dict["reward_gold"]) != int:
        raise InvalidDataFormatError("Quest reward must be integer")
    if type(quest_dict["required_level"]) != int:
        raise InvalidDataFormatError("Quest required_level must be integer")
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    
    required = ["item_id", "name", "type", "effect", "cost", "description"]
    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError("Item missing field: " + key)
    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError("Item type invalid")
    if type(item_dict["cost"]) != int:
        raise InvalidDataFormatError("Item cost must be integer")
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    
    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists("data/quests.txt"):
        f = open("data/quests.txt", "w")
        f.write(
            "QUEST_ID: first_quest\n"
            "TITLE: First Steps\n"
            "DESCRIPTION: Complete your first quest.\n"
            "REWARD_XP: 50\n"
            "REWARD_GOLD: 25\n"
            "REQUIRED_LEVEL: 1\n"
            "PREREQUISITE: NONE\n"
        )
        f.close()

    if not os.path.exists("data/items.txt"):
        f = open("data/items.txt", "w")
        f.write(
            "ITEM_ID: health_potion\n"
            "NAME: Health Potion\n"
            "TYPE: consumable\n"
            "EFFECT: health:20\n"
            "COST: 10\n"
            "DESCRIPTION: Restores 20 health.\n"
        )
        f.close()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    
    quest = {}
    try:
        for line in lines:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key in ["reward_xp", "reward_gold", "required_level"]:
                value = int(value)
            quest[key] = value
    except:
        raise InvalidDataFormatError("Failed to parse quest")
    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic

    item = {}
    try:
        for line in lines:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == "cost":
                value = int(value)
            item[key] = value
    except:
        raise InvalidDataFormatError("Failed to parse item")
    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")
    # Test creating default files
    create_default_data_files()

    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
        print(quests)
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")

    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
        print(items)
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
