from abc import abstractmethod

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from application.layouts.layouts import TabDataLayout
from parsing.data import DataGetterByPath
from patterns.singleton import Singleton


class ApplicationState(metaclass=Singleton):
    def __init__(self, layout):
        self._layout = layout

    @abstractmethod
    def update_events(self, application, canvas: FigureCanvasTkAgg) -> FigureCanvasTkAgg | None:
        pass

    @property
    def layout(self):
        return self._layout


class TabDataState(ApplicationState):
    def __init__(self):
        super().__init__(TabDataLayout())
        self.__data_class = None
        self.__format_data = None
        self.__from_which_file_to_read = None
        self.__new_window = None
        self.clicked_update_table = None

    def __clicked_update_table(self, application):
        from_which_file_to_read = application.window['-DD_READ_FROM_DATA-'].get()
        format_data = application.window['-DD_FORMAT_DATA-'].get()
        data_class = DataGetterByPath().get_data_class_by_path(from_which_file_to_read)

        if data_class is None:
            sg.popup_error(f'Не существует представления для файла -> {from_which_file_to_read}')
        if format_data not in data_class.available_formats():
            sg.popup_error(f'У этого представления нет такого типа -> {format_data}')
        df = data_class.get_df_by_key(format_data)

        self._layout.update_window_with_new_table(application=application, headings=df.columns.tolist(),
                                                  values=df.values.tolist(),
                                                  justification='center',
                                                  auto_size_columns=True,
                                                  num_rows=40,
                                                  display_row_numbers=True,
                                                  )

        return data_class, format_data, from_which_file_to_read

    @staticmethod
    def __clicked_save_table(window: sg.Window, data_class, format_data, from_which_file_to_read):
        if window['-SELECT_FOLDER-'].get() == '':
            sg.popup_error('Выберите путь для сохранения')
        elif window['-NAME_FILE-'].get() == '':
            sg.popup_error('Напишите название сохраняемого файла (название без расширения)')
        elif data_class is None:
            sg.popup_error(f'Невозможно сохранить! \n'
                           f'Не существует представления для файла -> {from_which_file_to_read}')
        elif format_data not in data_class.available_formats():
            sg.popup_error(f'Невозможно сохранить! \n'
                           f'У этого представления нет такого типа -> {format_data}')
        else:
            fmt = window['-UNIT_DF-'].get()
            path = window['-SELECT_FOLDER-'].get()
            name_file = window['-NAME_FILE-'].get()

            df = data_class.get_df_by_key(format_data)
            if fmt == 'xlsx':
                df.to_excel(f'{path}/{name_file}.{fmt}',
                            header=True,
                            index=False, )
            else:
                df.to_csv(f'{path}/{name_file}.{fmt}',
                          header=True,
                          index=False, sep='\t', )
            sg.popup_ok(f'Ваш файл успешно сохранен! По пути: {path}/{name_file}')

    def update_events(self, application, canvas: FigureCanvasTkAgg) -> FigureCanvasTkAgg | None:
        if (
                application.event == '-UPDATE_TABLE_DATA-'
                or
                (self.__data_class is None and self.__from_which_file_to_read is None and self.__format_data is None)
        ):
            self.__data_class, self.__format_data, self.__from_which_file_to_read = (
                self.__clicked_update_table(application)
            )
        if application.event == '-SAVE_DF-':
            self.__clicked_save_table(application, self.__data_class, self.__format_data,
                                      self.__from_which_file_to_read)

        return None
