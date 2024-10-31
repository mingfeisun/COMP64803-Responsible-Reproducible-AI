import torch
import sys

def main():
    # Get command-line arguments
    args = sys.argv[1:]  # sys.argv[0] is the script name, so we ignore it
    
    # Print arguments
    print("Arguments:", args)

    # Set up the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if device.type == "cuda":
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Using CPU")

if __name__ == "__main__":
    main()
