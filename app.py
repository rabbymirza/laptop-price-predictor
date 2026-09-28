import os
import re
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# The final Colab pipeline is saved as pipe.joblib.
MODEL_PATH = os.path.join(MODEL_DIR, "pipe.joblib")
DATA_PATH = os.path.join(MODEL_DIR, "df.joblib")

pipe = None
processed_df = None

if os.path.exists(MODEL_PATH):
    pipe = joblib.load(MODEL_PATH)

if os.path.exists(DATA_PATH):
    processed_df = joblib.load(DATA_PATH)


def prepare_input(form):
    """Recreate the feature engineering used in the Colab notebook."""
    company = form["Company"].strip()
    typename = form["TypeName"].strip()
    inches = float(form["Inches"])
    screen = form["ScreenResolution"].strip()
    cpu = form["Cpu"].strip()
    ram = int(form["Ram"].replace("GB", "").strip())
    memory = form["Memory"].strip()
    gpu = form["Gpu"].strip()
    opsys = form["OpSys"].strip()
    weight = float(form["Weight"].replace("kg", "").strip())

    # ScreenResolution -> Touchscreen, IPS, x_res, y_res, ppi
    touchscreen = 1 if "Touchscreen" in screen else 0
    ips = 1 if "IPS " in screen else 0

    resolution_match = re.search(r"(\d+)\s*x\s*(\d+)", screen)
    if not resolution_match:
        raise ValueError("Screen resolution must contain a value such as 1920x1080.")

    x_res = int(resolution_match.group(1))
    y_res = int(resolution_match.group(2))
    ppi = (((x_res ** 2) + (y_res ** 2)) ** 0.5) / inches

    # CPU brand logic from the notebook.
    cpu_brand = " ".join(cpu.split()[0:3])
    if cpu_brand in ["Intel Core i5", "Intel Core i7", "Intel Core i3"]:
        cpu_brand = cpu_brand
    elif cpu_brand.split()[0] == "Intel":
        cpu_brand = "Other Intel Processor"
    else:
        cpu_brand = "AMD Processor"

    # Memory -> HDD and SSD, following the notebook's feature engineering.
    memory_clean = memory.replace("TB", "000GB").replace("GB", "")
    first_raw = memory_clean.split("+")[0].strip()
    second_raw = memory_clean.split("+")[1].strip() if "+" in memory_clean else "0"

    def storage_value(raw, kind):
        value = re.sub(r"\D", "", raw)
        return int(value or 0) if kind in raw else 0

    hdd = storage_value(first_raw, "HDD") + storage_value(second_raw, "HDD")
    ssd = storage_value(first_raw, "SSD") + storage_value(second_raw, "SSD")

    # GPU brand and OS grouping from the notebook.
    gpu_brand = gpu.split()[0]
    if gpu_brand == "ARM":
        raise ValueError("ARM GPU entries were removed from the training data.")

    if opsys in ["Windows 10", "Windows 7", "Windows 10 S"]:
        os_group = "Windows"
    elif opsys in ["macOS", "Mac OS X"]:
        os_group = "Mac"
    else:
        os_group = "Others/No OS/Linux"

    # Final X columns used by the notebook after feature engineering.
    return pd.DataFrame([{
        "Company": company,
        "TypeName": typename,
        "Ram": ram,
        "Weight": weight,
        "Touchscreen": touchscreen,
        "IPS": ips,
        "ppi": ppi,
        "HDD": hdd,
        "SSD": ssd,
        "Gpu brand": gpu_brand,
        "os": os_group,
    }])


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            if pipe is None:
                raise FileNotFoundError(
                    "model/pipe.joblib is missing. Download it from Colab and put it inside the model folder."
                )

            input_df = prepare_input(request.form)

            # The notebook trained on log(Price), so convert the prediction back
            # to the original Price scale with exp().
            log_prediction = float(pipe.predict(input_df)[0])
            prediction = float(np.exp(log_prediction))
        except Exception as exc:
            error = str(exc)

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        has_model=pipe is not None,
    )


if __name__ == "__main__":
    # Local development only. Render uses Gunicorn.
    app.run(host="127.0.0.1", port=5000, debug=True)
