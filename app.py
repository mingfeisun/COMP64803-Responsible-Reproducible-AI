from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        food_type = request.form['food_type']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        # **Call your recommendation algorithm here**
        # Pass date, time, food_type, latitude, longitude to your algorithm
        recommendations = get_restaurant_recommendations(date, time, food_type, latitude, longitude)

        return render_template('results.html', recommendations=recommendations) # Create results.html next

    return render_template('index.html')


def get_restaurant_recommendations(date, time, food_type, latitude, longitude):
    """
    This is a placeholder for your restaurant recommendation algorithm.
    Replace this with your actual algorithm logic.
    """
    # For now, just return some dummy data based on food type
    print(date, time, food_type, latitude, longitude)
    dummy_restaurants = []
    if food_type == "Italian":
        dummy_restaurants = [
            {'name': 'Luigi\'s Pizzeria', 'address': '123 Main St', 'latitude': float(latitude)+0.01, 'longitude': float(longitude)+0.01},
            {'name': 'Pasta Palace', 'address': '456 Oak Ave', 'latitude': float(latitude)-0.01, 'longitude': float(longitude)-0.01}
        ]
    elif food_type == "Mexican":
        dummy_restaurants = [
            {'name': 'Taco Town', 'address': '789 Pine Ln', 'latitude': float(latitude)+0.02, 'longitude': float(longitude)-0.02},
            {'name': 'Salsa Shack', 'address': '101 Elm Rd', 'latitude': float(latitude)-0.02, 'longitude': float(longitude)+0.02}
        ]
    # ... add more food type based dummy data or integrate your real algorithm ...

    return dummy_restaurants

if __name__ == '__main__':
    app.run(debug=True, port=8080)