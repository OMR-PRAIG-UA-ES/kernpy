import argparse


# drizo: TODO
# joan: not tested
def main():
    parser = argparse.ArgumentParser(description="pyKern")

    # Boolean option
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')

    # Integer option
    parser.add_argument('--num_iterations', type=int, default=10, help='Number of iterations')

    args = parser.parse_args()

    # Accessing the values of the options
    print("Verbose mode:", args.verbose)
    print("Number of iterations:", args.num_iterations)


if __name__ == "__main__":
    main()

