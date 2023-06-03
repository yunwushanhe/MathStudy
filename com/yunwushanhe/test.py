import re
char01 = '你好'
char02 = '1'
if '\u4e00' <= char02 <= '\u9fa5':
    print("中文")
else:
    print("其他")

english_pattern = r'^[a-zA-Z]$'
if re.match(english_pattern, char02):
    print("英文")
else:
    print("其他")