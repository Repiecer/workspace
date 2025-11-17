import requests
import threading
kroud = 0
colect = input("Collection:")
if colect == '':
    colect = 985
partcu = input("Line_run:")
if partcu == '':
    partcu = 10
f = open('result.txt', 'w')
def part_req(m, n):
    for i in range(m, n):
        url = "https://vip.aqdw"+str(i)+".com/videos/tag/cartoon"
        try:
            resss = requests.get(url, timeout=1.0)
        except:
            print(f"URL:HTTPS_{i}", "FAIL")
        else:
            if resss.status_code == 200:
                print(f"URL:HTTPS_{i}", "CONNECT SUCCESSFULLY")
                f.write(f"{i}\n")
while True:
    if kroud * partcu + partcu < colect:
        new_threading = threading.Thread(target=part_req, args=(kroud * partcu, kroud * partcu + partcu))
        new_threading.start()
        kroud += 1
    else:
        new_threading = threading.Thread(target=part_req, args=(kroud * partcu, colect))
        new_threading.start()
        break
