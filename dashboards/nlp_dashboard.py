import utils.handle_args as arg_handler
from flask_restful import Resource
from flask_restful import reqparse
from utils.print_enh import print_begin
from utils.print_enh import print_end


class NlpDashboard(Resource):
    def post(self, sql_call):
        print_begin(sql_call)
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(arg_handler.ARG_RECORDCOUNT, type=str, help='record count', required=False)

        print_end(sql_call)
