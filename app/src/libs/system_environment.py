import os
import yaml


class SystemEnvironment:
    class __SystemEnvironment:
        def __init__(self, conf_folder_path: str = None):
            if conf_folder_path is None:
                self._conf_path = './conf'
            else:
                self._conf_path = conf_folder_path

            work_env = os.environ.get('WORK_ENV', 'local')

            self.env = yaml.load(open(self._conf_path + '/' + work_env + '.yaml'))

            if self.env:
                self.env = self.env.get('services', list())

            self.env['environment'] = work_env

            print(self.env)

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self, conf_folder_path: str = None):
        if not SystemEnvironment.instance:
            SystemEnvironment.instance = SystemEnvironment.__SystemEnvironment(conf_folder_path=conf_folder_path)

    def __getattr__(self, name):
        return getattr(self.instance, name)
