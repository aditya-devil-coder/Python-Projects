import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import time

def estimate_pi(n):
    """
    Estimate the value of π using Monte Carlo simulation with n random points.
    """
    # Generate n random points within [-1, 1] x [-1, 1]
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)
    
    # Calculate distance from origin for each point
    distances = x**2 + y**2
    
    # Count points inside the unit circle
    inside_circle = np.sum(distances <= 1)
    
    # Estimate π
    pi_estimate = 4 * inside_circle / n
    
    return pi_estimate, x, y, distances <= 1

def plot_simulation(x, y, inside_circle, pi_estimate, n):
    """
    Plot the Monte Carlo simulation results.
    """
    plt.figure(figsize=(10, 8))
    
    # Plot square boundaries
    square = Rectangle((-1, -1), 2, 2, fill=False, color='black', linewidth=2)
    plt.gca().add_patch(square)
    
    # Plot circle
    circle = Circle((0, 0), 1, fill=False, color='blue', linewidth=2)
    plt.gca().add_patch(circle)
    
    # Plot points
    plt.scatter(x[inside_circle], y[inside_circle], color='green', s=10, alpha=0.6, label='Inside Circle')
    plt.scatter(x[~inside_circle], y[~inside_circle], color='red', s=10, alpha=0.6, label='Outside Circle')
    
    plt.axis('equal')
    plt.grid(True)
    plt.title(f'Monte Carlo Estimation of π using {n} random points\nEstimated π = {pi_estimate:.6f}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    
    plt.show()

def analyze_convergence():
    """
    Analyze the convergence of the Monte Carlo estimation as N increases.
    """
    try:
        max_power = int(input("Enter the maximum power of 10 for analysis (e.g., 5 for up to 10^5 points): "))
    except ValueError:
        print("Invalid input. Using default value of 5.")
        max_power = 5
    
    sample_sizes = [10**i for i in range(1, max_power+1)]
    pi_estimates = []
    execution_times = []
    
    for n in sample_sizes:
        start_time = time.time()
        estimate, _, _, _ = estimate_pi(n)
        end_time = time.time()
        
        pi_estimates.append(estimate)
        execution_times.append(end_time - start_time)
        
        print(f"N = {n}, π estimate = {estimate:.6f}, Error = {abs(estimate - np.pi):.6f}, Time: {end_time - start_time:.4f} sec")
    
    # Plot convergence
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.semilogx(sample_sizes, pi_estimates, 'o-', label='Estimated π')
    plt.semilogx(sample_sizes, [np.pi] * len(sample_sizes), 'r--', label='Actual π')
    plt.xlabel('Number of Points (Log Scale)')
    plt.ylabel('Estimated Value of π')
    plt.title('Convergence of π Estimation')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.loglog(sample_sizes, [abs(est - np.pi) for est in pi_estimates], 'o-')
    plt.xlabel('Number of Points (Log Scale)')
    plt.ylabel('Absolute Error (Log Scale)')
    plt.title('Error in π Estimation')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def main():
    print("Monte Carlo Simulation for Estimating π")
    print("=======================================")
    
    while True:
        print("\nChoose an option:")
        print("1. Run a single simulation with N points")
        print("2. Analyze convergence with different sample sizes")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            try:
                n = int(input("Enter the number of points to use (e.g., 1000): "))
                if n <= 0:
                    print("Number of points must be positive. Using default value of 1000.")
                    n = 1000
            except ValueError:
                print("Invalid input. Using default value of 1000.")
                n = 1000
                
            print(f"\nRunning simulation with {n} points...")
            pi_estimate, x, y, inside_circle = estimate_pi(n)
            print(f"Estimated π: {pi_estimate:.6f}")
            print(f"Actual π value: {np.pi:.6f}")
            print(f"Absolute error: {abs(pi_estimate - np.pi):.6f}")
            
            show_plot = input("Do you want to see the visualization? (y/n): ").lower()
            if show_plot == 'y':
                plot_simulation(x, y, inside_circle, pi_estimate, n)
                
        elif choice == '2':
            analyze_convergence()
            
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()