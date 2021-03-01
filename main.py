import requests
from bs4 import BeautifulSoup
import sqlite3
import argparse
import warnings
import json


def get_book_info(website):
    """

    :param website:
    :return:
    """
    if get_book_table_size(conn, curr) > 200:
        warnings.warn("There are " + str(get_book_table_size(conn, curr)) + "authors in the table, already greater "
                                                                            "than 200")
    print("getting book info from " + website)
    html_text = requests.get(website)
    soup = BeautifulSoup(html_text.text, 'lxml')
    book_name = soup.find('h1', class_="gr-h1 gr-h1--serif").text.strip()
    book_url = website
    book_id = website.split('/')[-1][:8]
    book_ISBN = None
    book_ISBN_list = soup.find_all('div', class_="infoBoxRowItem")
    for each in book_ISBN_list:
        text = each.text.replace(' ', '').split('\n')
        if len(text) == 4:
            if text[1].isdigit():
                book_ISBN = text[1]
    book_author_url = "https://www.goodreads.com" + soup.find('div', class_="bookAuthorProfile__name").a['href']
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
        'book_ISBN': book_ISBN,
        'book_author_url': book_author_url,
        'author_name': author_name,
        'book_rating': book_rating,
        'rating_count': rating_count,
        'review_count': review_count,
        'image_url': image_url,
        'similar_books': similar_books
    }


def get_author_info(website):
    """

    :param website:
    :return:
    """
    if (get_author_table_size(conn, curr) > 50):
        warnings.warn(
            "There are " + str(get_author_table_size(conn, curr)) + " authors in the table, already greater than 50")
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
    related_author_soup = BeautifulSoup(requests.get("https://www.goodreads.com/" + related_author_link).text, 'lxml')
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


def store_book(conn, curr, book_info):
    """

    :param conn:
    :param curr:
    :param book_info:
    :return:
    """
    similar_books = book_info.get('similar_books')
    similar_books_list = ""
    for i, each_book_info in enumerate(similar_books, 1):
        similar_books_list += str(i) + ". " + each_book_info.get('bookname') + ": " + each_book_info.get('url')
        similar_books_list += "\n"

    curr.execute("""insert into book_tb values (?,?,?,?,?,?,?,?,?,?,?)""", (
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
    conn.commit()


def store_author(conn, curr, author_info):
    """

    :param conn:
    :param curr:
    :param author_info:
    :return:
    """
    related_author = author_info.get('related_author')
    related_author_list = ""
    for i, each_author_info in enumerate(related_author, 1):
        related_author_list += str(i) + ". " + each_author_info.get(
            'related_author_name') + ": " + each_author_info.get('related_author_url')
        related_author_list += "\n"

    author_books = author_info.get('author_books')
    author_books_list = ""
    for i, each_author_book in enumerate(author_books, 1):
        author_books_list += str(i) + ". " + each_author_book.get('book_name') + ": " + each_author_book.get('book_url')
        author_books_list += "\n"

    curr.execute("""insert into author_tb values (?,?,?,?,?,?,?,?,?)""", (
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
    conn.commit()


def store_similar_books(conn, curr, book_info, stop_number):
    """

    :param conn:
    :param curr:
    :param book_info:
    :param stop_number:
    :return:
    """
    similar_books = book_info.get('similar_books')
    for book in similar_books:
        info = get_book_info(book.get('url'))
        store_book(conn, curr, info)
    while True:
        for book in similar_books:
            if get_book_table_size(conn, curr) > stop_number:  # condition check if the requirement meets
                break
            else:
                more_similar_books = get_book_info(book.get('url')).get('similar_books')
                for more_book in more_similar_books:
                    info = get_book_info(more_book.get('url'))
                    store_book(conn, curr, info)
        break


def store_similar_author(conn, curr, author_info, stop_number):
    """

    :param conn:
    :param curr:
    :param author_info:
    :param stop_number:
    :return:
    """
    related_author = author_info.get('related_author')
    for author in related_author:
        info = get_author_info(author.get('related_author_url'))
        store_author(conn, curr, info)
    while True:
        for author in related_author:
            if get_author_table_size(conn, curr) > stop_number:  # condition check if the requirement meets
                break
            else:
                more_related_author = get_author_info(author.get('related_author_url')).get('related_author')
                for more_author in more_related_author:
                    info = get_author_info(more_author.get('related_author_url'))
                    store_author(conn, curr, info)
        break


def get_book_table_size(conn, curr):
    """

    :param conn:
    :param curr:
    :return:
    """
    curr.execute("""select * from book_tb""")
    results = curr.fetchall()
    conn.commit()
    # print("book table size: " + str(len(results)))
    return len(results)


def get_author_table_size(conn, curr):
    curr.execute("""select * from author_tb""")
    results = curr.fetchall()
    conn.commit()
    # print("author table size" + str(len(results)))
    return len(results)


def connect_to_db():
    conn = sqlite3.connect('book_and_author_db')
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    curr.execute("""DROP TABLE IF EXISTS author_tb""")
    curr.execute("""DROP TABLE IF EXISTS book_tb""")
    curr.execute("""CREATE TABLE author_tb(name text, url text, id text, rating text, rating_count text, 
                        review_count text, image_url text, related_author text, author_books text) """)
    curr.execute("""CREATE TABLE book_tb(name text, url text, id text, ISBN text, author_url text, author_name text, 
                        book_rating text, rating_count text, review_count text, image_url text, similar_books text) """)
    conn.commit()
    return conn, curr


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('book_url', type=str, help='the GoodReads book website to start with')
    parser.add_argument('--book_number', type=str, default=220, help='the number of books you want to store into '
                                                                     'database')
    parser.add_argument('--author_number', type=str, default=60, help='the number of authors you want to store into '
                                                                      'database')
    parser.add_argument('--import_JSON', type=str, help='the JSON file to read from')
    parser.add_argument('--export_JSON', type=str, help='the JSON file to write to')
    args = parser.parse_args()
    return args


def export_to_JSON(conn, curr, filename):
    curr.execute("""select * from book_tb""")
    results = curr.fetchall()
    conn.commit()
    results = [dict(ix) for ix in results]
    json_results = json.dumps(results, indent=2)
    with open(filename, 'w') as outfile:
        print("Writing JSON to file...")
        outfile.write(json_results)
    # print(json.dumps([dict(ix) for ix in results]))


if __name__ == '__main__':
    args = create_parser()
    # check book_url validity
    if args.book_url[:30] != "https://www.goodreads.com/book":
        raise Exception("The book url must be a GoodReads book!")

    conn, curr = connect_to_db()
    book_info = get_book_info(args.book_url)
    store_book(conn, curr, book_info)

    # just simple test
    book_info1 = get_book_info('https://www.goodreads.com/book/show/43702.The_Blackwater_Lightship')
    book_info2 = get_book_info('https://www.goodreads.com/book/show/998133.The_Gathering')
    book_info3 = get_book_info('https://www.goodreads.com/book/show/11711.Vernon_God_Little')
    store_book(conn, curr, book_info1)
    store_book(conn, curr, book_info2)
    store_book(conn, curr, book_info3)
    # store_author(conn, curr, get_author_info(book_info.get('book_author_url')))
    # store_similar_books(conn, curr, book_info, args.book_number)
    # store_similar_author(conn, curr, get_author_info(book_info.get('book_author_url')), args.author_number)
    if args.export_JSON is not None:
        export_to_JSON(conn, curr, args.export_JSON)