from flask import Flask, render_template, request
import requests

# Initialize Flask app
app = Flask(__name__)

# Spoonacular API Key and Base URL
API_KEY = '57fe33593b884371b5405a77f7915947'
BASE_URL = 'https://api.spoonacular.com/recipes'

# Route for Home Page
@app.route('/home', methods=['GET'])
def home():
    """Render the home page with an empty recipe list and search query."""

# Main Route for the App
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle search requests for recipes."""
    current_year = datetime.now().year  # Get the current year
    if request.method == 'POST':
        query = request.form.get('search_query', '').strip()  # Get the search query
        if query:
            recipes = search_recipes(query)  # Fetch recipes for the query
            return render_template('index.html', recipes=recipes, search_query=query, current_year=current_year)
        else:
            return render_template('index.html', recipes=[], search_query='', current_year=current_year)  # Empty search query
    else:
        return render_template('index.html', recipes=[], search_query='', current_year=current_year)  # Handle GET request

# Function to search for recipes from Spoonacular API
def search_recipes(query):
    """Search for recipes based on a search query."""
    if not query:
        return []

    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    try:
        response = requests.get(f"{BASE_URL}/complexSearch", params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        print("API Response:", data)  # Debug: Print the API response
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recipes: {e}")
        return []

# Route to view a specific recipe's details
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    """Display details of a specific recipe."""
    params = {'apiKey': API_KEY}

    try:
        response = requests.get(f"{BASE_URL}/{recipe_id}/information", params=params)
        response.raise_for_status()
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recipe details: {e}")
        return "Recipe not found", 404
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle form submission for registration
        username = request.form['username']
        password = request.form['password']
        print(f"Registering user: {username} with password: {password}")
    return render_template('register.html')  # Register page (HTML file located in 'templates/')

# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission for login
        username = request.form['username']
        password = request.form['password']
        print(f"Logging in user: {username} with password: {password}")
    return render_template('login.html')  # Login page (HTML file located in 'templates/')

# Cart Page Route
@app.route('/cart')
def cart():
    return render_template('cart.html')  # Cart page (HTML file located in 'templates/')

# Checkout Page Route
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')  # Checkout page (HTML file located in 'templates/')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
