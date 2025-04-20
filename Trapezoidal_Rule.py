import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify
import re

def get_function_from_user():
    """Get a mathematical function from user input and convert it to a Python function"""
    while True:
        try:
            # Get user input for the function
            func_str = input("Enter the function to integrate (e.g., x**2, sin(x), exp(-x**2), etc.): ")
            
            # Replace common math notation with Python syntax
            func_str = re.sub(r'(?<![a-zA-Z0-9_])e(?![a-zA-Z0-9_])', 'E', func_str)  # Replace e with E for scientific notation
            func_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', func_str)  # Replace '2x' with '2*x'
            
            # Define symbol and create sympify expression
            x = symbols('x')
            expr = sympify(func_str)
            
            # Convert to numpy function
            f = lambdify(x, expr, 'numpy')
            
            # Test the function with a simple value to make sure it works
            test_value = f(1.0)
            
            # Return both the function and its string representation
            return f, func_str
        except Exception as e:
            print(f"Error with function input: {e}")
            print("Please try again with a valid mathematical expression.")

def trapezoidal_rule(f, a, b, n):
    """
    Approximates the definite integral of f(x) from a to b using the trapezoidal rule.
    
    Parameters:
    f -- function to integrate
    a -- lower bound of integration
    b -- upper bound of integration
    n -- number of subintervals
    
    Returns:
    The approximate value of the integral and the x, y points
    """
    # Calculate step size
    h = (b - a) / n
    
    # Generate x points
    x = np.linspace(a, b, n+1)
    
    # Calculate function values at x points
    y = f(x)
    
    # Apply trapezoidal rule formula
    integral = h * (0.5 * y[0] + np.sum(y[1:n]) + 0.5 * y[n])
    
    return integral, x, y

def plot_trapezoidal(f, a, b, n, func_str):
    """Plot the function and the trapezoids used in the approximation"""
    integral, x, y = trapezoidal_rule(f, a, b, n)
    
    # Create a smooth curve for plotting the function
    x_curve = np.linspace(a, b, 1000)
    y_curve = f(x_curve)
    
    # Create plot
    plt.figure(figsize=(10, 6))
    
    # Plot the function
    plt.plot(x_curve, y_curve, 'b-', linewidth=2, label=f'f(x) = {func_str}')
    
    # Plot the trapezoids
    for i in range(n):
        # Plot each trapezoid
        plt.fill([x[i], x[i], x[i+1], x[i+1]], [0, y[i], y[i+1], 0], 'r', alpha=0.2)
        # Plot the lines of the trapezoid
        plt.plot([x[i], x[i+1]], [y[i], y[i+1]], 'r-', linewidth=1.5)
    
    # Add grid, legend, and labels
    plt.grid(True, alpha=0.3)
    plt.title(f'Trapezoidal Rule with n={n} subintervals\nIntegral ≈ {integral:.6f}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.tight_layout()
    
    plt.show()
    
    return integral

def get_float_input(prompt):
    """Get a valid float input from the user"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid number.")

def get_int_input(prompt, min_value=1):
    """Get a valid integer input from the user"""
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"Please enter an integer greater than or equal to {min_value}.")
            else:
                return value
        except ValueError:
            print("Please enter a valid integer.")

def main():
    print("=== Numerical Integration using Trapezoidal Rule ===\n")
    
    # Get function from user
    f, func_str = get_function_from_user()
    
    # Get integration bounds from user
    a = get_float_input("Enter the lower bound of integration (a): ")
    b = get_float_input("Enter the upper bound of integration (b, must be > a): ")
    while b <= a:
        print("Upper bound must be greater than lower bound.")
        b = get_float_input("Enter the upper bound of integration (b, must be > a): ")
    
    # Get number of subintervals from user
    n = get_int_input("Enter the number of subintervals (n): ")
    
    # Compute the integral using the trapezoidal rule
    integral, x, y = trapezoidal_rule(f, a, b, n)
    
    print(f"\nApproximation using {n} trapezoids: {integral:.6f}")
    
    # Plot the function and trapezoids
    plot_trapezoidal(f, a, b, n, func_str)
    
    # Optional: Compare with different numbers of subintervals
    compare = input("\nWould you like to compare results with different numbers of subintervals? (y/n): ")
    if compare.lower() == 'y':
        print("\nError vs number of subintervals:")
        subintervals = [n//2, n, n*2, n*4]
        if n < 4:  # Add smaller values if n is small
            subintervals = [2, 4, 8, 16]
        
        for n_test in subintervals:
            approx, _, _ = trapezoidal_rule(f, a, b, n_test)
            print(f"n = {n_test}: approximation = {approx:.6f}")

if __name__ == "__main__":
    main()