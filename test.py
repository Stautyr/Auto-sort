from pathlib import Path

#startpath = Path.cwd()
#print(startpath)
pathList = str(Path.cwd()).split("\\")
user = pathList[2]
print(user)
if (pathList[3] == "OneDrive"):
    print("true")
