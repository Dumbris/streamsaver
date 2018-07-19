import argparse
from streamsaver.streamsaver import transform

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("-u", "--uri", type=str, required=True, 
                        help="URI locator for input. e.g. udp://localhost:6002")

    parser.add_argument("-o", "--out", type=str, choices=["mp4", "frame"], default="mp4",
                        help="type of output")

    parser.add_argument("-d", "--dest", type=str, default="/tmp/out.mp4",
                        help='file path for output file/files. e.g. ~/video.mp4 or ~/frame%%0d.jpeg')

    parser.add_argument("-n", "--num-buffers", type=int, default=-1,
                        help='limit the number of buffers from source to read. The program will read first N buffers then will exit. Useful for testing purpose')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    transform(args.uri, args.out, args.dest, args.num_buffers)