from src.app import app, db


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    create_db()
    app.run(debug=True, host="0.0.0.0")
