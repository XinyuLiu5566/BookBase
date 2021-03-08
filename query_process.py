from main import *


def check_quote(string):
    if string.startswith("\"") and string.endswith("\""):
        return True
    else:
        return False


class queryProcessor:
    # init method or constructor
    def __init__(self, query):
        self.query = query
        self.CONN, self.CURR = connect_to_db()


    def execute_quote_query(self, table, field, value):
        value = value[1:-1]
        self.CURR.execute("""SELECT * from %s WHERE %s = (?)""" % (table, field), (value,))
        results = self.CURR.fetchall()
        results = [dict(ix) for ix in results]
        self.CONN.commit()
        return results

    def execute_nonquote_query(self, table, field, value):
        value = "%"+value+"%"
        self.CURR.execute("""SELECT * from %s WHERE %s LIKE (?)""" % (table, field), (value,))
        results = self.CURR.fetchall()
        results = [dict(ix) for ix in results]
        self.CONN.commit()
        return results
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

    def process_query(self):
        if '.' not in self.query or ':' not in self.query:
            raise Exception("Invalid query")
        split_query = self.query.split(".")
        table = split_query[0]
        query_attr = split_query[1]
        if table != 'book' and table != 'author':
            raise Exception("Table " + table + " does not exist")

        # results = []

        field = query_attr.split(':')[0].strip()
        value = query_attr.split(':')[1].strip()
        # print(field, value)
        if 'AND' in value:
            split_value = value.split('AND')
            first_value = split_value[0].strip()
            second_value = split_value[1].strip()
            if check_quote(first_value):
                first_results = self.execute_quote_query(table, field, first_value)
            else:
                first_results = self.execute_nonquote_query(table, field, first_value)
            if check_quote(second_value):
                second_results = self.execute_quote_query(table, field, second_value)
            else:
                second_results = self.execute_nonquote_query(table, field, second_value)
            final_result = []
            for each in first_results:
                if each in second_results:
                    final_result.append(each)
            results = final_result
        elif 'OR' in value:
            split_value = value.split('OR')
            first_value = split_value[0].strip()
            second_value = split_value[1].strip()
            if check_quote(first_value):
                first_results = self.execute_quote_query(table, field, first_value)
            else:
                first_results = self.execute_nonquote_query(table, field, first_value)
            if check_quote(second_value):
                second_results = self.execute_quote_query(table, field, second_value)
            else:
                second_results = self.execute_nonquote_query(table, field, second_value)

            results = first_results + second_results
            # print(results)
        elif 'NOT' in value:
            split_value = value.split('NOT')
            value = split_value[-1].strip()
            if check_quote(value):
                self.CURR.execute("""SELECT * from %s WHERE %s <> (?)""" % (table, field), (value,))
                results = self.CURR.fetchall()
                results = [dict(ix) for ix in results]
                print(results)
                self.CONN.commit()
            else:
                self.CURR.execute("""SELECT * from %s WHERE %s <> (?)""" % (table, field), (value,))
                results = self.CURR.fetchall()
                results = [dict(ix) for ix in results]
                print(results)
                self.CONN.commit()
        elif '<' in value:
            if field not in ('rating', 'rating_count', 'review_count'):
                raise Exception("Given field " + field + " not comparable")
            split_value = value.split('<')
            value = split_value[-1].strip()
            if check_quote(value):
                self.CURR.execute("""SELECT * from %s WHERE CAST(%s as INTEGER) < (?)""" % (table, field), (value,))
                results = self.CURR.fetchall()
                results = [dict(ix) for ix in results]
                print(results)
                self.CONN.commit()
            else:
                self.CURR.execute("""SELECT * from %s WHERE CAST(%s as INTEGER) < (?)""" % (table, field), (value,))
                results = self.CURR.fetchall()
                results = [dict(ix) for ix in results]
                print(results)
                self.CONN.commit()
        elif '>' in value:
            if field not in ('rating_count', 'review_count', 'rating'):
                raise Exception("Given field " + field + " not comparable")
            split_value = value.split('>')
            value = split_value[-1].strip()
            if check_quote(value):
                self.CURR.execute("""SELECT * from %s WHERE CAST(%s as INTEGER) > (?)""" % (table, field), (value,))
                results = self.CURR.fetchall()
                results = [dict(ix) for ix in results]
                print(results)
                self.CONN.commit()
            else:
                self.CURR.execute("""SELECT * from %s WHERE CAST(%s as INTEGER) > (?)""" % (table, field), (value,))
                results = self.CURR.fetchall()
                results = [dict(ix) for ix in results]
                print(results)
                self.CONN.commit()
        else:
            print(table, field, value)
            if check_quote(value):
                results = self.execute_quote_query(table, field, value)
            else:
                results = self.execute_nonquote_query(table, field, value)
        print(results)
        return results


if __name__ == '__main__':
    p = queryProcessor('book.id:"11711"')
    p.process_query()
