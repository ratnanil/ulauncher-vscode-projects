import os
import subprocess
from ulauncher.api.client.EventListener import EventListener


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        executable = extension.preferences['positron_executable_path']

        env = os.environ.copy()
        env.pop('PYTHONPATH', None)

        subprocess.Popen([executable, data['path']], env=env)
