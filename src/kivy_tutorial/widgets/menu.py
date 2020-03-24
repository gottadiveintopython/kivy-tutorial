__all__ = ('KTMenu', )
import typing
from collections.abc import Mapping

from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.factory import Factory as F
from kivy.uix.screenmanager import ScreenManager, SlideTransition, NoTransition
from triohelper.triouser import TrioUser, activate_nursery
from kivy_tutorial.widgets.basic import KTTightButton

Builder.load_string(r'''
<KTMenu>:
    Screen:
        name: 'A'
    Screen:
        name: 'B'
<KTMenuPage>:
    do_scroll_x: False
    BoxLayout:
        id: layout
        orientation: 'vertical'
        padding: dp(50)
        size_hint_y: None
        height: max(self.minimum_height, root.height)
<KTMenuItem>:
    size_hint_min_y: dp(80)
    KTTightButton:
        text: root.name
        on_release_anim: root.on_release()
''')

# define the data type of tree structure
Leaf = str
Branch = typing.Mapping[str, "Node"]
Node = typing.Union[Leaf, Branch]


def branchが自分の親を辿れるようにする(branch:Branch):
    for name, child in branch.items():
        if isinstance(child, Leaf):
            continue
        if name[0] == '@':
            continue
        if isinstance(child, Mapping):  # isinstance(child, Branch)
            child['@parent'] = branch
            branchが自分の親を辿れるようにする(child)
        else:
            raise ValueError(f"Invalid value type: {type(child)}")
            

class KTMenu(TrioUser, ScreenManager):
    __events__ = ('on_leaf_node', )
    root_node = ObjectProperty()
    current_node = ObjectProperty()
    '''(Read-only)'''

    source = StringProperty()

    def on_kv_post(self, *args, **kwargs):
        self.bind(root_node=self._on_root_node)
        self.property('root_node').dispatch(self)

    def _on_root_node(self, __, root_node):
        if root_node is None:
            return
        branchが自分の親を辿れるようにする(root_node)
        self.reset()

    def reset(self):
        self.switch_page(branch=self.root_node, transition=NoTransition())

    def on_source(self, __, value):
        from kivy.resources import resource_find
        from pathlib import Path
        path = Path(resource_find(value))
        if path.suffix in ('.yml', '.yaml'):
            import yaml
            root_node = yaml.safe_load(path.read_text(encoding='utf-8'))
        elif path.suffix == '.json':
            import json
            root_node = json.loads(path.read_text(encoding='utf-8'))
        else:
            raise ValueError(f"Unknown file type: {path.suffix}")
        self.root_node = root_node

    def switch_page(self, *, branch:Branch, transition=None):
        next_scr_name = self.next()
        next_scr = self.get_screen(next_scr_name)
        next_scr.clear_widgets()
        with activate_nursery(self.nursery):
            next_scr.add_widget(KTMenuPage(branch=branch))
        if transition is not None:
            self.transition = transition
        self.current = next_scr_name
        self.current_node = branch

    def on_leaf_node(self, *args, **kwargs):
        pass


class KTMenuPage(F.ScrollView):
    def __init__(self, **kwargs):
        self._branch:Branch = kwargs.pop('branch')
        super().__init__(**kwargs)
    def on_kv_post(self, *args, **kwargs):
        layout_add_widget = self.ids.layout.add_widget
        branch = self._branch
        for name, child_node in branch.items():
            if name[0] == '@':
                continue
            layout_add_widget(KTMenuItem(name=name, node=child_node))
        parent_branch = branch.get('@parent', None)
        if parent_branch is not None:
            layout_add_widget(KTMenuItem(name='戻る', node=parent_branch))


class KTMenuItem(F.AnchorLayout):
    name = StringProperty()
    node = ObjectProperty()

    @property
    def menu(self) -> KTMenu:
        return self.parent.parent.parent.parent

    def on_release(self):
        node = self.node
        menu = self.menu
        if isinstance(node, Leaf):
            menu.dispatch('on_leaf_node', node)
        elif isinstance(node, Mapping):  # isinstance(node, Branch)
            menu.switch_page(
                branch=self.node,
                transition=SlideTransition(
                    duration=.5,
                    direction='right' if self.name == '戻る' else 'left',
                ),
            )
        else:
            raise ValueError(f"Invalid value type: {type(value)}")
