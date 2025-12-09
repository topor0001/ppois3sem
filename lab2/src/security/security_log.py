class SecurityLog:
    def __init__(self, log_id, user_account, action, timestamp, ip_address, status):
        self.log_id = log_id
        self.user_account = user_account
        self.action = action
        self.timestamp = timestamp
        self.ip_address = ip_address
        self.status = status
        self.details = ""

    def log_security_event(self, event_details):
        self.details = event_details

    def analyze_suspicious_activity(self, similar_logs):
        failed_attempts = 0
        for log in similar_logs:
            if log.status == "FAILED":
                failed_attempts += 1
        return failed_attempts > 3