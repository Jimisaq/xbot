# Simple Callback Server for X (Twitter) Developer App
# This server provides callback URLs for OAuth authentication (No Streaming API)

from flask import Flask, request, render_template_string, jsonify
import logging
from datetime import datetime
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Store callback data (in production, use a proper database)
callback_data = []

# HTML template for the callback page
CALLBACK_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>X App Callback Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #1DA1F2; margin-bottom: 30px; }
        .status { padding: 15px; border-radius: 5px; margin: 10px 0; }
        .success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .info { background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .callback-item { background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .timestamp { color: #6c757d; font-size: 0.9em; }
        .code { background: #f1f3f4; padding: 10px; border-radius: 3px; font-family: monospace; word-break: break-all; }
        .endpoint { background: #e7f3ff; padding: 10px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #1DA1F2; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🐦 X App Callback Server</h1>
        
        <div class="status success">
            <strong>✅ Server is running!</strong> Ready to receive OAuth callbacks.
        </div>
        
        <div class="endpoint">
            <h3>📍 Available Endpoints:</h3>
            <p><strong>OAuth Callback:</strong> <code>http://localhost:5000/callback</code></p>
            <p><strong>Webhook:</strong> <code>http://localhost:5000/webhook</code></p>
            <p><strong>Health Check:</strong> <code>http://localhost:5000/health</code></p>
        </div>

        {% if callback_data %}
        <h2>Recent Callbacks:</h2>
        {% for callback in callback_data %}
        <div class="callback-item">
            <div class="timestamp">{{ callback.timestamp }}</div>
            <h4>{{ callback.type }}</h4>
            {% if callback.oauth_token %}
                <p><strong>OAuth Token:</strong> <span class="code">{{ callback.oauth_token }}</span></p>
            {% endif %}
            {% if callback.oauth_verifier %}
                <p><strong>OAuth Verifier:</strong> <span class="code">{{ callback.oauth_verifier }}</span></p>
            {% endif %}
            {% if callback.code %}
                <p><strong>Authorization Code:</strong> <span class="code">{{ callback.code }}</span></p>
            {% endif %}
            {% if callback.error %}
                <p><strong>Error:</strong> <span style="color: red;">{{ callback.error }}</span></p>
            {% endif %}
        </div>
        {% endfor %}
        {% else %}
        <div class="status info">
            <strong>ℹ️ No callbacks received yet.</strong> 
            <p>Configure your X app to use <code>http://localhost:5000/callback</code> as the callback URL.</p>
        </div>
        {% endif %}
        
        <div style="margin-top: 30px; text-align: center; color: #6c757d;">
            <p>This server is running on port 5000. Add this URL to your X Developer App settings!</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page showing server status and recent callbacks"""
    return render_template_string(CALLBACK_TEMPLATE, callback_data=callback_data[-10:])  # Show last 10 callbacks

@app.route('/callback', methods=['GET', 'POST'])
def oauth_callback():
    """Handle OAuth callbacks from X"""
    try:
        # Get all parameters from the request
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        error_description = request.args.get('error_description')
        
        # Log the callback
        callback_info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'OAuth Callback',
            'oauth_token': oauth_token,
            'oauth_verifier': oauth_verifier,
            'code': code,
            'state': state,
            'error': error,
            'error_description': error_description,
            'method': request.method,
            'all_args': dict(request.args)
        }
        
        callback_data.append(callback_info)
        
        # Log to console
        if error:
            logging.error(f"OAuth Error: {error} - {error_description}")
        else:
            logging.info(f"OAuth Callback received: token={oauth_token}, verifier={oauth_verifier}")
        
        # Return success response
        if error:
            return f"""
            <h2 style="color: red;">OAuth Error</h2>
            <p><strong>Error:</strong> {error}</p>
            <p><strong>Description:</strong> {error_description}</p>
            <p><a href="/">← Back to main page</a></p>
            """, 400
        else:
            return f"""
            <h2 style="color: green;">OAuth Callback Received!</h2>
            <p><strong>Token:</strong> {oauth_token}</p>
            <p><strong>Verifier:</strong> {oauth_verifier}</p>
            <p><strong>Code:</strong> {code}</p>
            <p><a href="/">← View all callbacks</a></p>
            """
            
    except Exception as e:
        logging.error(f"Error handling callback: {e}")
        return f"Error: {e}", 500

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Handle webhook requests (for future use)"""
    try:
        if request.method == 'GET':
            # Handle webhook verification (CRC challenge)
            crc_token = request.args.get('crc_token')
            if crc_token:
                # In production, you'd validate this properly
                response_token = f"sha256={crc_token}"
                return jsonify({'response_token': response_token})
            return "Webhook endpoint is active"
        
        elif request.method == 'POST':
            # Handle webhook data
            data = request.get_json()
            webhook_info = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'Webhook',
                'data': data,
                'headers': dict(request.headers)
            }
            callback_data.append(webhook_info)
            logging.info(f"Webhook received: {data}")
            return "OK", 200
            
    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        return f"Error: {e}", 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'callbacks_received': len(callback_data)
    })

@app.route('/clear')
def clear_data():
    """Clear all callback data"""
    global callback_data
    callback_data = []
    logging.info("Callback data cleared")
    return '<h2>✅ Data cleared!</h2><p><a href="/">← Back to main page</a></p>'

if __name__ == '__main__':
    print("🚀 Starting X API Callback Server...")
    print("📍 Callback URL: http://localhost:5000/callback")
    print("🌐 Webhook URL: http://localhost:5000/webhook")
    print("🏠 Home page: http://localhost:5000/")
    print("\n💡 Add 'http://localhost:5000/callback' to your X Developer Portal app settings")
    print("⏹️  Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
