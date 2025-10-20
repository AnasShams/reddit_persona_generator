#!/usr/bin/env python3
"""
Reddit User Persona Generator - Flask Web Application
"""

from flask import Flask, render_template, request, jsonify, send_file
import sys
import os
import json
import time
from datetime import datetime
from reddit_scraper import RedditScraper
from persona_generator import PersonaGenerator
import logging

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_persona():
    """Generate persona from Reddit profile URL"""
    try:
        # Get JSON data from frontend
        data = request.get_json()
        logger.info(f"Received data: {data}")
        
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
        
        profile_url = data['url'].strip()
        logger.info(f"Processing URL: {profile_url}")
        
        # Validate URL format
        if not profile_url.startswith("https://www.reddit.com/user/"):
            return jsonify({'error': 'Please provide a valid Reddit user profile URL. Format: https://www.reddit.com/user/username/'}), 400
        
        # Extract username from URL
        username = profile_url.split("/user/")[1].rstrip("/")
        logger.info(f"Extracted username: {username}")
        
        # Initialize scraper and generator
        scraper = RedditScraper()
        persona_generator = PersonaGenerator()
        
        # Scrape user data
        logger.info("Scraping Reddit data...")
        user_data = scraper.scrape_user_profile(username)
        
        logger.info(f"Scraped data - Posts: {len(user_data.get('posts', []))}, Comments: {len(user_data.get('comments', []))}")
        
        if not user_data or (not user_data.get('posts') and not user_data.get('comments')):
            return jsonify({'error': 'Failed to scrape user data. User might not exist, profile is private, or has no public posts/comments.'}), 404
        
        # Generate persona
        logger.info("Generating user persona...")
        persona = persona_generator.generate_persona(user_data)
        
        logger.info(f"Persona generated successfully. Length: {len(persona)} characters")
        
        # Return the persona - make sure it's properly formatted
        return jsonify({
            'success': True,
            'username': username,
            'persona': persona,
            'stats': {
                'posts': len(user_data.get('posts', [])),
                'comments': len(user_data.get('comments', []))
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating persona: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
@app.route('/download/<username>')
def download_persona(username):
    """Download the generated persona file"""
    try:
        output_filename = f"sample_outputs/{username}_persona.txt"
        if os.path.exists(output_filename):
            return send_file(
                output_filename,
                as_attachment=True,
                download_name=f"{username}_persona.txt",
                mimetype='text/plain'
            )
        else:
            return jsonify({'error': 'Persona file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)