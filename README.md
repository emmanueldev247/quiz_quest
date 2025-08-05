# 🎮 Quiz Quest CLI

**Quiz Quest** is a **gamified command-line quiz app** built with Python, designed to engage teenagers (ages 14–17) in a fun, educational way.

It’s perfect for learning programming through a playful project, introducing concepts like:
- Input/output
- Data structures
- Control flow
- File handling
- Error handling
- Basic gamification


## 🚀 Features

- 🧑‍🎓 **User Profiles**: Nickname and avatar selection
- 🧠 **Quiz Categories**: Science, Math and more
- 🎯 **Difficulty Levels**: Easy, Medium, Hard
- ❤️ **Lives**: Lose lives on wrong answers
- 💰 **Coins**: Earn coins for correct answers
- 🏆 **Local Leaderboard**: Save and show top scores


## 🛠 Tech Stack

- **Language**: Python 3
- **Libraries**: `json`, `os`, `random`, `sys`, `time` 
- **Interface**: Pure command-line interface (CLI)
- **Storage**: Local `JSON` files


## 📁 Project Structure

```yaml

quiz-quest-cli/
│
├── quiz_quest.py # Main game logic
├── questions.json # Quiz database
├── leaderboard.json # Local leaderboard (auto-generated)
└── README.md # Project info
```


## 💻 Setup Instructions

1. **Clone the repo**:
```bash
git clone https://github.com/emmanueldev247/quiz_quest.git
cd quiz-quest-cli
```

2. **Run the app**:
```bash
python3 quiz_quest.py
```
3. **Optional:** Add your own questions to questions.json

## 🧪 Sample Questions Format (questions.json)
```json
{
  "Science": {
    "Easy": [
      {
        "question": "What planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
      }
    ]
  }
}
```

## 🧑‍🏫 Ideal For
* Teaching beginner coding concepts
* Teen-friendly coding workshops or bootcamps
* Offline learning environments
* CLI project-based learning

## 🤝 Contribution Guide
I welcome your contributions!

* Fork the repo
* Create a branch (feature/my-feature)
* Commit changes (git commit -m 'Add feature')
* Push and open a pull request


## 📄 License
This project is licensed under the [MIT License](./LICENSE).

&copy; 2025 [Emmanuel Ademola](https://emmanueldev247.publicvm.com/)
