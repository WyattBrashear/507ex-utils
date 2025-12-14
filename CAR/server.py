from flask import request, Flask
from werkzeug.utils import secure_filename
import uuid
import os
if not os.path.exists("./static/507ex") or not os.path.exists("./static/"):
    os.makedirs("./static/507ex")
print(os.getcwd())
app = Flask(__name__)

@app.route('/push', methods=['POST'])
def upload_exec():
    if request.method == 'POST':
        executable = request.files['executable']
        if executable.filename.endswith('.507ex'):
            executable_id = uuid.uuid4()
            os.mkdir(f"./static/507ex/{executable_id}")
            executable.save(f"./static/507ex/{executable_id}/{secure_filename(executable.filename)}")
            return {
                "url": f"{request.url_root}static/507ex/{executable_id}/{secure_filename(executable.filename)}"
            }
        else:
            return {
                "error": "Invalid File Type"
            }
