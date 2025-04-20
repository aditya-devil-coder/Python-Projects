# Python-Projects
# Programming Projects Portfolio

This repository contains several Python projects demonstrating various concepts in programming, data analysis, and computational methods.

## Table of Contents
- [Project 1: Student Information System (SIS)]
- [Project 2: Expense Tracker with Data Analysis]
- [Project 3: Health & Fitness Tracker]
- [Project 4: Estimating π Using Monte Carlo Simulation]
- [Project 5: Numerical Integration Using Trapezoidal Rule]

---

## Student Information System – Documentation
##Purpose of the Program
The Student Information System is a Python program that helps manage students' academic records, including:

Personal and academic details

Courses and their respective marks

GPA calculation

Course-wise management

🔑 Main Features
Add Student – Capture student ID, name, age, grade level, and email.

Add Course – Add subjects with corresponding marks.

Remove Course – Delete a subject from a student’s record.

Calculate GPA – GPA calculation based on a 4.0 scale.

Interactive Menu – Options to update, delete, or view student data.

🧩 Code Breakdown
1. Student Class
Attributes:

student_id: Unique ID for each student

name, age, grade_level, email: Basic personal data

courses: Dictionary with course names and marks

Methods:

add_course(course, marks) – Add/Update a subject and its marks.

remove_course(course) – Remove a subject.

calculate_gpa() – Calculate GPA using a 4.0 scale.

__str__() – Return a summary of the student’s information.

2. CSV Handling
The system can save/load data using:

students.csv – Stores student and course info

Uses csv.DictWriter and csv.DictReader

3. Menu Execution
Main menu options allow:

Adding new student data

Viewing all student records

Updating/removing student info

Exiting the program

▶️ How to Run the Program
Just run the SIS.py Python file.


##Expense Tracker – Documentation
🎯 Purpose of the Program
This Python program is a command-line Expense Tracker that helps users:

Add and categorize daily expenses

Set monthly budgets per category

Generate weekly or monthly spending summaries

Visualize spending with charts

Export expense data to CSV

All data is saved in:

expenses.csv (expense records)

budgets.json (category budgets)

🔑 Main Features

Feature	Description
Add Expense	Record an expense (date, category, amount, description)
Set Budget	Assign a monthly budget for each category
Weekly/Monthly Summary	View spending by category within a time frame
Budget Alerts	Get notified when category budgets are exceeded
Visualizations	Pie chart, bar chart, and daily trend line
CSV Export	Export data to a file for external use
List Expenses	View recent expenses sorted by date

🧩 Code Breakdown
1. ExpenseTracker Class
Initialization:

Loads expenses.csv and converts Date to datetime.

Loads or initializes budgets in budgets.json.

Key Methods:

add_expense(date, category, amount, description)
Adds a new expense. Validates category and checks budget alerts.

set_budget(category, amount)
Saves a monthly budget for a category.

_check_budget_alert(category)
Alerts if total monthly spending exceeds the set budget.

get_summary(period='monthly')
Returns a breakdown of total and category-wise expenses, budget status included.

visualize_expenses(period='monthly')
Displays:

Pie chart of expenses by category

Bar chart comparing spending vs budget

Daily spending trend (line chart)

export_to_csv(filename='expense_export.csv')
Saves current expense data to a CSV file.

list_expenses(n)
Prints the most recent n expenses with all details.

2. run_example() Function
Runs the app with an interactive terminal menu:

markdown
Copy
Edit
1. Add Expense
2. Set Budget
3. List Recent Expenses
4. View Monthly Summary
5. View Weekly Summary
6. Visualize Monthly Expenses
7. Visualize Weekly Expenses
8. Export Expenses to CSV
0. Exit
▶️ How to Run the Program
Simply run the script in your terminal:

python ExpenseTracker.py


💡 Example Use Case

===== MAIN MENU =====
1. Add Expense
Enter date (YYYY-MM-DD) or press enter for today: 2025-04-21
Select category number: 1 (Food)
Enter amount: $15.75
Enter description: Breakfast at cafe
Expense added successfully!
You’ll also be notified if you exceed your set budget:


⚠️ ALERT: You've exceeded your Food budget!
Budget: $300.00, Spent: $312.50, Overage: $12.50
---



##  Health & Fitness Tracker – Documentation
🎯 Purpose of the Program
This Python program is a personal health monitoring system that helps users:

Log daily wellness data (steps, sleep, calories, water)

Track health goals over time

Generate weekly reports

View BMI and daily calorie needs

Visualize progress with charts and dashboards

Data is stored in:

health_data.json (daily metrics)

user_profile.json (user details and goals)

🔑 Main Features

Feature	Description
Add Daily Health Data	Log steps, sleep, calories, and water intake
Set & Update Goals	Customize health goals (e.g. 10,000 steps/day)
Weekly Report	Summary of progress with insights
BMI & Calorie Calculator	Calculates BMI and daily calorie needs
Trend Charts	Visualize steps, sleep, calories, water over a week
Dashboard View	All metrics in one view
Goal Comparison Chart	Visual comparison of average progress vs. goals
🧩 Code Breakdown
1. HealthFitnessTracker Class
Data Management

load_data() / save_data() – Handles health_data.json

load_user_profile() / save_user_profile() – Manages profile info

User Profile

update_user_profile(...) – Change name, age, gender, height, weight, and goals

calculate_bmi() / get_bmi_category(bmi) – Computes BMI and its category

calculate_calories_needed() – Uses BMR formula and assumes moderate activity

Health Data

add_health_data(date, steps, sleep, calories, water) – Add or update a day’s record

get_weekly_data(end_date=None) – Extracts the past 7 days for analysis

Reporting

generate_weekly_report() – Text-based insights on steps, sleep, etc.

Tracks % of goal completion and provides feedback

Visualization

plot_weekly_trend(metric) – Bar chart with optional goal line

plot_weekly_comparison() – Bar chart comparing all goals (in %)

plot_health_dashboard() – 2x2 subplot dashboard for all metrics

2. Interactive CLI (run_cli())
Offers a user-friendly menu with options:

1. Add Today's Data
2. Add Data for Specific Date
3. View/Update Profile
4. Generate Weekly Report
5. View Metric Trend
6. View Goals Comparison
7. Show Health Dashboard
8. Exit
▶️ How to Run the Program

python "heath fitness tracker.py"


💡 Example Use Case
yaml
Copy
Edit
===== Add Today's Health Data =====
Date: 2025-04-21
Steps (goal: 10000): 8750
Sleep hours (goal: 8): 7.5
Calories consumed (goal: 2000): 1950
Water glasses (goal: 8): 6.5
Data for 2025-04-21 saved successfully!
Generate a full report:


===== Weekly Health Report =====
BMI: 24.5 (Normal weight)
Estimated Daily Calorie Needs: 2100

Steps: 8900 / 10000 (89.0%)
Sleep: 7.2 / 8.0 (90.0%)
Calories: 1950 / 2000 (97.5%)
Water: 6.8 / 8.0 (85.0%)

Insights:
- Consider walking more to reach your step goals
- Try to improve your sleep duration for better health
---

## Project 4: Estimating π Using Monte Carlo Simulation – Documentation
🎯 Purpose of the Program
This Python script uses the Monte Carlo method to estimate the value of π (pi). It randomly generates points in a square and counts how many fall inside the inscribed circle, leveraging the ratio of areas to estimate π.

The program also visualizes the simulation and analyzes convergence behavior as the number of sample points increases.

🔑 Main Features

Feature	Description
Run Single Simulation	Estimates π using user-defined number of points
Visualize Simulation	Shows how points fall inside/outside the unit circle
Analyze Convergence	Runs multiple simulations with increasing sample sizes (10¹ to 10⁵+)
Error Analysis	Displays accuracy vs. actual value of π
Interactive Menu	CLI-based operation with step-by-step choices
🧩 Code Breakdown
1. estimate_pi(n)
Generates n random (x, y) coordinates in [-1, 1] x [-1, 1]

Checks if each point falls within the unit circle

Returns the estimated value of π and all point data

2. plot_simulation(...)
Displays:

Unit circle and square boundary

Green dots (inside circle)

Red dots (outside circle)

Shows estimated π value in the plot title

3. analyze_convergence()
Asks user for max power of 10 (e.g. 5 = 10⁵)

Runs simulations with sizes 10¹ to 10⁵+

Records error and runtime

Plots:

π estimates vs sample sizes (log scale)

Estimation error vs sample size (log-log)

4. main()
Presents a user menu:

1. Run a single simulation with N points
2. Analyze convergence with different sample sizes
3. Exit
▶️ How to Run the Program

python Monte_Carlo_Simulation.py

💡 Example Use Case

Choose an option:
1. Run a single simulation with N points
Enter the number of points to use (e.g., 1000): 5000

Estimated π: 3.144400
Actual π value: 3.141593
Absolute error: 0.002807

Do you want to see the visualization? (y/n): y
[shows circle and points plot]
Or analyze convergence:


Enter the maximum power of 10 for analysis (e.g., 5): 4
N = 10, π estimate = 3.200000, Error = 0.058407, Time: 0.0003 sec
...
[graph of π estimates and errors shown]
---

## Project 5: Numerical Integration Using Trapezoidal Rule– Numerical Integration
🎯 Purpose of the Program
This Python program uses the Trapezoidal Rule to numerically estimate the definite integral of a mathematical function over a given interval 
[
𝑎
,
𝑏
]
[a,b].

Users input the function, bounds, and number of subintervals. The script then calculates the approximate area under the curve and visualizes the trapezoids used in the calculation.

🔑 Main Features

Feature	Description
Input Any Function	Accepts symbolic math like x**2, sin(x), exp(-x**2)
Trapezoidal Rule Calculation	Approximates the definite integral of a function
Visual Representation	Plots trapezoids between each subinterval
Adaptive Comparison	Allows users to compare approximation with different values of n
Error Handling	Validates math input and numeric boundaries
🧩 Code Breakdown
1. get_function_from_user()
Accepts user input (e.g., x**2 + 2*x)

Converts to a symbolic expression using SymPy

Uses lambdify() to create a NumPy-compatible function

2. trapezoidal_rule(f, a, b, n)
Implements the formula:

Integral
≈
ℎ
[
𝑓
(
𝑎
)
+
𝑓
(
𝑏
)
2
+
∑
𝑖
=
1
𝑛
−
1
𝑓
(
𝑥
𝑖
)
]
Integral≈h[ 
2
f(a)+f(b)
​
 + 
i=1
∑
n−1
​
 f(x 
i
​
 )]
Returns the result and x, y points used

3. plot_trapezoidal(...)
Plots the function

Fills trapezoids under the curve for visual clarity

Adds title, labels, and grid

4. main()
Provides the interactive CLI:

Function input

Bounds input

Subinterval count (n)

Displays the result and graph

Optionally compares results with different n values

▶️ How to Run the Program

python Trapezoidal_Rule.py
The program runs in the terminal and uses matplotlib for plotting.

💡 Example Use Case

=== Numerical Integration using Trapezoidal Rule ===

Enter the function to integrate: x**2 + 2*x
Enter the lower bound of integration (a): 0
Enter the upper bound of integration (b): 3
Enter the number of subintervals (n): 6

Approximation using 6 trapezoids: 27.000000
[graph is shown]
Then:


Would you like to compare results with different numbers of subintervals? (y/n): y

Error vs number of subintervals:
n = 3: approximation = 27.750000
n = 6: approximation = 27.000000
n = 12: approximation = 26.812500
n = 24: approximation = 26.765625


