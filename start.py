import time

while True:
    try:
        exec(open("./bot.py").read())
    except Exception as p:
        print(f"Bot failed with exception: {p}")
        time.sleep(5)
        pass