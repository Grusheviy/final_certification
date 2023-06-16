from datetime import datetime


class Note:
    def __init__(self, title, content, created_at=None):
        self.title = title
        self.content = content
        self.created_at = created_at or datetime.now()

    def to_string(self):
        created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return f"{self.title}\n{self.content}\n{created_at_str}\n"

    @classmethod
    def from_string(cls, note_string):
        note_data = note_string.strip().split('\n')
        created_at = datetime.strptime(note_data[2], '%Y-%m-%d %H:%M:%S')
        return cls(note_data[0], note_data[1], created_at)


class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                note_strings = file.readlines()
                return [Note.from_string(note_string) for note_string in note_strings]
        except FileNotFoundError:
            return []

    def save_notes(self):
        note_strings = [note.to_string() for note in self.notes]
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.writelines(note_strings)

    def create_note_from_input(self):
        title = input("Введите заголовок заметки: ")
        content = input("Введите содержимое заметки: ")
        self.create_note(title, content)

    def create_note(self, title, content):
        note = Note(title, content)
        self.notes.append(note)
        self.save_notes()
        print('\n',"Заметка успешно создана.")

    def read_notes(self):
        if not self.notes:
            print('\n', "Список заметок пуст.")
        else:
            print("Список заметок:")
            for index, note in enumerate(self.notes):
                print('\n', f"{index + 1}. {note.title} ({note.created_at.strftime('%Y-%m-%d %H:%M:%S')})")

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

    def edit_note_from_input(self):
        note_index = int(input("Введите индекс заметки для редактирования: "))
        new_title = input("Введите новый заголовок заметки: ")
        new_content = input("Введите новое содержимое заметки: ")
        self.edit_note(note_index, new_title, new_content)

    def edit_note(self, note_index, new_title, new_content):
        if note_index < 1 or note_index > len(self.notes):
            print('\n', "Неверный индекс заметки.")
        else:
            note = self.notes[note_index - 1]
            note.title = new_title
            note.content = new_content
            self.save_notes()
            print('\n', "Заметка успешно отредактирована.")

    def delete_note_from_input(self):
        note_index = int(input("Введите индекс заметки для удаления: "))
        self.delete_note(note_index)

    def delete_note(self, note_index):
        if note_index < 1 or note_index > len(self.notes):
             print('\n', "Неверный индекс заметки.")
        else:
            note = self.notes.pop(note_index - 1)
            self.save_notes()
            print('\n', f"Заметка \"{note.title}\" успешно удалена.")


def ui():
    file_path = 'notes.txt'
    manager = NoteManager(file_path)

    while True:
        print('\n','----------------','\n')
        print('1. Создать заметку')
        print('2. Вывести список заметок')
        print('3. Прочитать выбранную заметку')
        print('4. Редактировать заметку')
        print('5. Удалить заметку')
        print('6. Выйти')
        print('\n','----------------','\n')

        choice = input('Выберите действие: ')
        if choice == '1':
            manager.create_note_from_input()
        elif choice == '2':
            manager.read_notes()
        elif choice == '3':
            manager.read_selected_note_from_input()
        elif choice == '4':
            manager.edit_note_from_input()
        elif choice == '5':
            manager.delete_note_from_input()
        elif choice == '6':
            print('Программа завершена.')
            break
