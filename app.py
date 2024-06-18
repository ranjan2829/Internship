from flask import Flask, request, jsonify, render_template, redirect, url_for
import cv2
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    candidate_name = request.form.get('name')
    email = request.form.get('email')
    
    if not candidate_name or not email:
        return jsonify({"error": "Name and email are required"}), 400
    
    if len(candidate_name) > 20:
        return jsonify({"error": "Name must be 20 characters or less"}), 400
    
    certificate_url = create_certificate(candidate_name)
    
    return redirect(url_for('view_certificate', certificate_url=certificate_url))

def add_name_to_certificate(candidate_name):
    cert_template_path = 'sample_certificate.png'
    if not os.path.exists(cert_template_path):
        raise FileNotFoundError(f"Certificate template not found at {cert_template_path}")
    
    cert_template = cv2.imread(cert_template_path)
    if cert_template is None:
        raise ValueError("Error loading certificate template")
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 2
    font_color = (0, 0, 0)  
    y_position = 500  
    
    text_size = cv2.getTextSize(candidate_name, font, font_size, 2)[0]
    x_position = (cert_template.shape[1] - text_size[0]) // 2

    cv2.putText(cert_template, candidate_name, (x_position, y_position), font, font_size, font_color, 2)
    
    output_dir = 'static/output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{candidate_name}.png')
    cv2.imwrite(output_path, cert_template)
    return output_path

def create_certificate(candidate_name):
    certificate_path = add_name_to_certificate(candidate_name)
    
    # Assuming certificates are accessible under the static directory
    certificate_url = url_for('static', filename=f'output/{candidate_name}.png', _external=True)
    
    return certificate_url

@app.route('/certificate')
def view_certificate():
    certificate_url = request.args.get('certificate_url')
    if certificate_url:
        return f'<iframe src="{certificate_url}" width="100%" height="100%"></iframe>'
    else:
        return jsonify({"error": "Certificate not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
