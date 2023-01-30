# Import local files
from dataloader import *
from plot import *
from leemoore import *
from astar import *
from initiatives import *

#########################################
# Modify these variables
single_circuit = True
single_circuit_name = 'stdcell'
all_circuits = False
plot_empty = False
plot_leemore = False
plot_astar = True
plot_initative = True
pausetime = 1 # in seconds
#########################################

def run(benchmarks, name, update_interval, plot_final_only):
    '''
    Helper function to run leemoore and astar algorithm, with plot animation.
    Inputs: Benchmark name, update interval for animation, plot final only boolean
    Outputs: none. 
    '''
    print(f'Running on {name}')

    if plot_empty:
        test = benchmarks[name]
        initialize_benchmark(test)
        frame = plot(test)
        plt.title("Empty")
        plt.pause(pausetime)
    if plot_leemore:
        test = benchmarks[name]
        # Initialize benchmark again just in case
        initialize_benchmark(test)
        # Get frame object from matplotlib plot and pass into leemoore
        frame = plot(test)
        plt.title("Lee Moore")
        leemoore(test, frame, update_interval, plot_final_only)
        plt.pause(pausetime)    
    if plot_astar:    
        test = benchmarks[name]
        # Initialize benchmark again just in case
        initialize_benchmark(test)
        # Get new frame object from matplotlib plot and pass into astar
        frame = plot(test)
        plt.title("A*")
        astar(test, frame, update_interval, plot_final_only)
        # Pause for 10 seconds
        plt.pause(pausetime)
    if plot_initative:
        test = benchmarks[name]
        # Initialize benchmark again just in case
        initialize_benchmark(test)
        # Get frame object from matplotlib plot and pass into leemoore
        frame = plot(test)
        # frame = None
        plt.title("A* + Initiatives")
        initiative(test, frame, update_interval, plot_final_only)
        plt.pause(pausetime)


def main():
    # Load data into benchmarks dict and names list
    benchmarks, names = dataloader()

    # Initialize each benchmark
    for benchmark in benchmarks:
        initialize_benchmark(benchmarks[benchmark])

    # # Individual run
    if single_circuit:
        run(benchmarks, single_circuit_name, update_interval=0.01, plot_final_only=True)

    # Run all 
    if all_circuits:
        for name in names:
            run(benchmarks, name, update_interval=0.01, plot_final_only=True)

    # Pause to see the routes
    plt.pause(10000)

if __name__ == '__main__':
    main()