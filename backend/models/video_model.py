from db_config import cursor, db


# ===============================
# Add Video (Staff)
# ===============================
def add_video(title, subject, youtube_link, staff_id):

    query = """
    INSERT INTO video_materials(title, subject, youtube_link, staff_id)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(query, (title, subject, youtube_link, staff_id))
    db.commit()


# ===============================
# Get Videos (Student)
# ===============================
def get_videos():

    query = "SELECT title, subject, youtube_link FROM video_materials ORDER BY subject"

    cursor.execute(query)

    return cursor.fetchall()