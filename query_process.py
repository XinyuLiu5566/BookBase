from main import *


class queryProcessor:
    # init method or constructor
    def __init__(self, query):
        self.query = query

    # def normal_search(self, value):

    # def not_search(self, value):

    # def and_search(self, value):
    #     split_value = value.split('AND')
    #     first_value = split_value[0].strip()
    #     second_value = split_value[1].strip()
    #     cursor.execute("""SELECT * from book_tb WHERE %s in (?, ?)""" % field, (first_value, second_value))
    #     results = cursor.fetchall()
    #     results = [dict(ix) for ix in results]
    #     print(results)
    #     connect.commit()

    # def or_search(self, value):
    #
    # def less_than_search(self, value):
    #
    # def greater_than_search(self, value):

    def process_query(self, connect, cursor):
        if '.' not in self.query or ':' not in self.query:
            raise Exception("Invalid query")
        split_query = self.query.split(".")
        table = split_query[0]
        query_attr = split_query[1]
        if table != 'book' and table != 'author':
            raise Exception("Table " + table + " does not exist")

        results = []

        field = query_attr.split(':')[0]
        value = query_attr.split(':')[1]
        # print(field, value)
        if 'AND' in value:
            split_value = value.split('AND')
            first_value = split_value[0].strip()
            second_value = split_value[1].strip()
            cursor.execute("""SELECT * from %s WHERE %s = (?)""" % (table, field), (first_value,))
            first_results = cursor.fetchall()
            first_results = [dict(ix) for ix in first_results]
            # print(first_results)
            connect.commit()

            cursor.execute("""SELECT * from %s WHERE %s = (?)""" % (table, field), (first_value,))
            second_results = cursor.fetchall()
            second_results = [dict(ix) for ix in second_results]
            # print(second_results)
            connect.commit()

            final_result = []
            for each in first_results:
                if each in second_results:
                    final_result.append(each)
            results = final_result
        elif 'OR' in value:
            split_value = value.split('OR')
            first_value = split_value[0].strip()
            second_value = split_value[1].strip()
            cursor.execute("""SELECT * from %s WHERE %s = (?)""" % (table, field), (first_value,))
            first_results = cursor.fetchall()
            first_results = [dict(ix) for ix in first_results]
            # print(first_results)
            connect.commit()

            cursor.execute("""SELECT * from %s WHERE %s = (?)""" % (table, field), (first_value,))
            second_results = cursor.fetchall()
            second_results = [dict(ix) for ix in second_results]
            # print(second_results)
            connect.commit()

            results = first_results + second_results
            # print(results)
        elif 'NOT' in value:
            split_value = value.split('NOT')
            value = split_value[-1].strip()
            cursor.execute("""SELECT * from %s WHERE %s <> (?)""" % (table, field), (value,))
            results = cursor.fetchall()
            results = [dict(ix) for ix in results]
            print(results)
            connect.commit()
        elif '<' in value:
            if field not in ('rating', 'rating_count', 'review_count'):
                raise Exception("Given field " + field + " not comparable")
            split_value = value.split('<')
            value = split_value[-1].strip()
            cursor.execute("""SELECT * from %s WHERE CAST(%s as INTEGER) < (?)""" % (table, field), (value,))
            results = cursor.fetchall()
            results = [dict(ix) for ix in results]
            print(results)
            connect.commit()
        elif '>' in value:
            if field not in ('rating_count', 'review_count', 'rating'):
                raise Exception("Given field " + field + " not comparable")
            split_value = value.split('>')
            value = split_value[-1].strip()
            cursor.execute("""SELECT * from %s WHERE CAST(%s as INTEGER) > (?)""" % (table, field), (value,))
            results = cursor.fetchall()
            results = [dict(ix) for ix in results]
            print(results)
            connect.commit()
        else:
            cursor.execute("""SELECT * from %s WHERE %s = (?)""" % (table, field), (value,))
            results = cursor.fetchall()
            results = [dict(ix) for ix in results]
            print(results)
            connect.commit()
        if table == 'author':
            cursor.execute("""SELECT * from %s WHERE %s = (?)""" % (table, field), (value,))
            results = cursor.fetchall()
            results = [dict(ix) for ix in results]
            connect.commit()

        return results


if __name__ == '__main__':
    p = queryProcessor('book.review_count:<100')
    connect, cursor = connect_to_db()
    p.process_query(connect, cursor)
