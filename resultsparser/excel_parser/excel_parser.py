# excel_parser.py
import pandas as pd
from resultsparser.student.student import Student


class ExcelParser:
    def __init__(self, act_results_file_path):
        self.act_results_file_path = act_results_file_path

    def parse(self):
        students = []
        df_result_file = pd.read_excel(self.act_results_file_path, engine="openpyxl")

        df_result_file["Full Name"] = df_result_file["First name"].str.capitalize() + " " + df_result_file[
            "Surname"].str.capitalize()
        df_result_file = df_result_file.drop(["First name", "Surname", "Last downloaded from this course"], axis=1)
        df_result_file = df_result_file.dropna(axis=1)
        columns_to_clean = df_result_file.columns.difference(["Full Name", "Email address"])
        for index, row in df_result_file.iterrows():
            name, student_email = row["Full Name"], row["Email address"]
            cleaned_columns = row[columns_to_clean].replace('%', '', regex=True)
            cleaned_columns = cleaned_columns.replace("-", 0, regex=True)
            quiz_scores = cleaned_columns.to_dict()
            student = Student(name, student_email, quiz_scores)
            students.append(student)

        return students
