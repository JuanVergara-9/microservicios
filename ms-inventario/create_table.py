from app import create_app, db

def create_table():
    app = create_app()
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_table()