import unittest
import log


class TestLogCollector(unittest.TestCase):

    def test_check_overload(self):

        test_logs = [
            '20201019133124,10.20.30.1/16,10',
            '20201019133125,10.20.30.2/16,10',
            '20201019133126,10.20.30.1/16,10',
            '20201019133127,10.20.30.2/16,9',
            '20201019133128,10.20.30.1/16,10',
            '20201019133129,10.20.30.2/16,10',
            '20201019133130,10.20.30.1/16,11',
            '20201019133131,10.20.30.2/16,10',
        ]

        collector = log.LogCollector(last_m_count=3)

        results = []
        for line in test_logs:
            log_line = log.LogLine(line)
            collector.collect_stats(log_line)
            collector.check_overload(
                log_line, overload_threshold_millis=10, output_consumer=lambda o: results.append(o))

        self.assertEqual(1, len(results))
        self.assertEqual('10.20.30.1,2020-10-19 13:31:26,2020-10-19 13:31:30', results[0])


    def test_check_recent_failure(self):

        test_logs = [
            '20201019133124,10.20.30.1/16,10',
            '20201019133125,10.20.30.2/16,10',
            '20201019133126,10.20.30.1/16,-',
            '20201019133127,10.20.30.2/16,-',
            '20201019133128,10.20.30.1/16,-',
            '20201019133129,10.20.30.2/16,10',
            '20201019133130,10.20.30.1/16,11',
            '20201019133131,10.20.30.2/16,10',
        ]

        collector = log.LogCollector(last_m_count=3)

        results = []
        for line in test_logs:
            log_line = log.LogLine(line)

            collector.check_recent_failure(log_line, n=2, output_consumer=lambda o: results.append(o))
            collector.collect_stats(log_line)

        self.assertEqual(1, len(results))
        self.assertEqual('10.20.30.1,4', results[0])

    def test_check_recent_network_failure(self):

        test_logs = [
            '20201019133100,10.20.30.1/16,10',
            '20201019133101,10.20.30.2/16,-',
            '20201019133102,10.20.30.3/16,10',
            '20201019133103,10.20.30.1/16,-',
            '20201019133104,10.20.30.2/16,-',
            '20201019133105,10.20.30.3/16,-',
            '20201019133106,10.20.30.1/16,-',
            '20201019133107,10.20.30.2/16,-',
            '20201019133108,10.20.30.3/16,-',
            '20201019133109,10.20.30.1/16,10',
        ]

        collector = log.LogCollector(last_m_count=3)

        results = []
        for line in test_logs:
            log_line = log.LogLine(line)

            collector.check_recent_network_failure(log_line, n=2, output_consumer=lambda o: results.append(o))
            collector.collect_stats(log_line)

        self.assertEqual(1, len(results))
        self.assertEqual('10.20.0.0/16,4', results[0])        


if __name__ == '__main__':
    unittest.main()