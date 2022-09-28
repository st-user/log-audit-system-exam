import log
import argparse

def n_type(x, arg_name):
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError(f"Minimum {arg_name} is 1")
    return x

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Question 3')
    parser.add_argument('-m', type=lambda m: n_type(m, 'm'), default=10)
    parser.add_argument('-t', type=lambda m: n_type(m, 't'), default=1000)
    parser.add_argument('filename')
    args = parser.parse_args()

    collector = log.LogCollector(last_m_count=args.m)

    with open(args.filename, 'r', newline='') as f:
        for index, line in enumerate(f):

            log_line = log.LogLine(line.strip())
            collector.collect_stats(log_line)
            collector.check_overload(log_line, overload_threshold_millis=args.t)

