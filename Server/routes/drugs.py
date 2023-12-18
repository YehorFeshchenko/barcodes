from flask import Blueprint
from Server.controllers.drugController import *

blueprint = Blueprint('drugs', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/all', methods=['GET'])(drugs)
blueprint.route('/barcode', methods=['POST'])(readBarcode)
blueprint.route('/add', methods=['POST'])(addDrug)
