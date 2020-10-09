import glob
from flask import Markup

SERVER_OPTIONS = [{'text': 'Local Host', 'value': '127.0.0.1'},
                  {'text': 'Test weved23962', 'value': '10.201.144.167'},
                  {'text': 'Stage weves31263', 'value': '10.50.8.130'},
                  {'text': 'Prod wevep31172', 'value': '10.48.164.198'}
                  ]


def server_options(ip_address: str) -> Markup:
    return Markup(SERVER_OPTIONS)


def sql_options(base_dir: str) -> [Markup, str]:
    """Create an option list based on files in the directory.
    
    :param base_dir: where the sql files are located  
    :return: list of options 
    """
    pattern = f'{base_dir}/*.sql'
    files = glob.glob(pattern, recursive=True)

    options = ''
    first = True
    first_file = ''
    for file in files:
        file = file.replace('\\', '/')
        description = file.replace('.sql', '').replace('_', ' ')
        last_count = description.rfind('/') + 1
        description = description[last_count:]
        # print(description)
        if first:
            options += f'<option value="{file}" selected="selected">{description}</option>\n'
            first_file = file
            first = False
        else:
            options += f'<option value="{file}">{description}</option>\n'
    return Markup(options), first_file


def vue_sql_select(base_dir: str) -> [Markup, str]:
    """Create an option list based on files in the directory.

    :param base_dir: where the sql files are located
    :return: list of options
    """
    pattern = f'{base_dir}/*.sql'
    files = glob.glob(pattern, recursive=True)

    options = []
    first = True
    first_file = ''
    for file in files:
        file = file.replace('\\', '/')
        description = file.replace('.sql', '').replace('_', ' ')
        last_count = description.rfind('/') + 1
        description = description[last_count:]
        # print(description)
        if first:
            first_file = file
            first = False
        # options += f"{{text: '{description}', value: '{file}'}},"
        options.append({'text': f'{description}', 'value': f'{file}'})
    return Markup(options), first_file


if __name__ == '__main__':
    print(vue_sql_select('../sql/pa_related/care_guidance'))
    print(sql_options('../sql/pa_related/care_guidance'))
