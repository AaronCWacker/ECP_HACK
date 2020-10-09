import dbase.sql_utils as sql_utils
import definitions
import importlib
import charts.plotter as plotter

from os import path
from datetime import datetime
from EmailReport import EmailReport
from utils.file_writer import SafeTextFileWriter


def email_sql_reports(module: str, sql_report_list: list, email_list: list, embed: bool, env: str = '') -> str:
    """Given a module, a list of sql reports, and a list of email addresses, create and email the reports.
    """
    if not sql_report_list:
        return f'No reports specified. {sql_report_list}'
    if not email_list:
        return f'No email recipients. {email_list}'

    module_dir = module.replace('.', '/')
    module_dir = f'{definitions.get_project_root()}/{module_dir}'
    now = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    response_str = f'Find reports in {module_dir}. Report names match the SQL file names minus the ".sql".\n'
    files_to_send = []
    plots = plotter.plotter()
    for sql_report in sql_report_list:
        print(f'Working on report {sql_report}')
        sql_file_name = f'{module_dir}/{sql_report}.sql'
        if path.exists(sql_file_name):
            data_frame = sql_utils.read_data_frame(sql_file_name)
            if path.exists(f'{module_dir}/{sql_report}.py'):
                m1 = importlib.import_module(f'{module}.{sql_report}')
                data_frame = m1.modify_dataframe(data_frame)
            data_uri_html = data_frame.to_html(classes="hsc", table_id='report', justify='left', index=False)
            # data_uri_html = json2html.convert(json=items, table_attributes='class="hsc"')

            file_name = f'{sql_report}_{now}.csv'
            response_str += f'\tCreated report "{sql_report}" in file \n\t    "{file_name}".\n'
            # save file
            safe_writer = SafeTextFileWriter(f'{sql_report}_{now}', '')
            full_file_name_csv = safe_writer.full_path_plus_file_name('csv')
            ##   full_file_name_html = safe_writer.save_html_report_file(data_uri_html, env.upper())    <<<<<<<<< This isn't working. I'll skip it for now.
            # email file
            print('email config', env)
            data_frame.to_csv(full_file_name_csv, index=False)
            #  files_to_send.append(full_file_name_html)                      <<<<<<<<<<<<<<<    And this one
            files_to_send.append(full_file_name_csv)
            graph_file = plots.bar_plot(data_frame, sql_report)
            if graph_file:
                files_to_send.append(graph_file)
            # I can put a file into the sql directory with a type of 'plot' and
            #   the same name as the SQL file. If it exists,
            # Better idea - one csv file that has a list of all the plottable queries, with the data elements.
            #    It's also easier to deal with in the code.
            #    If I want to get really fancy, I can use it for different kinds of plots.
            #
            #   Just to get things working, I'm going to use proc code as x-axis.      <<<<<<<<<<<<<<<<<<<<<<<
            #     Eventually, will need to figure out what it really should be. I'll probably need
            #       a new (derived) column in the output.
            #
            #   I will call the plotter, passing in the dataframe
            # I may want to update file_writer (SafeWriter) to write the plot. It will be html; not sure if I cam
            #   use the existing html method.
            # Need to look into that
        else:
            response_str += f'\tCould not create report "{sql_report}".\n'
        print(f'Finished with report {sql_report}')

    if files_to_send:
        print(f'Emailing files {files_to_send}')
        email_report = EmailReport(embed)
        email_report.send_report(files_to_send, email_list, subject_addendum=env.upper())
    return response_str

