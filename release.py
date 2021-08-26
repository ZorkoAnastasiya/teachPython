# coding=utf-8
import my_function


def preparation_db() -> None:
    """Creating a table in the database."""

    sql = """
        CREATE TABLE IF NOT EXISTS numbers(
        name text NOT NULL UNIQUE,
        number integer NOT NULL DEFAULT 0
        );
    """

    my_function.execute_sql(sql)


if __name__ == '__main__':

    preparation_db()

    print('DATABASE is prepared')
