import json
from reddit_scraper import RedditScraper
from persona_generator import PersonaGenerator

def handler(request):
    try:
        # Extract Reddit profile URL from query parameter
        profile_url = request.get("queryStringParameters", {}).get("url")

        if not profile_url or not profile_url.startswith("https://www.reddit.com/user/"):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Invalid or missing Reddit user URL"})
            }

        username = profile_url.split("/user/")[1].rstrip("/")

        scraper = RedditScraper()
        user_data = scraper.scrape_user_profile(username)

        if not user_data:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "User not found or profile is private"})
            }

        persona_generator = PersonaGenerator()
        persona = persona_generator.generate_persona(user_data)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "username": username,
                "persona": persona,
                "stats": {
                    "posts": len(user_data["posts"]),
                    "comments": len(user_data["comments"])
                }
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
