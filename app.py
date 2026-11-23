import flet as ft
import socket
import requests

def main(page: ft.Page):
    page.title = "NetGuard Security Toolkit"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "auto"
    page.padding = 20

    header = ft.Container(
        content=ft.Column([
            ft.Text("NetGuard Toolkit", size=28, weight="bold", color=ft.Colors.CYAN_400),
            ft.Text("Ethical Security Scanner & Utilities", size=14, color=ft.Colors.GREEN_400),
        ]),
        padding=15,
        border_radius=10,
        bgcolor=ft.Colors.BLUE_GREY_900,
    )

    target_input = ft.TextField(
        label="Enter Domain or IP (e.g. example.com)",
        border_color=ft.Colors.CYAN_400,
    )

    result_box = ft.Text("Results will appear here...", size=15, selectable=True)
    result_card = ft.Container(
        content=result_box,
        padding=15,
        border_radius=10,
        bgcolor=ft.Colors.GREY_900,
        width=float("inf")
    )

    def run_port_scan(e):
        raw_target = target_input.value.strip().replace("https://", "").replace("http://", "")
        target = raw_target.split("/")[0]
        if not target:
            result_box.value = "Please enter a target first!"
            page.update()
            return
        result_box.value = f"Scanning common ports for {target}..."
        page.update()
        common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
        open_ports = []
        try:
            ip = socket.gethostbyname(target)
            for port in common_ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((ip, port)) == 0:
                    open_ports.append(str(port))
                s.close()
            if open_ports:
                result_box.value = f"Target: {target} ({ip})\nOpen Ports: {', '.join(open_ports)}"
            else:
                result_box.value = f"Target: {target} ({ip})\nNo common open ports found."
        except Exception as ex:
            result_box.value = f"Error: {ex}"
        page.update()

    def run_header_check(e):
        url = target_input.value.strip()
        if not url:
            result_box.value = "Please enter a website URL first!"
            page.update()
            return
        if not url.startswith("http"):
            url = "https://" + url
        result_box.value = f"Checking security headers for {url}..."
        page.update()
        try:
            res = requests.get(url, timeout=5)
            headers = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options"]
            report = [f"Security Report for {url}:\n"]
            for h in headers:
                status = "[OK] Present" if h in res.headers else "[!] Missing"
                report.append(f"{status} : {h}")
            result_box.value = "\n".join(report)
        except Exception as ex:
            result_box.value = f"Connection failed: {ex}"
        page.update()

    def run_url_unshorten(e):
        url = target_input.value.strip()
        if not url:
            result_box.value = "Please enter a shortened URL first!"
            page.update()
            return
        if not url.startswith("http"):
            url = "https://" + url
        result_box.value = "Tracing final destination URL..."
        page.update()
        try:
            res = requests.head(url, allow_redirects=True, timeout=5)
            result_box.value = f"Original URL:\n{url}\n\nFinal Destination:\n{res.url}"
        except Exception as ex:
            result_box.value = f"Trace failed: {ex}"
        page.update()

    buttons = ft.Column([
        ft.ElevatedButton("Port Scanner", on_click=run_port_scan, width=float("inf")),
        ft.ElevatedButton("Security Headers Check", on_click=run_header_check, width=float("inf")),
        ft.ElevatedButton("URL Unshortener", on_click=run_url_unshorten, width=float("inf")),
    ], spacing=10)

    page.add(header, target_input, buttons, result_card)

ft.run(main)
