import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("Food_Nutrition_Processed.csv")

df["iron"] = df["iron"].fillna(df["iron"].median())

df["vitamin_c"] = df["vitamin_c"].fillna(df["vitamin_c"].median())

recommendation_features = [
    "calories",
    "protein",
    "carbs",
    "fat",
    "iron",
    "vitamin_c"
]

features = df[recommendation_features]

scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)

similarity = cosine_similarity(scaled_features)

# BMI FUNCTIONS

def calculate_bmi(weight, height):
    height_in_meter = height / 100
    bmi = weight / (height_in_meter ** 2)
    return round(bmi, 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"
    
# ==========================
# CALORIE FUNCTIONS
# ==========================

def calculate_bmr(gender, weight, height, age):
    gender = gender.strip().lower()

    if gender == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    elif gender == "female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    else:
        raise ValueError("Gender must be 'male' or 'female'")

    return round(bmr, 2)


def calculate_daily_calories(bmr, activity_level):
    activity_level = activity_level.strip().lower()

    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9
    }

    if activity_level not in activity_factors:
        raise ValueError(
            "Activity must be sedentary, light, moderate, active, or very active"
        )

    daily_calories = bmr * activity_factors[activity_level]

    return round(daily_calories, 2)


def calorie_goal(daily_calories, goal):
    goal = goal.strip().lower()

    if goal == "weight loss":
        target = daily_calories - 500

    elif goal == "maintain":
        target = daily_calories

    elif goal == "weight gain":
        target = daily_calories + 500

    else:
        raise ValueError(
            "Goal must be weight loss, maintain, or weight gain"
        )

    return round(target)

# RECOMMENDATION FUNCTIONS

def search_food(food_name, top_n=10):

    food_name = food_name.strip().lower()

    matches = df[
        df["food_name"]
        .astype(str)
        .str.lower()
        .str.contains(food_name, na=False, regex=False)
    ]

    if matches.empty:
        return "No matching food found"

    return matches[
        [
            "food_name",
            "category",
            "calories",
            "protein",
            "carbs",
            "fat"
        ]
    ].head(top_n).reset_index(drop=True)

def recommend_food(food_name, top_n=5):

    food_name = food_name.strip().lower()

    food_names_lower = (
        df["food_name"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    matched_positions = np.where(
        food_names_lower == food_name
    )[0]

    if len(matched_positions) == 0:
        return "Food not found in dataset"

    food_position = matched_positions[0]

    similarity_scores = list(
        enumerate(similarity[food_position])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda item: item[1],
        reverse=True
    )

    recommendations = []

    for index, score in similarity_scores:

        # Same food ko recommendation me include nahi karna
        if index == food_position:
            continue

        recommendations.append({
            "Food": df.iloc[index]["food_name"],
            "Category": df.iloc[index]["category"],
            "Calories": df.iloc[index]["calories"],
            "Protein": df.iloc[index]["protein"],
            "Carbs": df.iloc[index]["carbs"],
            "Fat": df.iloc[index]["fat"],
            "Iron": df.iloc[index]["iron"],
            "Vitamin C": df.iloc[index]["vitamin_c"],
            "Similarity (%)": round(score * 100, 2)
        })

        if len(recommendations) == top_n:
            break

    return pd.DataFrame(recommendations)

def smart_recommend_food(food_name, top_n=5):

    food_name_clean = food_name.strip().lower()

    food_names_lower = (
        df["food_name"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    exact_match = df[food_names_lower == food_name_clean]

    if not exact_match.empty:
        return recommend_food(food_name, top_n)

    partial_matches = df[
        food_names_lower.str.contains(
            food_name_clean,
            na=False,
            regex=False
        )
    ]

    if partial_matches.empty:
        return "Food not found in dataset"

    print("Exact food name not found. Matching foods are:")

    return partial_matches[
        [
            "food_name",
            "category",
            "calories",
            "protein",
            "carbs",
            "fat"
        ]
    ].head(10).reset_index(drop=True)

def recommend_by_goal(goal, top_n=10):

    goal = goal.strip().lower()

    result = df.copy()

    if goal == "weight loss":

        result = result[
            (result["calories"] <= 150) &
            (result["fat"] <= 5)
        ]

        result = result.sort_values(
            by=["calories", "fat"],
            ascending=[True, True]
        )

    elif goal == "weight gain":

        result = result[
            (result["calories"] >= 250)
        ]

        result = result.sort_values(
            by=["calories", "protein"],
            ascending=[False, False]
        )

    elif goal == "high protein":

        result = result[
            result["protein"] >= 10
        ]

        result = result.sort_values(
            by="protein",
            ascending=False
        )

    elif goal == "low fat":

        result = result[
            result["fat"] <= 3
        ]

        result = result.sort_values(
            by="fat",
            ascending=True
        )

    else:
        return (
            "Invalid goal. Choose: weight loss, "
            "weight gain, high protein, or low fat"
        )

    columns = [
        "food_name",
        "category",
        "calories",
        "protein",
        "carbs",
        "fat",
        "iron",
        "vitamin_c"
    ]

    return result[columns].head(top_n).reset_index(drop=True)

def recommend_by_goal_and_category(goal, category=None, top_n=10):

    result = df.copy()

    if category is not None:

        result = result[
            result["category"]
            .astype(str)
            .str.lower()
            .str.contains(
                category.strip().lower(),
                na=False,
                regex=False
            )
        ]

    goal = goal.strip().lower()

    if goal == "weight loss":

        result = result[
            (result["calories"] <= 150) &
            (result["fat"] <= 5)
        ]

        result = result.sort_values(
            by=["calories", "fat"],
            ascending=True
        )

    elif goal == "weight gain":

        result = result[
            result["calories"] >= 250
        ]

        result = result.sort_values(
            by=["calories", "protein"],
            ascending=False
        )

    elif goal == "high protein":

        result = result[
            result["protein"] >= 10
        ]

        result = result.sort_values(
            by="protein",
            ascending=False
        )

    elif goal == "low fat":

        result = result[
            result["fat"] <= 3
        ]

        result = result.sort_values(
            by="fat",
            ascending=True
        )

    else:
        return "Invalid goal"

    columns = [
        "food_name",
        "category",
        "calories",
        "protein",
        "carbs",
        "fat"
    ]

    return result[columns].head(top_n).reset_index(drop=True)


# ==========================
# MEAL PLANNER FUNCTIONS
# ==========================

def divide_daily_calories(target_calories):

    meal_calories = {
        "Breakfast": round(target_calories * 0.25),
        "Lunch": round(target_calories * 0.35),
        "Dinner": round(target_calories * 0.30),
        "Snacks": round(target_calories * 0.10)
    }

    return meal_calories


def find_foods_for_meal(
    meal_name,
    meal_calories,
    top_n=5
):

    result = df.copy()

    # Sirf selected meal ke foods
    result = result[
        result["meal_type"]
        .astype(str)
        .str.lower()
        == meal_name.strip().lower()
    ]

    # Basic nutrition filtering
    result = result[
        (result["fat"] <= 20) &
        (result["protein"] >= 2)
    ]

    # Target calories se difference
    result["calorie_difference"] = abs(
        result["calories"] - meal_calories
    )

    # Closest calories first
    result = result.sort_values(
        by=[
            "calorie_difference",
            "protein",
            "fat"
        ],
        ascending=[
            True,
            False,
            True
        ]
    )

    columns = [
        "food_name",
        "category",
        "meal_type",
        "calories",
        "protein",
        "carbs",
        "fat",
        "calorie_difference"
    ]

    return (
        result[columns]
        .head(top_n)
        .reset_index(drop=True)
    )

def create_daily_meal_plan(
    target_calories,
    top_n=5
):

    meal_targets = divide_daily_calories(
        target_calories
    )

    meal_plan = {}

    for meal_name, calories in meal_targets.items():

        meal_plan[meal_name] = {
            "Target Calories": calories,

            "Recommended Foods": find_foods_for_meal(
                meal_name,
                calories,
                top_n
            )
        }

    return meal_plan
# ==========================
# MASTER FUNCTION
# ==========================

def generate_diet_plan(
    age,
    gender,
    height,
    weight,
    activity,
    goal,
    top_n=5
):

    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)

    bmr = calculate_bmr(
        gender,
        weight,
        height,
        age
    )

    daily_calories = calculate_daily_calories(
        bmr,
        activity
    )

    target_calories = calorie_goal(
        daily_calories,
        goal
    )

    meal_plan = create_daily_meal_plan(
        target_calories,
        top_n
    )

    return {
        "BMI": bmi,
        "BMI Category": category,
        "BMR": bmr,
        "Daily Calories": daily_calories,
        "Target Calories": target_calories,
        "Meal Plan": meal_plan
    }
