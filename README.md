# blogandposts 🌐

### Project description:
This is a simplified Instagram or Facebook type site written in Django 5.1. 
- Social authentication (Google and VK) was implemented in the project. As well as authentication via the site itself (Django auth) 🔑
- A Bootstrap and css was used for styling. 🎨
- Sending email messages for password recovery (Gmail SMTP) 📧
- CRUD operations with comments and posts 📝
- Implemented tags and a simple system for recommending posts by tags 🏷️
- Pagination using the new template tag {% querystring %} from Django 5.1 📄
- Profiles with general information and the ability to change profile photos are implemented 👤

[This is a link to the website of this project (if the trial period of hosting has ended, then the site may not work 😅)](https://blogandposts.pythonanywhere.com/)

(I used PythonAnywhere hosting to deploy the application) ☁️

_______________________________________________________________________________________
### To run the project, you need to:
1) Add 'localhost' to the allowed_hosts parameter in `settings.py`. 🛠️
2) Add a `.env` file with your own variables (add to the directory at the level of `manage.py`) 📂
3) Install all dependencies (requirements.txt is in blog/ directory): 
```bash
pip install -r requirements.txt 
```

_______________________________________________________________________________________
what does .env look like:
(without spaces and buckets)
```plaintext
SECRET_KEY=...
DATABASE_NAME=...
DATABASE_USER=...
DATABASE_PASSWORD=...
DATABASE_HOST=...
DATABASE_PORT=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
VK_APP_ID=...
VK_API_SECRET=...
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=...
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=...
```
