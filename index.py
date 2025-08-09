from app import app

# Vercel expects this for Python apps
def handler(request, context):
    return app.wsgi_app(request.environ, context)

# For direct execution
if __name__ == '__main__':
    app.run()
