from datetime import datetime
import PySimpleGUI as sg
import json
from datetime import datetime


class Note:
    def __init__(self, title, content, created_at=None):
        self.title = title
        self.content = content
        self.created_at = created_at or datetime.now()

    def to_json(self):
        return json.dumps({
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    @classmethod
    def from_json(cls, note_json):
        note_data = json.loads(note_json)
        created_at = datetime.strptime(note_data['created_at'], '%Y-%m-%d %H:%M:%S')
        return cls(note_data['title'], note_data['content'], created_at)


class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()
    
#ФУНКЦИЯ ДЛЯ ЗАГРУЗКИ ЗАМЕТОК
    def load_notes(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                note_jsons = file.readlines()
                return [Note.from_json(note_json) for note_json in note_jsons]
        except FileNotFoundError:
            return []

# ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ ЗАМЕТОК
    def save_notes(self):
            note_jsons = [note.to_json() for note in self.notes]
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.writelines(note_jsons)
    
# ФУНКЦИЯ ДЛЯ СОЗДАНИЯ ЗАМЕТОК ЧЕРЕЗ GUI 
    def create_note(self, title, content):
        note = Note(title, content)
        self.notes.append(note)
        self.save_notes()
   
    # ФУНКЦИЯ ДЛЯ ВЫВОДА СПИСКА ЗАМЕТОК ЧЕРЕЗ GUI            
    def get_note_list(self):
        if not self.notes:
            return "Список заметок пуст."
        else:
            return [f"{note.title} ({note.created_at.strftime('%Y-%m-%d %H:%M:%S')})" for note in self.notes]

# ФУНКЦИЯ ДЛЯ ЧТЕНИЯ ВЫБРАНОЙ ЗАМЕТКИ ЧЕРЕЗ GUI
    def read_selected(self, note_index):
        if note_index < 1 or note_index > len(self):
            return "Неверный индекс заметки."
        else:
            note = self.notes[note_index - 1]
            return f"Заголовок: {note}\nСодержимое: {note}\nДата создания: {note('%Y-%m-%d %H:%M:%S')}"
      
# ФУНКЦИЯ ДЛЯ РЕДАКТИРОВАНИЯ ЗАМЕТКИ ЧЕРЕЗ GUI 
    def read_selected(self, note_index):
        if note_index < 1 or note_index > len(self.notes):
            return "Неверный индекс заметки."
        else:
            note = self.notes[note_index - 1]
            return f"Заголовок: {note.title}\nСодержимое: {note.content}\nДата создания: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

# ФУНКЦИЯ ДЛЯ УДАЛЕНИЕ ЗАМЕТКИ ЧЕРЕЗ GUI    
    def edit_note(self, note_index, new_title, new_content):
        if note_index < 1 or note_index > len(self.notes):
            return "Неверный индекс заметки."
        else:
            note = self.notes[note_index - 1]
            note.title = new_title
            note.content = new_content
            self.save_notes()

# ФУНКЦИЯ ДЛЯ УДАЛЕНИЯ ЗАМЕТКИ         
    def delete_note(self, note_index):
            if note_index < 1 or note_index > len(self.notes):
                return "Неверный индекс заметки."
            else:
                note = self.notes.pop(note_index - 1)
                self.save_notes()
                return f"Заметка \"{note.title}\" успешно удалена."

#  ИНТЕРФЕЙС
def ui():
    file_path = 'notes.json'
    manager = NoteManager(file_path)

# Интерфейс
    layout = [
        [sg.Text('Заголовок'), sg.Input(key='-TITLE-')],
        [sg.Text('Содержимое'), sg.Input(key='-CONTENT-')],
        [sg.Button('Создать заметку'), sg.Button('Вывести список заметок')],
        [sg.Text(size=(40, 1), key='-OUTPUT-')],
        [sg.Text('Индекс заметки'), sg.Input(key='-INDEX-')],
        [sg.Button('Прочитать выбранную заметку'), sg.Button('Редактировать заметку'), sg.Button('Удалить заметку')],
        [sg.Button('Выход')]
    ]

    window = sg.Window('Менеджер заметок', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Выход':
            break
        if event == 'Создать заметку':
            title = values['-TITLE-']
            content = values['-CONTENT-']
            manager.create_note(title, content)
            sg.popup('Заметка успешно создана.')
        if event == 'Вывести список заметок':
            note_list = manager.get_note_list()
            if isinstance(note_list, list):
                sg.popup('\n'.join(note_list))
            else:
                sg.popup(note_list)
        if event == 'Прочитать выбранную заметку':
            index = int(values['-INDEX-'])
            result = manager.read_selected(index)
            sg.popup(result)
        if event == 'Редактировать заметку':
            index = int(values['-INDEX-'])
            new_title = sg.popup_get_text('Введите новый заголовок заметки')
            new_content = sg.popup_get_text('Введите новое содержимое заметки')
            manager.edit_note(index, new_title, new_content)
            sg.popup('Заметка успешно отредактирована.')
        if event == 'Удалить заметку':
            index = int(values['-INDEX-'])
            result = manager.delete_note(index)
            sg.popup(result)

    window.close()
