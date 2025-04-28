from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz  # Цагийн бүс тохируулахад хэрэгтэй

app = Flask(__name__)

# Google Sheets API тохиргоо
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Dump inspection sheet").worksheet("Өдөр.дутмын.үзлэг")

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        damp_number = request.form.get("damp_number")
        moto_hour = request.form.get("moto_hour")
        shift = request.form.get("shift")
        operator_name = request.form.get("operator_name")
        mechanic_name = request.form.get("mechanic_name")
        description = request.form.get("description")

        # 37 асуултын хариулт
        checks = []
        for i in range(1, 38):
            checks.append(request.form.get(f"check_{i}"))

        # Монголын цагийг тохируулъя
        mongolia_timezone = pytz.timezone('Asia/Ulaanbaatar')
        timestamp = datetime.now(mongolia_timezone).strftime("%Y-%m-%d %H:%M:%S")

        row = [timestamp, damp_number, moto_hour, shift, operator_name, mechanic_name] + checks + [description]

        try:
            sheet.append_row(row)
        except Exception as e:
            return f"Алдаа гарлаа: {str(e)}"

        # Амжилтын хуудас руу шилжүүлнэ
        return redirect(url_for('success'))

    return render_template("form.html")

# Амжилтын хуудас
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
