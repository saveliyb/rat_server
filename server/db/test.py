import hashlib

result = hashlib.sha1(b'hello World!').hexdigest()
print(result)

# Будет выведено: aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d