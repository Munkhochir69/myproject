# qr_code_generator.py
import qrcode

# Таны вэб хаяг
url = "http://localhost:5000/"  # Энд URL нь таны серверийн хаяг байх ёстой

# QR код үүсгэнэ
qr = qrcode.make(url)

# QR кодыг зураг файл болгон хадгална
qr.save("static/qrcode/dump_395_qr.png")
