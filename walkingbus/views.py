from . import app
from .models import Parent


@app.route('/')
def index():
    return 'Hello, World!'
