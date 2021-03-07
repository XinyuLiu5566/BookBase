from flask import Flask, jsonify, request, Response
from main import connect_to_db, get_book_table, get_author_table, \
    get_book_info, get_author_info, store_author, store_book
from query_process import *


app = Flask(__name__)
app.config["DEBUG"] = True
connect, cursor = connect_to_db()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/book', methods=['GET'])
def get_book_by_id():
    books = get_book_table(connect, cursor)
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "You must have an id to search"
    results = []
    for book in books:
        if book['id'] == id:
            results.append(book)
    if results:
        return jsonify(results)
    else:
        return Response(status=400)


@app.route('/api/author', methods=['GET'])
def get_author_by_id():
    authors = get_author_table(connect, cursor)
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "You must have an id to search"

    results = []
    for author in authors:
        if author['id'] == id:
            results.append(author)
    if results:
        print(jsonify(results))
        return jsonify(results)
    else:
        return Response(status=400)


@app.route('/api/search', methods=['GET'])
def search():
    if 'q' in request.args:
        query = request.args['q']
        query_processor = queryProcessor(query)
        results = query_processor.process_query(connect, cursor)
    else:
        return "you must have a query to search!"
    if results is not None:
        return jsonify(results)
    else:
        return Response(status=400)


@app.route('/api/book', methods=['PUT'])
def update_book_by_id():
    books = get_book_table(connect, cursor)
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "You must have an id to update"
    if not books:
        return Response(status=400)
    book = None
    cursor.execute("""DELETE FROM book WHERE id=(?)""", (id,))
    connect.commit()
    for each_book in books:
        if each_book['id'] == id:
            book = each_book
    # print(book)
    for each_attr, attr_value in request.json.items():
        book[each_attr] = attr_value
    # print(book)
    cursor.execute("""insert into book values (?,?,?,?,?,?,?,?,?,?,?)""", (
        book.get('name'),
        book.get('url'),
        book.get('id'),
        book.get('ISBN'),
        book.get('author_url'),
        book.get('author_name'),
        book.get('book_rating'),
        book.get('rating_count'),
        book.get('review_count'),
        book.get('image_url'),
        book.get('similar_books')
    ))
    connect.commit()
    if book:
        return Response(status=204)
    else:
        return Response(status=400)


@app.route('/api/author', methods=['PUT'])
def update_author_by_id():
    authors = get_author_table(connect, cursor)
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "You must have an id to update"
    if not authors:
        return Response(status=400)

    author = None
    cursor.execute("""DELETE FROM author WHERE id=(?)""", (id,))
    connect.commit()
    for each_author in authors:
        if each_author['id'] == id:
            author = each_author
    # print(book)
    for each_attr, attr_value in request.json.items():
        author[each_attr] = attr_value
    # print(book)
    cursor.execute("""insert into author values (?,?,?,?,?,?,?,?,?,?,?)""", (
        author.get('author_name'),
        author.get('author_url'),
        author.get('author_id'),
        author.get('author_rating'),
        author.get('rating_count'),
        author.get('review_count'),
        author.get('author_image_url'),
        author.get('related_author'),
        author.get('author_book')
    ))
    connect.commit()
    if author:
        return Response(status=204)
    else:
        return Response(status=400)


@app.route('/api/book', methods=['POST'])
def post_book_to_database():
    book = request.json
    cursor.execute("""insert into book values (?,?,?,?,?,?,?,?,?,?,?)""", (
        book.get('name'),
        book.get('url'),
        book.get('id'),
        book.get('ISBN'),
        book.get('author_url'),
        book.get('author_name'),
        book.get('book_rating'),
        book.get('rating_count'),
        book.get('review_count'),
        book.get('image_url'),
        book.get('similar_books')
    ))
    connect.commit()
    if book:
        return Response(status=204)
    else:
        return Response(status=400)


@app.route('/api/author', methods=['POST'])
def post_author_to_database():
    author = request.json
    cursor.execute("""insert into author values (?,?,?,?,?,?,?,?,?,?,?)""", (
        author.get('author_name'),
        author.get('author_url'),
        author.get('author_id'),
        author.get('author_rating'),
        author.get('rating_count'),
        author.get('review_count'),
        author.get('author_image_url'),
        author.get('related_author'),
        author.get('author_book')
    ))
    connect.commit()
    if author:
        return Response(status=204)
    else:
        return Response(status=400)


@app.route('/api/books', methods=['POST'])
def post_books_to_database():
    books = request.json
    for book in books:
        cursor.execute("""insert into book values (?,?,?,?,?,?,?,?,?,?,?)""", (
            book.get('name'),
            book.get('url'),
            book.get('id'),
            book.get('ISBN'),
            book.get('author_url'),
            book.get('author_name'),
            book.get('book_rating'),
            book.get('rating_count'),
            book.get('review_count'),
            book.get('image_url'),
            book.get('similar_books')
        ))
        connect.commit()
    if books:
        return Response(status=204)
    else:
        return Response(status=400)


@app.route('/api/authors', methods=['POST'])
def post_authors_to_database():
    authors = request.json
    for author in authors:
        cursor.execute("""insert into author values (?,?,?,?,?,?,?,?,?,?,?)""", (
            author.get('author_name'),
            author.get('author_url'),
            author.get('author_id'),
            author.get('author_rating'),
            author.get('rating_count'),
            author.get('review_count'),
            author.get('author_image_url'),
            author.get('related_author'),
            author.get('author_book')
        ))
        connect.commit()
    if authors:
        return Response(status=204)
    else:
        return Response(status=400)


@app.route('/api/scrape', methods=['POST'])
def post_scrape():
    book_id = None
    author_id = None
    book_info = None
    author_info = None
    if 'book_id' in request.args:
        book_id = request.args['book_id']
    elif 'author_id' in request.args:
        author_id = request.args['author_id']
    else:
        return "You must have either an book_id or author_id to search"

    if book_id:
        url = "https://www.goodreads.com/book/show/" + book_id
        print(url)
        book_info = get_book_info(connect, cursor, url)
        store_book(connect, cursor, book_info)

    if author_id:
        url = "https://www.goodreads.com/book/show/" + author_id
        author_info = get_author_info(connect, cursor, url)
        store_author(connect, cursor, author_info)

    if book_info or author_info:
        return Response(status=204)
    else:
        return Response(status=400)


@app.route('/api/book', methods=['DELETE'])
def delete_book_by_id():
    books = get_book_table(connect, cursor)
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "You must have an id to delete"

    cursor.execute("""DELETE FROM book WHERE id=(?)""", (id,))
    connect.commit()

    book = None
    for each_book in books:
        if each_book['id'] == id:
            book = each_book
    if book:
        return Response(status=204)
    else:
        return Response(status=400)


@app.route('/api/author', methods=['DELETE'])
def delete_author_by_id():
    authors = get_author_table(connect, cursor)
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "You must have an id to delete"

    cursor.execute("""DELETE FROM author WHERE id=(?)""", (id,))
    connect.commit()

    author = None
    for each_author in authors:
        if each_author['id'] == id:
            author = each_author
    if author:
        return Response(status=204)
    else:
        return Response(status=400)


app.run()
