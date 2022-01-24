from src.app import app, db


def create_db():
    print(f'db_start: {db}')
    db.drop_all()
    db.create_all()
    db.session.commit()
    print(f'db_commit: {db}')


if __name__ == "__main__":
    print('Within the main function and invoking createdb')
    create_db()
    print('Completed invoking createdb function')
    app.run(debug=True, host="0.0.0.0")
