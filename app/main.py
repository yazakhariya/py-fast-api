from fastapi import FastAPI, HTTPException
from utils import json_to_dict
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel
import requests

script_dir = Path(__file__).parent.resolve()
path_to_json = script_dir.parent / 'students.json'

class Student(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    date_of_birth: str
    email: str
    address: str
    enrollment_year: Optional[int]
    major: Optional[str]
    course: int

app = FastAPI()
students_data = None

def load_students_data():
    global students_data
    if students_data is None:
        students_data = json_to_dict(path_to_json) # Load JSON only once
    return students_data

@app.get("/students")
def get_students():
    return json_to_dict(path_to_json)

@app.get("/students/{course}", response_model=List[Student])
def get_students_by_courses(
        course: int, 
        major: Optional[str] = None, 
        enrollment_year: Optional[int] = 2018
    ) -> List[Student]:
    students_data = json_to_dict(path_to_json)
    students = [Student(**s) for s in students_data]

    filtered_students = [
        s for s in students
        if s.course == course
        and (major is None or s.major.lower() == major.lower())
        and (enrollment_year is None or s.enrollment_year == enrollment_year)
    ]

    if not filtered_students:
        raise HTTPException(status_code=404, detail="No students are found")

    return filtered_students


def get_students_with_params(
        course: int, 
        major: Optional[str] = None,
        enrollment_year: Optional[int] = None
    ):

    url = f"http://127.0.0.1:8000/students/{course}"
    params = {"major": major, "enrollment_year": enrollment_year}

    try:
        response = requests.get(url, 
            params={k: v for k, v in params.items() if v is not None}
        )
        return response.json()
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return []
    
@app.get("/test")
def test_endpoint():
    students = get_students_with_params(3, major="Математика")
    return {"result": students}