res=['GET', '/echo/grape', 'HTTP/1.1', 'Host:', 'localhost:4221', 'Accept-Encoding:', 'gzip']
fields = res
fields = fields[2:]
headers = {}
for field in fields:
 if ':' in field:
     key, value = field.split(":", 1)
     headers[key.strip()] = value.strip()
print(headers)