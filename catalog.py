from app import app, db
from app.models.category import Category
from app.models.item import Item
from app.models.user import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Category': Category, 'Item': Item}
