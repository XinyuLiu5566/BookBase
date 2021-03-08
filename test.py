from main import *
from query_process import *
import unittest
import filecmp
import requests


class TestStringMethods(unittest.TestCase):

    def test_database(self):
        connect, cursor = connect_to_db()
        self.assertIsNotNone(connect, "no database found")

    def test_database_write_and_read(self):
        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info = get_book_info(CONN, CURR,'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)

        CURR.execute("""select * from book""")
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
        self.assertEqual(book_info.get('review_count'), '1,401')

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
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)
        export_book_json(CONN,CURR, 'test_json.txt')
        with open('test_json.txt') as inputfile:
            file_data = json.load(inputfile)
        self.assertEqual(file_data[0]['id'], '11711')
        self.assertEqual(file_data[0]['name'], 'Vernon God Little')

    def test_invalid_query(self):
        CONN, CURR = connect_to_db()
        q = queryProcessor('book.id... "11711"')
        with self.assertRaises(Exception) as context:
            results = q.process_query()
        self.assertTrue('Invalid query' in str(context.exception))

    def test_normal_query(self):
        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)
        q = queryProcessor('book.id: "11711"')
        results = q.process_query()
        self.assertEqual(len(results), 1)

    def test_not_query(self):
        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)
        q = queryProcessor('book.id: NOT "300"')
        results = q.process_query()
        self.assertEqual(len(results), 1)

    def test_and_query(self):
        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)
        q = queryProcessor('book.id: "200" AND "300"')
        results = q.process_query()
        self.assertEqual(len(results), 0)

    def test_or_query(self):
        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info1 = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info1)
        book_info2 = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/48677116-little-scratch')
        store_book(CONN, CURR, book_info2)
        q = queryProcessor('book.id: "11711" OR "48677116"')
        results = q.process_query()
        self.assertEqual(len(results), 2)

    def test_less_than_query(self):
        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info1 = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info1)
        book_info2 = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/48677116-little-scratch')
        store_book(CONN, CURR, book_info2)
        q = queryProcessor('book.rating: < "4"')
        results = q.process_query()
        self.assertEqual(len(results), 2)

    def test_GET_request(self):
        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)

        results = requests.get('http://127.0.0.1:5000/api/book?id=11711')
        self.assertEqual(len(results.json()), 1)

    def test_DELETE_request(self):
        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()
        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)

        CURR.execute("""select COUNT(*) from book""")
        results = CURR.fetchall()
        CONN.commit()
        results = [dict(ix) for ix in results]
        self.assertEqual(results[0]['COUNT(*)'], 1)

        requests.delete('http://127.0.0.1:5000/api/book?id=11711')

        CURR.execute("""select COUNT(*) from book""")
        results = CURR.fetchall()
        CONN.commit()
        results = [dict(ix) for ix in results]
        self.assertEqual(results[0]['COUNT(*)'], 0)

    def test_POST_request(self):
        book = {
            "name": "Vernon God Little",
            "url": "https://www.goodreads.com/book/show/11711.Vernon_God_Little",
            "id": "11711",
            "ISBN": "0571215165",
            "author_url": "https://www.goodreads.com/author/show/7471.D_B_C_Pierre",
            "author_name": "D.B.C. Pierre",
            "book_rating": "3.59",
            "rating_count": "30,696",
            "review_count": "1,400",
            "image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1339082247l/11711.jpg",
            "similar_books": "1. True History of the Kelly Gang: https://www.goodreads.com/book/show/110090.True_History_of_the_Kelly_Gang\n2. The Finkler Question: https://www.goodreads.com/book/show/8664368-the-finkler-question\n3. Paddy Clarke Ha Ha Ha: https://www.goodreads.com/book/show/30512.Paddy_Clarke_Ha_Ha_Ha\n4. The Sea: https://www.goodreads.com/book/show/3656.The_Sea\n5. Possession of My Heart (The Three Immortal Blades, #2): https://www.goodreads.com/book/show/23291161-possession-of-my-heart\n6. Oscar and Lucinda: https://www.goodreads.com/book/show/316496.Oscar_and_Lucinda\n7. Summer in February: https://www.goodreads.com/book/show/345309.Summer_in_February\n8. The Gathering: https://www.goodreads.com/book/show/998133.The_Gathering\n9. How Late It Was, How Late: https://www.goodreads.com/book/show/89208.How_Late_It_Was_How_Late\n10. The Line of Beauty: https://www.goodreads.com/book/show/139087.The_Line_of_Beauty\n11. Phantom Wolf (Phantom Wolf, #1): https://www.goodreads.com/book/show/22404103-phantom-wolf\n12. Last Orders: https://www.goodreads.com/book/show/5068.Last_Orders\n13. Amsterdam: https://www.goodreads.com/book/show/6862.Amsterdam\n14. The Inheritance of Loss: https://www.goodreads.com/book/show/95186.The_Inheritance_of_Loss\n15. Extreme: https://www.goodreads.com/book/show/53483098-extreme\n16. Unless: https://www.goodreads.com/book/show/74462.Unless\n17. The Book of Occult: https://www.goodreads.com/book/show/20388847-the-book-of-occult\n"
        }

        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()

        results = requests.post(url='http://127.0.0.1:5000/api/book', json=book)
        CURR.execute("""select COUNT(*) from book""")
        results = CURR.fetchall()
        CONN.commit()
        results = [dict(ix) for ix in results]
        self.assertEqual(results[0]['COUNT(*)'], 1)

    def test_PUT_request(self):
        update_info = {
            "name": "abc",
        }

        CONN, CURR = connect_to_db()
        CURR.execute("""DELETE from book""")
        CONN.commit()

        book_info = get_book_info(CONN, CURR, 'https://www.goodreads.com/book/show/11711.Vernon_God_Little')
        store_book(CONN, CURR, book_info)

        results = requests.put(url='http://127.0.0.1:5000/api/book?id=11711', json=update_info)
        CURR.execute("""select * from book""")
        results = CURR.fetchall()
        CONN.commit()
        results = [dict(ix) for ix in results]
        self.assertEqual(results[0]['name'], 'abc')






if __name__ == '__main__':
    unittest.main()
