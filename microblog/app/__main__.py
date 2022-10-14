from .app import app

if __name__ == "__main__":
    print("Hello world")
    app.run(debug=True, host="0.0.0.0")
