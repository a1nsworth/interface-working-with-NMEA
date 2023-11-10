from abc import ABC, abstractmethod

import PySimpleGUI as sg
from parsing.data import DataGPGGAGPRMC
from application.constants import *


class Layout(ABC):
    def __init__(self, layout):
        self._layout = layout

    @property
    def layout(self):
        return self._layout


class TabDataLayout(Layout):
    def __init__(self, path: str):
        self.__table = [
            [
                sg.Table(values=DataGPGGAGPRMC(path).df_gpgga.values.tolist(),
                         headings=DataGPGGAGPRMC(path).df_gpgga.columns.tolist(),
                         justification='center',
                         auto_size_columns=True,
                         num_rows=20,
                         display_row_numbers=True,
                         key='-CURRENT_TABLE-')
            ]
        ]

        super().__init__(
            [
                [
                    sg.Column(layout=self.__table),
                    sg.Column(layout=[
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
                ]
            ]
        )


class ApplicationLayout(Layout):
    def __init__(self):
        super().__init__([
            [
                sg.TabGroup(
                    layout=[
                        [sg.Tab(title='Графики', layout=[]),
                         sg.Tab(title='Данные',
                                layout=TabDataLayout(GPGGA_GPRMC_PATH).layout)]
                    ]
                )
            ]
        ])
