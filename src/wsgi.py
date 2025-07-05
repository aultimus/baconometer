from app import create_app

# Only create the app if this file is run directly OR imported by Gunicorn
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
