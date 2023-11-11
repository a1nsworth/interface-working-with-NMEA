from application.layouts.layouts import ApplicationLayout
from application.states.states import TabDataState, sg
from patterns.singleton import Singleton

DEBUG_EVENT_VALUES = True


class Application(metaclass=Singleton):

    def __init__(self):
        sg.theme('DarkGrey3')
        self.__event = None
        self.__values = None
        self.__layout = ApplicationLayout().layout
        self.title = 'Application'
        self.__window = sg.Window(self.title, self.__layout, finalize=True)
        TabDataState().clicked_update_table = self.click_update_table_handler

    def click_update_table_handler(self, window: sg.Window):
        self.__window = window

    @property
    def event(self):
        return self.__event

    @property
    def values(self):
        return self.__values

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window: sg.Window):
        self.__window = window

    def run(self):
        while True:
            self.__event, self.__values = self.__window.read()
            if DEBUG_EVENT_VALUES:
                print(self.__event, self.__values)
            if self.__event == sg.WINDOW_CLOSED or self.__event == 'Exit':
                break

            TabDataState().update_events(self, None)

        self.__window.close()
