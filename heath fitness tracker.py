# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 13:16:15 2025

@author: Dell
"""

import os
import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class HealthFitnessTracker:
    def __init__(self):
        self.data_file = "health_data.json"
        self.user_file = "user_profile.json"
        self.load_data()
        self.load_user_profile()

    def load_data(self):
        """Load existing health data or create empty structure"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                # Convert to DataFrame
                if data:
                    records = []
                    for date, metrics in data.items():
                        metrics['date'] = date
                        records.append(metrics)
                    self.health_data = pd.DataFrame(records)
                    self.health_data.set_index('date', inplace=True)
                else:
                    self.health_data = pd.DataFrame(columns=['steps', 'sleep', 'calories', 'water'])
                    self.health_data.index.name = 'date'
        else:
            self.health_data = pd.DataFrame(columns=['steps', 'sleep', 'calories', 'water'])
            self.health_data.index.name = 'date'

    def load_user_profile(self):
        """Load user profile or create default profile"""
        if os.path.exists(self.user_file):
            with open(self.user_file, 'r') as f:
                self.user_profile = json.load(f)
        else:
            self.user_profile = {
                "name": "",
                "age": 30,
                "gender": "Not specified",
                "height": 170,  # cm
                "weight": 70,   # kg
                "goals": {
                    "steps": 10000,
                    "sleep": 8,  # hours
                    "calories": 2000,
                    "water": 8    # glasses
                }
            }

    def save_data(self):
        """Save health data to file"""
        # Convert DataFrame to dictionary for JSON storage
        data_dict = self.health_data.to_dict(orient='index')
        with open(self.data_file, 'w') as f:
            json.dump(data_dict, f)

    def save_user_profile(self):
        """Save user profile to file"""
        with open(self.user_file, 'w') as f:
            json.dump(self.user_profile, f)

    def calculate_bmi(self):
        """Calculate BMI based on user profile"""
        height_m = self.user_profile["height"] / 100
        weight_kg = self.user_profile["weight"]
        bmi = weight_kg / (height_m * height_m)
        return round(bmi, 2)

    def get_bmi_category(self, bmi):
        """Return BMI category based on BMI value"""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def calculate_calories_needed(self):
        """Calculate daily calorie needs based on user profile using BMR"""
        weight = self.user_profile["weight"]
        height = self.user_profile["height"]
        age = self.user_profile["age"]
        gender = self.user_profile["gender"]

        if gender.lower() == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:  # Female or not specified
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Assuming moderate activity level (multiply by 1.55)
        return round(bmr * 1.55)

    def add_health_data(self, date, steps, sleep, calories, water):
        """Add health data for a specific date"""
        # Create new row data
        new_data = pd.DataFrame({
            'steps': [steps],
            'sleep': [sleep],
            'calories': [calories],
            'water': [water]
        }, index=[date])
        
        # Update or add row
        self.health_data = pd.concat([self.health_data.drop(index=date, errors='ignore'), new_data])
        self.save_data()
        print(f"Data for {date} saved successfully!")

    def get_weekly_data(self, end_date=None):
        """Get data for the last 7 days"""
        if end_date is None:
            end_date = datetime.date.today()
        elif isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            
        start_date = end_date - datetime.timedelta(days=6)
        
        # Create date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        date_strings = [date.strftime("%Y-%m-%d") for date in date_range]
        
        # Filter data for these dates
        weekly_data = pd.DataFrame(index=date_strings, columns=['steps', 'sleep', 'calories', 'water'])
        
        # Fill with available data
        for date in date_strings:
            if date in self.health_data.index:
                weekly_data.loc[date, :] = self.health_data.loc[date, :]
        
        # Fill NaN with 0
        weekly_data.fillna(0, inplace=True)
        
        return weekly_data

    def generate_weekly_report(self, end_date=None):
        """Generate weekly health report"""
        weekly_df = self.get_weekly_data(end_date)
        
        bmi = self.calculate_bmi()
        bmi_category = self.get_bmi_category(bmi)
        calorie_needs = self.calculate_calories_needed()
        
        report = f"Weekly Health Report\n"
        report += f"Week: {weekly_df.index[0]} to {weekly_df.index[-1]}\n\n"
        
        report += f"BMI: {bmi} ({bmi_category})\n"
        report += f"Estimated Daily Calorie Needs: {calorie_needs} calories\n\n"
        
        # Weekly averages
        avg_steps = weekly_df['steps'].mean()
        avg_sleep = weekly_df['sleep'].mean()
        avg_calories = weekly_df['calories'].mean()
        avg_water = weekly_df['water'].mean()
        
        report += f"Weekly Averages:\n"
        report += f"Steps: {avg_steps:.0f} / {self.user_profile['goals']['steps']} ({(avg_steps/self.user_profile['goals']['steps']*100):.1f}%)\n"
        report += f"Sleep: {avg_sleep:.1f} / {self.user_profile['goals']['sleep']} hours ({(avg_sleep/self.user_profile['goals']['sleep']*100):.1f}%)\n"
        report += f"Calories: {avg_calories:.0f} / {self.user_profile['goals']['calories']} ({(avg_calories/self.user_profile['goals']['calories']*100):.1f}%)\n"
        report += f"Water: {avg_water:.1f} / {self.user_profile['goals']['water']} glasses ({(avg_water/self.user_profile['goals']['water']*100):.1f}%)\n\n"
        
        # Insights
        report += "Weekly Insights:\n"
        if avg_steps < self.user_profile['goals']['steps'] * 0.8:
            report += "- Consider walking more to reach your step goals\n"
        else:
            report += "- Great job reaching your step goals!\n"
            
        if avg_sleep < self.user_profile['goals']['sleep'] * 0.9:
            report += "- Try to improve your sleep duration for better health\n"
        else:
            report += "- You're getting adequate sleep, well done!\n"
            
        if avg_water < self.user_profile['goals']['water'] * 0.8:
            report += "- Drink more water throughout the day\n"
        else:
            report += "- Good water intake habits!\n"
            
        return report

    def update_user_profile(self, name=None, age=None, gender=None, height=None, weight=None, 
                          steps_goal=None, sleep_goal=None, calories_goal=None, water_goal=None):
        """Update user profile with provided values"""
        if name is not None:
            self.user_profile["name"] = name
        if age is not None:
            self.user_profile["age"] = age
        if gender is not None:
            self.user_profile["gender"] = gender
        if height is not None:
            self.user_profile["height"] = height
        if weight is not None:
            self.user_profile["weight"] = weight
        
        if steps_goal is not None:
            self.user_profile["goals"]["steps"] = steps_goal
        if sleep_goal is not None:
            self.user_profile["goals"]["sleep"] = sleep_goal
        if calories_goal is not None:
            self.user_profile["goals"]["calories"] = calories_goal
        if water_goal is not None:
            self.user_profile["goals"]["water"] = water_goal
        
        self.save_user_profile()
        print("User profile updated successfully!")

    def plot_weekly_trend(self, metric='steps', end_date=None, show_goal=True):
        """Plot weekly trend for specified metric"""
        weekly_df = self.get_weekly_data(end_date)
        
        plt.figure(figsize=(10, 6))
        
        # Plot data with improved style
        ax = weekly_df[metric].plot(kind='bar', color='skyblue', alpha=0.7)
        
        # Add goal line if requested
        if show_goal:
            goal = self.user_profile["goals"][metric]
            plt.axhline(y=goal, color='red', linestyle='--', label=f'Goal: {goal}')
        
        # Format x-axis dates to be more readable
        dates = [date.split('-')[1:] for date in weekly_df.index]
        dates = [f"{month}/{day}" for month, day in dates]
        plt.xticks(range(len(dates)), dates, rotation=45)
        
        # Labels and title
        metric_labels = {
            "steps": "Steps", 
            "sleep": "Sleep (hours)", 
            "calories": "Calories", 
            "water": "Water (glasses)"
        }
        plt.xlabel('Date')
        plt.ylabel(metric_labels.get(metric, metric.capitalize()))
        plt.title(f'Weekly {metric_labels.get(metric, metric.capitalize())} Trend')
        
        plt.tight_layout()
        plt.legend()
        plt.show()

    def plot_weekly_comparison(self, end_date=None):
        """Plot comparison of all metrics against goals for the week"""
        weekly_df = self.get_weekly_data(end_date)
        
        # Calculate average values
        avg_values = weekly_df.mean()
        
        # Get goals
        goals = pd.Series({
            'steps': self.user_profile['goals']['steps'],
            'sleep': self.user_profile['goals']['sleep'],
            'calories': self.user_profile['goals']['calories'],
            'water': self.user_profile['goals']['water']
        })
        
        # Calculate percentages
        percentages = (avg_values / goals * 100).clip(upper=100)
        
        # Plot
        plt.figure(figsize=(10, 6))
        
        metric_names = ['Steps', 'Sleep', 'Calories', 'Water']
        x = np.arange(len(metric_names))
        width = 0.35
        
        plt.bar(x, percentages, width, color=['skyblue', 'lightgreen', 'coral', 'plum'])
        
        # Add percentage text on bars
        for i, v in enumerate(percentages):
            plt.text(i, v + 2, f"{v:.1f}%", ha='center')
        
        plt.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Goal (100%)')
        
        plt.xlabel('Metrics')
        plt.ylabel('Goal Achievement (%)')
        plt.title('Weekly Goals Completion')
        plt.xticks(x, metric_names)
        plt.ylim(0, 120)  # Leave room for text
        plt.legend()
        
        plt.tight_layout()
        plt.show()

    def plot_health_dashboard(self, end_date=None):
        """Create a comprehensive dashboard with all health metrics"""
        weekly_df = self.get_weekly_data(end_date)
        
        # Create a 2x2 subplot figure
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        
        # Flatten for easier indexing
        axs = axs.flatten()
        
        metrics = ['steps', 'sleep', 'calories', 'water']
        colors = ['royalblue', 'forestgreen', 'darkorange', 'darkviolet']
        titles = ['Daily Steps', 'Sleep Duration (hours)', 'Calorie Intake', 'Water Consumption (glasses)']
        
        for i, (metric, color, title) in enumerate(zip(metrics, colors, titles)):
            # Plot data
            axs[i].bar(weekly_df.index, weekly_df[metric], color=color, alpha=0.7)
            
            # Add goal line
            goal = self.user_profile['goals'][metric]
            axs[i].axhline(y=goal, color='red', linestyle='--', label=f'Goal: {goal}')
            
            # Format x-axis dates
            dates = [date.split('-')[2] for date in weekly_df.index]  # Just the day
            axs[i].set_xticks(range(len(dates)))
            axs[i].set_xticklabels(dates, rotation=45)
            
            # Add labels and title
            axs[i].set_title(title)
            axs[i].legend()
            
            # Add average value text
            avg = weekly_df[metric].mean()
            axs[i].text(0.5, 0.9, f'Weekly Avg: {avg:.1f}', 
                      transform=axs[i].transAxes, ha='center', 
                      bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.suptitle('Weekly Health Dashboard', fontsize=16, y=1.02)
        plt.show()

    def show_menu(self):
        """Display the main menu options"""
        print("\n===== Health & Fitness Tracker =====")
        print("1. Add/Update Today's Data")
        print("2. Add/Update Health Data for a Specific Date")
        print("3. View/Update User Profile")
        print("4. Generate Weekly Report")
        print("5. View Weekly Trend for a Metric")
        print("6. View Weekly Goals Comparison")
        print("7. Show Health Dashboard")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ")
        return choice

    def add_today_data(self):
        """Add health data for today"""
        print("\n===== Add Today's Health Data =====")
        
        today = datetime.date.today().strftime("%Y-%m-%d")
        print(f"Date: {today}")
        
        try:
            steps = int(input(f"Steps (goal: {self.user_profile['goals']['steps']}): "))
            sleep = float(input(f"Sleep hours (goal: {self.user_profile['goals']['sleep']}): "))
            calories = int(input(f"Calories consumed (goal: {self.user_profile['goals']['calories']}): "))
            water = float(input(f"Water glasses (goal: {self.user_profile['goals']['water']}): "))
            
            self.add_health_data(today, steps, sleep, calories, water)
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    def add_specific_date_data(self):
        """Add health data for a specific date"""
        print("\n===== Add Health Data for Specific Date =====")
        
        date_input = input("Enter date (YYYY-MM-DD): ")
        try:
            # Validate date format
            datetime.datetime.strptime(date_input, "%Y-%m-%d")
            
            # Check if data exists for this date
            if date_input in self.health_data.index:
                print(f"Existing data for {date_input}:")
                print(f"Steps: {self.health_data.loc[date_input, 'steps']}")
                print(f"Sleep: {self.health_data.loc[date_input, 'sleep']}")
                print(f"Calories: {self.health_data.loc[date_input, 'calories']}")
                print(f"Water: {self.health_data.loc[date_input, 'water']}")
                
                update = input("Do you want to update this data? (y/n): ").lower()
                if update != 'y':
                    return
            
            steps = int(input(f"Steps (goal: {self.user_profile['goals']['steps']}): "))
            sleep = float(input(f"Sleep hours (goal: {self.user_profile['goals']['sleep']}): "))
            calories = int(input(f"Calories consumed (goal: {self.user_profile['goals']['calories']}): "))
            water = float(input(f"Water glasses (goal: {self.user_profile['goals']['water']}): "))
            
            self.add_health_data(date_input, steps, sleep, calories, water)
        except ValueError:
            print("Invalid input. Please check the date format and numeric values.")

    def view_update_profile(self):
        """View and update user profile"""
        print("\n===== User Profile =====")
        print(f"Name: {self.user_profile['name']}")
        print(f"Age: {self.user_profile['age']}")
        print(f"Gender: {self.user_profile['gender']}")
        print(f"Height: {self.user_profile['height']} cm")
        print(f"Weight: {self.user_profile['weight']} kg")
        
        bmi = self.calculate_bmi()
        bmi_category = self.get_bmi_category(bmi)
        print(f"BMI: {bmi} ({bmi_category})")
        
        calories = self.calculate_calories_needed()
        print(f"Estimated daily calorie needs: {calories}")
        
        print("\n--- Goals ---")
        print(f"Steps: {self.user_profile['goals']['steps']}")
        print(f"Sleep: {self.user_profile['goals']['sleep']} hours")
        print(f"Calories: {self.user_profile['goals']['calories']}")
        print(f"Water: {self.user_profile['goals']['water']} glasses")
        
        update = input("\nDo you want to update your profile? (y/n): ").lower()
        if update == 'y':
            try:
                print("\nLeave blank to keep current value")
                
                name = input(f"Name [{self.user_profile['name']}]: ") or None
                age = int(input(f"Age [{self.user_profile['age']}]: ") or self.user_profile['age'])
                gender = input(f"Gender [{self.user_profile['gender']}]: ") or None
                height = float(input(f"Height in cm [{self.user_profile['height']}]: ") or self.user_profile['height'])
                weight = float(input(f"Weight in kg [{self.user_profile['weight']}]: ") or self.user_profile['weight'])
                
                steps_goal = int(input(f"Steps goal [{self.user_profile['goals']['steps']}]: ") or self.user_profile['goals']['steps'])
                sleep_goal = float(input(f"Sleep goal [{self.user_profile['goals']['sleep']}]: ") or self.user_profile['goals']['sleep'])
                calories_goal = int(input(f"Calories goal [{self.user_profile['goals']['calories']}]: ") or self.user_profile['goals']['calories'])
                water_goal = float(input(f"Water goal [{self.user_profile['goals']['water']}]: ") or self.user_profile['goals']['water'])
                
                self.update_user_profile(name, age, gender, height, weight, 
                                       steps_goal, sleep_goal, calories_goal, water_goal)
            except ValueError:
                print("Invalid input. Profile not updated.")

    def view_weekly_report(self):
        """View the weekly health report"""
        print("\n===== Weekly Health Report =====")
        
        date_input = input("Enter end date (YYYY-MM-DD) or press Enter for today: ")
        if date_input:
            try:
                # Validate date format
                datetime.datetime.strptime(date_input, "%Y-%m-%d")
                report = self.generate_weekly_report(date_input)
            except ValueError:
                print("Invalid date format. Using today's date.")
                report = self.generate_weekly_report()
        else:
            report = self.generate_weekly_report()
        
        print("\n" + report)

    def view_metric_trend(self):
        """View trend for a specific metric"""
        print("\n===== Weekly Metric Trend =====")
        
        print("Available metrics:")
        print("1. Steps")
        print("2. Sleep")
        print("3. Calories")
        print("4. Water")
        
        choice = input("Select metric (1-4): ")
        metrics = ['steps', 'sleep', 'calories', 'water']
        
        try:
            metric = metrics[int(choice) - 1]
            
            date_input = input("Enter end date (YYYY-MM-DD) or press Enter for today: ")
            if date_input:
                try:
                    # Validate date format
                    datetime.datetime.strptime(date_input, "%Y-%m-%d")
                    self.plot_weekly_trend(metric, date_input)
                except ValueError:
                    print("Invalid date format. Using today's date.")
                    self.plot_weekly_trend(metric)
            else:
                self.plot_weekly_trend(metric)
        except (ValueError, IndexError):
            print("Invalid choice.")

    def view_goals_comparison(self):
        """View comparison of all goals"""
        print("\n===== Weekly Goals Comparison =====")
        
        date_input = input("Enter end date (YYYY-MM-DD) or press Enter for today: ")
        if date_input:
            try:
                # Validate date format
                datetime.datetime.strptime(date_input, "%Y-%m-%d")
                self.plot_weekly_comparison(date_input)
            except ValueError:
                print("Invalid date format. Using today's date.")
                self.plot_weekly_comparison()
        else:
            self.plot_weekly_comparison()

    def view_dashboard(self):
        """View comprehensive health dashboard"""
        print("\n===== Health Dashboard =====")
        
        date_input = input("Enter end date (YYYY-MM-DD) or press Enter for today: ")
        if date_input:
            try:
                # Validate date format
                datetime.datetime.strptime(date_input, "%Y-%m-%d")
                self.plot_health_dashboard(date_input)
            except ValueError:
                print("Invalid date format. Using today's date.")
                self.plot_health_dashboard()
        else:
            self.plot_health_dashboard()

    def run_cli(self):
        """Run command-line interface loop"""
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.add_today_data()
            elif choice == '2':
                self.add_specific_date_data()
            elif choice == '3':
                self.view_update_profile()
            elif choice == '4':
                self.view_weekly_report()
            elif choice == '5':
                self.view_metric_trend()
            elif choice == '6':
                self.view_goals_comparison()
            elif choice == '7':
                self.view_dashboard()
            elif choice == '8':
                print("Exiting Health & Fitness Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

            input("\nPress Enter to continue...")

# Example of how to use the tracker
if __name__ == "__main__":
    tracker = HealthFitnessTracker()
    
    # Add some sample data if needed (uncomment to use)
    # today = datetime.date.today().strftime("%Y-%m-%d")
    # yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    # tracker.add_health_data(today, 8500, 7.5, 1800, 6)
    # tracker.add_health_data(yesterday, 9200, 8.2, 2100, 7)
    
    # Run the application
    tracker.run_cli()