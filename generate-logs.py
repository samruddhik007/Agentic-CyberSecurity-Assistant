import json
import random
from datetime import datetime, timedelta

def generate_fake_attack_logs(filename="logs.json"):
    """Generates a realistic multi-stage cyber attack sequence."""
    base_time = datetime.utcnow() - timedelta(minutes=15)
    
    # Attack parameters
    attacker_ip = "192.168.1.105"
    target_ip = "10.0.0.5"
    target_host = "prod-db-01"
    victim_user = "admin"

    logs = []
    
    # -------------------------------------------------------------
    # Stage 1: Reconnaissance / Port Scanning (Time: T+0s to T+15s)
    # -------------------------------------------------------------
    for i, port in enumerate([22, 80, 443, 3389, 8080]):
        log_time = base_time + timedelta(seconds=i * 3)
        logs.append({
            "timestamp": log_time.isoformat() + "Z",
            "source": "firewall",
            "event_type": "connection_attempt",
            "status": "success" if port in [22, 3389] else "failed",
            "src_ip": attacker_ip,
            "dest_ip": target_ip,
            "dest_port": port,
            "user": "unknown",
            "hostname": target_host,
            "details": f"Inbound TCP connection attempt to port {port}"
        })

    # -------------------------------------------------------------
    # Stage 2: SSH Brute-Force Attack (Time: T+30s to T+60s)
    # -------------------------------------------------------------
    for i in range(5):
        log_time = base_time + timedelta(seconds=30 + i * 5)
        logs.append({
            "timestamp": log_time.isoformat() + "Z",
            "source": "auth_service",
            "event_type": "ssh_auth",
            "status": "failed",
            "src_ip": attacker_ip,
            "dest_ip": target_ip,
            "dest_port": 22,
            "user": victim_user,
            "hostname": target_host,
            "details": f"Failed password attempt for user '{victim_user}'"
        })

    # -------------------------------------------------------------
    # Stage 3: Compromise & Successful Login (Time: T+90s)
    # -------------------------------------------------------------
    logs.append({
        "timestamp": (base_time + timedelta(seconds=90)).isoformat() + "Z",
        "source": "auth_service",
        "event_type": "ssh_auth",
        "status": "success",
        "src_ip": attacker_ip,
        "dest_ip": target_ip,
        "dest_port": 22,
        "user": victim_user,
        "hostname": target_host,
        "details": f"Accepted password for user '{victim_user}' from {attacker_ip} port 22"
    })

    # -------------------------------------------------------------
    # Stage 4: Privilege Escalation (Time: T+120s)
    # -------------------------------------------------------------
    logs.append({
        "timestamp": (base_time + timedelta(seconds=120)).isoformat() + "Z",
        "source": "endpoint_agent",
        "event_type": "sudo_exec",
        "status": "success",
        "src_ip": attacker_ip,
        "dest_ip": target_ip,
        "dest_port": 0,
        "user": victim_user,
        "hostname": target_host,
        "details": "NOPASSWD sudo /bin/bash executed; shell spawned with root privileges"
    })

    # Save to JSON file
    with open(filename, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"✅ Generated {len(logs)} attack log entries in '{filename}' successfully!")

if __name__ == "__main__":
    generate_fake_attack_logs()
