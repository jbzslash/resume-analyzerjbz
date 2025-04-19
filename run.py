import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Use the port provided by Render or default to 5000 if not available
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
