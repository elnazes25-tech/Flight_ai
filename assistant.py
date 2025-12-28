# -*- coding: utf-8 -*-

from datetime import datetime

print(":airplane: دستیار هوشمند پرواز (NLP + فیلتر + لاگ)")
print("=" * 50)

text = input("چی می‌خوای؟ ").strip().lower()
words = text.split()

cheap = "ارزون" in words or "cheap" in words

origin = None
destination = None
max_price = None

for i, w in enumerate(words):
    if w == "از" and i + 1 < len(words):
        origin = words[i + 1].upper()
    if w == "به" and i + 1 < len(words):
        destination = words[i + 1].upper()
    if w == "زیر" and i + 1 < len(words):
        try:
            max_price = int(words[i + 1])
        except:
            pass

if not origin or not destination:
    print(":x: نتونستم مبدا یا مقصد رو بفهمم")
    exit()

flights = []

with open("flights.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) != 4:
            continue
        o, d, time, price = parts
        flights.append((o, d, time, int(price)))

matched = [f for f in flights if f[0] == origin and f[1] == destination]

if max_price is not None:
    matched = [f for f in matched if f[3] <= max_price]

if not matched:
    print(":x: پرواز مناسب پیدا نشد")
    exit()

matched.sort(key=lambda x: x[3])

if cheap:
    best = matched[0]
    result_text = f"BEST: {best[0]}->{best[1]} {best[2]} {best[3]}"
    print("\n:star: بهترین گزینه:")
    print(f":clock3: {best[2]} | :moneybag: {best[3]}")
else:
    result_text = "LIST"
    print("\n:airplane: پروازهای موجود:")
    for o, d, time, price in matched:
        print(f":clock3: {time} | :moneybag: {price}")

# ---------- ذخیره لاگ ----------
with open("logs.txt", "a", encoding="utf-8") as log:
    log.write(
        f"{datetime.now()} | INPUT: {text} | FROM: {origin} | TO: {destination} | RESULT: {result_text}\n"
    )

