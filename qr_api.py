# from flask import Flask, request, jsonify
# from reportlab.graphics.barcode.qr import QrCodeWidget
# import qrcode
# from qrcode.constants import ERROR_CORRECT_H
# from PIL import Image
# from flask_cors import CORS
# import os
# import base64
# from io import BytesIO

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002","https://admin.neet720.com", "https://neet720.com"])

# # Ensure output folders exist
# os.makedirs("output/batch_qr", exist_ok=True)
# os.makedirs("output/student_qr", exist_ok=True)

# def generate_qr(data_dict, save_path):
#     qr = qrcode.QRCode(
#         version=4,
#         error_correction=ERROR_CORRECT_H,
#         box_size=10,
#         border=4
#     )
#     qr.add_data(str(data_dict))
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

#     img.save(save_path, dpi=(300, 300))

#     buffer = BytesIO()
#     img.save(buffer, format="PNG")
#     encoded = base64.b64encode(buffer.getvalue()).decode()
#     return f"data:image/png;base64,{encoded}"

# @app.route("/health", methods=["GET"])
# def health_check():
#     return jsonify({"status": "ok"}), 200

# @app.route("/api/generate-qr", methods=["POST"])
# def generate_qr_api():
#     qr_images = []
#     try:
#         data = request.get_json()
#         form_type = data.get("form_type")
#         test_id = data["test_id"]
#         test_name = data["test_name"]

#         subject = data["subject"]
#         student_name = data.get("student_name", "")
#         quantity = int(data["quantity"])

#         if form_type == "batch":
#             batch_id = data["batch_id"]
#             for i in range(1, quantity + 1):
#                 student_id = f"{batch_id}_STU_{i:03}"
#                 qr_data = {
#                     "batch_id": batch_id,
#                     "student_id": student_id,
#                     "test_id": test_id,
#                     "test_name": test_name,
#                     "subject": subject
#                 }
#                 path = f"output/batch_qr/{student_id}.png"
#                 preview = generate_qr(qr_data, path)
#                 qr_images.append({"label": student_id, "img": preview})

#         elif form_type == "student":
#             for i in range(1, quantity + 1):
#                 student_id = f"STU_{i:03}"
#                 qr_data = {
#                     "student_id": student_id,
#                     "test_id": test_id,
#                     "test_name": test_name,
#                     "student_name": student_name,
#                     "subject": subject
#                 }
#                 path = f"output/student_qr/{student_id}.png"
#                 preview = generate_qr(qr_data, path)
#                 qr_images.append({"label": student_id, "img": preview})

#         return jsonify({"success": True, "qr_images": qr_images})

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# from PIL import Image, ImageDraw
# import base64
# from io import BytesIO

# def generate_qr_image(data_dict, size=(78, 78)):
#     """Generate a QR code PIL Image from a data dict."""
#     student_data = "|".join(f"{k}:{v}" for k, v in data_dict.items())
    
#     qr_widget = QrCodeWidget(student_data)
#     qr_obj = qr_widget.qr
#     qr_obj.make()

#     module_count = qr_obj.getModuleCount()
#     cell_size = 5
#     border = 2
#     img_size = (module_count + border * 2) * cell_size
    
#     qr_img = Image.new("RGB", (img_size, img_size), "white")
#     draw = ImageDraw.Draw(qr_img)

#     for row in range(module_count):
#         for col in range(module_count):
#             if qr_obj.isDark(row, col):
#                 x0 = (col + border) * cell_size
#                 y0 = (row + border) * cell_size
#                 draw.rectangle([x0, y0, x0 + cell_size, y0 + cell_size], fill="black")

#     return qr_img.resize(size, Image.NEAREST)


# def embed_qr_on_omr(omr_path, qr_img, box=(718, 8, 796, 90)):
#     """Paste QR onto the OMR sheet at the given box coords and return base64."""
#     omr = Image.open(omr_path).convert("RGB")
#     x1, y1, x2, y2 = box
#     pad = 4
#     qr_resized = qr_img.resize((x2 - x1 - pad * 2, y2 - y1 - pad * 2), Image.NEAREST)
#     omr.paste(qr_resized, (x1 + pad, y1 + pad))

#     buf = BytesIO()
#     omr.save(buf, format="PNG", dpi=(300, 300))
#     encoded = base64.b64encode(buf.getvalue()).decode()
#     return f"data:image/png;base64,{encoded}"


# @app.route("/api/generate-omr-with-qr", methods=["POST"])
# def generate_omr_with_qr():
#     """
#     Generates QR codes embedded directly into OMR sheet images.
#     Expects: { omr_template_path, form_type, test_id, test_name, subject, quantity, batch_id? }
#     """
#     try:
#         data = request.get_json()
#         omr_path = data["omr_template_path"]   # path to the blank OMR PNG
#         form_type = data.get("form_type", "batch")
#         test_id = data["test_id"]
#         test_name = data["test_name"]
#         subject = data["subject"]
#         quantity = int(data["quantity"])
#         results = []

#         for i in range(1, quantity + 1):
#             if form_type == "batch":
#                 batch_id = data["batch_id"]
#                 student_id = f"{batch_id}_STU_{i:03}"
#                 qr_data = {
#                     "batch_id": batch_id,
#                     "student_id": student_id,
#                     "test_id": test_id,
#                     "test_name": test_name,
#                     "subject": subject,
#                 }
#             else:
#                 student_id = f"STU_{i:03}"
#                 qr_data = {
#                     "student_id": student_id,
#                     "test_id": test_id,
#                     "test_name": test_name,
#                     "student_name": data.get("student_name", ""),
#                     "subject": subject,
#                 }

#             qr_img = generate_qr_image(qr_data)
#             omr_base64 = embed_qr_on_omr(omr_path, qr_img)

#             results.append({"label": student_id, "img": omr_base64})

#         return jsonify({"success": True, "omr_sheets": results})

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

from flask import Flask, request, jsonify
from flask_cors import CORS
from reportlab.graphics.barcode.qr import QrCodeWidget
from PIL import Image, ImageDraw
import base64
import os
from io import BytesIO

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "https://admin.neet720.com",
    "https://neet720.com"
])

os.makedirs("output/batch_qr", exist_ok=True)
os.makedirs("output/student_qr", exist_ok=True)


def generate_qr_image(data_dict, size=(78, 78)):
    """Generate a QR code PIL Image from a data dict."""
    student_data = "|".join(f"{k}:{v}" for k, v in data_dict.items())

    qr_widget = QrCodeWidget(student_data)
    qr_obj = qr_widget.qr
    qr_obj.make()

    module_count = qr_obj.getModuleCount()
    cell_size = 5
    border = 2
    img_size = (module_count + border * 2) * cell_size

    qr_img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(qr_img)

    for row in range(module_count):
        for col in range(module_count):
            if qr_obj.isDark(row, col):
                x0 = (col + border) * cell_size
                y0 = (row + border) * cell_size
                draw.rectangle([x0, y0, x0 + cell_size, y0 + cell_size], fill="black")

    return qr_img.resize(size, Image.NEAREST)


def embed_qr_on_omr(omr_path, qr_img, box=(718, 8, 796, 90)):
    """Paste QR onto the OMR sheet at the given box coords and return base64."""
    omr = Image.open(omr_path).convert("RGB")
    x1, y1, x2, y2 = box
    pad = 4
    qr_resized = qr_img.resize((x2 - x1 - pad * 2, y2 - y1 - pad * 2), Image.NEAREST)
    omr.paste(qr_resized, (x1 + pad, y1 + pad))

    buf = BytesIO()
    omr.save(buf, format="PNG", dpi=(300, 300))
    encoded = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/api/generate-omr-with-qr", methods=["POST"])
def generate_omr_with_qr():
    try:
        data = request.get_json()
        omr_path = data["omr_template_path"]
        form_type = data.get("form_type", "batch")
        test_id = data["test_id"]
        test_name = data["test_name"]
        subject = data["subject"]
        quantity = int(data["quantity"])
        results = []

        for i in range(1, quantity + 1):
            if form_type == "batch":
                batch_id = data["batch_id"]
                student_id = f"{batch_id}_STU_{i:03}"
                qr_data = {
                    "batch_id": batch_id,
                    "student_id": student_id,
                    "test_id": test_id,
                    "test_name": test_name,
                    "subject": subject,
                }
            else:
                student_id = f"STU_{i:03}"
                qr_data = {
                    "student_id": student_id,
                    "test_id": test_id,
                    "test_name": test_name,
                    "student_name": data.get("student_name", ""),
                    "subject": subject,
                }

            qr_img = generate_qr_image(qr_data)
            omr_base64 = embed_qr_on_omr(omr_path, qr_img)
            results.append({"label": student_id, "img": omr_base64})

        return jsonify({"success": True, "omr_sheets": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
