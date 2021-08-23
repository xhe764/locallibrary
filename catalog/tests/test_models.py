from django.test import TestCase
from catalog.models import Author, Book, Genre, Language, BookInstance
import uuid, names, random, datetime
from lorem_text import lorem

"""
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
"""

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(
            # create a title of 1 to 15 words
            title = lorem.words(random.randint(1, 15)),
            # Generate a random paragraph as the summary
            summary = lorem.paragraph(),
            # Randomly select a language from the list of languages
            language = Language.objects.create(name="Englisg"),
            # Randomly select an author from the Author database
            author = Author.objects.create(first_name='Big', last_name='Bob'),
            # Generate a random isbn of 13 digits
            isbn = ''.join(str(random.randint(0, 9)) for _ in range(13))
        )
        genres = ["Fantasy", "Fiction", "Non-Fiction", "Science Fiction", "Mystery", "Romance", "History"]
        for genre in genres:
            Genre.objects.create(
                name = genre
            )
        book = Book.objects.get(id=1)
        genre_objects = Genre.objects.filter(id__in=range(1,4))
        book.genre.set(genre_objects)

    def test_maxlength_of_fields(self):
        book = Book.objects.get(pk=1)
        title_max_len = book._meta.get_field('title').max_length
        summary_max_len = book._meta.get_field('summary').max_length
        isbn_max_len = book._meta.get_field('isbn').max_length
        self.assertEqual(title_max_len, 200)
        self.assertEqual(summary_max_len, 2000)
        self.assertEqual(isbn_max_len, 13)

    def test_help_text(self):
        book = Book.objects.get(pk=1)
        summary_help_text = book._meta.get_field('summary').help_text
        isbn_help_text = book._meta.get_field('isbn').help_text
        genre_help_text = book._meta.get_field('genre').help_text
        self.assertEqual(summary_help_text, "Enter a brief description of the book")
        self.assertEqual(isbn_help_text, "13 Character <a href=\"https://www.isbn-international.org/content/what-isbn\">ISBN number</a>")
        self.assertEqual(genre_help_text, "Select a genre for this book")

    def test_object_name_is_title(self):
        book = Book.objects.get(pk=1)
        expected_book_name = f'{book.title}'
        self.assertEqual(str(book), expected_book_name)

    def test_get_absolute_url(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(book.get_absolute_url(), "/catalog/book/1")

    def test_display_genre(self):
        book = Book.objects.get(pk=1)
        genres = book.genre.all()
        self.assertEqual(book.display_genre(), "Fantasy, Fiction, Non-Fiction")


class BookInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a book
        Book.objects.create(
            # create a title of 1 to 15 words
            title = lorem.words(random.randint(1, 15)),
            # Generate a random paragraph as the summary
            summary = lorem.paragraph(),
            # Randomly select a language from the list of languages
            language = Language.objects.create(name="Englisg"),
            # Randomly select an author from the Author database
            author = Author.objects.create(first_name='Big', last_name='Bob'),
            # Generate a random isbn of 13 digits
            isbn = ''.join(str(random.randint(0, 9)) for _ in range(13))
        )
        genres = ["Fantasy", "Fiction", "Non-Fiction", "Science Fiction", "Mystery", "Romance", "History"]
        for genre in genres:
            Genre.objects.create(
                name = genre
            )
        book = Book.objects.get(id=1)
        genre_objects = Genre.objects.filter(id__in=range(1,4))
        book.genre.set(genre_objects)

        LOAN_STATUS = (
            ('m', 'Maintenance'),
            ('o', 'On loan'),
            ('a', 'Available'),
            ('r', 'Reserved'),
        )

        # Create a BookInstance
        BookInstance.objects.create(
            book = Book.objects.get(pk=1),
            imprint = "Unlikely Imprint, 2016",
        )

    def test_maxlength_of_fields(self):
        bookinstance = BookInstance.objects.all()[0]
        imprint_max_len = bookinstance._meta.get_field("imprint").max_length
        status_max_len = bookinstance._meta.get_field("status").max_length
        self.assertEqual(imprint_max_len, 200)
        self.assertEqual(status_max_len, 1)

    def test_help_text_of_fields(self):
        bookinstance = BookInstance.objects.all()[0]
        id_help_text = bookinstance._meta.get_field('id').help_text
        status_help_text = bookinstance._meta.get_field('status').help_text
        self.assertEqual(status_help_text, 'Book availability')
        self.assertEqual(id_help_text, 'Unique ID for this particular book across whole library')

    def test_object_name_is_id_book_title(self):
        bookinstance = BookInstance.objects.all()[0]
        expected_object_name = f'{bookinstance.id} ({bookinstance.book.title})'
        self.assertEqual(str(bookinstance), expected_object_name)

    def test_is_overdue_method(self):
        bookinstance = BookInstance.objects.all()[0]
        # First test case, no due_back is set
        self.assertFalse(bookinstance.is_overdue)
        # 2nd test case, due_back is set today
        bookinstance.due_back = datetime.date.today()
        self.assertFalse(bookinstance.is_overdue)
        # 3rd test case, due_back is set before today
        bookinstance.due_back = datetime.date.today()-datetime.timedelta(weeks=1)
        self.assertTrue(bookinstance.is_overdue)
        # 4th test case, due_back is set after today
        bookinstance.due_back = datetime.date.today()+datetime.timedelta(weeks=1)
        self.assertFalse(bookinstance.is_overdue)
