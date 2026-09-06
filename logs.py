import time

def stream_linux_auth_logs(log_file_path="/var/log/auth.log"):
    """Tails a live Linux auth log file like 'tail -f'."""
    with open(log_file_path, "r") as file:
        # Move to the end of the file to read new incoming logs
        file.seek(0, 2)
        
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)  # Wait for new log entries
                continue
            
            # Parse raw log text into structured dictionary
            if "Failed password" in line:
                print(f"[LIVE DETECTED] Failed Login: {line.strip()}")
            elif "sudo" in line:
                print(f"[LIVE DETECTED] Privilege Escalation: {line.strip()}")

# Run the live stream
# stream_linux_auth_logs()
