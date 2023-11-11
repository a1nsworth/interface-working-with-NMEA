import PySimpleGUI as sg
from patterns.singleton import Singleton
from parsing.data import DataGPGGAGPRMC
from application.constants import *


class Layout(metaclass=Singleton):
    def __init__(self, layout):
        self._layout = layout

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        self._layout = layout


class TabDataLayout(Layout):
    def __init__(self, path: str = GPGGA_GPRMC_PATH):
        self.__table = [
            [
                sg.Table(values=DataGPGGAGPRMC(path).df_gpgga.values.tolist(),
                         headings=DataGPGGAGPRMC(path).df_gpgga.columns.tolist(),
                         justification='center',
                         auto_size_columns=True,
                         num_rows=40,
                         display_row_numbers=True,
                         key='-CURRENT_TABLE-')
            ]
        ]
        self.__column_with_table = sg.Column(layout=self.__table)
        self.__column_with_actions = sg.Column(layout=[
            [sg.Text('Файл с данными:')],
            [sg.DropDown(values=[GPGGA_GPRMC_PATH, ALL_TYPE_1_PATH, ALL_TYPE_2_PATH],
                         default_value=GPGGA_GPRMC_PATH,
                         readonly=True,
                         key='-DD_READ_FROM_DATA-')],
            [sg.Text('Формат:')],
            [sg.DropDown(values=list(FORMATS.values()),
                         default_value=FORMATS[0],
                         readonly=True,
                         size=(7, 4),
                         key='-DD_FORMAT_DATA-')],
            [sg.Button(button_text='Обновить таблицу', key='-UPDATE_TABLE_DATA-')],
            [sg.HorizontalSeparator()],
            [sg.Text('Формат: '),
             sg.DropDown(values=['csv', 'txt', 'xlsx'], default_value='csv', readonly=True,
                         key='-UNIT_DF-')],
            [sg.Text('Название файла: '),
             sg.Input(key='-NAME_FILE-', size=(10, 2))],
            [sg.HorizontalSeparator()],
            [sg.Text("Выберите путь для сохранения:")],
            [sg.Input(size=(20, 2), enable_events=True, key='-SELECT_FOLDER-'),
             sg.FolderBrowse()],
            [sg.Button('Сохранить', key='-SAVE_DF-')],
        ])

        super().__init__(
            [
                [
                    self.__column_with_table,
                    self.__column_with_actions,
                ],
            ]
        )

    def __rebuild_layout(self, **table_options):
        self.__table = [
            [
                sg.Table(**table_options,
                         key='-CURRENT_TABLE-')
            ]
        ]
        self.__column_with_table = sg.Column(layout=self.__table)
        self.__column_with_actions = sg.Column(layout=[
            [sg.Text('Файл с данными:')],
            [sg.DropDown(values=[GPGGA_GPRMC_PATH, ALL_TYPE_1_PATH, ALL_TYPE_2_PATH],
                         default_value=GPGGA_GPRMC_PATH,
                         readonly=True,
                         key='-DD_READ_FROM_DATA-')],
            [sg.Text('Формат:')],
            [sg.DropDown(values=list(FORMATS.values()),
                         default_value=FORMATS[0],
                         readonly=True,
                         size=(7, 4),
                         key='-DD_FORMAT_DATA-')],
            [sg.Button(button_text='Обновить таблицу', key='-UPDATE_TABLE_DATA-')],
            [sg.HorizontalSeparator()],
            [sg.Text('Формат: '),
             sg.DropDown(values=['csv', 'txt', 'xlsx'], default_value='csv', readonly=True,
                         key='-UNIT_DF-')],
            [sg.Text('Название файла: '),
             sg.Input(key='-NAME_FILE-', size=(10, 2))],
            [sg.HorizontalSeparator()],
            [sg.Text("Выберите путь для сохранения:")],
            [sg.Input(size=(20, 2), enable_events=True, key='-SELECT_FOLDER-'),
             sg.FolderBrowse()],
            [sg.Button('Сохранить', key='-SAVE_DF-')],
        ])

        self._layout = [
            [
                self.__column_with_table,
                self.__column_with_actions
            ],
        ]

    def update_window_with_new_table(self, application, **table_options):
        if application.window is not None:
            application.window.close()

        self.__rebuild_layout(**table_options)
        ApplicationLayout().rebuild_layout(ApplicationLayout().plot_tab[1], self._layout)

        application.window = sg.Window(application.title, ApplicationLayout().layout, finalize=True)
        application.window['-DATA_TAB-'].select()


class ApplicationLayout(Layout):
    def __init__(self):
        self.plot_tab = ['Графики', []]
        self.data_tab = ['Данные', TabDataLayout(GPGGA_GPRMC_PATH).layout]

        super().__init__([
            [
                sg.TabGroup(
                    layout=[
                        [sg.Tab(title='Графики', layout=[], key='-PLOT_TAB-'),
                         sg.Tab(title='Данные',
                                layout=TabDataLayout(GPGGA_GPRMC_PATH).layout, key='-DATA_TAB-')]
                    ]
                )
            ]
        ])

    def rebuild_layout(self, plot_tab_value, data_tab_value):
        self.plot_tab[1] = plot_tab_value
        self.data_tab[1] = data_tab_value
        self._layout = [
            [
                sg.TabGroup(
                    layout=[
                        [sg.Tab(title=self.plot_tab[0], layout=self.plot_tab[1], key='-PLOT_TAB-'),
                         sg.Tab(title=self.data_tab[0], layout=self.data_tab[1], key='-DATA_TAB-')]
                    ]
                )
            ]
        ]
