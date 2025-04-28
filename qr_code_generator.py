# qr_code_generator.py
import qrcode

# Таны вэб хаяг
url = "https://myproject-3u58.onrender.com/"  # Энд URL нь таны серверийн хаяг байх ёстой

# QR код үүсгэнэ
qr = qrcode.make(url)

# QR кодыг зураг файл болгон хадгална
qr.save("static/qrcode/dump_395_qr.png")
