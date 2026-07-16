# Personalized Food Recommendation System

A Flask-based food and nutrition recommendation application that creates a personalized daily diet plan using the user's age, gender, height, weight, activity level, and fitness goal.

## Features

- Calculates Body Mass Index (BMI) and BMI category
- Calculates Basal Metabolic Rate (BMR)
- Estimates daily calorie requirements
- Adjusts target calories for weight loss, maintenance, or weight gain
- Divides calories across breakfast, lunch, dinner, and snacks
- Recommends foods using nutrition data
- Uses standardized nutrition features and cosine similarity for food recommendations
- Displays results through a responsive Flask web interface

## Technologies Used

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- HTML and CSS
- Jupyter Notebook

## Project Structure

```text
Food Recommendation System/
├── app.py
├── diet_utils.py
├── Food_Nutrition_Dataset.csv
├── Food_Nutrition_Processed.csv
├── food_calorie_model.lb
├── Recommendation_System.ipynb
├── requirements.txt
├── templates/
│   ├── index.html
│   └── result.html
└── static/
    └── css/
        └── style.css
```

## How the Application Works

1. The user enters personal details and selects an activity level and goal.
2. The application calculates BMI, BMR, daily calories, and target calories.
3. Target calories are divided among four meals.
4. Foods are filtered and ranked using calories and nutritional values.
5. A personalized meal plan is displayed on the result page.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd "Food Recommendation System"
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask application

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

## Input Details

The application accepts:

- Age
- Gender
- Height in centimeters
- Weight in kilograms
- Activity level
- Fitness goal

## Main Calculations

- **BMI:** Based on weight and height
- **BMR:** Calculated using the Mifflin-St Jeor equation
- **Daily calories:** BMR multiplied by an activity factor
- **Target calories:** Adjusted according to the selected goal

## Future Improvements

- Nutrition charts for calories, protein, carbohydrates, and fat
- Water intake recommendation
- Downloadable PDF diet plan
- User authentication and saved diet-plan history
- More advanced dietary preference and allergy filters

## Disclaimer

This project is created for educational purposes. The generated diet plan is a general recommendation and is not a substitute for advice from a qualified doctor or dietitian.

## Author

**Ajit Bairwa**  
B.Tech Computer Science student
