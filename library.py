import json
import os
from typing import List, Dict, Optional

class Book:
    """
    Класс для представления книги.

    Атрибуты:
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        id (int): Уникальный идентификатор книги.
        status (str): Статус книги ("в наличии" или "выдана").
    """

    def __init__(self, title: str, author: str, year: int, book_id: int, status: str = "в наличии"):
        """
        Инициализация объекта книги.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            book_id (int): Уникальный идентификатор книги.
            status (str, optional): Статус книги. По умолчанию "в наличии".
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        """
        Преобразование объекта книги в словарь.

        Returns:
            Dict: Словарь с данными книги.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Book':
        """
        Создание объекта книги из словаря.

        Args:
            data (Dict): Словарь с данными книги.

        Returns:
            Book: Объект книги.
        """
        return Book(data["title"], data["author"], data["year"], data["id"], data["status"])

class Library:
    """
    Класс для управления библиотекой.

    Атрибуты:
        storage_file (str): Имя файла для хранения данных.
        books (List[Book]): Список книг в библиотеке.
    """

    def __init__(self, storage_file: str):
        """
        Инициализация объекта библиотеки и загрузка данных.

        Args:
            storage_file (str): Имя файла для хранения данных.
        """
        self.storage_file = storage_file
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """
        Загрузка данных о книгах из файла.
        """
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as file:
                    data = file.read().strip()
                    if data:
                        self.books = [Book.from_dict(book) for book in json.loads(data)]
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON. Файл поврежден или пуст.")

    def save_books(self):
        """
        Сохранение данных о книгах в файл.
        """
        with open(self.storage_file, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавление книги в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        new_id = self._generate_id()
        new_book = Book(title, author, year, new_id)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id: int):
        """
        Удаление книги из библиотеки.

        Args:
            book_id (int): Идентификатор книги.
        """
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Поиск книги по идентификатору.

        Args:
            book_id (int): Идентификатор книги.

        Returns:
            Optional[Book]: Найденная книга или None.
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def find_books(self, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
        """
        Поиск книг по названию, автору или году издания.

        Args:
            title (Optional[str]): Название книги.
            author (Optional[str]): Автор книги.
            year (Optional[int]): Год издания книги.

        Returns:
            List[Book]: Список найденных книг.
        """
        result = self.books
        if title:
            result = [book for book in result if title.lower() in book.title.lower()]
        if author:
            result = [book for book in result if author.lower() in book.author.lower()]
        if year:
            result = [book for book in result if book.year == year]
        return result

    def list_books(self) -> List[Book]:
        """
        Отображение всех книг в библиотеке.

        Returns:
            List[Book]: Список всех книг.
        """
        return self.books

    def change_status(self, book_id: int, new_status: str):
        """
        Изменение статуса книги.

        Args:
            book_id (int): Идентификатор книги.
            new_status (str): Новый статус книги.
        """
        book = self.find_book_by_id(book_id)
        if book:
            book.status = new_status
            self.save_books()
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def _generate_id(self) -> int:
        """
        Генерация уникального идентификатора для новой книги.

        Returns:
            int: Уникальный идентификатор.
        """
        if self.books:
            return max(book.id for book in self.books) + 1
        return 1

def main():
    """
    Основная функция для запуска консольного интерфейса управления библиотекой.
    """
    library = Library("library.json")

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            library.add_book(title, author, year)
            print("Книга добавлена.")
        elif choice == "2":
            book_id = int(input("Введите ID книги, которую нужно удалить: "))
            library.remove_book(book_id)
        elif choice == "3":
            search_choice = input("Искать по (title/author/year): ").strip().lower()
            if search_choice == "title":
                title = input("Введите название книги: ")
                books = library.find_books(title=title)
            elif search_choice == "author":
                author = input("Введите автора книги: ")
                books = library.find_books(author=author)
            elif search_choice == "year":
                year = int(input("Введите год издания книги: "))
                books = library.find_books(year=year)
            else:
                print("Неверный выбор.")
                continue

            if books:
                for book in books:
                    print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
            else:
                print("Книги не найдены.")
        elif choice == "4":
            books = library.list_books()
            for book in books:
                print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            new_status = input("Введите новый статус книги (в наличии/выдана): ").strip().lower()
            if new_status in ["в наличии", "выдана"]:
                library.change_status(book_id, new_status)
                print("Статус книги обновлен.")
            else:
                print("Неверный статус.")
        elif choice == "6":
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()
