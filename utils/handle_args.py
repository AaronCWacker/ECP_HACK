from flask_restful import Api, Resource, reqparse, abort

ARG_SITE = 'site'
ARG_USERNAME = 'userName'
ARG_PASSWORD = 'password'
ARG_RECORDCOUNT = 'recordCount'
ARG_HSC_LIST_SQL_SELECTED = 'hscListSqlSelected'


class DbaseArgs:
    def __init__(self, parser: reqparse.RequestParser):
        args = parser.parse_args()
        self.site = args[ARG_SITE]
        self.userName = args[ARG_USERNAME]
        self.password = args[ARG_PASSWORD]


def abort_missing_args(parser):
    args = parser.parse_args()

    messages = ""
    for item in parser.args:
        if not args[item.name]:
            messages += "Parameter '{}' is empty. {} is required. <br>".format(item.name, item.help)
    if messages:
        abort(404, message=messages)

    return args


def parse_dbase_args(parser):
    parser.add_argument(ARG_SITE, type=str, help='Database to access', required=True)
    parser.add_argument(ARG_USERNAME, type=str, help='Database user name', required=True)
    parser.add_argument(ARG_PASSWORD, type=str, help='Database password', required=True)
    abort_missing_args(parser)
    return DbaseArgs(parser)


if __name__ == '__main__':
    rp = reqparse.current_app
    parse_dbase_args(rp)
