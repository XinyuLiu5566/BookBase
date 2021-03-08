"""
packages used in this file
"""
import json
import sqlite3
import argparse
import warnings
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import requests

load_dotenv()
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


def get_book_info(CONN, CURR, website):
    """
    get the html info of a book
    :param CONN: database connect
    :param CURR: database cursor
    :param website: the website of the book to scrape
    :return: the dictionary contains the required book information
    """

    if website[:30] != "https://www.goodreads.com/book":
        raise Exception("The book url must be a GoodReads book!")
    # if get_book_table_size(CONN, CURR) > ARGS.book_number:
    #     warnings.warn("There are " + str(get_book_table_size(CONN, CURR))
    #                   + " books in the table, already greater than 200")
    print("getting book info from " + website)
    html_text = requests.get(website)
    soup = BeautifulSoup(html_text.text, 'lxml')
    book_name = soup.find('h1', class_="gr-h1 gr-h1--serif").text.strip()
    book_url = website
    book_id = website.split('/')[-1]
    if '.' in book_id:
        book_id = book_id.split('.')[0]
    elif '-' in book_id:
        book_id = book_id.split('-')[0]
    book_isbn = None
    book_isbn_list = soup.find_all('div', class_="infoBoxRowItem")
    for each in book_isbn_list:
        text = each.text.replace(' ', '').split('\n')
        if len(text) == 4:
            if text[1].isdigit():
                book_isbn = text[1]
    if book_isbn is None:
        print("Exception: The book does not have an ISBN number!")
    book_author_url = "https://www.goodreads.com" \
                      + soup.find('div', class_="bookAuthorProfile__name").a['href']
    author_name = soup.find('div', class_="bookAuthorProfile__name").a.text.strip()
    book_rating = soup.find_all("span", {"itemprop": "ratingValue"})[0].text.replace(' ', '').strip()
    rating_count = soup.find_all("a", class_="gr-hyperlink")[-3].text.replace(' ', '').strip().split('\n')[0]
    review_count = soup.find_all("a", class_="gr-hyperlink")[-2].text.replace(' ', '').strip().split('\n')[0]
    image_url = None
    image_url_list = soup.findAll("img", {"id": "coverImage"})
    if len(image_url_list) > 0:
        image_url = image_url_list[0]['src']
    similar_books = []
    similar_books_list = soup.find_all('li', class_="cover")
    for book in similar_books_list:
        similar_books.append({
            'url': book.find('a')['href'],
            'bookname': book.find('img')['alt']
        })
    return {
        'book_name': book_name,
        'book_url': book_url,
        'book_id': book_id,
        'book_ISBN': book_isbn,
        'book_author_url': book_author_url,
        'author_name': author_name,
        'book_rating': book_rating,
        'rating_count': rating_count,
        'review_count': review_count,
        'image_url': image_url,
        'similar_books': similar_books
    }


def get_author_info(CONN, CURR, website):
    """
    get the html info of a author
    :param CONN: database connect
    :param CURR: database cursor
    :param website: the website of the author to scrape
    :return: the dictionary contains the required author information
    """
    # if get_author_table_size(CONN, CURR) > 50:
    #     warnings.warn("There are " + str(get_author_table_size(CONN, CURR))
    #                   + " authors in the table, already greater than 50")
    print("getting author info from " + website)
    html_text = requests.get(website)
    soup = BeautifulSoup(html_text.text, 'lxml')
    author_name = soup.find_all("span", {"itemprop": "name"})[0].text
    author_url = website
    author_id = website.split('/')[-1][:4]
    author_rating = soup.find_all("span", class_="average")[0].text
    rating_count = soup.find_all("span", class_="value-title")[0].text.strip()
    review_count = soup.find_all("span", class_="value-title")[1].text.strip()
    author_image_url = soup.find('img', {'alt': author_name})['src']
    related_author_list = soup.find('div', class_="hreview-aggregate").find_all('a')
    for item in related_author_list:
        if "Similar" not in item.text:
            related_author_list.remove(item)
    related_author_link = related_author_list[0]['href']
    related_author_soup = BeautifulSoup(requests.get("https://www.goodreads.com/"
                                                     + related_author_link).text, 'lxml')
    related_author_list = related_author_soup.find_all('a', class_='gr-h3 gr-h3--serif gr-h3--noMargin')
    related_author_list.pop(0)  # remove the author self
    related_author = []
    for each_author in related_author_list:
        related_author_url = each_author['href']
        related_author_name = each_author.span.text
        related_author.append({
            'related_author_url': related_author_url,
            'related_author_name': related_author_name
        })

    author_books = []
    author_books_list = soup.find_all('tr', {'itemtype': 'http://schema.org/Book'})
    for each_book in author_books_list:
        book_name = each_book.find('span').text
        book_url = "https://www.goodreads.com" + each_book.find('a')['href']
        author_books.append({
            'book_name': book_name,
            'book_url': book_url
        })
    return {
        'author_name': author_name,
        'author_url': author_url,
        'author_id': author_id,
        'author_rating': author_rating,
        'rating_count': rating_count,
        'review_count': review_count,
        'author_image_url': author_image_url,
        'related_author': related_author,
        'author_books': author_books
    }


def store_book(connect, cursor, book_info):
    """
    store the book information into database
    :param connect: database connect
    :param cursor: database cursor
    :param book_info: the information of the book (dict) to store into database
    :return:
    """
    cursor.execute("""SELECT * from book WHERE id = (?)""", (book_info.get('book_id'),))
    results = cursor.fetchall()
    results = [dict(ix) for ix in results]
    connect.commit()
    if len(results) > 0:
        return

    similar_books = book_info.get('similar_books')
    similar_books_list = ""
    for i, each_book_info in enumerate(similar_books, 1):
        similar_books_list += str(i) + ". " + each_book_info.get('bookname') \
                              + ": " + each_book_info.get('url')
        similar_books_list += "\n"

    cursor.execute("""insert into book values (?,?,?,?,?,?,?,?,?,?,?)""", (
        book_info.get('book_name'),
        book_info.get('book_url'),
        book_info.get('book_id'),
        book_info.get('book_ISBN'),
        book_info.get('book_author_url'),
        book_info.get('author_name'),
        book_info.get('book_rating'),
        book_info.get('rating_count'),
        book_info.get('review_count'),
        book_info.get('image_url'),
        similar_books_list
    ))
    connect.commit()
    print("There are " + str(get_book_table_size(connect, cursor)) + " books in boot_tb table")


def store_author(connect, cursor, author_info):
    """
    store the author information into database
    :param connect: database connect
    :param cursor: database cursor
    :param author_info: the information of the author (dict) to store into database
    :return:
    """
    cursor.execute("""SELECT * from author WHERE id = (?)""", (author_info.get('author_id'),))
    results = cursor.fetchall()
    results = [dict(ix) for ix in results]
    connect.commit()
    if len(results) > 0:
        return

    related_author = author_info.get('related_author')
    related_author_list = ""
    for i, each_author_info in enumerate(related_author, 1):
        related_author_list += str(i) + ". " + each_author_info.get(
            'related_author_name') + ": " + each_author_info.get('related_author_url')
        related_author_list += "\n"

    author_books = author_info.get('author_books')
    author_books_list = ""
    for i, each_author_book in enumerate(author_books, 1):
        author_books_list += str(i) + ". " + each_author_book.get('book_name') \
                             + ": " + each_author_book.get('book_url')
        author_books_list += "\n"

    cursor.execute("""insert into author values (?,?,?,?,?,?,?,?,?)""", (
        author_info.get('author_name'),
        author_info.get('author_url'),
        author_info.get('author_id'),
        author_info.get('author_rating'),
        author_info.get('rating_count'),
        author_info.get('review_count'),
        author_info.get('author_image_url'),
        related_author_list,
        author_books_list
    ))
    connect.commit()
    print("There are " + str(get_author_table_size(connect, cursor)) + " authors in author table")


def store_similar_books(connect, cursor, book_info, stop_number):
    """
    store the similar books in order to traverse
    :param connect: database connect
    :param cursor: database cursor
    :param book_info: current book
    :param stop_number: the critical point that satisfies the requirement
    :return:
    """
    similar_books = book_info.get('similar_books')
    for book in similar_books:
        if get_book_table_size(connect, cursor) >= int(stop_number):
            break
        info = get_book_info(connect, cursor, book.get('url'))
        store_book(connect, cursor, info)
    while True:
        for book in similar_books:
            # condition check if the requirement meets
            if get_book_table_size(connect, cursor) >= int(stop_number):
                break
            more_similar_books = get_book_info(connect, cursor, book.get('url')).get('similar_books')
            for more_book in more_similar_books:
                if get_book_table_size(connect, cursor) >= int(stop_number):
                    break
                info = get_book_info(connect, cursor, more_book.get('url'))
                store_book(connect, cursor, info)
        break


def store_similar_author(connect, cursor, author_info, stop_number):
    """
    store the similar related authors in order to traverse
    :param connect: database connect
    :param cursor: database cursor
    :param author_info: current author
    :param stop_number: the critical point that satisfies the requirement
    :return:
    """
    related_author = author_info.get('related_author')
    for author in related_author:
        if get_author_table_size(connect, cursor) > int(stop_number):
            break
        info = get_author_info(connect, cursor, author.get('related_author_url'))
        store_author(connect, cursor, info)
    while True:
        for author in related_author:
            # condition check if the requirement meets
            if get_author_table_size(connect, cursor) > int(stop_number):
                break
            author_info = author.get('related_author_url')
            more_related_author = get_author_info(connect, cursor, author_info).get('related_author')
            for more_author in more_related_author:
                if get_author_table_size(connect, cursor) > int(stop_number):
                    break
                info = get_author_info(connect, cursor, more_author.get('related_author_url'))
                store_author(connect, cursor, info)
        break


def get_book_table_size(connect, cursor):
    """
    get the current size of book table in the database
    :param connect: database connect
    :param cursor: database cursor
    :return: the size of the book table in the database
    """
    cursor.execute("""select * from book""")
    results = cursor.fetchall()
    connect.commit()
    return len(results)


def get_author_table_size(connect, cursor):
    """
    get the current size of author table in the database
    :param connect: database connect
    :param cursor: database cursor
    :return: the size of the author table in the database
    """
    cursor.execute("""select * from author""")
    results = cursor.fetchall()
    connect.commit()
    return len(results)


def connect_to_db():
    """
    connect to the database
    :return: return the connect and cursor of the connection
    """
    connect = sqlite3.connect('book_and_author_db', check_same_thread=False)
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()
    return connect, cursor


def create_tables(connect, cursor):
    cursor.execute("""DROP TABLE IF EXISTS author""")
    cursor.execute("""DROP TABLE IF EXISTS book""")
    cursor.execute("""CREATE TABLE author(name text, url text, id text, rating text,
                    rating_count text, review_count text, image_url text,
                    related_author text, author_books text) """)
    cursor.execute("""CREATE TABLE book(name text, url text, id text, ISBN text,
                    author_url text, author_name text, rating text, rating_count text,
                    review_count text, image_url text, similar_books text) """)
    connect.commit()


def create_parser():
    """
    create the Command Line Interface
    :return: the arguments that the Command Line Interface has
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('book_url', type=str, help='the GoodReads book website to start with')
    parser.add_argument('--book_number', type=str, default=220,
                        help='the number of books you want to store into database')
    parser.add_argument('--author_number', type=str, default=60,
                        help='the number of authors you want to store into database')
    parser.add_argument('--import_author', type=str, help='the JSON file of author to read from')
    parser.add_argument('--export_author', type=str, help='the JSON file to write the author table to')
    parser.add_argument('--import_book', type=str, help='the JSON file of book to read from')
    parser.add_argument('--export_book', type=str, help='the JSON file to write the book table to')
    parser.add_argument('--GET', type=str, help='GET request')
    return parser.parse_args()


def get_book_table(CONN, CURR):
    CURR.execute("""select * from book""")
    results = CURR.fetchall()
    CONN.commit()
    results = [dict(ix) for ix in results]
    return results


def get_author_table(CONN, CURR):
    CURR.execute("""select * from author""")
    results = CURR.fetchall()
    CONN.commit()
    results = [dict(ix) for ix in results]
    return results


def export_book_json(connect, cursor, filename):
    """
    export the database to a json file
    :param connect: the database connection
    :param cursor: the database cursor
    :param filename: the export file name
    :return:
    """
    results = get_book_table(connect, cursor)
    json_results = json.dumps(results, indent=2)
    with open(filename, 'w') as outfile:
        print("Writing book JSON to file...")
        outfile.write(json_results)


def export_author_json(connect, cursor, filename):
    """
    export the database to a json file
    :param connect: the database connection
    :param cursor: the database cursor
    :param filename: the export file name
    :return:
    """
    cursor.execute("""select * from author""")
    results = cursor.fetchall()
    connect.commit()
    results = [dict(ix) for ix in results]
    json_results = json.dumps(results, indent=2)
    with open(filename, 'w') as outfile:
        print("Writing author JSON to file...")
        outfile.write(json_results)


def import_book_json(connect, cursor, filename):
    """
    import a json file to update database
    :param connect: the database connection
    :param cursor: the database cursor
    :param filename: the imported filename
    :return:
    """
    with open(filename) as inputfile:
        file_data = json.load(inputfile)

    if (type(file_data)) is not dict:
        raise Exception("Wrong data type; expected dict, but got " + type(file_data))

    for data in file_data:
        cursor.execute("""DELETE FROM book WHERE name=(?)""", (data['name'],))
        cursor.execute("""insert into book values (?,?,?,?,?,?,?,?,?,?,?)""", (
            data.get('book_name'),
            data.get('book_url'),
            data.get('book_id'),
            data.get('book_ISBN'),
            data.get('book_author_url'),
            data.get('author_name'),
            data.get('book_rating'),
            data.get('rating_count'),
            data.get('review_count'),
            data.get('image_url'),
            data.get('similar_books')
        ))
        connect.commit()
        print("Book" + data.get('book_name') + " get updated!")


def import_author_json(connect, cursor, filename):
    """
    import a json file to update database
    :param connect: the database connection
    :param cursor: the database cursor
    :param filename: the imported filename
    :return:
    """
    with open(filename) as inputfile:
        file_data = json.load(inputfile)

    if (type(file_data)) is not dict:
        raise Exception("Wrong data type; expected dict, but got " + type(file_data))

    for data in file_data:
        cursor.execute("""DELETE FROM author WHERE name=(?)""", (data['name'],))
        cursor.execute("""insert into author values (?,?,?,?,?,?,?,?,?,?,?)""", (
            data.get('author_name'),
            data.get('author_url'),
            data.get('author_id'),
            data.get('author_rating'),
            data.get('rating_count'),
            data.get('review_count'),
            data.get('author_image_url'),
            data.get('related_author'),
            data.get('author_book')
        ))
        connect.commit()
        print("Author" + data.get('author_name') + " get updated!")


if __name__ == '__main__':
    ARGS = create_parser()
    # check book_url validity
    if ARGS.book_url[:30] != "https://www.goodreads.com/book":
        raise Exception("The book url must be a GoodReads book!")

    CONN, CURR = connect_to_db()
    create_tables(CONN, CURR)
    BOOKINFO = get_book_info(CONN, CURR, ARGS.book_url)
    store_book(CONN, CURR, BOOKINFO)
    store_book(CONN, CURR, get_book_info(CONN, CURR, "https://www.goodreads.com/book/show/54549665-the-death-of-francis-bacon"))
    store_author(CONN, CURR, get_author_info(CONN, CURR, BOOKINFO.get('book_author_url')))
    export_book_json(CONN, CURR, 'temp.txt')
    export_author_json(CONN, CURR, 'temp_author.txt')
    # store_similar_books(CONN, CURR, BOOKINFO, ARGS.book_number)
    # store_similar_author(CONN, CURR, get_author_info(CONN, CURR, BOOKINFO.get('book_author_url')), ARGS.author_number)
    # if ARGS.import_book is not None:
    #     import_book_json(CONN, CURR, ARGS.import_book)
    # if ARGS.export_book is not None:
    #     export_book_json(CONN, CURR, ARGS.export_book)
    # if ARGS.export_author is not None:
    #     export_author_json(CONN, CURR, ARGS.export_author)
    # if ARGS.import_author is not None:
    #     import_author_json(CONN, CURR, ARGS.export_author)
