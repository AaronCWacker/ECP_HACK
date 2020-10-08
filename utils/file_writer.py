import os
import definitions
# import pdfkit
import threading

from config.config_rw import ConfigRW
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from definitions import Settings

config_rw = ConfigRW(Settings.PRIOR_AUTH_SETTINGS.value)
config_settings = config_rw.read_settings()
date_time_stamp = datetime.now().strftime('%Y%m%d')
report_name = config_settings.report_name
report_save_path = config_settings.report_save_path
report_file_name = config_settings.report_file_name
report_file_extension = config_settings.report_file_extension
report_templates_path = config_settings.report_templates_path
report_templates_name = config_settings.report_templates_name


class SafeTextFileWriter:
    file_lock = threading.Lock()
    templates_dir = os.path.join(definitions.get_project_root(), report_templates_path)

    def __init__(self, base_file_name: str, first_line: str):
        self.base_file_name = base_file_name
        self.first_line = first_line

    def write_line(self, line: str):
        with self.file_lock:
            with open(self.base_file_name, 'a') as fh:
                if fh.tell() == 0:
                    fh.write(f'{self.first_line}\n')
                fh.write(f'{line}\n')

    def full_path_plus_file_name(self, ext: str) -> str:
        return (f'{definitions.get_project_root()}/{report_save_path}/{report_file_name}'
                f'{self.base_file_name}.{ext}')

    def save_html_report_file(self, result: str, env_str: str) -> str:
        # https://code-maven.com/minimal-example-generating-html-with-python-jinja
        env = Environment(loader=FileSystemLoader(self.templates_dir))

        # template = env.get_template(report_templates_path+report_templates_name+'.'+report_file_extension)
        template = env.get_template('mlpa_report_template.html')

        full_file_name_html = self.full_path_plus_file_name('html')
        display_file_name = self.base_file_name.replace('_', ' ')
        with open(full_file_name_html, 'w') as fh:
            fh.write(template.render(
                report_name=f'{display_file_name}',
                env_str=env_str,
                data=result
            ))
        return full_file_name_html


if __name__ == '__main__':
    my_file_name = datetime.now().strftime('Test_%Y%M%d_%H')
    safe_file_writer = SafeTextFileWriter(my_file_name, 'SRN,HSC')
    # safe_file_writer.write_line('A0,12345')
    safe_file_writer.save_html_report_file('result here', 'env')
