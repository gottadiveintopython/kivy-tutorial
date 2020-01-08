__all__ = ('KTLazyScreenManager', )

from kivy.logger import Logger
from importlib import import_module
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager


class KTLazyScreenManager(ScreenManager):
    pkg_name = StringProperty()
    def switch_screen(self, name, *, transition=None):
        if self.transition.is_active:
            Logger.warning(f"KTLazyScreenManager: Switching is ignored because the previous transition is not done.")
            return False
        if not self.has_screen(name):
            try:
                module = import_module('.' + name, self.pkg_name)
            except ModuleNotFoundError:
                Logger.warning(f"KTLazyScreenManager: No module named '{self.pkg_name}.{name}'")
                return False
            screen = module.create_screen()
            screen.name = name
            self.add_widget(screen)
        if transition is not None:
            self.transition = transition
        self.current = name
        return True
