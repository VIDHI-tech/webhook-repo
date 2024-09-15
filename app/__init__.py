from flask import Flask, jsonify,render_template
from .extensions import init_mongo
from .webhook.routes import webhook

def create_app():
    app = Flask(__name__)

    # Initialize MongoDB
    mongo = init_mongo(app)

    # Register the webhook blueprint
    app.register_blueprint(webhook)

    # Attach the MongoDB collection to the webhook blueprint
    webhook.collection = mongo.db['events']

    # Serve the frontend
    @app.route('/')
    def index():
        return render_template('index.html')

    # API to get events for the UI
    @app.route('/get_events', methods=['GET'])
    def get_events():
        # Fetch the latest 10 events
        events = list(mongo.db['events'].find().sort('timestamp', -1).limit(10))
        
        # Convert ObjectId to string for each event
        for event in events:
            event['_id'] = str(event['_id'])
        
        return jsonify(events)

    return app
