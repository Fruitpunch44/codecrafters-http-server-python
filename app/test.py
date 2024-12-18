resp=['GET', '/echo/raspberry', 'HTTP/1.1', 'Host:', 'localhost:4221', 'Accept-Encoding:', 'gzip']

resp=''.join(resp)
print(resp)
headers={}
fields=resp.split('\r\n')
fields=fields[1:]
for field in fields:
    if ':' in field:
        key,value=field.split(':',1)
        headers[key]=value
print(headers)