import os
import json
from datetime import datetime

class CofiLogger:
    """
    A logger class to record reduction steps and parameters for reproducibility.
    """
    def __init__(self):
        """Initializes the logger."""
        self.log_file_path = None
        self.log_dir = 'reduction_log'
        self._ensure_log_directory()

    def _ensure_log_directory(self):
        """Ensures the log directory exists."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def set_log_file(self, star_name):
        """
        Sets and creates the log file for the current reduction session based on a star name.
        A header is written to the new log file.
        """
        date_str = datetime.now().strftime('%Y-%m-%d')
        # Sanitize star_name to be a valid filename component
        safe_star_name = "".join([c for c in star_name if c.isalpha() or c.isdigit() or c in ('_','-')]).rstrip()
        filename = f"{safe_star_name}_log_{date_str}.txt"
        self.log_file_path = os.path.join(self.log_dir, filename)
        
        with open(self.log_file_path, 'w') as f:
            f.write(f"# CofI Reduction Log for Target: {star_name}\n")
            f.write(f"# Date: {date_str}\n")
            f.write("# This file contains the parameters used in each reduction step.\n")
            f.write("# It can be used to restore widget settings for reproducibility.\n")
            f.write("-" * 60 + "\n")
        print(f"📝 Logging session to: {self.log_file_path}")

    def log_action(self, tab_name, action_name, parameters):
        """
        Logs a specific action with its parameters in a structured, machine-readable format.
        """
        if not self.log_file_path:
            # Silently return if logging is not initiated, to avoid interrupting the user.
            return

        with open(self.log_file_path, 'a') as f:
            f.write(f"\n[TAB: {tab_name}]\n")
            f.write(f"ACTION: {action_name}\n")
            f.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
            # Write parameters as a JSON block for easy and robust parsing
            f.write("PARAMETERS:\n")
            f.write(json.dumps(parameters, indent=4))
            f.write("\n" + "-" * 60 + "\n")