import os
from flask import Flask, request, send_file, render_template_string
import requests
from fpdf import FPDF
from bs4 import BeautifulSoup

app = Flask(__name__)

TEMPLATE = '''
<!doctype html>
<title>NhentaiWorld Downloader</title>
<h2>NhentaiWorld PDF Downloader</h2>
<form method=post>
  <input type=text name=url placeholder="Dán link chương tại đây" style="width: 300px">
  <input type=submit value=Tải về>
</form>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        image_urls = extract_image_urls(url)
        if not image_urls:
            return "Không thể lấy ảnh từ chương truyện."
        pdf_path = create_pdf(image_urls)
        return send_file(pdf_path, as_attachment=True)
    return render_template_string(TEMPLATE)

def extract_image_urls(chapter_url):
    try:
        res = requests.get(chapter_url)
        soup = BeautifulSoup(res.text, "html.parser")
        imgs = soup.select("img[src]")
        urls = [img["src"] for img in imgs if "nhentai" in img["src"]]
        return urls
    except:
        return []

def create_pdf(img_urls):
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    for url in img_urls:
        img_data = requests.get(url).content
        with open("tmp.jpg", "wb") as f:
            f.write(img_data)
        pdf.add_page()
        pdf.image("tmp.jpg", 0, 0, 210, 297)
    output_path = "output.pdf"
    pdf.output(output_path)
    return output_path

if __name__ == "__main__":
    app.run(debug=True)