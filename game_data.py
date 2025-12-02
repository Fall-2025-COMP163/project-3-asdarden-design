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

    quests = {}
    current = {}

    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f]

        for line in lines + [""]:  # Add empty line to flush last quest
            if line == "":
                if current:
                    # Normalize keys to lowercase
                    quest = {k.lower(): v for k, v in current.items()}

                    # Validate required fields
                    required = ["quest_id", "title", "description", "reward_xp",
                                "reward_gold", "required_level", "prerequisite"]
                    for key in required:
                        if key not in quest:
                            raise InvalidDataFormatError(f"Quest missing field '{key}'")

                    # Convert numeric fields
                    try:
                        quest['reward_xp'] = int(quest['reward_xp'])
                        quest['reward_gold'] = int(quest['reward_gold'])
                        quest['required_level'] = int(quest['required_level'])
                    except ValueError:
                        raise InvalidDataFormatError(f"Quest has invalid number field: {quest}")

                    quests[quest['quest_id']] = quest
                    current = {}
                continue
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid quest line: {line}")
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip()

    except FileNotFoundError:
        raise MissingDataFileError(f"Quest file '{filename}' not found.")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Could not read quest data: {e}")

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
    items = {}
    current = {}

    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f]

        for line in lines + [""]:
            if line == "":
                if current:
                    # Normalize keys to lowercase
                    item = {k.lower(): v for k, v in current.items()}

                    # Validate required fields
                    required = ["item_id", "name", "type", "effect", "cost", "description"]
                    for key in required:
                        if key not in item:
                            raise InvalidDataFormatError(f"Item missing field '{key}'")

                    # Convert numeric fields
                    try:
                        item['cost'] = int(item['cost'])
                    except ValueError:
                        raise InvalidDataFormatError(f"Item has invalid number field: {item}")

                    items[item['item_id']] = item
                    current = {}
                continue
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid item line: {line}")
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip()

    except FileNotFoundError:
        raise MissingDataFileError(f"Item file '{filename}' not found.")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Could not read item data: {e}")

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
    
    required = ["quest_id", "title", "description",
                "reward_xp", "reward_gold",
                "required_level", "prerequisite"]

    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Quest missing field '{key}'")

    for key in ["reward_xp", "reward_gold", "required_level"]:
        if not isinstance(quest_dict[key], int):
            raise InvalidDataFormatError(f"Quest field '{key}' must be an integer")

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
            raise InvalidDataFormatError(f"Item missing field '{key}'")

    if not isinstance(item_dict['cost'], int):
        raise InvalidDataFormatError("Item field 'cost' must be an integer")

    valid_types = ["weapon", "armor", "consumable"]
    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

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
    
    os.makedirs("data", exist_ok=True)

    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w", encoding="utf-8") as f:
            f.write(
                "QUEST_ID: first_quest\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Complete your first quest.\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 25\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )

    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w", encoding="utf-8") as f:
            f.write(
                "ITEM_ID: health_potion\n"
                "NAME: Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 10\n"
                "DESCRIPTION: Restores 20 health.\n"
            )
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
            if ":" not in line:
                raise InvalidDataFormatError("Malformed quest line")
            key, value = line.split(":", 1)
            key = key.strip().upper()
            value = value.strip()
            if key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
                value = int(value)
            quest[key] = value
        if "QUEST_ID" not in quest:
            raise InvalidDataFormatError("Quest missing QUEST_ID")
    except Exception:
        raise InvalidDataFormatError("Failed to parse quest block")
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
            if ":" not in line:
                raise InvalidDataFormatError("Malformed item line")
            key, value = line.split(":", 1)
            key = key.strip().upper()
            value = value.strip()
            if key == "COST":
                value = int(value)
            item[key] = value
        if "ITEM_ID" not in item:
            raise InvalidDataFormatError("Item missing ITEM_ID")
    except Exception:
        raise InvalidDataFormatError("Failed to parse item block")
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
    # Load quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests: {list(quests.keys())}")
    except Exception as e:
        print(f"Quest loading error: {e}")

    # Load items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items: {list(items.keys())}")
    except Exception as e:
        print(f"Item loading error: {e}")
