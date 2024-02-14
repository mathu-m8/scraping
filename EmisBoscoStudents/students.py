import requests
from bs4 import BeautifulSoup


def get_students(url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    students = soup.select_one(".TFtable")
    studentDetails = []
    for row in students.find_all("tr"):
        columns = row.find_all('td')
        student_data = [column.get_text(strip=True) for column in columns]
        if student_data[0] != "S.No.":
            studentDetails.append({
                "full_name": student_data[2],
                "student_id": student_data[1],
                "DOB": student_data[3],
                "grade": student_data[4],
                "division": student_data[5],
                "year": student_data[6]
            })
    return studentDetails


session = requests.Session()

initial_response = session.get("http://www.edudept.np.gov.lk/schoolacc/schoolsignin.php")

if initial_response.ok:
    csrf_token = session.cookies.get_dict().get("csrftoken")

    login_response = session.post(
        "http://www.edudept.np.gov.lk/schoolacc/loginchksch.php",
        data={
            "csrfmiddlewaretoken": csrf_token,
            "username": "1001019",
            "password": "II93xh72",
        },
    )
    if "http://www.edudept.np.gov.lk/schoolacc/search-sch.php" in login_response.url:
        grade_one_Students_details = get_students(
            "http://www.edudept.np.gov.lk/schoolacc/StudentDetails/studenteditlist.php?in=1&ind=All&iny=All")
        grade_two_Students_details = get_students(
            "http://www.edudept.np.gov.lk/schoolacc/StudentDetails/studenteditlist.php?in=2&ind=All&iny=All")
        grade_three_Students_details = get_students(
            "http://www.edudept.np.gov.lk/schoolacc/StudentDetails/studenteditlist.php?in=3&ind=All&iny=All")
        grade_four_Students_details = get_students(
            "http://www.edudept.np.gov.lk/schoolacc/StudentDetails/studenteditlist.php?in=4&ind=All&iny=All")
        grade_five_Students_details = get_students(
            "http://www.edudept.np.gov.lk/schoolacc/StudentDetails/studenteditlist.php?in=5&ind=All&iny=All")
        print(
            grade_one_Students_details + grade_two_Students_details + grade_three_Students_details
            + grade_four_Students_details + grade_five_Students_details
        )

    else:
        print("Login failed")
else:
    print(f"Initial request failed: {initial_response.status_code}")
