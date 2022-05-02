import os

from src import create_app

app = create_app()
app.app_context().push()

from src import db

if __name__ == '__main__':
    db.create_all()
    app.run(
        debug=True,
        port=os.getenv("PORT")
    )
