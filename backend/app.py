"""HostelEase - Flask REST API for the educational mini project."""
from datetime import datetime
import os

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:5173", "http://127.0.0.1:5173",
    "http://localhost:5174", "http://127.0.0.1:5174"
]}})

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/hostelease")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client["hostelease"]
users = db["users"]
ALLOWED_COLLECTIONS = {"rooms", "fees", "complaints", "visitors", "notices"}


def clean(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    doc.pop("password", None)
    return doc


def error(message, status=400):
    return jsonify(status="error", message=message), status


@app.get("/api/health")
def health():
    return jsonify(status="ok", project="HostelEase", message="Flask backend is running")


@app.get("/api/db-test")
def db_test():
    try:
        client.admin.command("ping")
        return jsonify(status="ok", database="hostelease", message="MongoDB connected successfully")
    except Exception:
        app.logger.exception("MongoDB connection check failed")
        return error("MongoDB is not reachable. Start MongoDB and check backend/.env MONGO_URI.", 503)


@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    required = ["name", "email", "phone", "studentId", "roomNumber", "password"]
    if any(not str(data.get(k, "")).strip() for k in required):
        return error("Please fill in all required fields.")
    if len(str(data["password"])) < 6:
        return error("Password must be at least 6 characters long.")
    email = str(data["email"]).strip().lower()
    try:
        if users.find_one({"email": email}):
            return error("This email is already registered. Please log in.", 409)
        users.insert_one({
            "name": str(data["name"]).strip(), "email": email,
            "phone": str(data["phone"]).strip(),
            "studentId": str(data["studentId"]).strip(),
            "roomNumber": str(data["roomNumber"]).strip(),
            "password": generate_password_hash(str(data["password"])),
            "role": "student", "createdAt": datetime.utcnow().isoformat()
        })
        return jsonify(status="ok", message="Registration successful. Please log in."), 201
    except Exception:
        app.logger.exception("Registration failed")
        return error("Could not register. Check that MongoDB is running.", 503)


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    if not email or not password:
        return error("Email and password are required.")
    try:
        user = users.find_one({"email": email})
        if not user:
            return error("Invalid email or password.", 401)
        stored = str(user.get("password", ""))
        try:
            valid = check_password_hash(stored, password)
        except (ValueError, TypeError):
            valid = False
        # Support records from older classroom demos, then upgrade to a hash.
        if not valid and stored == password:
            valid = True
            users.update_one({"_id": user["_id"]}, {"$set": {"password": generate_password_hash(password)}})
        if not valid:
            return error("Invalid email or password.", 401)
        return jsonify(status="ok", message="Login successful", user=clean(user))
    except Exception:
        app.logger.exception("Login failed")
        return error("Could not log in. Check that MongoDB is running.", 503)


@app.get("/api/students")
def students():
    """Return basic student fields for module dropdowns; never return passwords."""
    try:
        docs = users.find({}, {"name": 1, "email": 1, "studentId": 1, "roomNumber": 1}).sort("name", 1).limit(500)
        return jsonify(status="ok", items=[clean(x) for x in docs])
    except Exception:
        app.logger.exception("Student list failed")
        return error("Could not load students. Check MongoDB connection.", 503)


@app.get("/api/dashboard")
def dashboard():
    try:
        return jsonify(status="ok", stats={
            "students": users.count_documents({}),
            "totalRooms": db.rooms.count_documents({}),
            "availableRooms": db.rooms.count_documents({"status": "Available"}),
            "pendingFees": db.fees.count_documents({"status": {"$ne": "Paid"}}),
            "openComplaints": db.complaints.count_documents({"status": {"$ne": "Resolved"}}),
            "visitorsToday": db.visitors.count_documents({"date": datetime.now().strftime("%Y-%m-%d")})
        })
    except Exception:
        app.logger.exception("Dashboard stats failed")
        return error("Could not load dashboard data. Check MongoDB connection.", 503)


@app.route("/api/<collection>", methods=["GET", "POST"])
def collection_route(collection):
    if collection not in ALLOWED_COLLECTIONS:
        return error("Unknown module.", 404)
    col = db[collection]
    try:
        if request.method == "GET":
            query = {}
            email = request.args.get("email", "").strip().lower()
            if email and collection in {"fees", "complaints", "visitors"}:
                query["email"] = email
            docs = col.find(query).sort("_id", -1).limit(300)
            return jsonify(status="ok", items=[clean(x) for x in docs])

        data = request.get_json(silent=True) or {}
        data = {str(k): v for k, v in data.items() if k not in {"_id", "id", "password"}}
        if collection in {"fees", "complaints", "visitors"}:
            email = str(data.get("email", "")).strip().lower()
            if not email:
                return error("Student email is required for this record.")
            data["email"] = email
        if collection == "rooms":
            data["roomNumber"] = str(data.get("roomNumber", "")).strip()
            if not data["roomNumber"]:
                return error("Room number is required.")
            data.setdefault("capacity", 2)
            data.setdefault("status", "Available")
        elif collection == "fees":
            try:
                total = float(data.get("amount", data.get("totalFee", 0)))
                paid = float(data.get("paid", 0))
                if total <= 0 or paid < 0 or paid > total:
                    return error("Total fee must be positive and paid amount must be between 0 and total fee.")
            except (TypeError, ValueError):
                return error("Enter valid numbers for total fee and paid amount.")
            pending = round(total - paid, 2)
            data.update({"amount": total, "totalFee": total, "paid": paid, "pending": pending,
                         "status": "Paid" if pending == 0 else ("Partial" if paid > 0 else "Pending")})
        elif collection == "complaints":
            if not str(data.get("title", "")).strip():
                return error("Complaint title is required.")
            data.setdefault("status", "Open")
        elif collection == "visitors":
            if not str(data.get("visitorName", "")).strip():
                return error("Visitor name is required.")
            data.setdefault("status", "Inside")
            data.setdefault("date", datetime.now().strftime("%Y-%m-%d"))
        elif collection == "notices" and not str(data.get("title", "")).strip():
            return error("Notice title is required.")
        data["createdAt"] = datetime.utcnow().isoformat()
        col.insert_one(data)
        return jsonify(status="ok", message="Record added successfully."), 201
    except Exception:
        app.logger.exception("Collection operation failed: %s", collection)
        return error("Could not complete this operation. Check MongoDB connection.", 503)


@app.patch("/api/<collection>/<record_id>")
def update_record(collection, record_id):
    if collection not in ALLOWED_COLLECTIONS:
        return error("Unknown module.", 404)
    data = request.get_json(silent=True) or {}
    data.pop("_id", None)
    data.pop("id", None)
    data.pop("email", None)
    if not data:
        return error("No changes provided.")
    try:
        if collection == "fees" and ("paid" in data or "amount" in data or "totalFee" in data):
            current = db.fees.find_one({"_id": ObjectId(record_id)})
            if not current:
                return error("Record not found.", 404)
            total = float(data.get("amount", data.get("totalFee", current.get("totalFee", current.get("amount", 0)))))
            paid = float(data.get("paid", current.get("paid", 0)))
            if total <= 0 or paid < 0 or paid > total:
                return error("Invalid fee amounts.")
            data.update({"amount": total, "totalFee": total, "paid": paid, "pending": round(total-paid, 2),
                         "status": "Paid" if paid == total else ("Partial" if paid > 0 else "Pending")})
        result = db[collection].update_one({"_id": ObjectId(record_id)}, {"$set": data})
        if not result.matched_count:
            return error("Record not found.", 404)
        return jsonify(status="ok", message="Record updated successfully.")
    except Exception:
        return error("Invalid record ID or update data.")


@app.delete("/api/<collection>/<record_id>")
def delete_record(collection, record_id):
    if collection not in ALLOWED_COLLECTIONS:
        return error("Unknown module.", 404)
    try:
        result = db[collection].delete_one({"_id": ObjectId(record_id)})
        if not result.deleted_count:
            return error("Record not found.", 404)
        return jsonify(status="ok", message="Record deleted successfully.")
    except Exception:
        return error("Invalid record ID.")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
