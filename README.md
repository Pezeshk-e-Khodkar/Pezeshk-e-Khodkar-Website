![Pezeshk-e-Khodkar-logo](pages/static/site-icon.png)
# The Website of Pezeshk-e-Khodkar
**Pezeshk-e-Khodkar-Webaite** is a website that can detect diseases from images with AI models. Now, it 's available to detect skin cancer
(melanoma, basal cell carcinomas and squamous cell carcinoma)

## Installing and running Website
### 1. Clone repository
```
git clone https://github.com/Pezeshk-e-Khodkar/Pezeshk-e-Khodkar-Webaite.git
```

### 2. Configure VENV
You can use [virtual environments](https://docs.python.org/3/library/venv.html) to run project. (recommended)
### 3. Install requirements
```commandline
pip install -r requirements.txt
```
### 4. Create .env
Create a file called `.env` under root folder and configure it.
```
SECRET_KEY = 'Django secret key'
ADMIN_URL = 'Url of admin page on the website'
ALLOWED_HOSTS = 'http://yourdomain.com'
VIRUSTOTAL_API_KEY = 'API-key of VirusTotal'
SKINCANCER_AI_MODEL = 'name of Skin Cancer AI model'
RECAPTCHA_PUBLIC_KEY = 'Public Key of recaptch'
RECAPTCHA_PRIVATE_KEY = 'Private Key of recaptch'
RECAPTCHA_REQUIRED_SCORE = 0.85
EMAIL_HOST_USER = 'A Gmail that we use it to send emails.'
EMAIL_HOST_PASSWORD = 'Password App of your gmail'
```
Also, if you want to upload this website to a server (DEBUG=False), it uses mysql with config options below:
```
MYSQL_DB_NAME= 'Database name'
MYSQL_DB_USER= 'DataBase user'
MYSQL_DB_PASSWORD= 'user's password'
MYSQL_DB_HOST='Database host'
MYSQL_DB_PORT='Database port'
```
### 5. Add admin-honeypot app
Download [admin-honeypot](https://github.com/dmpayton/django-admin-honeypot/)
and copy `admin-honeypot` folder under root folder of project.

### 6. Create folders
Create two folders called `media` and  `models` under root folder.

### 7. Configure AI model
Put AI model file under `models` folder.

### 8. Migrations:
On linux, replace `python` to `python3`.
```commandline
python manage.py makemigrations
python manage.py migrate
```

### 9. Configure StaticFiles
```commandline
python manage.py collectstatic
```
### 10. Run it!
```commandline
python manage.py runserver
```
## Run Tests

### 1. Create Folders
Create two folders called `output_images` and `test_images` under `libs/tests/`.

### 2. Set Test images
Set images that you want test API with, under `libs/tests/test_images`.

### 3. Configure `dataset.csv`
Create a file called `dataset.csv` under `libs/tests/`
and write something like this in it.
```csv
FileName,AntiVirusTest,SkinCancerDetectorTest,ImageVerifierTest,FileSizeVerifierTest,ImageUploaderTest
1.jpg,0,1,1,1,1
2.jpg,0,0,0,1,0
3.png,0,0,0,0,0
4.jpg,0,1,1,1,1
5.jpg,0,1,1,1,1
```
`0` means that class should return False.\
`1` means that class should return True.

### 4. Run tests
```commandline
python manage.py test
```
## License
```
MIT License

Copyright (c) 2023 Pezeshk-e-Khodkar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```