from flask import Flask, request, jsonify
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import os
import base64
from io import BytesIO

app = Flask(__name__)

# Ensure output folders exist
os.makedirs("output/batch_qr", exist_ok=True)
os.makedirs("output/student_qr", exist_ok=True)

def generate_qr(data_dict, save_path):
    qr = qrcode.QRCode(
        version=4,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(str(data_dict))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    img.save(save_path, dpi=(300, 300))

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/api/generate-qr", methods=["POST"])
def generate_qr_api():
    qr_images = []
    try:
        data = request.get_json()
        form_type = data.get("form_type")
        test_id = data["test_id"]
        test_name = data["test_name"]
        chapters = data["chapters"]
        subject = data["subject"]
        quantity = int(data["quantity"])

        if form_type == "batch":
            batch_id = data["batch_id"]
            for i in range(1, quantity + 1):
                student_id = f"{batch_id}_STU_{i:03}"
                qr_data = {
                    "batch_id": batch_id,
                    "student_id": student_id,
                    "test_id": test_id,
                    "test_name": test_name,
                    "chapters": chapters,
                    "subject": subject
                }
                path = f"output/batch_qr/{student_id}.png"
                preview = generate_qr(qr_data, path)
                qr_images.append({"label": student_id, "img": preview})

        elif form_type == "student":
            for i in range(1, quantity + 1):
                student_id = f"STU_{i:03}"
                qr_data = {
                    "student_id": student_id,
                    "test_id": test_id,
                    "test_name": test_name,
                    "chapters": chapters,
                    "subject": subject
                }
                path = f"output/student_qr/{student_id}.png"
                preview = generate_qr(qr_data, path)
                qr_images.append({"label": student_id, "img": preview})

        return jsonify({"success": True, "qr_images": qr_images})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
