## 📁 Project Structure in FastAPI

```text
laptop-price-predictor/
│
├── api.py                  # FastAPI App (Prediction Backend)
├── app.py                  # Flask App (Frontend UI)
├── requirements.txt        # Dependencies list
├── Dockerfile              # Container configuration
├── .dockerignore           # Docker ignore file
├── .gitignore              # Git ignore file
│
├── model/                  # ML Models
│   ├── pipe.joblib
│   └── df.joblib
│
├── templates/              # HTML Templates
│   └── index.html
│
└── static/                 # CSS / JS Files
    └── style.css
# Laptop Price Predictor - Flask

This project converts the provided Colab laptop-price ML model into a Flask web app.

🚀 **Live Demo:** [Click Here to Visit Live Site]https://laptop-price-predictor-8wmb.onrender.com/


## Project structure

```text
laptop_price_flask/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── render.yaml
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── model/
    ├── pipe.joblib
    └── df.joblib
```

## Model files

Download these from Colab and copy them into `model/`:

- `pipe.joblib` - final trained StackingRegressor pipeline
- `df.joblib` - processed dataframe (optional for this Flask app)

The app's prediction flow recreates the feature engineering used in the notebook and sends the final feature set to `pipe.joblib`.

## Run locally on Windows

Open the project folder in VS Code, then Terminal > New Terminal:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## GitHub

```powershell
git init
git add .
git commit -m "Initial laptop price predictor Flask app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Create the GitHub repository first. Do not initialize the GitHub repository with another README if you are pushing this existing local project.

## Render

Create a Render Web Service from the GitHub repository.

Build Command:
```text
pip install -r requirements.txt
```

Start Command:
```text
gunicorn app:app
```

Choose Python 3 and your desired plan.

