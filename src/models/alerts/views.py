from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/')
def index():
    return 'This is the alerts index'

@alert_blueprint.route('/new', methods=['POST', 'GET'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = request.form['price_limit']
        print(name)
        print(url)
        print(price_limit)
        item = Item(name, url)
        print(item)
        item.save_to_mongo()
        #
        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()
    return render_template('alerts/new_alert.jinja2')

@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    pass

@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.jinja2', alert=alert)


