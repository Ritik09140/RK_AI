import os

settings_path = r'r:\RK_AI\rk_ai_project\settings.py'
with open(settings_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add apps
if "'assistant'" not in content:
    content = content.replace(
        "'django.contrib.staticfiles',",
        "'django.contrib.staticfiles',\n    'rest_framework',\n    'assistant',\n    'csc_services',"
    )

# Add os import at top if not there
if 'import os' not in content:
    content = 'import os\n' + content

# Configure templates dirs
content = content.replace(
    "'DIRS': [],",
    "'DIRS': [os.path.join(BASE_DIR, 'templates')],",
)

# Add STATICFILES_DIRS and MEDIA
if 'STATICFILES_DIRS' not in content:
    content += "\nSTATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]\n"
    content += "MEDIA_URL = '/media/'\n"
    content += "MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n"

with open(settings_path, 'w', encoding='utf-8') as f:
    f.write(content)

# create directories
os.makedirs(r'r:\RK_AI\templates\assistant', exist_ok=True)
os.makedirs(r'r:\RK_AI\static\assistant\css', exist_ok=True)
os.makedirs(r'r:\RK_AI\static\assistant\js', exist_ok=True)

# move files
import shutil
try:
    if os.path.exists(r'r:\RK_AI\index.html'):
        shutil.move(r'r:\RK_AI\index.html', r'r:\RK_AI\templates\assistant\index.html')
    if os.path.exists(r'r:\RK_AI\style.css'):
        shutil.move(r'r:\RK_AI\style.css', r'r:\RK_AI\static\assistant\css\style.css')
    if os.path.exists(r'r:\RK_AI\main.js'):
        shutil.move(r'r:\RK_AI\main.js', r'r:\RK_AI\static\assistant\js\main.js')
except Exception as e:
    print(f"Error moving files: {e}")

# edit index.html for static tags
html_path = r'r:\RK_AI\templates\assistant\index.html'
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if '{% load static %}' not in html:
        html = '{% load static %}\n' + html
        html = html.replace('href="style.css"', 'href="{% static \'assistant/css/style.css\' %}"')
        html = html.replace('src="main.js"', 'src="{% static \'assistant/js/main.js\' %}"')
        
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Settings updated and files moved successfully.")
