import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

from positron_projects.listeners.query import KeywordQueryEventListener
from positron_projects.listeners.item_enter import ItemEnterEventListener
from positron_projects.projects import load_projects

LOGGING = logging.getLogger(__name__)

MAX_PROJECTS_IN_LIST = 8


class PositronProjectsExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def get_projects(self, query):
        projects = load_projects(self.preferences)

        if query:
            query_lower = query.strip().lower()
            projects = [p for p in projects if query_lower in p['name'].lower()]

        if not projects:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='No projects found matching: %s' % query,
                    highlightable=False,
                    on_enter=HideWindowAction())
            ])

        items = []
        for project in projects[:MAX_PROJECTS_IN_LIST]:
            items.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=project['name'],
                    description=project['path'],
                    on_enter=ExtensionCustomAction({'path': project['path']}),
                    on_alt_enter=OpenAction(project['path'])))

        return RenderResultListAction(items)
