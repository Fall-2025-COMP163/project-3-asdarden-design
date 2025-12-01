"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Anzino Darden

AI Usage: ChatGPT assistance for function implementations.

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list

    if 'inventory' not in character:
        character['inventory'] = []

    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")
    character['inventory'].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list

    if 'inventory' not in character or item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check

    if 'inventory' not in character:
        return False

    if item_id in character['inventory']:
        return True
    else:
        return False

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    if 'inventory' not in character:
        return 0
    if item_id in character['inventory']:
        return character['inventory'].count(item_id)
    else:
        return 0

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation

    if 'inventory' not in character:
        used = 0
    else:
        used = len(character['inventory'])
    remaining = MAX_INVENTORY_SIZE - used
    if remaining < 0:
        remaining = 0
    return remaining

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list

    removed_items = []
    for item in character['inventory']:
        removed_items.append(item)

    character['inventory'] = []
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory

    # Verify item exists
    if not has_item(character, item_id):
        raise ItemNotFoundError("Item not found in inventory.")
    if item_data.get('type') != 'consumable':
        raise InvalidItemTypeError("Item is not a consumable.")

    stat, value = parse_item_effect(item_data.get('effect', ''))
    if stat:
        apply_stat_effect(character, stat, value)

    remove_item_from_inventory(character, item_id)

    if stat == 'health':
        return f"Used {item_id}. Healed {value} health points (capped at max)."
    elif stat:
        return f"Used {item_id}. {stat} changed by {value}."
    else:
        return f"Used {item_id}. No effect."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory

    if not has_item(character, item_id):
        raise ItemNotFoundError("Weapon not found in inventory.")
    if item_data.get('type') != 'weapon':
        raise InvalidItemTypeError("Item is not a weapon.")

    if 'equipped_weapon' not in character:
        character['equipped_weapon'] = None
        character['equipped_weapon_effect'] = None

    # Unequip old weapon
    if character.get('equipped_weapon'):
        unequip_weapon(character)

    stat, value = parse_item_effect(item_data.get('effect', ''))
    if stat:
        apply_stat_effect(character, stat, value)

    character['equipped_weapon'] = item_id
    character['equipped_weapon_effect'] = item_data.get('effect', '')
    remove_item_from_inventory(character, item_id)
    return f"Equipped weapon: {item_id}."

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor

    if not has_item(character, item_id):
        raise ItemNotFoundError("Armor not found in inventory.")
    if item_data.get('type') != 'armor':
        raise InvalidItemTypeError("Item is not armor.")

    if 'equipped_armor' not in character:
        character['equipped_armor'] = None
        character['equipped_armor_effect'] = None

    # Unequip old armor
    if character.get('equipped_armor'):
        unequip_armor(character)

    stat, value = parse_item_effect(item_data.get('effect', ''))
    if stat:
        apply_stat_effect(character, stat, value)

    character['equipped_armor'] = item_id
    character['equipped_armor_effect'] = item_data.get('effect', '')
    remove_item_from_inventory(character, item_id)
    return f"Equipped armor: {item_id}."

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character

    weapon = character.get('equipped_weapon')
    if not weapon:
        return None

    effect = character.get('equipped_weapon_effect', '')
    if effect:
        stat, value = parse_item_effect(effect)
        apply_stat_effect(character, stat, -value)

    if len(character.get('inventory', [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full, cannot unequip weapon.")

    character['inventory'].append(weapon)
    character['equipped_weapon'] = None
    character['equipped_weapon_effect'] = None
    return weapon

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping

    armor = character.get('equipped_armor')
    if not armor:
        return None

    effect = character.get('equipped_armor_effect', '')
    if effect:
        stat, value = parse_item_effect(effect)
        apply_stat_effect(character, stat, -value)

    if len(character.get('inventory', [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full, cannot unequip armor.")

    character['inventory'].append(armor)
    character['equipped_armor'] = None
    character['equipped_armor_effect'] = None
    return armor

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory

    cost = item_data.get('cost', 0)
    if character.get('gold', 0) < cost:
        raise InsufficientResourcesError("Not enough gold.")
    if len(character.get('inventory', [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    character['gold'] -= cost
    add_item_to_inventory(character, item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character

    if not has_item(character, item_id):
        raise ItemNotFoundError("Item not in inventory.")
    sell_price = item_data.get('cost', 0) // 2
    remove_item_from_inventory(character, item_id)
    character['gold'] = character.get('gold', 0) + sell_price
    return 

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    if not isinstance(effect_string, str) or ":" not in effect_string:
        return "", 0
    parts = effect_string.split(":", 1)
    stat_name = parts[0].strip()
    try:
        value = int(parts[1].strip())
    except Exception:
        value = 0
    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health

    if not stat_name:
        return

    if stat_name not in character:
        character[stat_name] = 0

    if stat_name == 'health':
        max_hp = character.get('max_health', 0)
        character['health'] = min(character.get('health', 0) + value, max_hp)
        if character['health'] < 0:
            character['health'] = 0
    else:
        character[stat_name] += value

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    
    inventory = character.get('inventory', [])
    summary = {}
    for item in inventory:
        summary[item] = summary.get(item, 0) + 1

    print("=== INVENTORY LIST ===")
    if not summary:
        print("(Empty)")
        return
    for item_id, count in summary.items():
        item_info = item_data_dict.get(item_id, {})
        name = item_info.get('name', 'Unknown Item')
        item_type = item_info.get('type', 'unknown')
        print(f"{name} ({item_type}) (Count: {count})")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")
    except InvalidItemTypeError:
        print("Invalid item type")


    # Test equipping weapon (wrapped in try/except)
    test_weapon = {'item_id': 'sword_1', 'type': 'weapon', 'effect': 'strength:5'}
    try:
        add_item_to_inventory(test_char, 'sword_1')
    except InventoryFullError:
        print("Inventory is full, cannot add weapon for test")


    try:
        print(equip_weapon(test_char, 'sword_1', test_weapon))
    except ItemNotFoundError:
        print("Weapon not found")
    except InvalidItemTypeError:
        print("Invalid weapon type")


    # Test equipping armor (wrapped in try/except)
    test_armor = {'item_id': 'armor_1', 'type': 'armor', 'effect': 'max_health:10'}
    try:
        add_item_to_inventory(test_char, 'armor_1')
    except InventoryFullError:
        print("Inventory is full, cannot add armor for test")


    try:
        print(equip_armor(test_char, 'armor_1', test_armor))
    except ItemNotFoundError:
        print("Armor not found")
    except InvalidItemTypeError:
        print("Invalid armor type")


    # Test selling an item (wrapped in try/except)
    try:
        add_item_to_inventory(test_char, 'potion_sell')
    except InventoryFullError:
        pass
    test_sell_item = {'item_id': 'potion_sell', 'type': 'consumable', 'effect': 'health:5', 'cost': 20}
    try:
        gold = sell_item(test_char, 'potion_sell', test_sell_item)
        print(f"Sold potion for {gold} gold")
    except ItemNotFoundError:
        print("Item to sell not found")

    # Display inventory at end
    item_data_dict = {
        'health_potion': test_item,
        'sword_1': test_weapon,
        'armor_1': test_armor,
        'potion_sell': test_sell_item
    }
    display_inventory(test_char, item_data_dict)
