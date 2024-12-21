import gzip


stringme= "hello therer how can i help"

zipped=gzip.compress(stringme.encode())
print(zipped)
on=zipped.hex()
print(on)
