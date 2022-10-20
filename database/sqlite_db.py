import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect("artel.db")
    cur = base.cursor()
    if base:
        print('Database connected!')

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "orders (subject VARCHAR(128), status BOOL, "
                 "description TEXT, full_name VARCHAR(128))")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "performers (subject VARCHAR(128), skills TEXT, "
                 "full_name VARCHAR(128))")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "others (full_name VARCHAR(128), suggestion TEXT)")
    base.commit()


async def add_sql_command(table_name, state):
    async with state.proxy() as data:
        cur.execute(f"INSERT INTO {table_name} VALUES {tuple(data.values())}")
        base.commit()
