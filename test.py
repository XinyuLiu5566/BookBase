from main import *
import unittest
import filecmp


class TestStringMethods(unittest.TestCase):

    def test_database(self):
        connect, cursor = connect_to_db()
        self.assertIsNotNone(connect, "no database found")

    def test_database_write_and_read(self):
        CONN, CURR = connect_to_db()
        book_info = get_book_info(CONN, CURR,'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)

        CURR.execute("""select * from book_tb""")
        results = CURR.fetchall()
        CONN.commit()
        results = [dict(ix) for ix in results]
        self.assertEqual(results[0].get('name'), 'Vernon God Little')

    def test_invalid_url(self):
        CONN, CURR = connect_to_db()
        with self.assertRaises(Exception) as context:
            get_book_info(CONN, CURR, "https://www.google.com")
        self.assertTrue('The book url must be a GoodReads book!' in str(context.exception))

    def test_book_name(self):
        CONN, CURR = connect_to_db()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        self.assertEqual(book_info.get('book_name'), 'Vernon God Little')

    def test_book_review_count(self):
        CONN, CURR = connect_to_db()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        self.assertEqual(book_info.get('review_count'), '1400')

    def test_book_isbn(self):
        CONN, CURR = connect_to_db()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        self.assertEqual(book_info.get('book_ISBN'), '0571215165')

    def test_author_name(self):
        CONN, CURR = connect_to_db()
        author_info = get_author_info(CONN, CURR, 'https://www.goodreads.com/author/show/7471.D_B_C_Pierre')
        self.assertEqual(author_info.get('author_name'), 'D.B.C. Pierre')

    def test_author_rating(self):
        CONN, CURR = connect_to_db()
        author_info = get_author_info(CONN, CURR, 'https://www.goodreads.com/author/show/7471.D_B_C_Pierre')
        self.assertEqual(author_info.get('author_rating'), '3.56')

    def test_author_book_number(self):
        CONN, CURR = connect_to_db()
        author_info = get_author_info(CONN, CURR, 'https://www.goodreads.com/author/show/7471.D_B_C_Pierre')
        self.assertEqual(len(author_info.get('author_books')), 10)

    def test_export_json(self):
        CONN, CURR = connect_to_db()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)
        export_json(CONN,CURR, 'test_json.txt')
        self.assertTrue(filecmp.cmp('test_json.txt', 'expected_test_json.txt'))


if __name__ == '__main__':
    unittest.main()
