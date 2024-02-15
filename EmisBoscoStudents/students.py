import requests
from bs4 import BeautifulSoup
import json


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

        students = grade_one_Students_details + grade_two_Students_details + grade_three_Students_details + grade_four_Students_details + grade_five_Students_details
        #     get students all details
        modified_students_details = []
        enrollments = []
        student_basic_modified_data = {}
        for student in students:
            student_basic_data = {}
            single_student_basic_modified_details = {}
            enrolled_student = {}
            student_id = student['student_id']
            response = session.get(
                f"http://www.edudept.np.gov.lk/schoolacc/StudentDetails/dbstudenteditlistSch.php?StudentID={student_id}&selectins=1&selectinsd=All&selectinsy=All")
            soup = BeautifulSoup(response.text, "html.parser")
            elements_input = soup.find_all("input")
            for element in elements_input:
                input_name = element['name']
                input_value = element['value']
                student_basic_data[input_name] = input_value

            elements_select = soup.find_all("select")
            for element in elements_select:
                select_element_name = element["name"]
                elements_select_first_option = element.find("option")["value"]
                student_basic_data[select_element_name] = elements_select_first_option
            # set school id - pk
            single_student_basic_modified_details["pk"] = "01HKJF6VRGPDD46MCVV02VTPSD"
            # set grade one entry year + index number - sk
            if student_basic_data["Grade"] == "1":
                student_basic_data["grade_one_entry_year"] = 2023
            if student_basic_data["Grade"] == "2":
                student_basic_data["grade_one_entry_year"] = 2022
            if student_basic_data["Grade"] == "3":
                student_basic_data["grade_one_entry_year"] = 2021
            if student_basic_data["Grade"] == "4":
                student_basic_data["grade_one_entry_year"] = 2020
            if student_basic_data["Grade"] == "5":
                student_basic_data["grade_one_entry_year"] = 2019
            single_student_basic_modified_details[
                "sk"] = f"{student_basic_data['grade_one_entry_year']}:{student_basic_data['CurrSchAdmNo']}"  # SK

            # first_name  and last name
            full_name = student_basic_data["StFullName"]
            split_name = student_basic_data["StNameWithInitial"].split(
                ".")
            student_first_name = ''
            if split_name[-1] == '':
                student_first_name = split_name[-2]
            else:
                student_first_name = split_name[-1]
            father_name = full_name.replace(student_first_name, "")

            if student_basic_data["Sex"] == "Female":
                single_student_basic_modified_details["first_name"] = student_first_name
                single_student_basic_modified_details[
                    "last_name"] = father_name
            else:
                single_student_basic_modified_details[
                    "first_name"] = father_name
                single_student_basic_modified_details[
                    "last_name"] = student_first_name

            # phone
            single_student_basic_modified_details["phone"] = student_basic_data["ContactNo"]
            # gender
            single_student_basic_modified_details["gender"] = student_basic_data["Sex"]
            # dob
            single_student_basic_modified_details["dob"] = student_basic_data["DateofBirth"]
            # is_special_need
            if student_basic_data["SpecialNeed"] == "Yes":
                single_student_basic_modified_details["is_special_need"] = True
            else:
                single_student_basic_modified_details["is_special_need"] = False
            # address
            single_student_basic_modified_details["address"] = student_basic_data["StHomeAddress"]
            # gn_division
            single_student_basic_modified_details["gn_division"] = student_basic_data["GNdivision"]
            # religion
            single_student_basic_modified_details["religion"] = student_basic_data["Religion"]
            # medium
            single_student_basic_modified_details["medium"] = student_basic_data["Medium"]
            # family_income_range
            single_student_basic_modified_details["family_income_range"] = student_basic_data["FamilyIncome"]
            # father_first_name
            single_student_basic_modified_details["father_first_name"] = student_basic_data["FatherFName"]
            # father_last_name
            single_student_basic_modified_details["father_last_name"] = student_basic_data["FatherLName"]
            # father_nic_no
            single_student_basic_modified_details["father_nic_no"] = student_basic_data["FatherNIC"]
            # father_phone
            single_student_basic_modified_details["father_phone"] = student_basic_data["FatherContactNo"]
            # mother_first_name
            single_student_basic_modified_details["mother_first_name"] = student_basic_data["MotherFName"]
            # mother_last_name
            single_student_basic_modified_details["mother_last_name"] = student_basic_data["MotherLName"]
            # mother_nic_no
            single_student_basic_modified_details["mother_nic_no"] = student_basic_data["MotherNIC"]
            # mother_phone
            single_student_basic_modified_details["mother_phone"] = student_basic_data["MotherContactNo"]

            # pk of enrollment
            enrolled_student["pk"] = student_basic_data["yearofstudy"]
            # sk of enrollment
            enrolled_student[
                "sk"] = f"{student_basic_data['Grade']}:{student_basic_data['GradeDivision']}:{student_basic_data['grade_one_entry_year']}_{student_basic_data['CurrSchAdmNo']}"
            enrolled_student["first_name"] = single_student_basic_modified_details["first_name"]
            enrolled_student["last_name"] = single_student_basic_modified_details["last_name"]
            enrolled_student["gender"] = single_student_basic_modified_details["gender"]

            modified_students_details.append(single_student_basic_modified_details)
            enrollments.append(enrolled_student)
        json_students_data = json.dumps(modified_students_details, indent=2)
        json_enrollment_data = json.dumps(modified_students_details, indent=2)

        with open('students.json', 'w') as json_file:
            json_file.write(json_students_data)
        with open('enrollments.json', 'w') as json_file:
            json_file.write(json_enrollment_data)
        print("Successfully saved")
