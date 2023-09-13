import os.path
import sys

from flask import Flask, render_template, request, send_file
from pathlib import Path
from resultsparser.excel_parser.excel_parser import ExcelParser
from resultsparser.result_generator.result_generator import ResultsGenerator


app = Flask(__name__, template_folder="front_end/templates/")


# Define the route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
            # Save the uploaded file to a folder
                if not Path('uploads').exists():
                    Path('uploads').mkdir()
                file_path = Path('uploads') / uploaded_file.filename
                uploaded_file.save(file_path)

                excel_file = file_path
                parser = ExcelParser(excel_file)
                student_data = parser.parse()
                for student in student_data:
                    student.perform_logic()
                results = ResultsGenerator(student_list=student_data)
                results.output_results()
                output_file_dir = Path("output")
                output_results_file = list(output_file_dir.glob("*.xlsx"))[0]
                return send_file(path_or_file=output_results_file, as_attachment=False)

    return render_template("template.html")

if __name__ == '__main__':
    app.run()
