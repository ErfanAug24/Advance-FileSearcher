from pathlib import Path
import os

index = 0
for root, folders, files in Path("/home/erfan/").walk():

    for file in files:
        entry = Path(os.path.join(root, file))
        print(f"Index Number {index} | {os.path.join(root,file)}")
        # if index == 26:
        #     break
        print(f"Index Number {index} | {entry.name}")
        # print(f"Index Number : {index} | {entry.stat().st_mtime}")
        index += 1
    print(root)
