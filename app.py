from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets API тохиргоо
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Бичих sheet-ээ сонго
sheet = client.open("Dump inspection sheet").Өдөрдутмынүзлэг  # Чиний Google Sheet нэрийг тааруулна уу!

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        damp_number = request.form.get("damp_number")
        moto_hour = request.form.get("moto_hour")
        shift = request.form.get("shift")
        operator_name = request.form.get("operator_name")
        mechanic_name = request.form.get("mechanic_name")
        description = request.form.get("description")

        # 37 асуултын хариултыг авах
        checks = []
        for i in range(1, 38):
            checks.append(request.form.get(f"check_{i}"))

        # Огноо цаг
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sheet рүү бичих утгуудыг дараалуулах
        row = [timestamp, damp_number, moto_hour, shift, operator_name, mechanic_name] + checks + [description]

        # Sheet рүү мөр нэмэх
        sheet.append_row(row)

        return redirect("/")  # Амжилттай хадгалаад гол хуудас руу буцаана

    return render_template("form.html")  # Чиний HTML файлын нэрийг энд тааруулна

if __name__ == "__main__":
    app.run(debug=True)
