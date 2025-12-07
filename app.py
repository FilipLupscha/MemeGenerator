from flask import Flask, request, render_template, send_file, flash
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_meme_text(img, top_text, bottom_text):
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Privzeta pisava (fallback na sistemsko)
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()

    # Zgornji tekst (centriran)
    top_bbox = draw.textbbox((0, 0), top_text, font=font)
    top_width = top_bbox[2] - top_bbox[0]
    draw.text(((width - top_width) / 2, 10), top_text, fill="white", font=font, stroke_width=3, stroke_fill="black")

    # Spodnji tekst (centriran)
    bottom_bbox = draw.textbbox((0, 0), bottom_text, font=font)
    bottom_width = bottom_bbox[2] - bottom_bbox[0]
    draw.text(((width - bottom_width) / 2, height - 80), bottom_text, fill="white", font=font, stroke_width=3,
              stroke_fill="black")

    return img


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Ni datoteke!')
            return render_template('index.html')

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            flash('Neveljavna datoteka!')
            return render_template('index.html')

        top_text = request.form.get('top_text', '').upper()
        bottom_text = request.form.get('bottom_text', '').upper()

        try:
            img = Image.open(file.stream)
            img = add_meme_text(img, top_text, bottom_text)

            img_io = io.BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)

            return send_file(img_io, mimetype='image/png', as_attachment=False, download_name='meme.png')
        except Exception:
            flash('Napaka pri obdelavi slike!')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
