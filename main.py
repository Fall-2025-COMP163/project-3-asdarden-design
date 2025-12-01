"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print("Invalid input. Please enter 1, 2, or 3.")


def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    print("\n=== NEW GAME ===")
    
    name = input("Enter your character's name: ").strip()
    
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    while True:
        print("Choose a class:")
        for i, c in enumerate(valid_classes, start=1):
            print(f"{i}. {c}")
        class_choice = input(f"Enter choice (1-{len(valid_classes)}): ").strip()
        if class_choice in [str(i) for i in range(1, len(valid_classes)+1)]:
            character_class = valid_classes[int(class_choice)-1]
            break
        print("Invalid choice. Try again.")
    
    try:
        current_character = character_manager.create_character(name, character_class)
        character_manager.save_character(current_character)
        print(f"Character '{name}' the {character_class} created and saved!")
    except InvalidCharacterClassError as e:
        print(f"Error: {e}")
        return

    game_loop()


def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    print("\n=== LOAD GAME ===")
    saved_characters = character_manager.list_saved_characters()
    
    if not saved_characters:
        print("No saved characters found.")
        return
    
    print("Saved characters:")
    for i, c in enumerate(saved_characters, start=1):
        print(f"{i}. {c}")
    
    while True:
        choice = input(f"Enter number to load (1-{len(saved_characters)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(saved_characters):
            selected_name = saved_characters[int(choice)-1]
            break
        print("Invalid choice. Try again.")
    
    try:
        current_character = character_manager.load_character(selected_name)
        print(f"Loaded character '{selected_name}' successfully!")
    except CharacterNotFoundError:
        print(f"Character '{selected_name}' not found.")
        return
    except SaveFileCorruptedError:
        print("Save file is corrupted. Cannot load character.")
        return
    
    game_loop()

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    print(f"\nWelcome, {current_character['name']}! Let the adventure begin.")
    
    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Goodbye!")
            game_running = False
            
def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")
    while True:
        choice = input("Enter choice (1-6): ").strip()
        if choice in [str(i) for i in range(1, 7)]:
            return int(choice)
        print("Invalid input. Enter a number between 1 and 6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler

    print("\n=== CHARACTER STATS ===")
    char = current_character
    print(f"Name: {char['name']}")
    print(f"Class: {char['class']}")
    print(f"Level: {char['level']}")
    print(f"Health: {char['health']}/{char['max_health']}")
    print(f"Strength: {char['strength']}")
    print(f"Magic: {char['magic']}")
    print(f"Experience: {char['experience']}")
    print(f"Gold: {char['gold']}")
    print(f"Inventory: {', '.join(char['inventory']) if char['inventory'] else 'Empty'}")
    quest_handler.display_character_quest_progress(current_character, all_quests)

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    inventory = current_character["inventory"]
    inventory_system.display_inventory(current_character, all_items)
    
def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Completed Quests")
    print("3. Accept Quest")
    print("4. Abandon Quest")
    print("5. Back")
    choice = input("> ").strip()
    
    if choice == "1":
        active = quest_handler.get_active_quests(current_character, all_quests)
        quest_handler.display_quest_list(active)
    elif choice == "2":
        completed = quest_handler.get_completed_quests(current_character, all_quests)
        quest_handler.display_quest_list(completed)
    elif choice == "3":
        available = quest_handler.get_available_quests(current_character, all_quests)
        if not available:
            print("No quests available.")
            return
        for i, q in enumerate(available, start=1):
            print(f"{i}. {q['title']} (Level {q['required_level']})")
        sel = input("Enter quest number to accept, or 0 to cancel: ")
        if sel.isdigit():
            sel = int(sel)
            if 1 <= sel <= len(available):
                quest_handler.accept_quest(current_character, available[sel-1]['quest_id'], all_quests)
                print(f"Accepted quest: {available[sel-1]['title']}")
    elif choice == "4":
        active = quest_handler.get_active_quests(current_character, all_quests)
        if not active:
            print("No active quests to abandon.")
            return
        for i, q in enumerate(active, start=1):
            print(f"{i}. {q['title']}")
        sel = input("Enter quest number to abandon, or 0 to cancel: ")
        if sel.isdigit():
            sel = int(sel)
            if 1 <= sel <= len(active):
                quest_handler.abandon_quest(current_character, active[sel-1]['quest_id'])
                print(f"Abandoned quest: {active[sel-1]['title']}")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    enemy = combat_system.generate_enemy(current_character['level'])
    print(f"A wild {enemy['name']} appears!")
    try:
        result = combat_system.simple_battle(current_character, enemy)
        if result['status'] == "defeat":
            handle_character_death()
        else:
            character_manager.gain_experience(current_character, result['xp'])
            character_manager.add_gold(current_character, result['gold'])
            print(f"Defeated {enemy['name']}! Gained {result['xp']} XP and {result['gold']} gold.")
    except CombatError as e:
        print(f"Combat error: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    
    inventory_system.shop_menu(current_character, all_items)
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()

    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except (MissingDataFileError, InvalidDataFormatError):
        print("Data files missing or corrupted. Creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False

    print(f"\n{current_character['name']} has fallen!")
    print("1. Revive (50 gold)")
    print("2. Quit")
    while True:
        choice = input("Enter choice (1-2): ").strip()
        if choice == "1":
            if current_character['gold'] >= 50:
                current_character['gold'] -= 50
                character_manager.revive_character(current_character)
                print(f"{current_character['name']} has been revived with 50% health.")
                return
            print("Not enough gold!")
        elif choice == "2":
            game_running = False
            print("Game over.")
            return

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

