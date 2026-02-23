# app/routes/ia_chat.py
# AI Chat functionality - handles the chat interface and API endpoints

from flask import Blueprint, request, jsonify, render_template
from app.utils.ia_engine import IAEngine

# Create blueprint for AI chat routes
# The base URL is /ia (set in __init__.py with url_prefix)
ia_chat_bp = Blueprint('ia_chat', __name__)

# Initialize the AI engine that connects to DeepSeek API
engine = IAEngine()

@ia_chat_bp.route('/')
def index():
    """
    Main chat page route
    Renders the chat interface where users can interact with the AI
    Returns: HTML page with chat UI (ia_chat.html)
    """
    return render_template('ia_chat.html')

@ia_chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint for chat messages
    Expects a JSON with 'pregunta' field containing the user's question
    Returns: JSON with 'respuesta' field containing the AI's answer
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Extract the question, default to empty string if not provided
        question = data.get('pregunta', '')
        
        # Validate that a question was provided
        if not question:
            return jsonify({'respuesta': 'Please write a question.'}), 400
        
        # Generate response using the AI engine
        answer = engine.generar_respuesta(question)
        
        # Return the response as JSON
        return jsonify({'respuesta': answer})
    
    except Exception as e:
        # Handle any errors gracefully
        return jsonify({'respuesta': f'Error: {str(e)}'}), 500