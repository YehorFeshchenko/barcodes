from flask import Blueprint
from Server.controllers.componentController import *

blueprint = Blueprint('components', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/all', methods=['GET'])(components)
blueprint.route('/barcode', methods=['POST'])(read_barcode)
blueprint.route('/add', methods=['POST'])(add_component)
