import argparse
import os
import sys
from run import run


def parse_arguments():
    '''
    Parse command-line arguments
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--input', 
        type=str,required=True,
        help='Path in the filesystem to a directory where guitar pro files are located.'
    )
    parser.add_argument(
        '-o', '--output', 
        type=str,required=True,
        help='Path in the filesystem to a directory where processed data will be exported.'
    )
    parser.add_argument(
        '-m', '--multiproc', 
        action='store_true',required=False,
        help='Will process gp files with multiprocessing if enabled.'
    )
    parser.add_argument(
        '-r', '--report', 
        action='store_true',required=False,
        help='Will generate a report CSV file if enabled.'
    )

    return parser.parse_args()


def check_parameters(args):
    '''
    Check if parameters are valid
    '''
    if not os.path.isdir(args.input):
        print(f"Error: Input directory '{args.input}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(args.output):
        print(f"Error: Output directory '{args.output}' does not exist.")
        sys.exit(1)


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Check parameters
    check_parameters(args)

    # Run program
    run(args)
