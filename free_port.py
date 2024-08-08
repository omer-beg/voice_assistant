import psutil

def free_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        for conn in proc.connections(kind='inet'):
            if conn.laddr.port == port:
                print(f"Terminating process {proc.info['name']} (PID: {proc.info['pid']}) using port {port}")
                proc.terminate()

# Free specific ports
free_port(5051)
free_port(5052)
free_port(5053)
free_port(5000)
free_port(8080)
free_port(5001)
