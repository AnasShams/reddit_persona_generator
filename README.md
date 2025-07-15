# Reddit User Persona Generator

A Python tool that scrapes a public Reddit user's posts and comments using Reddit's free JSON API (no login or API key required), and generates a detailed user persona with interests, personality traits, goals, frustrations, behavior, and citations.

---

## 🚀 Features

- ✅ **No Reddit API key needed** – Works entirely using Reddit's free public JSON endpoints
- 📊 **Scrapes posts + comments** – Pulls up to 300 recent items from a user’s profile
- 🧠 **Generates personas** – Analyzes interests, personality, behavior, goals, and frustrations
- 🔗 **Citations included** – Links to Reddit posts/comments are provided for traceability
- 💾 **Dual output** – Human-readable `.txt` + raw `.json` data saved in `sample_outputs/`
- 🧩 **Modular structure** – Clean and well-documented Python scripts

---

## 📁 Project Structure

reddit_persona_generator/
├── main.py # Entry point: takes Reddit profile URL as input
├── reddit_scraper.py # Scrapes posts/comments using Reddit's JSON API
├── persona_generator.py # Analyzes scraped text and generates persona
├── config.py # Global config (user agent, timeouts, limits)
├── requirements.txt # Python dependencies (currently just requests)
├── README.md # Documentation (this file)
└── sample_outputs/ # Output directory for generated personas


---

## 🔧 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/<your-username>/reddit-persona-generator.git
cd reddit-persona-generator
```

2. **Install the required Python package:**
```bash
pip install -r requirements.txt
```


---

## 🧪 Usage

Run the script with a Reddit user profile URL:

```bash
python main.py https://www.reddit.com/user/kojied/
```
This will:

-Scrape the user's public posts and comments

-Analyze their behavior, interests, and personality traits

-Save two output files to the sample_outputs/ folder:

--kojied_persona.txt — Human-readable summary

--kojied_raw_data.json — Raw post/comment data


---

## 📌 How It Works

1. **Scraping**
Uses https://www.reddit.com/user/{username}.json to fetch up to 3 pages of posts and comments with no authentication.

2. **Analysis**

-Extracts interests using keyword matching across categories like technology, gaming, food, etc.

-Detects personality traits (introvert, analytical, creative, etc.)

-Identifies behavior like post/comment frequency and subreddit activity

-Pulls out goals and frustrations from sentiment-rich phrases

3. **Output**

-Human-readable .txt persona

-Raw .json data for transparency and future reuse


---

## 🧾 Sample Output Preview

```yaml
USER PERSONA: kojied
============================================================

BASIC INFORMATION:
• Username: kojied
• Account Age: 734 days
• Total Karma: 1241
• Posts Created: 12
• Comments Made: 67

TOP SUBREDDITS:
• r/programming (22 interactions)
• r/gaming (18 interactions)

INTERESTS & HOBBIES:
• Technology: 36 mentions
  - Citation: r/programming - "I love working with AI models..."
    Link: https://www.reddit.com/r/programming/comments/abc123

...

Generated on: 2025-07-15 14:02:10
```


---

## 🐞 Troubleshooting

-❌ "User not found": Check for typos, private profiles, or deleted accounts

-⏱️ Slow responses: The tool waits 1 second between page requests to respect Reddit rate limits

-🛑 No output generated: The user may not have any public activity


---

## 📌 Requirements

-Python 3.7+

-requests==2.31.0

To install:

```bash
pip install -r requirements.txt
```


---

## 🧑‍💻 Developer Notes

-Code is PEP8 compliant and uses type annotations

-No external NLP or LLM libraries used — only lightweight keyword matching

-Highly modular: edit config.py to adjust scraping limits and persona parameters


---

## 📄 License

This tool is intended for educational and research purposes only.
Please respect Reddit's Terms of Service and users' privacy.


---

## 🙋 Support

Feel free to raise an issue or open a pull request if you have suggestions or bugs to report.


---