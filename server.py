# Session 1
from flask import Flask, jsonify, request

app = Flask(__name__) # Instance of Flask

@app.get("/")
def index():
    return jsonify("Welcome")

@app.get("/say-hi")
def hi():
    return jsonify("Hello CH 70")

@app.get("/students-coh-70")
def get_students():
    students_names = ["Lina", "Khaleel", "Jose", "Leo"]
    return jsonify(students_names)

@app.get("/contact")
def get_contact_information():
    contact_information = {
        "email": "lmiranda@sdgku.edu",
        "phone": "619-123-1234"
        }
    return jsonify(contact_information)

# MINI-CHALLENGE
# Create a /user-information endpoint
# Return a dictionary with: name, role, is_active, favorite_technologies
# Test it by visiting http://127.0.0.1:5000/user-information}
@app.get("/user-information")
def get_user_information():
    user_information = {
        "name": "Leo",
        "role": "Instructor",
        "is_active": True,
        "favorite_technologies": ["OpenGL", "uv"]
    }
    return jsonify(user_information)

# Session 2: Path parameter

# http://127.0.0.1:5000/greet/xxx
@app.get("/greet/<string:student_name>")
def greet(student_name):
    return jsonify({"message": f"Hi, {student_name}"}), 200 # OK

products = [
    {
        "_id": 1,
        "name": "cake",
        "price": 25
    },
    {
        "_id": 2,
        "name": "ice-cream",
        "price": 5
    },
    {
        "_id": 3,
        "name": "cookie",
        "price": 3
    },
    {
        "_id": 4,
        "name": "chocolate",
        "price": 10
    },
]

# MINI CHALLENGE
# GET /api/products -> return a list of products + count (bonus)
@app.get("/api/products")
def get_products():
    return jsonify(products), 200 # OK

@app.get("/api/products/count")
def get_products_count():
    return jsonify(len(products))

# GET /api/products/2 -> returns a product by id
@app.get("/api/products/<int:product_id>")
def get_product_by_id(product_id):
    for product in products:
        print(product)
        if product["_id"] == product_id:
            return jsonify(product), 200
    return jsonify("Product not found"), 404  # Not Found

# Assignment 1: Coupons

coupons = [
    {"_id": 1, "code": "WELCOME10", "discount": 10},
    {"_id": 2, "code": "SPOOKY25", "discount": 25},
    {"_id": 3, "code": "VIP50", "discount": 50}
]

@app.get("/api/coupons")
def get_coupons():
    return jsonify(coupons)


@app.get("/api/coupons/count")
def get_coupon_count():
    return jsonify(len(coupons))


# Assignment 2: Get a Coupon by ID

@app.get("/api/coupons/<int:coupon_id>")
def get_coupon_by_id(coupon_id):
    for coupon in coupons:
        if coupon["_id"] == coupon_id:
            return jsonify(coupon), 200

    return jsonify("Coupon not found"), 404


# Session 3: More endpoints

# POST /api/products -> create a product
@app.post("/api/products")
def create_product():
    new_product = request.get_json()
    print(new_product)

    new_product["_id"] = products[-1]["_id"]+1
    products.append(new_product)

    return jsonify({
        "message": "Product created successfully"
    }), 201

# PUT

@app.put("/api/products/<int:product_id>")
def update_product_by_id(product_id):
    updated_product = request.get_json()
    print(updated_product)

    for product in products:
        if product["_id"] == product_id:
            product["name"] = updated_product["name"]
            product["price"] = updated_product["price"]

            return jsonify({
                "message": "Product updated successfully"
            }), 200

    return jsonify({
        "message": "Product not found"
    }), 404

# DELETE

@app.delete("/api/products/<int:product_id>")
def delete_product_by_id(product_id):
    for product in products:
        if product["_id"] == product_id:
            products.remove(product)
            return jsonify({
                "message": "Product deleted successfully"
            }), 200

    return jsonify({
        "message": "Product not found"
    }), 404


# Final Assignment: Coupon CRUD

@app.post("/api/coupons")
def create_coupon():
    if not request.is_json:
        return jsonify({
            "message": "Content-Type must be application/json"
        }), 415

    new_coupon = request.get_json(silent=True)

    if (not isinstance(new_coupon, dict)
            or not isinstance(new_coupon.get("code"), str)
            or not new_coupon["code"].strip()
            or not isinstance(new_coupon.get("discount"), (int, float))):
        return jsonify({
            "message": "Coupon must include a code and discount"
        }), 400

    new_coupon["_id"] = max(coupon["_id"] for coupon in coupons) + 1
    coupons.append(new_coupon)

    return jsonify(new_coupon), 201


@app.put("/api/coupons/<int:coupon_id>")
def update_coupon_by_id(coupon_id):
    if not request.is_json:
        return jsonify({
            "message": "Content-Type must be application/json"
        }), 415

    updated_coupon = request.get_json(silent=True)

    if (not isinstance(updated_coupon, dict)
            or not isinstance(updated_coupon.get("code"), str)
            or not updated_coupon["code"].strip()
            or not isinstance(updated_coupon.get("discount"), (int, float))):
        return jsonify({
            "message": "Coupon must include a code and discount"
        }), 400

    for coupon in coupons:
        if coupon["_id"] == coupon_id:
            coupon["code"] = updated_coupon["code"]
            coupon["discount"] = updated_coupon["discount"]

            return jsonify(coupon), 200

    return jsonify({
        "message": "Coupon not found"
    }), 404


@app.delete("/api/coupons/<int:coupon_id>")
def delete_coupon_by_id(coupon_id):
    for coupon in coupons:
        if coupon["_id"] == coupon_id:
            coupons.remove(coupon)

            return jsonify({
                "message": "Coupon deleted successfully"
            }), 200

    return jsonify({
        "message": "Coupon not found"
    }), 404

app.run(debug=True)
