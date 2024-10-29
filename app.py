from flask import Flask, redirect, render_template, request, url_for, flash,session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users=[{"name":"ran","password":"123"}]
car1 = {"number":"111","problems":"gear","urgent":True,"image_url": "https://www.chevrolet.com/content/dam/chevrolet/na/us/english/index/cars/segment-page/01-images/2025-malibu-highlights-04.png?imwidth=960", "description": "Car1"}
car2 = {"number":"314","problems":"engine","urgent":False,"image_url": "https://chevrolet.com.ph/wp-content/uploads/2024/04/What-Makes-a-Car-a-%E2%80%98Sports-Car.png", "description": "Car2"}
car3 = {"number":"159","problems":"gear","urgent":True,"image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScOFHqTcy4k9bm1p7MgKJNRlmuaCpZDgSzTw&s", "description": "Car1"}
car4 = {"number":"265","problems":"engine","urgent":False,"image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTl1aiLA2CMgDQnx8P7fGLtenpSxzw--sGpLg&s", "description": "Car2"}

cars =[car1, car2, car3, car4]



@app.route("/")
def cars_list():
    if not session.get("logged_in"):
        flash("please login","danger")
        return redirect(url_for("login"))
    urgent = request.args.get('urgent', 'not_urgent')  # Default to 'not_urgent' if not provided
    problem = request.args.get('problems')
    num = request.args.get('number')
    filtered_cars = cars

    # Filter by urgency
    if urgent == 'true':
        filtered_cars = [car for car in filtered_cars if car.get('urgent')]

    if num:
        filtered_cars = [car for car in filtered_cars if (num in car.get('number')
                                                          if isinstance(car.get('number'), list)
                                                          else num == car.get('number'))]
    
    # Filter by problems if provided
    if problem:
        filtered_cars = [car for car in filtered_cars if (problem in car.get('problems')
                                                          if isinstance(car.get('problems'), list)
                                                          else problem == car.get('problems'))]

    return render_template("cars_list2.html", car_list=filtered_cars)

    #final_str=""
    #for car in cars:
     #   final_str += f"<p>{car["number"]}</p>"

   # return final_str

@app.route("/single_car/<int:index>")
def single_car(index):
    if index < 0 or index >= len(cars):
        return render_template("cars_list2.html", car_list=cars)
    return render_template("single_car2.html", car=cars[index], index=index)

@app.route("/add_car/", methods=["GET", "POST"])
def add_car():
    if not session.get("logged_in"):
        flash("please login","danger")
        return redirect(url_for("login"))
        
    if request.method == "POST":
        number = request.form.get("number")
        problems = request.form.get("problems")
        urgent = request.form.get("urgent") == 'on'
        image_url = request.form.get("image_url")

        new_car = {
            "number": number,
            "problems": problems.split(",") if problems else [],
            "image_url": image_url
        }

        cars.append(new_car)
        flash(f'Added Car {new_car.get("number")}', "success")
        return redirect(url_for("cars_list"))

    return render_template("add_car2.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")  
        for user in users:
            if user.get("name") == username and user.get("password") == password:
                flash("Login successful!", "success")
                session['logged_in'] = True
                session['username'] = username  # Store the username in session
                return redirect("/")     
        flash("Invalid username or password. Please try again.", "danger")
        return redirect(url_for("login"))
    return render_template("login2.html")
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)  # Remove username from session
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)