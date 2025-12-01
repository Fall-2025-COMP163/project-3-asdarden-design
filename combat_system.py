"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Anzino Darden

AI Usage: Chatgpt implemented all functions in this file.

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)
import random 
# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward

    if enemy_type == 'goblin':
        return {'name': 'Goblin', 'health': 50, 'max_health': 50, 'strength': 8, 'magic': 2, 'xp_reward': 25, 'gold_reward': 10}
    elif enemy_type == 'orc':
        return {'name': 'Orc', 'health': 80, 'max_health': 80, 'strength': 12, 'magic': 5, 'xp_reward': 50, 'gold_reward': 25}
    elif enemy_type == 'dragon':
        return {'name': 'Dragon', 'health': 200, 'max_health': 200, 'strength': 25, 'magic': 15, 'xp_reward': 200, 'gold_reward': 100}
    else:
        raise InvalidTargetError(f"Enemy type '{enemy_type}' not recognized.")

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type

    if character_level <= 2:
        return create_enemy('goblin')
    elif character_level <= 5:
        return create_enemy('orc')
    else:
        return create_enemy('dragon')

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter

        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 1
        self.character['in_battle'] = True

        # Ensure ability cooldown tracking exists
        ensure_abilities_initialized(self.character)
        # mark character as in_battle to help other logic if needed
        self.character['in_battle'] = True

        # Ensure abilities structure exists so cooldown helpers won't fail
        ensure_abilities_initialized(self.character)
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight.")
        
        while self.combat_active:
            self.player_turn()
            if not self.combat_active:
                break
            self.enemy_turn()
        # clear in_battle flag
        self.character['in_battle'] = False
        winner = self.check_battle_end()
        rewards = {'xp_gained': 0, 'gold_gained': 0}
        
        if winner == 'player':
            rewards['xp_gained'] = self.enemy['xp_reward']
            rewards['gold_gained'] = self.enemy['gold_reward']
        
        return {'winner': winner, 'xp_gained': rewards['xp_gained'], 'gold_gained': rewards['gold_gained']}
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action

        if not self.combat_active:
            raise CombatNotActiveError("Cannot take turn, combat is not active.")

        display_combat_stats(self.character, self.enemy)

        # Determine if special ability option is available
        ensure_abilities_initialized(self.character)
        ability_name = None
        for a in self.character['abilities']:
            ability_name = a
            break  # pick first ability key as the special ability

        can_use_special = ability_name is not None and is_ability_available(self.character, ability_name)

        # Present choices
        print("\n--- Your Turn ---")
        print("1. Basic Attack")
        if can_use_special:
            print(f"2. Use Special Ability ({ability_name})")
            print("3. Try to Run")
            selection = input("Choose an action (1-3): ").strip()
        else:
            print("2. Try to Run")
            selection = input("Choose an action (1-2): ").strip()

        if not selection.isdigit():
            selection = "1"
        sel = int(selection)

        if sel == 1:
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character.get('name','Player')} attacks for {damage} damage!")
        elif sel == 2 and can_use_special:
            try:
                text = use_special_ability(self.character, self.enemy)
                # set cooldown already done in use_special_ability
                display_battle_log(text)
            except AbilityOnCooldownError as e:
                display_battle_log(str(e))
        elif (sel == 2 and not can_use_special) or (sel == 3 and can_use_special):
            # Try to run
            success = self.attempt_escape()
            if success:
                display_battle_log(f"{self.character.get('name','Player')} escaped successfully!")
                self.combat_active = False
            else:
                display_battle_log(f"{self.character.get('name','Player')} failed to escape!")
        else:
            # fallback to basic attack
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character.get('name','Player')} attacks for {damage} damage!")

        # After player's action, decrement cooldowns
        decrement_ability_cooldowns(self.character)

        if self.check_battle_end() is not None:
            self.combat_active = False

    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take turn, combat is not active.")

        # Basic enemy attack
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy.get('name','Enemy')} attacks for {damage} damage!")

        if self.check_battle_end() is not None:
            self.combat_active = False
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        atk_str = int(attacker.get('strength', 1))
        def_str = int(defender.get('strength', 0))
        damage = atk_str - (def_str // 4)
        if damage < 1:
            damage = 1
        return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        current = int(target.get('health', 0))
        new = current - int(damage)
        target['health'] = new if new > 0 else 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy.get('health', 0) <= 0:
            return 'player'
        elif self.character.get('health', 0) <= 0:
            return 'enemy'
        else:
            return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        success = random.randint(0, 1) == 1
        if success:
            self.combat_active = False
        return success


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================


def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    ensure_abilities_initialized(character)

    # pick the first ability defined for the character
    ability_name = None
    for aname in character['abilities']:
        ability_name = aname
        break

    if ability_name is None:
        # no ability configured, fall back to class default behavior
        cls = character.get('class', '').lower()
        if cls == 'warrior':
            return warrior_power_strike(character, enemy)
        elif cls == 'mage':
            return mage_fireball(character, enemy)
        elif cls == 'rogue':
            return rogue_critical_strike(character, enemy)
        elif cls == 'cleric':
            return cleric_heal(character)
        else:
            return "No special ability available."

    # Check cooldown
    if not is_ability_available(character, ability_name):
        raise AbilityOnCooldownError(f"Ability '{ability_name}' is on cooldown.")

    cls = character.get('class', '').lower()
    result = None
    if cls == 'warrior':
        result = warrior_power_strike(character, enemy)
    elif cls == 'mage':
        result = mage_fireball(character, enemy)
    elif cls == 'rogue':
        result = rogue_critical_strike(character, enemy)
    elif cls == 'cleric':
        result = cleric_heal(character)
    else:
        # fallback: use warrior power strike
        result = warrior_power_strike(character, enemy)

    # Put ability on cooldown after use (if ability entry has max_cooldown)
    set_ability_cooldown(character, ability_name)

    return result

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    damage = int(character.get('strength', 1)) * 2 - (enemy.get('strength', 0) // 4)
    if damage < 1:
        damage = 1
    enemy['health'] = max(0, enemy.get('health', 0) - damage)
    return f"{character.get('name','Player')} used Power Strike! {damage} damage dealt."

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    damage = int(character.get('magic', 1)) * 2 - (enemy.get('magic', 0) // 4)
    if damage < 1:
        damage = 1
    enemy['health'] = max(0, enemy.get('health', 0) - damage)
    return f"{character.get('name','Player')} cast Fireball! {damage} damage dealt."


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    crit = random.randint(0, 1) == 1
    if crit:
        damage = int(character.get('strength', 1)) * 3 - (enemy.get('strength', 0) // 4)
    else:
        damage = int(character.get('strength', 1)) - (enemy.get('strength', 0) // 4)
    if damage < 1:
        damage = 1
    enemy['health'] = max(0, enemy.get('health', 0) - damage)
    return f"{character.get('name','Player')} used Critical Strike! {damage} damage dealt."


def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    character['health'] = min(character.get('max_health', heal_amount), character.get('health', 0) + heal_amount)
    return f"{character.get('name','Player')} healed for {heal_amount} HP."


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def ensure_abilities_initialized(character):
    """
    Section created by me and Chatgpt for AbilityOnCooldownErrorDecrement
    Ensure the character has an 'abilities' dict set up.

    Format:
    character['abilities'] = {
        'Power Strike': {'cooldown': 0, 'max_cooldown': 3},
        ...
    }

    This function will not overwrite existing abilities but will create
    a sensible default based on class if none exist.
    """
    if 'abilities' not in character:
        character['abilities'] = {}

    # If abilities dict empty, populate a default ability keyed by class
    if not character['abilities']:
        cls = character.get('class', '').lower()
        if cls == 'warrior':
            character['abilities']['Power Strike'] = {'cooldown': 0, 'max_cooldown': 3}
        elif cls == 'mage':
            character['abilities']['Fireball'] = {'cooldown': 0, 'max_cooldown': 3}
        elif cls == 'rogue':
            character['abilities']['Critical Strike'] = {'cooldown': 0, 'max_cooldown': 3}
        elif cls == 'cleric':
            character['abilities']['Heal'] = {'cooldown': 0, 'max_cooldown': 3}
        else:
            # generic ability fallback
            character['abilities']['Special'] = {'cooldown': 0, 'max_cooldown': 3}


def is_ability_available(character, ability_name):
    """
    Section created by me and Chatgpt for AbilityOnCooldownErrorDecrement
    Return True if ability exists and cooldown == 0.
    """
    ensure_abilities_initialized(character)
    ability = character['abilities'].get(ability_name)
    if ability is None:
        return False
    return int(ability.get('cooldown', 0)) == 0


def set_ability_cooldown(character, ability_name):
    """
    Section created by me and Chatgpt for AbilityOnCooldownErrorDecrement
    Set the ability's cooldown to its max_cooldown (if defined).
    If ability not found, do nothing.
    """
    ensure_abilities_initialized(character)
    ability = character['abilities'].get(ability_name)
    if not ability:
        return
    max_cd = ability.get('max_cooldown', 0)
    # set cooldown to max_cooldown (do not decrement here)
    ability['cooldown'] = int(max_cd)


def decrement_ability_cooldowns(character):
    """
    Section created by me and Chatgpt for AbilityOnCooldownErrorDecrement
    cooldowns for all abilities on the character by 1 (to minimum 0).

    This function exists because the combat loop expects ability cooldowns to be
    decremented at the end of player turns.
    """
    if 'abilities' not in character:
        # Nothing to do
        return

    abilities = character['abilities']
    if not isinstance(abilities, dict):
        # malformed; don't crash
        return

    for ability_name in abilities:
        ability = abilities[ability_name]
        if 'cooldown' in ability and isinstance(ability['cooldown'], int):
            if ability['cooldown'] > 0:
                ability['cooldown'] -= 1
                if ability['cooldown'] < 0:
                    ability['cooldown'] = 0
                    
def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    if character.get('health', 0) > 0 and not character.get('in_battle', False):
        return True
    return False

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    xp_amount = enemy.get('xp_reward', 0)
    gold_amount = enemy.get('gold_reward', 0)
    return {'xp': xp_amount, 'gold': gold_amount}

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print("\n" + character.get('name', 'Player') + ": HP=" + str(character.get('health', 0)) + "/" + str(character.get('max_health', 0)))
    print(enemy.get('name', 'Enemy') + ": HP=" + str(enemy.get('health', 0)) + "/" + str(enemy.get('max_health', 0)))

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")

    # Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }

    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")
