# Goal is to minimize halfperimeter of smallest bounding box containing all pins for each net





from dataloader import *
from placement import *

def main():
    # Load data into circuits dict and names list
    circuits, names = dataloader()

    # Initialize each circuit
    for circuit in circuits:
        x = circuits[circuit]
        
        initialize(x)
        init_normal(x)
        init_hpwl(x)
        calc_cost(x)

    print(circuits)
    # # Individual run
    # if single_circuit:
    #     run(benchmarks, single_circuit_name, update_interval, plot_final_only)

    # # Run all 
    # if all_circuits:
    #     for name in names:
    #         run(benchmarks, name, update_interval, plot_final_only)

    # # Pause to see the routes
    # plt.pause(10000)

if __name__ == '__main__':
    main()