import os
from flask import Flask, flash, request, redirect, render_template, send_file

app = Flask(__name__)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'upload_files'
app.config['DOWNLOAD_FOLDER'] = 'download_files'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 * 1024 * 1024 * 1024

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'zip']  
uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
downloads = os.path.join(app.root_path, app.config['DOWNLOAD_FOLDER'])
        
@app.route('/')
def main_page() -> 'html':
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        input_file = request.files['file']
        if input_file.filename == '':
            return redirect(request.url)
        if input_file and allowed_file(input_file.filename):
            filename = input_file.filename
            file_extension = os.path.splitext(uploads + '/' + filename)[1]
            
            input_file.save(uploads + '/' + filename)

            file = input_file

            # Место для изменения файла
                            
            ###########################

            output_file = file

            output_file.save(downloads + '/' + filename)

            flash(filename)
            return redirect('/download/' + filename)
        else:
            flash('Allowed file types are ' + ALLOWED_EXTENSIONS)
            return redirect(request.url) 

@app.route('/download/<filename>')
def download_file(filename):

    return send_file(uploads + '/' + filename, attachment_filename=filename, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True)        