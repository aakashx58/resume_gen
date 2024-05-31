from flask import Flask, render_template, request, send_file, Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            details = {
                'name': request.form['name'],
                'email': request.form['email'],
                'contact': request.form['contact'],
                'role': request.form['role'],
                'profile': request.form['profile'],
                'education': request.form['education'],
                'additional_education': request.form['additional_education'],
                'experience': request.form['experience'],
                'past_experience': request.form['past_experience'],
                'skills': request.form['skills'].split(','),
                'projects': request.form['projects']
            }

            pdf_buffer = io.BytesIO()
            p = canvas.Canvas(pdf_buffer, pagesize=letter)
            width, height = letter

            y_pos = height - 72
            for key, value in details.items():
                if isinstance(value, list):
                    value = ', '.join(value)
                p.drawString(72, y_pos, f"{key.capitalize()}: {value}")
                y_pos -= 28

            p.showPage()
            p.save()
            pdf_buffer.seek(0)

            response = send_file(
                io.BytesIO(pdf_buffer.getvalue()),
                mimetype='application/pdf',
                as_attachment=True,
                download_name='resume.pdf'
            )
            return response
        except Exception as e:
            return str(e), 500

    return render_template('index.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

if __name__ == '__main__':
    app.run(debug=True)
