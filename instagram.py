from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# إعدادات Google API
GOOGLE_API_KEY = "ضع_مفتاح_Google_API_هنا"
SEARCH_ENGINE_ID = "ضع_معرف_محرك_البحث_هنا"

def check_instagram_user(username):
    """يتحقق مما إذا كان اسم المستخدم مستخدمًا في إنستقرام عبر البحث في Google"""
    query = f"site:instagram.com {username}"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"

    response = requests.get(url)
    data = response.json()

    if "items" in data:
        return False  # اليوزر مستخدم
    else:
        return True  # اليوزر متاح

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>فحص أسماء المستخدمين</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
            textarea { width: 80%; height: 200px; margin-bottom: 10px; }
            button { padding: 10px 20px; margin: 5px; cursor: pointer; }
            #result { margin-top: 20px; font-weight: bold; }
        </style>
    </head>
    <body>

        <h2>تحقق من توفر أسماء المستخدمين في إنستقرام</h2>
        <textarea id="usernames" placeholder="أدخل الأسماء، كل اسم في سطر جديد..."></textarea><br>
        
        <button onclick="checkUsernames()">🔍 ابحث أنا</button>
        <button onclick="customSearch()">🔎 ابحث بنفسك</button> 
        
        <div id="result"></div>

        <script>
            function checkUsernames() {
                let usernames = document.getElementById("usernames").value;
                fetch("/check", {
                    method: "POST",
                    body: new URLSearchParams({ "usernames": usernames }),
                    headers: { "Content-Type": "application/x-www-form-urlencoded" }
                })
                .then(response => response.json())
                .then(data => {
                    let resultDiv = document.getElementById("result");
                    if (data.available.length > 0) {
                        resultDiv.innerHTML = "<h3>الأسماء المتاحة:</h3><p>" + data.available.join("<br>") + "</p>";
                    } else {
                        resultDiv.innerHTML = "<h3>لم يتم العثور على أسماء متاحة.</h3>";
                    }
                });
            }

            function customSearch() {
                alert("ميزة البحث بنفسك ستتم إضافتها لاحقًا!");
            }
        </script>

    </body>
    </html>
    """)

@app.route('/check', methods=['POST'])
def check():
    usernames = request.form.get("usernames").split("\n")
    available_users = [user.strip() for user in usernames if check_instagram_user(user.strip())]

    return jsonify({"available": available_users})

if __name__ == '__main__':
    app.run(debug=True)
