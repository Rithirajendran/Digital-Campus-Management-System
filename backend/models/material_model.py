from db_config import cursor, db


def add_material(title, subject, file_path, staff_id):

    query = """
    INSERT INTO materials(title, subject, file_path, staff_id)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(query,(title,subject,file_path,staff_id))
    db.commit()


def get_materials():
    query = """
    SELECT material_id, title, subject, file_path
    FROM materials
    ORDER BY subject
    """
    cursor.execute(query)
    return cursor.fetchall()