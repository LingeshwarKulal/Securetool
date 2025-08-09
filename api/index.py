"""
Vercel API entry point
"""
from web_app import app

# This is the entry point for Vercel
def handler(request, context):
    return app(request.environ, context)

# For local development
if __name__ == '__main__':
    app.run(debug=True)
