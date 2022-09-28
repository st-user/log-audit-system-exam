import ipaddress
import datetime
from collections import defaultdict


class LogLine:

    def __init__(self, line):
        line_arr = line.split(',')
        # TODO value error
        self.timestamp = datetime.datetime.strptime(
            line_arr[0].strip(), '%Y%m%d%H%M%S')
        self.server_ip = ipaddress.ip_interface(line_arr[1].strip())

        str_ping_interval = line_arr[2].strip()
        if str_ping_interval != '-':
            self.ping_interval = int(str_ping_interval)
        else:
            self.ping_interval = None

    def is_failure(self):
        return self.ping_interval is None

    def __str__(self):
        return f'{self.timestamp},{self.server_ip},{self.ping_interval}'

    def format_timestamp(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')


class LogStats:

    def __init__(self):
        self.consecutive_failure_count = 0
        self.last_failure_timestamp = None
        self.last_success_m_logs = []


class LogCollector:

    def __init__(self, last_m_count=10):
        self.stats_by_server = dict()
        self.server_group = defaultdict(set)
        self.last_m_count = last_m_count

    def collect_stats(self, log_line):
        server_id = log_line.server_ip.ip

        self.server_group[log_line.server_ip.network].add(log_line.server_ip.ip)

        stats = None
        if server_id in self.stats_by_server:
            stats = self.stats_by_server[server_id]
        else:
            stats = LogStats()
            self.stats_by_server[server_id] = stats

        if log_line.ping_interval is None:
            stats.consecutive_failure_count += 1
            if stats.last_failure_timestamp is None:
                stats.last_failure_timestamp = log_line.timestamp
        else:
            stats.consecutive_failure_count = 0
            stats.last_failure_timestamp = None
            if self.last_m_count <= len(stats.last_success_m_logs):
                stats.last_success_m_logs.pop(0)

            stats.last_success_m_logs.append(log_line)

    def check_overload(self, log_line, overload_threshold_millis=100, output_consumer=lambda o: print(o)):
        server_id = log_line.server_ip.ip
        if server_id in self.stats_by_server:
            server_stats = self.stats_by_server[server_id]
            if len(server_stats.last_success_m_logs) < self.last_m_count:
                return

            avg_response_time = sum(
                [log.ping_interval for log in server_stats.last_success_m_logs]) / len(server_stats.last_success_m_logs)

            if avg_response_time > overload_threshold_millis:
                start_timestamp = server_stats.last_success_m_logs[0].format_timestamp(
                )
                end_timestamp = server_stats.last_success_m_logs[-1].format_timestamp(
                )
                output_consumer(f'{server_id},{start_timestamp},{end_timestamp}')

    def check_recent_failure(self, log_line, n=1, output_consumer=lambda o: print(o)):
        if log_line.ping_interval != None:
            server_id = log_line.server_ip.ip
            if server_id in self.stats_by_server:
                stats = self.stats_by_server[server_id]
                if stats.consecutive_failure_count >= n:
                    mean_time = log_line.timestamp - stats.last_failure_timestamp
                    output_consumer(f'{server_id},{mean_time.seconds}')
    
    def check_recent_network_failure(self, log_line, n=1, output_consumer=lambda o: print(o)):
        if log_line.ping_interval is None:
            return

        server_ips = self.server_group[log_line.server_ip.network]
        if len(server_ips) == 0:
            return

        # 初めて「全てのサーバーが応答しなくなった」状態となった時刻を、「故障期間」の開始とみなす。
        # すなわち、対象の全てのサーバーの「最初のタイムアウト」のうち、最も遅い時刻を「故障期間」の開始とみなす
        failure_timestamps = []
        for server_id in server_ips:
            stats = self.stats_by_server[server_id]
            if stats.consecutive_failure_count >= n:
                failure_timestamps.append(stats.last_failure_timestamp)

        if len(failure_timestamps) != len(server_ips):
            return
        
        failure_timestamps.sort()

        mean_time = log_line.timestamp - failure_timestamps[-1]
        output_consumer(f'{log_line.server_ip.network},{mean_time.seconds}')




