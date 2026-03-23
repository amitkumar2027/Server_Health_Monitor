import psutil
import paramiko

from config.settings import USE_LOCAL, SERVER


def get_stats():

    try:
        # ✅ LOCAL MONITORING
        if USE_LOCAL:

            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent

            # Windows safe disk path
            disk = psutil.disk_usage('C:\\').percent

            return cpu, ram, disk

        # ✅ SSH MONITORING
        else:

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                hostname=SERVER["host"],
                username=SERVER["username"],
                password=SERVER["password"],
                timeout=10
            )

            # CPU
            stdin, stdout, stderr = ssh.exec_command(
                "top -bn1 | grep 'Cpu(s)' | awk '{print 100 - $8}'"
            )
            cpu_output = stdout.read().decode().strip()

            # RAM
            stdin, stdout, stderr = ssh.exec_command(
                "free | grep Mem | awk '{print ($3/$2) * 100.0}'"
            )
            ram_output = stdout.read().decode().strip()

            # Disk
            stdin, stdout, stderr = ssh.exec_command(
                "df -h / | awk 'NR==2 {print $5}' | sed 's/%//'"
            )
            disk_output = stdout.read().decode().strip()

            ssh.close()

            # 🔥 SAFE FLOAT (no crash)
            cpu = float(cpu_output) if cpu_output else 0.0
            ram = float(ram_output) if ram_output else 0.0
            disk = float(disk_output) if disk_output else 0.0

            return cpu, ram, disk

    except Exception as e:

        print("Monitoring error:", e)

        # 💀 Never crash GUI
        return 0.0, 0.0, 0.0
