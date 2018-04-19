from flask import Flask, Blueprint
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

from app.HostAPI.routes import mod
from app.ClientAPI.routes import mod

app.register_blueprint(HostAPI.routes.mod)
app.register_blueprint(ClientAPI.routes.mod, url_prefix='/store')
