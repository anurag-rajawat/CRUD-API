courses = [
    {
        "id": 1,
        "name": "Introduction to Database",
        "description": "This course is designed by keeping beginners in mind",
        "length": "2.10.00"},
    {
        "id": 2,
        "name": "Introduction to DB-Design",
        "description": "This is an intermediate course for this you've a good understanding of databases",
        "length": "5.10.00"},
    {
        "id": 3,
        "name": "Introduction to Flask",
        "description": "Introductory Flask course",
        "length": "1.12.11"}
]

ID = 4  # ID of newly added courses


def find_course(id):
    for course in courses:
        if course["id"] == id:
            return course
    return None


def find_course_idx(id):
    for idx, course in enumerate(courses):
        if course['id'] == id:
            return idx
    return None
