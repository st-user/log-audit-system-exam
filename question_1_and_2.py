import log
import argparse

def n_type(x):
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError("Minimum n is 1")
    return x

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Question 1/2')
    parser.add_argument('-n', type=n_type, default=1)
    parser.add_argument('filename')
    args = parser.parse_args()

    collector = log.LogCollector()

    with open(args.filename, 'r', newline='') as f:
        for index, line in enumerate(f):

            log_line = log.LogLine(line.strip())
            collector.check_recent_failure(log_line, n=args.n)
            collector.collect_stats(log_line)

