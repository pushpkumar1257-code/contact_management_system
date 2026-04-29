from flask import Flask, render_template, request, redirect

app = Flask(__name__)

contacts = [
    {"id": 1, "name": "Pushp", "phone": "9999999999", "email": "pushp@gmail.com", "created": "today"},
    {"id": 2, "name": "Rahul", "phone": "8888888888", "email": "rahul@gmail.com", "created": "today"}
]
next_id = 1


# HOME + SEARCH
@app.route("/")
def home():
    q = request.args.get("q", "").lower()

    if q:
        filtered = [c for c in contacts if q in c["name"].lower() or q in c["phone"]]
    else:
        filtered = contacts

    return render_template("index.html", data=filtered)


# ADD
@app.route("/add", methods=["GET", "POST"])
def add():
    global next_id

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        contacts.append({
            "id": next_id,
            "name": name,
            "phone": phone,
            "email": email,
            "created": "now"
        })

        next_id += 1
        return redirect("/")

    return render_template("add.html")


# EDIT
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    for c in contacts:
        if c["id"] == id:

            if request.method == "POST":
                c["name"] = request.form["name"]
                c["phone"] = request.form["phone"]
                c["email"] = request.form["email"]
                return redirect("/")

            return render_template("edit.html", c=c)

    return redirect("/")


# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    global contacts
    contacts = [c for c in contacts if c["id"] != id]
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)