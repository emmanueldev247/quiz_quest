import json
import os
import random
import sys
import time

# Constants
LIVES = 3
COINS_PER_CORRECT = 10
QUESTIONS_PER_QUIZ = 10


# Clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Loading animation
def loading(message="Loading", duration=1):
    print(message, end='', flush=True)
    steps = max(1, int(duration * 3))
    for _ in range(steps):
        time.sleep(0.3)
        print('.', end='', flush=True)
    print()  # Move to new line after loading


# Choose an avatar
def choose_avatar():
    avatar_choices = ['🧠', '🐉', '⚔️', '🦸', '👽', '🤖', '🎓']
    print("\nChoose an avatar by typing the number (or press Enter to skip):")
    for i, avatar in enumerate(avatar_choices, 1):
        print(f"  {i}. {avatar}")
    
    while True:
        choice = input("Your choice (1-7 or Enter to skip): ").strip()
        if choice == "":
            return "👤"  # Default avatar
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(avatar_choices):
                return avatar_choices[choice - 1]
        print("⚠️  Invalid choice. Please enter a number between 1-7 or press Enter.\n")


# Validate questions structure
def validate_questions(questions):
    if not isinstance(questions, dict):
        return False
    for category, levels in questions.items():
        if not isinstance(levels, dict):
            return False
        for difficulty, q_list in levels.items():
            if not isinstance(q_list, list):
                return False
            for q in q_list:
                if not all(k in q for k in ['question', 'options', 'answer']):
                    return False
    return True


# Load questions
def load_questions():
    with open('questions.json') as f:
        return json.load(f)


# Save leaderboard
def save_leaderboard(nickname, avatar, score):
    filename = 'leaderboard.json'
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                leaderboard = json.load(f)
        except json.JSONDecodeError:
            leaderboard = []
    else:
        leaderboard = []

    leaderboard.append({'nickname': nickname, 'avatar': avatar, 'score': score})
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    leaderboard = leaderboard[:5]

    with open(filename, 'w') as f:
        json.dump(leaderboard, f, indent=2)


# Show leaderboard
def show_leaderboard():
    print("\n🏆 Leaderboard:")
    try:
        with open('leaderboard.json') as f:
            data = json.load(f)
            for i, entry in enumerate(data, 1):
                print(f"{i}. {entry['avatar']}  {entry['nickname']} - {entry['score']} coins")
    except (json.JSONDecodeError, FileNotFoundError):
        print("No leaderboard data yet.")


# Quiz logic
def start_quiz(questions, category, difficulty):
    loading("Starting quiz")
    clear_screen()

    selected = questions[category][difficulty]
    score = 0
    lives = LIVES

    print(f"\n🎮 Starting quiz: {category} - {difficulty}")
    random.shuffle(selected)

    for item in selected[:QUESTIONS_PER_QUIZ]:
        print(f"\n❓ {item['question']}")
        for i, option in enumerate(item['options'], 1):
            print(f"  {i}. {option}")
        try:
            answer = int(input("Your answer (1-4): "))
            if answer < 1 or answer > 4:
                raise IndexError

            if item['options'][answer - 1].lower() == item['answer'].lower():
                print("✅ Correct!")
                score += COINS_PER_CORRECT
            else:
                print(f"❌ Wrong! Correct answer: {item['answer']}")
                lives -= 1

        except ValueError:
            print("⚠️  Invalid input. Skipping.")
            lives -= 1
            continue

        except IndexError:
            print("⚠️  Invalid option number. You must choose between 1-4.")
            lives -= 1

        if lives == 0:
            print("\n💀 You've lost all your lives!")
            break

    print(f"\n🎉 Quiz complete! You scored {score} coins.")
    return score


# Main menu
def main():
    try:
        clear_screen()
        questions = load_questions()
        if not validate_questions(questions):
            print("⚠️ Question file is malformed. Please check 'questions.json'.")
            loading("Exiting due to error")
            clear_screen()
            sys.exit(1)

        print("🧠 Welcome to Quiz Quest! 🧠\n")
        while True:
            nickname = input("Enter your nickname: ").strip()
            if nickname:
                break
            print("⚠️  Nickname cannot be empty.\n")
        
        avatar = choose_avatar()
        loading("Loading your adventure")
        clear_screen()

        while True:
            print("\n=== MAIN MENU ===")
            print("1. Play Quiz")
            print("2. View Leaderboard")
            print("3. Exit")

            choice = input("Choose an option: ")

            if choice == '1':
                if not questions:
                    print("⚠️  No questions available. Please check the questions file.")
                    continue

                loading("Loading quiz categories")
                clear_screen()

                while True:
                    print("\nAvailable Categories:")
                    for cat in questions:
                        print(f"- {cat}")
                    print("Type 'back' to return to the main menu.")

                    category = input("Enter category: ").capitalize()

                    if category.lower() == "back":
                        loading()
                        clear_screen()
                        break

                    if category in questions:
                        # Proceed to difficulty selection
                        while True:
                            available_difficulties = list(questions[category].keys())
                            print("\nAvailable Difficulties:")
                            for difficulty in available_difficulties:
                                print(f"- {difficulty}")
                            print("Type 'back' to return to the main menu.")

                            difficulty = input("Choose difficulty: ").capitalize()
                            
                            if difficulty.lower() == "back":
                                loading()
                                clear_screen()
                                break                            

                            
                            if difficulty not in questions[category] or not isinstance(questions[category][difficulty], list):
                                print("⚠️ Invalid or empty difficulty set.")
                                continue
                            
                            if not questions[category][difficulty]:
                                print("⚠️ No questions available at this difficulty.")
                                continue

                            if difficulty in available_difficulties:
                                score = start_quiz(questions, category, difficulty)
                                loading("Saving your score", duration=3)
                                save_leaderboard(nickname, avatar, score)
                                clear_screen()
                                break
                            else:
                                print("⚠️ Invalid difficulty. Please choose from the available options.")
                        break  # break category loop after quiz is done
                    else:
                        print("⚠️ Invalid category.")

            elif choice == '2':
                loading("Loading leaderboard")
                clear_screen()
                show_leaderboard()

            elif choice == '3':
                print("\n👋 Goodbye!")
                loading("Exiting Quiz Quest", duration=2)
                break

            else:
                print("❌  Invalid input.")

    except KeyboardInterrupt:
        print("\n👋 Closing Quiz Quest. See you next time!")
        loading("Exiting", duration=2)
        clear_screen()
        sys.exit(0)

    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")
        loading("Exiting due to error", duration=2)
        clear_screen()
        sys.exit(1)


if __name__ == "__main__":
    loading("Starting Quiz Quest")
    main()
    clear_screen()
