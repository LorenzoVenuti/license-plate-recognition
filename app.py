import gradio as gr
from ultralytics import YOLO
import cv2

def LPdetection (img):
    # Load YOLO model 
    model = YOLO("models/LP.pt")
    results = model.predict(img, conf=0.25)
    result = results[0]  # Single image input

    return result


def process(image):
    
    
    result = LPdetection(image)
    

    img = result.orig_img.copy()  # BGR format
    boxes = result.boxes
    class_names = result.names

    # Fix typo: COLOR_BGR2RGB not RGR2RGB
    #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = float(box.conf[0].cpu().numpy())  # Fix: box.conf not box.xyxy
        cls_id = int(box.cls[0].cpu().numpy())
        label = class_names[cls_id]

        # Draw rectangle
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        # Fix typos: putText, img_rgb
        text = f"{label}"
        cv2.putText(img, text, (int(x1), int(y1) - 8), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 0, 0), 2)
    

    return img

def ocr(img):
    result = LPdetection(img)
    imagec = img.copy()
    for i, box in enumerate(result.boxes.xyxy.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box[:4])
        cropped = imagec[y1:y2,x1:x2]


    modelocr = YOLO("models/Ocr.pt")
    result = modelocr.predict(cropped)
    # step1 get result
    boxes = result[0].boxes
    class_ids = boxes.cls.cpu().numpy()
    xyxy = boxes.xyxy.cpu().numpy()

    # step2 combine coordinates with class IDs
    boxes_cls = list(zip(xyxy, class_ids))

    #step3 sort left to right then top to bottom 
    line_tolerance = 10
    boxes_cls.sort(key=lambda box: (round(box[0][1]/line_tolerance), box[0][0]))

    # step4 map class IDs to characters
    class_names = modelocr.names
    ordered_text = ''.join(class_names[cls_id] for _, cls_id in boxes_cls)

    return ordered_text

def checkingNumbers(image, video_input, expected_plate):
    if image is None:
        return None, "<div style='color:#991B1B;'>❌ No image uploaded.</div>"
    No = ocr(image)
    boundingimg = process(image)

    expected = expected_plate.strip().upper()
    if expected == "":
        status = f"<div style='color:#16a34a;'>✅ Detected Number is <b>{No}</b>.</div>"
    elif expected == No:
        status = f"<div style='color:#16a34a;'>✅ Exact Match! Detected: <b>{No}</b></div>"
    else:
        status = f"<div style='color:#eab308;'>⚠️ Mismatch! Detected: <b>{No}</b>, Expected: <b>{expected}</b></div>"


    return boundingimg, status


def dummy_process(image, video, expected_plate):
    # This is a placeholder for your real logic
    return image, "<div style='color:#16a34a;'>✅ Dummy result: backend not connected yet.</div>"

def do_reset():
    return None, "<div style='color:#6B7280;'>🧹 Results cleared.</div>", None, None, ""






# -------------------------
# Custom CSS for styling
# -------------------------
CUSTOM_CSS = """
/* Header */
.header {
  background: linear-gradient(90deg, #4f9dfb, #7b6bfa);
  color: white;
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 12px 30px rgba(16,24,40,0.06);
  margin-bottom: 18px;
}
.header h1 { margin: 0; font-size:34px; font-weight:800; letter-spacing: -0.5px; }
.header p { margin:6px 0 0 0; opacity:0.95; }

/* Main card */
.app-card {
  background: white;
  padding: 26px;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(16,24,40,0.04);
}

/* Upload area */
.upload-wrap .gr-image, .upload-wrap .gr-video, .upload-wrap .gr-file {
  min-height: 240px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(16,24,40,0.03);
  border: 1px dashed #E6E9EE;
  padding: 6px;
}

/* Buttons */
.process-btn .gr-button {
  width: 100%;
  padding: 16px 20px;
  font-size: 18px;
  border-radius: 12px;
}
.reset-btn .gr-button {
  width: 100%;
  padding: 12px 18px;
  font-size: 16px;
  border-radius: 12px;
}

/* Result card */
.result-card {
  background: #FFFFFF;
  border-radius:12px;
  padding:12px;
  border: 1px solid #F3F4F6;
}
"""

# -------------------------
# Placeholder functions
# -------------------------

# -------------------------
# UI Layout
# -------------------------
with gr.Blocks(css=CUSTOM_CSS) as demo:
    # Header section
    with gr.Column(elem_id="top-column"):
        gr.HTML(
            "<div class='header'>"
            "<h1>🚗 License Plate Detection</h1>"
            "<p>Upload an image or video file to detect license plates and check matches.</p>"
            "</div>"
        )

    # Main content layout
    with gr.Row():
        # Left: Inputs
        with gr.Column(scale=1):
            with gr.Group(elem_classes="app-card"):
                gr.Markdown("### Upload Media")

                with gr.Row(elem_classes="upload-wrap"):
                    image_input = gr.Image(
                        label="Upload Image", 
                        type="numpy", 
                        sources=["upload"], 
                        interactive=True
                    )

                    video_input = gr.File(
                        label="Upload Video File (mp4, mkv, mov, etc.)",
                        file_types=[".mp4", ".webm", ".mkv", ".mov", ".avi", ".mpeg", ".mpg"]
                    )

                gr.Markdown()
                expected_plate = gr.Textbox(
                    placeholder="e.g. ABC1234", 
                    label="Expected Plate (optional)", 
                    lines=1
                )

                with gr.Row():
                    process_btn = gr.Button("🔍 Process", variant="primary", elem_classes="process-btn")

                with gr.Row():
                    reset_btn = gr.Button("♻ Reset", variant="secondary", elem_classes="reset-btn")

        # Right: Outputs
        with gr.Column(scale=1):
            with gr.Group(elem_classes="app-card"):
                gr.Markdown("### Detection Result")
                output_image = gr.Image(label="Processed Image", interactive=False)
                status_html = gr.HTML(value="<div style='color:#6B7280;'>Results will appear here after processing.</div>")

    # Button logic
    process_btn.click(
        fn=checkingNumbers,
        inputs=[image_input, video_input, expected_plate],
        outputs=[output_image, status_html]
    )

    reset_btn.click(
        fn=do_reset,
        outputs=[output_image, status_html, image_input, video_input, expected_plate]
    )

# Launch
if __name__ == "__main__":
    demo.launch()
