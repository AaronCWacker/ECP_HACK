import configparser
import cryptography
import definitions
import os
import socket


from cryptography.fernet import Fernet
from pathlib import Path

DEFAULT = 'DEFAULT'
TCPIP_DBASE = 'tcpip_dbase'
PAB = 'pab'


class ConfigSettings:
    def __init__(self, config_inst):
        self.db_site = config_inst.config_get(TCPIP_DBASE, 'site')
        self.db_user_name = config_inst.config_get(TCPIP_DBASE, 'user_name')
        self.db_password = config_inst.config_get(TCPIP_DBASE, 'user_password', encrypted=True)

        self.env = config_inst.config_get(DEFAULT, 'env')
        my_env = 'env_{}'.format(self.env)

        self.discharge_url = config_inst.config_get(my_env, 'discharge_url')
        self.alert_url = config_inst.config_get(my_env, 'alert_url')
        self.jwt = config_inst.config_get(my_env, 'jwt')
        self.ip_address = config_inst.config_get(my_env, 'ip_address')
        self.mirth_receiver = config_inst.config_get(my_env, 'mirth_receiver')

        # CJB 21Jan2020 - Created config params
        self.report_name = config_inst.config_get(my_env, 'report_name')
        self.report_save_path = config_inst.config_get(my_env, 'report_save_path')
        self.report_file_name = config_inst.config_get(my_env, 'report_file_name')
        self.report_file_extension = config_inst.config_get(my_env, 'report_file_extension')
        self.report_templates_path = config_inst.config_get(my_env, 'report_templates_path')
        self.report_templates_name = config_inst.config_get(my_env, 'report_templates_name')

        my_walker = 'walker_{}'.format(self.env)
        self.meta_path = config_inst.config_get(my_walker, 'meta_path')
        self.source_file_path = config_inst.config_get(my_walker, 'source_file_path')
        self.processed_file_log = config_inst.config_get(my_walker, 'processed_file_log')
        
        my_pab = f'pab_{self.env}'
        self.temp_var = config_inst.config_get(my_pab, 'temp_var')
        self.graph_endpoint = config_inst.config_get(my_pab, 'graph_endpoint')
        self.graph_user_name = config_inst.config_get(my_pab, 'graph_user_name')
        self.graph_password = config_inst.config_get(my_pab, 'graph_password')


class ConfigRW:
    """Get a subset of values for the hl7 settings.  The last file found wins. The file read in is 
    of these formats in this order, when available
        <base_file_name>.<file_ext>  
        <base_file_name>_<variant>.<file_ext>
        <base_file_name>_<username>.<file_ext>
     where username is read from the os.environment.
     
     The encryption key is stored in 
         <base_file_name>.key
    
    Keyword arguments:
    base_file_name - name of file
    file_ext - extension to append, defaults '.ini'
    allow_missing_options - True - missing options default to '', othweise an error is thrown.
        True = This is used in this main to set hl7 settings.  
        False = Used when all options need to exist.  
    """
    def __init__(self, base_file_name, file_ext: str = 'ini', allow_missing_options: bool = False):
        self.config_parser = configparser.ConfigParser()
        self.base_file_name = base_file_name
        self.file_ext = file_ext
        self.allow_missing_options = allow_missing_options
        try:
            self.server_name = socket.gethostname()
        except KeyError:
            self.server_name = 'none'

    @property
    def key_file_name(self) -> str:
        return '{}_{}.key'.format(self.base_file_name, self.server_name)

    @property
    def ini_files(self) -> list:
        """List of files to read options from.  The order is important since the last one read wins."""
        file_list = ['{}.{}'.format(self.base_file_name, self.file_ext)]
        if self.server_ini_file_name:
            file_list.append(self.server_ini_file_name)
        return file_list

    @property
    def server_ini_file_name(self) -> str:
        """Name of the user's settings based on machine name."""
        return '{}_{}.{}'.format(self.base_file_name, self.server_name, self.file_ext)

    def read_settings(self, show_files: bool=False) -> ConfigSettings:
        """Read the hl7 settings from a list of files.  Last file wins.
            <base_file_name>.<file_ext>  
            <base_file_name>_<variant>.<file_ext>
            <base_file_name>_<username>.<file_ext>
         where username is read from the os.environment.
            
        Return Values:
        db_site -- site to use
        db_user_name -- dbase login name
        db_password -- dbase login password
        """
        if show_files:
            for file_name in self.ini_files:
                print('\t', file_name)
        self.config_parser.read(self.ini_files)
        config_settings = ConfigSettings(self)
        return config_settings

    def set_personal_settings(self):
        config_settings = self.read_settings()
        result = input('DB Site [{}]: '.format(config_settings.db_site))
        db_site = result if result else config_settings.db_site

        result = input('DB User Name [{}]: '.format(config_settings.db_user_name))
        db_user_name = result if result else config_settings.db_user_name

        result = input('DB Password [{}]: '.format(config_settings.db_password))
        if result:
            enc_db_password = self._encrypt(TCPIP_DBASE, 'user_password', result)
            self.config_parser.set(TCPIP_DBASE, 'user_password', enc_db_password)
        elif config_settings.db_password:
            enc_db_password = self._encrypt(TCPIP_DBASE, 'user_password', config_settings.db_password)
            self.config_parser.set(TCPIP_DBASE, 'user_password', enc_db_password)

        self.config_parser.set(TCPIP_DBASE, 'site', db_site)
        self.config_parser.set(TCPIP_DBASE, 'user_name', db_user_name)

        with open(self.server_ini_file_name, 'w') as configfile:
            self.config_parser.write(configfile)

    def create_encryption_key(self) -> None:
        key_file = Path(self.key_file_name)
        if key_file.is_file():
            print('Key file {} already exists.'.format(self.key_file_name))
            print('If you overwrite this file, currently encrypted information will be lost.')
            print('You will have to replace encoded entries.')
            result = input('Overwrite key file "{}"  Y/N [N]: '.format(self.key_file_name))
        else:
            print('No key file found.  A key file is needed to store encoded information.')
            result = input('Create key file "{}"  Y/N [N]: '.format(self.key_file_name))

        if result == 'Y' or result == 'y':
            key = Fernet.generate_key()
            with open(self.key_file_name, 'wb') as f:
                f.write(key)  # The key is type bytes still
            print('Created/Overwrote key file "{}".'.format(self.key_file_name))
        else:
            print('Key file {} left unchanged.'.format(self.key_file_name))

    def config_get(self, section: str, option: str, encrypted: bool=False) -> str:
        """Get an option value. This will throw an exception if the option is missing and allow_missing_options is false."""
        try:
            option_value = self.config_parser.get(section, option)
            if encrypted and option_value:
                option_value = self._decrypt(section, option, option_value)

        except (configparser.NoOptionError, configparser.NoSectionError) as err:
            if self.allow_missing_options:
                option_value = ''
            else:
                raise Exception(
                    f"Missing section's [{section}] with option '{option}' in one of these files {self.ini_files}.",
                    err)
        except KeyError as err:
            raise Exception(
                f"Missing section's [{section}] with option '{option}' in one of these files {self.ini_files}.", err)

        return option_value

    def _encrypt(self, section: str, option: str, option_value: str) -> str:
        if option_value:
            text_bytes = option_value.encode()
            try:
                with open(self.key_file_name, 'rb') as f:
                    key = f.read()  # The key will be type bytes
            except FileNotFoundError:
                print('You must create a key file {} to store "[{}] {} = {}".'.format(self.key_file_name, section, option, option_value))
            else:
                f = Fernet(key)
                enc_text = f.encrypt(text_bytes)
                return enc_text.decode()
        return ''

    def _decrypt(self, section: str, option: str, option_value: str) -> str:
        if option_value:
            with open(self.key_file_name, 'rb') as f:
                key = f.read()  # The key will be type bytes
            f = Fernet(key)
            try:
                value = f.decrypt(option_value.encode())
                return value.decode()
            except cryptography.fernet.InvalidToken:
                print('Key file {} changed, "[{}] {} =" could not be decrypted.'.format(self.key_file_name, section, option))
        return ''


def ask_user(query) -> bool:
    print(query)
    response = ''
    while response.lower() not in ('y', 'n', 'yes', 'no'):
        response = input('Please enter y or n: ')
    return response.lower() == 'y' or response.lower() == 'yes'


if __name__ == '__main__':
    """Set dbase parameters.  Key for encryption changes by platform."""
    base_root = definitions.get_project_root()

    base_name = ''
    for choice in definitions.Settings:
        my_response = ask_user('Do you want to create settings for {}'.format(choice.value))
        if my_response:
            base_name = choice.value
            break

    if not base_name:
        print('No settings choice selected.')
        exit(0)
    use_base = '{}/{}'.format(base_root, base_name)
    config_rw = ConfigRW(use_base, allow_missing_options=True)

    last_ini_file = ''
    print('Config ini files for settings')
    for f in config_rw.ini_files:
        last_ini_file = f
        print('\t', f)
    print('You can move the values from one ini file to another.  The last file that has the settings wins.\n')

    print('\nStoring configuration in file {}'.format(last_ini_file))
    config_rw.create_encryption_key()
    config_rw.set_personal_settings()
    print('Stored values.')
    print('\nConfiguration stored in file {}.  You may copy the settings to any of these files'.format(last_ini_file))
    config_rw.read_settings(True)
