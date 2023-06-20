from datetime import datetime
import json

class Note:
    def __init__(self, title, content, created_at=None):
        self.title = title
        self.content = content
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return {
            'title': self.title,
            'content': self.content,
            'created_at': created_at_str
        }

    @classmethod
    def from_dict(cls, note_dict):
        created_at = datetime.strptime(note_dict['created_at'], '%Y-%m-%d %H:%M:%S')
        return cls(note_dict['title'], note_dict['content'], created_at)


class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()

# ЗАГРУЗКА ЗАМЕТОК
    def load_notes(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                notes_data = json.load(file)
                return [Note.from_dict(note_data) for note_data in notes_data]
        except FileNotFoundError:
            return []

# СОХРАНЕНИЕ ЗАМЕТОК
    def save_notes(self):
        note_data = [note.to_dict() for note in self.notes]
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(note_data, file, indent=4)

# СОЗДАНИЕ ЗАМЕТОК
    def create_note_from_input(self):
        title = input("Введите заголовок заметки: ")
        content = input("Введите содержимое заметки: ")
        self.create_note(title, content)

    def create_note(self, title, content):
        note = Note(title, content)
        self.notes.append(note)
        self.save_notes()
        print('\n', "Заметка успешно создана.")

# ЧТЕНИЕ ЗАМЕТОК
    def read_notes(self):
        if not self.notes:
            print('\n', "Список заметок пуст.")
        else:
            print("Список заметок:")
            for index, note in enumerate(self.notes):
                print('\n', f"{index + 1}. {note.title} ({note.created_at.strftime('%Y-%m-%d %H:%M:%S')})")

# ВЫБОР ЗАМЕТКИ ДЛЯ ПРОЧТЕНИЯ
    def read_selected_note_from_input(self):
        note_index = int(input("Введите индекс заметки для прочтения: "))
        self.read_selected_note(note_index)

    def read_selected_note(self, note_index):
        if note_index < 1 or note_index > len(self.notes):
            print('\n', "Неверный индекс заметки.")
        else:
            note = self.notes[note_index - 1]
            print('\n')
            print(f"Заголовок: {note.title}")
            print(f"Содержимое: {note.content}")
            print(f"Дата создания: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

# ВЫБОР ЗАМЕТКИ ДЛЯ РЕДАКТИРОВАНИЯ
    def edit_note_from_input(self):
        note_index = int(input("Введите индекс заметки для редактирования: "))
        new_title = input("Введите новый заголовок заметки: ")
        new_content = input("Введите новое содержимое заметки: ")
        self.edit_note(note_index, new_title, new_content)

#РЕДАКТИРОВАНИЕ ЗАМЕТКИ
    def edit_note(self, note_index, new_title, new_content):
        if note_index < 1 or note_index > len(self.notes):
            print('\n', "Неверный индекс заметки.")
        else:
            note = self.notes[note_index - 1]
            note.title = new_title
            note.content = new_content
            self.save_notes()
            print('\n', "Заметка успешно отредактирована.")

# ФУНКЦИЯ ВЫБОРА ЗАМЕТКИ ДЛЯ УДАЛЕНИЯ
    def delete_note_from_input(self):
        note_index = int(input("Введите индекс заметки для удаления: "))
        self.delete_note(note_index)

# ФУНКЦИЯ УДАЛЕНИЯ ЗАМЕТКИ
    def delete_note(self, note_index):
        if note_index < 1 or note_index > len(self.notes):
            print('\n', "Неверный индекс заметки.")
        else:
            note = self.notes.pop(note_index - 1)
            self.save_notes()
            print('\n', f"Заметка \"{note.title}\" успешно удалена.")


#ИНТЕРФЕЙС

def ui():
    file_path = 'notes.json'
    manager = NoteManager(file_path)
    
    while True:
        print('\n', '----------------', '\n')
        print('1. Создать заметку')
        print('2. Вывести список заметок')
        print('3. Прочитать выбранную заметку')
        print('4. Редактировать заметку')
        print('5. Удалить заметку')
        print('6. Выйти')
        print('\n', '----------------', '\n')

        choice = input('Выберите действие: ')

        actions = {
            '1': manager.create_note_from_input,
            '2': manager.read_notes,
            '3': manager.read_selected_note_from_input,
            '4': manager.edit_note_from_input,
            '5': manager.delete_note_from_input,
            '6': lambda: print('Программа завершена.')
        }

        if choice in actions:
            actions[choice]()
        else:
            print('Неверный выбор. Попробуйте еще раз.')

        if choice == '6':
            break