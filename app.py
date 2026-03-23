import frida
import json
import http.server
import socketserver
import threading
import sys

PORTA_WEB = 1337  # Mude se desejar
PACKAGE_NAME = "br.com.seu.app" # Ajuste para o pacote real do app

findings = []
seen_data = set()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MemorySight</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <meta http-equiv="refresh" content="3"> <style>
        body { background: #0f0f0f; color: #00ff41; font-family: 'Courier New', Courier, monospace; }
        .table { color: #00ff41; border-color: #333; }
        .badge-infra { background-color: #ff4500; }
        .badge-auth { background-color: #1e90ff; }
        .badge-target { background-color: #32cd32; }
        .addr { color: #888; font-size: 0.8em; }
    </style>
</head>
<body>
    <div class="container-fluid mt-4">
        <h2 class="text-center">MemorySight: Dashboard</h2>
        <p class="text-center text-secondary border-bottom pb-2">Monitorando: """ + PACKAGE_NAME + """</p>
        
        <div class="table-responsive">
            <table class="table table-dark table-hover mt-3">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Categoria</th>
                        <th>Alvo</th>
                        <th>Endereço</th>
                        <th>Dados Extraídos (Payload)</th>
                    </tr>
                </thead>
                <tbody>
                    {%ROWS%}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

class WebHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        rows = ""
        # Mostra os últimos achados no topo
        for f in reversed(findings):
            badge_class = f"badge-{f['category'].lower()}"
            rows += f"<tr>"
            rows += f"<td>{f['timestamp']}</td>"
            rows += f"<td><span class='badge {badge_class}'>{f['category']}</span></td>"
            rows += f"<td>{f['label']}</td>"
            rows += f"<td class='addr'>{f['address']}</td>"
            rows += f"<td class='text-break'><code>{f['data']}</code></td>"
            rows += f"</tr>"
        self.wfile.write(HTML_TEMPLATE.replace("{%ROWS%}", rows).encode())

def run_server():
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORTA_WEB), WebHandler) as httpd:
        print(f"\n[!] DASHBOARD ONLINE: http://localhost:{PORTA_WEB}")
        httpd.serve_forever()

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        
        if payload['data'] not in seen_data:
            seen_data.add(payload['data'])
            findings.append(payload)
            print(f"[+] [{payload['category']}] Capturado: {payload['label']}")


try:
    device = frida.get_usb_device()
    
    try:
        session = device.attach(PACKAGE_NAME)
    except:
        pid = device.spawn([PACKAGE_NAME])
        session = device.attach(pid)
        device.resume(pid)

    with open("scanner.js", "r") as f:
        script = session.create_script(f.read())
    
    script.on('message', on_message)
    script.load()

    threading.Thread(target=run_server, daemon=True).start()
    
    print("[*] Scanner carregado. Pressione Ctrl+C para encerrar.")
    sys.stdin.read()

except KeyboardInterrupt:
    print("\n[-] Encerrando sessão...")
    sys.exit()
