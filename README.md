# cover_helper
Cover letter ai-generator telegram bot  
![Demo](https://github.com/justtomu/cover_helper/assets/54885261/3f08b946-b25d-48e9-9c89-bc77e5560acb)

## Installation
```
pip install pipenv
pipenv install
cp .env.template .env
```
1. Visit https://bard.google.com/
2. F12 for console
3. Session: Application → Cookies → Copy the value of  `__Secure-1PSID` cookie.
4. Modify `.env` file and insert bard cookie token here
## Usage
```
pipenv shell
python coverbot/main.py
```
