import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Default to 10000 if no port is set
    app.run(host='0.0.0.0', port=port)
