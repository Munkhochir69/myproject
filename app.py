from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets API тохиргоо
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Бичих sheet-ээ зөв сонго
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

        # Огноо цаг
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sheet рүү бичих утгууд
        row = [timestamp, damp_number, moto_hour, shift, operator_name, mechanic_name] + checks + [description]

        try:
            sheet.append_row(row)
        except Exception as e:
            return f"Алдаа гарлаа: {str(e)}"

        return redirect("/")  # Амжилттай хадгалаад буцана

    return render_template("form.html")  # Таны формын html файл

if __name__ == "__main__":
    app.run(debug=True)
