'''
测试数据1:
输入: mn, Ozsj
输出: hi, June


测试数据2:
输入: udymts, N qtaj z
输出: python, I love u
'''
def decoder(text):
     result = []
     for char in text:
          if 'a' <= char <= 'z':
               new_char = chr((ord(char) - ord('a') - 5) % 26 + ord('a'))
               result.append(new_char)
          elif 'A' <= char <= 'Z':
               new_char = chr((ord(char) - ord('A') - 5) % 26 + ord('A'))
               result.append(new_char)
          else:
               result.append(char)
     return ''.join(result)
def main():
    text = input()
    ans = decoder(text)
    print(ans)


main()