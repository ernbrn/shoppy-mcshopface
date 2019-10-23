from flask import (jsonify)


def return_list(rows):
    return jsonify(array_of_dicts_from_rows(rows))


def return_dict(row):
    return jsonify(create_dict_from_row(row))


def create_dict_from_row(row):
    row_dict = {}

    if row is None:
        return row_dict

    row_keys = row.keys()
    for row_key in row_keys:
        row_dict[row_key] = row[row_key]
    return row_dict


def array_of_dicts_from_rows(rows):
    return_array = []
    for row in rows:
        return_array.append(create_dict_from_row(row))

    return return_array


def last_inserted_row(db, table_name):
    last_row_id = db.execute(
        'SELECT last_insert_rowid() as id').fetchone()['id']
    return db.execute(
        'SELECT * FROM ' + table_name + ' WHERE id = ?', (last_row_id,)).fetchone()
