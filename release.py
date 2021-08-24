# coding=utf-8
import my_function


def preparation_db():
    sql = """
        CREATE TABLE numbers(
        name text NOT NULL UNIQUE,
        number integer NOT NULL DEFAULT 0
        );
    """
    my_function.execute_sql(sql)


if __name__ == '__main__':
    preparation_db()
    print('DB is prepared')
