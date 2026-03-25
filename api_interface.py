try:
    from flask import Flask, request, jsonify
except ImportError:
    print("Flask is not installed. Install it with 'pip install flask' to use API interface.")
    raise

from services.user_service import get_user_by_id
from services.demand_service import fetch_last_n_records, fetch_prev_day_demand, insert_demand, fetch_all_demand
from schemas.demand_schema import build_demand_doc
from ml.train import load_models
from ml.predict import build_features, predict
from datetime import datetime

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    req = request.get_json(force=True)
    user_id = req.get("user_id")
    if not isinstance(user_id, int):
        return jsonify({"error": "user_id must be integer"}), 400

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User {user_id} not found"}), 404

    records = fetch_last_n_records(user_id, n=14)
    if len(records) < 7:
        return jsonify({"error": "At least 7 historical daily records are required"}), 400

    all_data = fetch_all_demand()
    global_avg = sum(x.get("Total_Batter_Required_kg", 0) for x in all_data) / len(all_data) if all_data else 0.0
    features = build_features(user, records, global_avg_demand=global_avg)
    if features is None:
        return jsonify({"error": "Failed to build features"}), 500

    rf_model, xgb_model = load_models()
    rf_pred = rf_model.predict(features)[0]
    xgb_pred = xgb_model.predict(features)[0]
    avg_pred = (rf_pred + xgb_pred) / 2.0
    return jsonify({
        "user_id": user_id,
        "user_name": user.get("name"),
        "rf_pred": float(rf_pred),
        "xgb_pred": float(xgb_pred),
        "avg_pred": float(avg_pred),
    })


@app.route("/log", methods=["POST"])
def log_endpoint():
    req = request.get_json(force=True)
    user_id = req.get("user_id")
    if not isinstance(user_id, int):
        return jsonify({"error": "user_id must be integer"}), 400

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User {user_id} not found"}), 404

    date_str = req.get("date")
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "date format must be YYYY-MM-DD"}), 400
    else:
        date_obj = datetime.today()

    try:
        amount_sold = float(req.get("amount_sold_kg", 0.0))
        rainy = int(req.get("rainy", 0))
        holiday = int(req.get("holiday", 0))
        promo = int(req.get("promo", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid numeric values"}), 400

    constants = user.get("shop_constants", {})
    share = float(constants.get("restaurant_sales_share", 0.6))
    restaurant_sales = amount_sold * share
    retail_sales = amount_sold - restaurant_sales
    temp = float(req.get("temp", 30.0))

    prev_demand = fetch_prev_day_demand(user_id)
    record = build_demand_doc(user_id, date_obj, temp, rainy, holiday, promo,
                              restaurant_sales, retail_sales, prev_demand)
    insert_demand(record)

    return jsonify({"status": "ok", "inserted_for": user_id, "date": date_obj.strftime("%Y-%m-%d")})


if __name__ == "__main__":
    print("Starting API on http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
