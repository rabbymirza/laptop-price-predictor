from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# templates ফোল্ডারের লোকেশন সেট করা
templates = Jinja2Templates(directory="templates")

# ১. হোম রুট (Browser-এ ওয়েবসাইট ওপেন করার জন্য)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "title": "Laptop Price Predictor",
            "message": "Welcome to Laptop Price Prediction System!"
        }
    )

# ২. প্রেডিকশন রুট (Form Submit করার পর ডাটা প্রসেস করার জন্য)
@app.post("/predict")
async def predict(value: float = Form(...)):
    # উদাহরণ হিসেবে আপনার ML Model Predict এর লজিক এখানে লিখবেন
    # যেমন: estimated_price = model.predict([[value]])
    estimated_price = value * 1000  # একটি ডামি ক্যালকুলেশন
    
    return {
        "status": "success", 
        "input_value": value, 
        "predicted_price": estimated_price
    }