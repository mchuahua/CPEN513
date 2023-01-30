# Import local files
from dataloader import *
from plot import *
from leemoore import *
from astar import *
from initiatives import *

def run(benchmarks, name, update_interval, plot_final_only):
    '''
    Helper function to run leemoore and astar algorithm, with plot animation.
    Inputs: Benchmark name, update interval for animation, plot final only boolean
    Outputs: none. 
    '''
    # print(name)
    # test = benchmarks[name]
    # # Initialize benchmark again just in case
    # initialize_benchmark(test)
    # # Get frame object from matplotlib plot and pass into leemoore
    # frame = plot(test)
    # plt.title("Lee Moore")
    # leemoore(test, frame, update_interval, plot_final_only)
    # # Pause for 10 seconds
    # plt.pause(10)    
    # # Initialize benchmark again just in case
    # initialize_benchmark(test)
    # # Get new frame object from matplotlib plot and pass into astar
    # frame = plot(test)
    # plt.title("A*")
    # astar(test, frame, update_interval, plot_final_only)
    # # Pause for 10 seconds
    # plt.pause(10)

    test = benchmarks[name]

    initialize_benchmark(test)

    frame = plot(test)
    plt.pause(10)

    print(name)
    test = benchmarks[name]
    # Initialize benchmark again just in case
    initialize_benchmark(test)
    # Get frame object from matplotlib plot and pass into leemoore
    frame = plot(test)
    # frame = None
    plt.title("A* + Initiatives")
    initiative(test, frame, update_interval, plot_final_only)
    plt.pause(100)


def main():
    # Load data into benchmarks dict and names list
    benchmarks, names = dataloader()

    # Initialize each benchmark
    for benchmark in benchmarks:
        initialize_benchmark(benchmarks[benchmark])

    # Individual run
    name = 'impossible'
    run(benchmarks, name, update_interval=0.01, plot_final_only=True)

    # Run all 
    # for name in names:
    #     run(name, update_interval=0.01, plot_final_only=False)

if __name__ == '__main__':
    main()