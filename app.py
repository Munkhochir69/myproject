import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Google Sheets API тохиргоо
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Dump inspection sheet").worksheet("Өдөр.дутмын.үзлэг")

# Асуумжийн жагсаалт
all_questions = {
    'dump': [
        'ХАБ-ын иж бүрдэл', 'Кардан голны бүрэн байдал',
        'Хойд дугуй, урд дугуйнууд, бэхэлгээнүүд',
        'Захын дамжуулагч, подвескны гоожилт шалгах',
        'Тэвш, өргөх цилиндрийн пальц, суурь боолт',
        'Тормозны шугамуудыг шалгах', 'Хойд тэнхлэгний боолтуудыг шалгах',
        'Чулуу зайлуулагч, шаврын хаалтны бүрэн байдал',
        'Шланк, цилиндр, хомутны бэхэлгээ', 'Дулаан мэдрэгч хоолой зөв холбогдсон эсэх',
        'Цилиндрүүдийн кронштейн зөв эсэх',
        'Подвискнуудын даралтыг шалгах', 'Галын систем',
        'Аккумуляторын бэхэлгээ, клем, толгой', 'Коллектор, яндангийн бүрэн байдал',
        'Гидрийн шингэний түвшин', 'Радиаторын гуурс, хоолой',
        'Хөдөлгүүрийн тосны түвшин', 'Трансмиссын шингэний түвшин',
        'Радиаторын антифризийн түвшин', 'Гидрийн бак, шланкны бүрэн байдал',
        'Хөргөлтийн системийн бүрэн байдал', 'Сэнс, жанам, агааржуулагчийн ремен',
        'Рулийн цилиндр болон шланкны гоожилт', 'Хөдөлгүүрийн доод хэсгээр гоожиж байгаа эсэх',
        'Толь, шил арчигч, цонхнуудын бүрэн байдал', 'Суудлын бүс',
        'Трансмисс болон тормоз удаашруулагч хөшүүрэг',
        'Бүх хянах самбар, дуут дохио, ухрах дохио, гэрэл',
        'Суурин станц', 'Дугуйн элэгдэл'
    ],
    'excavator': [
        'ХАБ-ын иж бүрдэл', 'Шанаганы шүд, бэхэлгээ, цилиндрийн пальцнууд',
        'Хөдөлгүүрийн тос, шингэний түвшин', 'Радиаторын антифриз, хөргөлтийн систем',
        'Гидрийн шингэн, шланкны гоожилт', 'Гидромотор, редукторын бүрэн байдал',
        'Гусеницийн хөвч, зам, хөтлөгч', 'Кабины удирдлага, самбар, гэрэл'
    ],
    'dozer': ['ХАБ-ын иж бүрдэл', 'Dozer асуумж 2'],
    'grader': ['ХАБ-ын иж бүрдэл', 'Grader асуумж 2'],
    'loader': ['ХАБ-ын иж бүрдэл', 'Ковшны шанаганы ир', 'Гидрийн шингэн']
}

# Нүүр хуудас
@app.route("/")
def index():
    return render_template("index.html")

# Формын хуудас
@app.route("/form/<vehicle>")
def form(vehicle):
    questions = all_questions.get(vehicle, [])
    return render_template("form.html", vehicle=vehicle, questions=questions)

# Илгээх route
@app.route("/submit", methods=["POST"])
def submit():
    data = request.form
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        timestamp,
        data.get("vehicle"),
        data.get("park_number"),
        data.get("shift"),
        data.get("operator"),
        data.get("mechanic")
    ]

    # Асуултуудыг нэмэх
    questions = all_questions.get(data.get("vehicle"), [])
    for i in range(1, len(questions) + 1):
        row.append(data.get(f"q{i}", ""))

    # Sheet рүү бичих
    sheet.append_row(row)

    return redirect(url_for("index"))

# Server run
if __name__ == "__main__":
    app.run(debug=True)
