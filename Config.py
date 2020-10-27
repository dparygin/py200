import configparser

class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.db_name = config.get('Settings', 'db_name')

    def create():
        config = configparser.ConfigParser()
        config.add_section('Settings')
        config.set('Settings', 'db_name', '')
        with open('settings.ini', 'w') as config_file:
            config.write(config_file)


    def get_db_name(self):
        return self.db_name

    def set_db_name(self, db_name: str):
        if not isinstance(db_name, str):
            print('Некорректный ввод')
        self.db_name = db_name
        return self.db_name

    def change_settings(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        config.set('Settings', 'db_name', self.db_name)
        with open('settings.ini', 'w') as config_file:
            config.write(config_file)

