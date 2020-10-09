from waitress import serve

import definitions
from app import app


if __name__ == '__main__':
    DASHBOARD_PORT = 5000
    IP_ADDRESS = definitions.get_ip_address()

    serve(app, host=IP_ADDRESS, port=DASHBOARD_PORT, threads=20)
