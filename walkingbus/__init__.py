from flask import Flask, redirect, flash, request, url_for, render_template
from flask_login import LoginManager
from flask_sqlalchemy import Model as BaseModel
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import FlaskConfig


class ModelMixin(BaseModel):

    @classmethod
    def commit(cls):
        return db.session.commit()

    @classmethod
    def add(cls, commit: bool = False, **kwargs):
        model = cls(**kwargs)
        db.session.add(model)
        if commit:
            cls.commit()
        return model

    def tojson(self):
        serializable = {}
        for name in dir(self):
            attr = getattr(self, name)
            if not name.startswith('_') and (isinstance(attr, str) or isinstance(attr, int) or 
               isinstance(attr, float) or isinstance(attr, bool) or isinstance(attr, dict) or 
               isinstance(attr, list) or hasattr(attr, 'tojson') or attr is None):
                serializable[name] = attr
        return serializable

    def update(self, obj: dict, commit: bool = False, **kwargs):
        if obj and kwargs:
            raise TypeError('Undefined behaviour: cannot call update() with both obj and kwargs passed.')
        elif kwargs:
            obj: dict = kwargs
        for name, value in obj.items():
            setattr(self, name, value)

        if commit:
            self.commit()
        return self

    def delete(self, commit: bool = False):
        db.session.delete(self)
        if commit:
            self.commit()


app = Flask(__name__, static_folder='assets')
app.config.from_object(FlaskConfig)

db = SQLAlchemy(app, model_class=ModelMixin)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

from .models import Parent, Child, School, Group


@app.route('/')
def index():
    return render_template('index.html')