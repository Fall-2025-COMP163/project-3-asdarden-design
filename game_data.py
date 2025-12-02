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
            lines = f.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Data file '{filename}' not found.")

    try:
        for line in lines + ["\n"]:
            line = line.strip()
            if not line: 
                if current:
                    normalized = {}
                    required_fields = {
                        "QUEST_ID": "quest_id",
                        "TITLE": "title",
                        "DESCRIPTION": "description",
                        "REWARD_XP": "reward_xp",
                        "REWARD_GOLD": "reward_gold",
                        "REQUIRED_LEVEL": "required_level",
                        "PREREQUISITE": "prerequisite"
                    }

                    for k, lower_k in required_fields.items():
                        if k not in current:
                            raise InvalidDataFormatError(f"Quest missing field '{k}'")
                        normalized[lower_k] = current[k]
                        # Convert numeric fields
                        if lower_k in ["reward_xp", "reward_gold", "required_level"]:
                            try:
                                normalized[lower_k] = int(normalized[lower_k])
                            except ValueError:
                                raise InvalidDataFormatError(
                                    f"Quest field '{k}' must be an integer."
                                )

                    quest_id = normalized['quest_id']
                    quests[quest_id] = normalized
                    current = {}
                continue

            # Parse line like KEY: value
            if ':' not in line:
                raise InvalidDataFormatError(f"Invalid line format: {line}")
            key, value = line.split(":", 1)
            key = key.strip().upper()
            value = value.strip()
            current[key] = value

    except Exception as e:
        if isinstance(e, InvalidDataFormatError):
            raise e
        raise CorruptedDataError(f"Error reading quest data: {e}")

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
            lines = f.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Data file '{filename}' not found.")

    for line in lines + ["\n"]:
        line = line.strip()
        if not line:
            if current:
                # Normalize keys
                normalized = {
                    "item_id": current.get("ITEM_ID"),
                    "name": current.get("NAME"),
                    "type": current.get("TYPE"),
                    "effect": current.get("EFFECT"),
                    "cost": int(current.get("COST", 0)),
                    "description": current.get("DESCRIPTION"),
                }

                if None in normalized.values():
                    raise InvalidDataFormatError(f"Item missing required field(s): {normalized}")

                items[normalized["item_id"]] = normalized
                current = {}
            continue

        if ":" not in line:
            raise InvalidDataFormatError(f"Invalid line: {line}")
        key, value = line.split(":", 1)
        current[key.strip().upper()] = value.strip()

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

    # Check numeric fields
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

    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Item has invalid type '{item_dict['type']}'")
    
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError(f"Item 'cost' must be an integer")

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
