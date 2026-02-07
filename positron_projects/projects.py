import os
import json


def load_projects(preferences):
    full_path = os.path.expanduser(preferences['projects_file_path'])

    projects = []
    if os.path.isfile(full_path):
        with open(full_path) as f:
            projects = json.load(f)
    elif os.path.isdir(full_path):
        for filename in os.listdir(full_path):
            if not filename.endswith('.json'):
                continue
            filepath = os.path.join(full_path, filename)
            with open(filepath) as f:
                projects += json.load(f)

    return [
        {
            'name': p['name'],
            'path': p.get('rootPath') or p.get('fullPath', ''),
        }
        for p in projects
        if p.get('enabled', True)
    ]
