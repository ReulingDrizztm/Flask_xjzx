from flask import Blueprint

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')



@app.route('/')
def ():
    pass