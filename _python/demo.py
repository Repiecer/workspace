import random
import os

class GachaSim:
    def __init__(self):
        self.pity6 = 0
        self.pity5 = 0
        self.total = 0

    def get_6star_rate(self):
        if self.pity6 < 65:
            return 0.008
        elif self.pity6 >= 79:
            return 1.0
        else:
            return 0.058 + (self.pity6 - 65) * (0.758 - 0.058) / 14

    def pull(self):
        self.pity6 += 1
        self.pity5 += 1
        self.total += 1
        r = random.random()
        rate6 = self.get_6star_rate()
        if r < rate6:
            self.pity6 = 0
            self.pity5 = 0
            return 6
        if self.pity5 >= 10:
            self.pity5 = 0
            return 5
        if r < rate6 + 0.08:
            self.pity5 = 0
            return 5
        return 4

    def single(self):
        star = self.pull()
        print(f"第{self.total}抽: {star}星")
        self.show_status()

    def ten(self):
        print("\n=== 十连结果 ===")
        for i in range(10):
            star = self.pull()
            print(f"  第{i+1}抽: {star}星")
        self.show_status()

    def show_status(self):
        rate = self.get_6star_rate() * 100
        print(f"\n当前六星保底: {self.pity6}  五星保底: {self.pity5}/10  六星概率: {rate:.2f}%")

    def reset(self):
        self.pity6 = 0
        self.pity5 = 0
        self.total = 0
        print("已重置")

    def run(self):
        print("=== 明日方舟:终末地 抽卡模拟器 ===")
        print("六星:0.8% (65抽后概率提升,80抽保底)")
        print("五星:8% (10抽内必出五星)")
        while True:
            print("\n1.单抽 2.十连 3.状态 4.重置 5.退出")
            cmd = input("选择: ").strip()
            if cmd == "1":
                self.single()
            elif cmd == "2":
                self.ten()
            elif cmd == "3":
                self.show_status()
            elif cmd == "4":
                self.reset()
            elif cmd == "5":
                break

if __name__ == "__main__":
    GachaSim().run()