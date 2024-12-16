from pypdf import PdfReader
from dataclasses import dataclass
import re
import os

# Regexes
code_reg = r'([A-Z]{4}\d{2})'
scope_reg = r'\b(\d+\.\d+)\s*hp\b'
grade_reg = r'(?<!\S)([G345])(?!\S)'


@dataclass
class Course:
    code: str
    scope: float
    grade: int


pdf_file = "Records.pdf"
reader = PdfReader(pdf_file)

courses = []

for page in reader.pages:
    text = page.extract_text()
    # Split the lines at the last integer on each line
    # and not on actual newlines in the pdf
    lines = re.split(r'\b(?<!\S)(1|2)(?!\S)\b', text)

    for line in lines:
        code_match = re.search(code_reg, line)

        scope_match = re.search(scope_reg, line)

        grade_match = re.search(grade_reg, line)

        if code_match and scope_match and grade_match:
            course_code = code_match.group()
            course_scope = scope_match.group().replace("hp", "")
            course_grade = grade_match.group()
            courses.append(Course(
                code=course_code,
                scope=float(course_scope),
                grade=int(course_grade) if course_grade.isdigit(
                ) else course_grade
            ))

# Extract text from page 2
text = reader.pages[1].extract_text()

# Total HP
match = re.search(r'\b(\d+\.\d+)\s*hp\b', text)

total_hp = float(match.group().replace("hp", ""))

sum = 0
scope_to_exclude = 0
for course in courses:
    if isinstance(course.grade, int):
        sum += course.grade * course.scope
    else:
        scope_to_exclude += course.scope

gpa = sum / (total_hp - scope_to_exclude)

print(f"Grade point average: {gpa}")
