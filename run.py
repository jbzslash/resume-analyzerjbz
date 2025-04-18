
from app import create_app

# Create and run the Flask app
app = create_app()

if __name__ == "__main__":
    # Start the Flask server on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
