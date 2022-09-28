import log
import argparse

def n_type(x, arg_name):
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError(f"{arg_name}は、1以上の整数を入力してください")
    return x
def o_type(o):
    if o != 'F' and o != 'L' and o != 'S':
        raise argparse.ArgumentTypeError(f"oは、F,L,Sのいづれかを入力してください")
    return o

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ログ解析プログラム')
    parser.add_argument('-o', type=o_type, default='F')
    parser.add_argument('-n', type=lambda n: n_type(n, 'n'), default=1)
    parser.add_argument('-m', type=lambda m: n_type(m, 'm'), default=10)
    parser.add_argument('-t', type=lambda t: n_type(t, 't'), default=1000)
    parser.add_argument('filename')
    args = parser.parse_args()

    collector = log.LogCollector(last_m_count=args.m)

    with open(args.filename, 'r', newline='') as f:
        for index, line in enumerate(f):

            log_line = None
            try:
                log_line = log.LogLine(line.strip())
            except Exception as e:
                print(f'ERR: ログの行解析中にエラーが発生しました L:{index + 1} {line.strip()}')
                print(f'ERR: {e}')
                continue

            if args.o == 'F':
                collector.check_recent_failure(log_line, n=args.n)

            if args.o == 'S':
                collector.check_recent_network_failure(log_line, n=args.n)
            
            collector.collect_stats(log_line)

            if args.o == 'L':
                collector.check_overload(log_line, overload_threshold_millis=args.t)


