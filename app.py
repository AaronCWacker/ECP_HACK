import logging

# import utils.html_markup as markup
# from config.config_rw import ConfigRW
from dashboards.nlp_dashboard import NlpDashboard
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_cors import CORS
from inMemoryData.InMemoryManager import InMemoryManager

import definitions
# from definitions import Settings
from utils.print_enh import print_begin
from utils.print_enh import print_end

# from flask_swagger_ui import get_swaggerui_blueprint as get_blueprint
# from waitress import serve

# think of using connexion for swagger implementation
app = Flask(__name__,
            template_folder=f'{definitions.get_project_root()}/web',
            static_folder=f'{definitions.get_project_root()}/web')
CORS(app)
# DASHBOARD_PORT = 5000
my_ip_address = definitions.get_ip_address()
# BASE_URL = f'http://{my_ip_address}:{DASHBOARD_PORT}'
imm = InMemoryManager()

# def start_app() -> None:
current_logger = definitions.setup_logger(__name__, level=logging.DEBUG)


# current_logger.info(BASE_URL)
# app.run(host=ip_address, port=dashboard_port, threaded=True, debug=True)
# serve(app, host=my_ip_address, port=DASHBOARD_PORT, threads=20)


@app.route('/status')
def hello_world():
    """
    See if the application is up and running.
    :return: nothing
    ---
    tag:
        - status
    """
    print_begin()
    #  date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print_end()
    return f'<b>Hello World!</b> I\'m alive. prior_auth<p>'


@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template(f'temp/{page_name}.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Login
    :return: redirects to the page
    ---
    tag:
        - login
    """

    error = None
    try:
        user_name = request.form['userName']
    except Exception:
        user_name = ''

    print_begin()
    if request.method == 'POST' and user_name:
        # login_obj = Login()
        # success, display_name = login_obj.ldap_login(user_name, request.form['password'])
        # if success:
        return redirect(url_for('main_page', display_name=user_name))
        # else:
        #     error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error, user_name=user_name)


@app.route('/main_page/<display_name>')
def main_page(display_name):
    """
    :param display_name:hwo to get requirements.
    :return:
    ---
    tags:
        - main page
    """
    # config_rw = ConfigRW(Settings.PRIOR_AUTH_SETTINGS.value)
    print_begin()
    ip_address = definitions.get_ip_address()
    # server_options = markup.server_options(ip_address)
    return render_template('DashboardPriorAuth.html', error=None,
                           def_server_option=ip_address,
                           display_name=display_name,
                           )
    # server_options=server_options,


dashboard = NlpDashboard()


@app.route('/basic/<method_call>', methods=['POST'])
def main_dashboard(method_call):
    """
    Main application call
    :param method_call:
    :return:
    ---
    tags:
        - main dashboard
    """
    return dashboard.post(method_call)


@app.route('/search', methods=['POST'])
def search_data():
    """
    search for data with in pandas
    :param speech_text:
    :return:
    ---
    tags:
        - search text
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    speech_text = request.json.get("speech_text", None)

    if not speech_text:
        return jsonify({"msg": "Missing search parameter"}), 400

    return jsonify({"speech_text": f'{imm.dataframes_search(str(speech_text))}'}), 200

# if __name__ == '__main__':
#     start_app()
