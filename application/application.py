from application.states.states import TabDataState, sg
from application.layouts.layouts import ApplicationLayout
from patterns.singleton import Singleton

DEBUG_EVENT_VALUES = True


class Application(metaclass=Singleton):
    def __init__(self):
        sg.theme('DarkGrey3')
        self.__layout = ApplicationLayout().layout
        self.__window = sg.Window('Application', self.__layout, finalize=True, resizable=True)

    def run(self):
        while True:
            event, values = self.__window.read()
            if DEBUG_EVENT_VALUES:
                print(event, values)
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break

            TabDataState().update_events(self.__window, None, event, values)

        self.__window.close()
