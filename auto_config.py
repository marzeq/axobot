import sys
import os
import platform


os.chdir(f"{os.getcwd()}/")
if not os.path.exists("config"):
    os.mkdir("config/")
os.chdir(f"{os.getcwd()}/config/")

print("""
INSTALLING REQUIRED PACKAGES
""")
os.system(f"{sys.executable} -m pip install -r ../requirements.txt")

print("""
CREATING CONFIG FILES THAT DON'T REQUIRE ANY USER INTERRACION
""")

nointerract = ["config.json", "tasks.json"]
for file in nointerract:
    if not os.path.isfile(file):
        with open(file, "w") as f:
            f.write("{}")
    else:
        print(f"Skipping {file}")

if not os.path.isfile("sbitems.json"):
    if platform.system() == "Windows":
        os.system(f"move ../THIS_IS_MOVED_WHEN_THE_BOT_IS_SET_UP_sbitems.json {os.getcwd()}")
        os.system(f"ren THIS_IS_MOVED_WHEN_THE_BOT_IS_SET_UP_sbitems.json sbitems.json")
    else:
        os.system(f"mv ../THIS_IS_MOVED_WHEN_THE_BOT_IS_SET_UP_sbitems.json {os.getcwd()}/sbitems.json")
else:
    print("Skipping sbitems.json")

print("""
CREATING CONFIG FILES THAT REQUIRE USER INTERRACION
""")

if not os.path.isfile("hypixelapi.json"):
    with open("hypixelapi.json", "w") as f:
        f.write('{\n\t"api_key": "' + input("Your Hypixel API key (Join mc.hypixel.net on Minecraft and type /api new) > ") + '"\n}')
else:
    print("Skipping hypixelapi.json")

if not os.path.isfile("pastebinapi.json"):
    with open("pastebinapi.json", "w") as f:
        f.write('{\n\t"api_key": "' + input("Your Pastebin Dev API key > ") + '",\n\t"username": "' + input("Your Pastebin username > ") + '",\n\t"password": "' + input("Your Pastebin password > ") + '"\n}')
else:
    print("Skipping pastebinapi.json")

if not os.path.isfile("reddit.json"):
    with open("reddit.json", "w") as f:
        f.write('{\n\t"secret": "' + input("Your Reddit app secret > ") + '",\n\t"id": "' + input("Your Reddit app ID > ") + '"\n}')
else:
    print("Skipping reddit.json")

if not os.path.isfile("token.txt"):
    with open("token.txt", "w") as f:
        f.write(input("Your bot token > "))
else:
    print("Skipping token.txt")

print("The file config/sbitems.json should be updated frequently!")
input("Press ENTER to quit. ")
