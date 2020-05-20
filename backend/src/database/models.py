import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()


# Binds Flask Application with SQLAlchemy
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Drop DB and Creat DB
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


# Drink Model
class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': str, 'name':str, 'parts':str}]
    recipe = Column(String(180), nullable=False)

    # Short Form Represenation
    def short(self):
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']}
                        for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    # Long Form Represenation
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    # Insert

    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Update
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
