import json
import os
import random
import sys
import time

# Constants
LIVES = 3
COINS_PER_CORRECT = 10
QUESTIONS_PER_QUIZ = 10


class InvalidQuestionFileError(Exception):
    pass


class QuestionFileNotFoundError(Exception):
    pass


# Clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Loading animation
def loading(message="Loading", duration=1):
    print()
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
        raise InvalidQuestionFileError("\n     Expected questions to be a dictionary at the top level.")

    for category, levels in questions.items():
        if not isinstance(levels, dict):
            raise InvalidQuestionFileError(f"\n     In category '{category}', expected a dictionary for difficulty levels.")

        for difficulty, q_list in levels.items():
            if not isinstance(q_list, list):
                raise InvalidQuestionFileError(
                    f"\n     In category '{category}' under difficulty '{difficulty}', "
                    f"expected a list of questions but got {type(q_list).__name__}."
                )

            for i, q in enumerate(q_list):
                if not isinstance(q, dict):
                    raise InvalidQuestionFileError(
                        f"\n     In category '{category}', difficulty '{difficulty}', question index {i}: "
                        f"expected a dictionary for a question but got {type(q).__name__}."
                    )

                required_keys = {'question', 'options', 'answer'}
                missing_keys = required_keys - q.keys()
                if missing_keys:
                    raise InvalidQuestionFileError(
                        f"\n     In category '{category}', difficulty '{difficulty}', question index {i}: "
                        f"missing required keys: {', '.join(missing_keys)}."
                    )

                if not isinstance(q['options'], list):
                    raise InvalidQuestionFileError(
                        f"\n     In category '{category}', difficulty '{difficulty}', question index {i}: "
                        f"'options' must be a list, got {type(q['options']).__name__}."
                    )

                if q['answer'] not in q['options']:
                    raise InvalidQuestionFileError(
                        f"\n     In category '{category}', difficulty '{difficulty}', question index {i}: "
                        f"'answer' value '{q['answer']}' not found in options: {q['options']}."
                    )
    return True


# Load questions
def load_questions():
    try:
        if not os.path.exists('questions.json'):
            raise QuestionFileNotFoundError("\n     'questions.json' file not found.")

        with open('questions.json') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise InvalidQuestionFileError(f"\n     Invalid questions file format -> {e}")


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



def print_question_analytics(questions):
    print("\n📊 Available Question Analytics:\n")
    for category, levels in questions.items():
        total = sum(len(questions[category][difficulty]) for difficulty in levels)
        label = "Questions" if total > 1 else "Question"
        print(f"{category} - {total} {label}")
        for difficulty, q_list in levels.items():
            label2 = "Questions" if len(q_list) > 1 else "Question"
            print(f" - {difficulty}: {len(q_list)} {label2}")
        print()
    print("💡 You can add your own questions to the 'questions.json' file to expand the quiz!\n")
    input("Press enter to continue ...")
    clear_screen()


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
            answer = int(input("Your answer (1-4): ").strip())
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
            raise InvalidQuestionFileError(f"\n     Question file is malformed. Please check 'questions.json'.")

        print("🧠 Welcome to Quiz Quest! 🧠\n")
        while True:
            nickname = input("Enter your nickname: ").strip().title()
            if nickname:
                break
            print("⚠️  Nickname cannot be empty.\n")
        
        avatar = choose_avatar()
        loading("Loading your adventure")
        clear_screen()

        while True:
            print("\n=== MAIN MENU ===")
            print("1. Take Quiz")
            print("2. View Leaderboard")
            print("3. View Question Analytics")
            print("4. Exit")

            choice = input("Choose an option: ").strip()

            if choice == '1':
                if not questions:
                    print("⚠️  No questions available. Please check the questions file.")
                    continue

                loading("Loading quiz categories")
                clear_screen()

                while True:
                    print("\nAvailable Categories:")
                    category_list = list(questions.keys())
                    for i, cat in enumerate(category_list, start=1):
                        print(f"{i}. {cat}")
                    print("Type 'back' to return to the main menu.")

                    category_input = input("Enter category: ").strip().title()

                    if category_input.lower() == "back":
                        loading()
                        clear_screen()
                        break

                    # Check if input is a number
                    if category_input.isdigit():
                        cat_index = int(category_input) - 1
                        if 0 <= cat_index < len(category_list):
                            category = category_list[cat_index]
                        else:
                            print("⚠️  Invalid category number.")
                            continue
                    elif category_input in category_list:
                        category = category_input
                    else:
                        print("⚠️  Invalid category.")
                        continue

                    while True:
                        available_difficulties = list(questions[category].keys())
                        print("\nAvailable Difficulties:")
                        for i, difficulty in enumerate(available_difficulties, start=1):
                            print(f"{i}. {difficulty}")
                        print("Type 'back' to return to the main menu.")

                        difficulty_input = input("Choose difficulty: ").strip().title()

                        if difficulty_input.lower() == "back":
                            loading()
                            clear_screen()
                            break

                         # Check if input is a number
                        if difficulty_input.isdigit():
                            diff_index = int(difficulty_input) - 1
                            if 0 <= diff_index < len(available_difficulties):
                                difficulty = available_difficulties[diff_index]
                            else:
                                print("⚠️  Invalid difficulty number.")
                                continue
                        elif difficulty_input in available_difficulties:
                            difficulty = difficulty_input
                        else:
                            print("⚠️  Invalid difficulty.")
                            continue

                        if not questions[category][difficulty]:
                            print("⚠️  No questions available at this difficulty.")
                            continue

                        score = start_quiz(questions, category, difficulty)
                        loading("Saving your score", duration=3)
                        save_leaderboard(nickname, avatar, score)
                        clear_screen()
                        break
                    break  # break category loop after quiz is done

            elif choice == '2':
                loading("Loading leaderboard")
                clear_screen()
                show_leaderboard()

            elif choice == '3':
                loading("Loading question analytics")
                clear_screen()
                print_question_analytics(questions)

            elif choice == '4':
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
        print(f"\n⚠️  An unexpected error occurred: {e}")
        print("\nExiting due to error")
        sys.exit(1)


if __name__ == "__main__":
    loading("Starting Quiz Quest")
    main()
    clear_screen()
