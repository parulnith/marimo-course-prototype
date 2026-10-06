"""Copy the occupancy exercise assets and create its learner download."""
from pathlib import Path
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[2]
source = root / "course/notebooks/module-5"
target = root / "preview/public/notebooks/module-5"
(target / "public").mkdir(parents=True, exist_ok=True)
shutil.copyfile(source / "occupancy.py", target / "occupancy.py")
shutil.copyfile(source / "occupancy.py", target / "public/occupancy.py")
shutil.copyfile(source / "occupancy.csv", target / "public/occupancy.csv")
files = ["occupancy.py", "occupancy.csv", "LICENSE.txt"]
with ZipFile(target / "module-5-occupancy.zip", "w", ZIP_DEFLATED) as archive:
    for name in files:
        archive.write(source / name, "module-5-occupancy/" + name)
print("Packaged occupancy notebooks and data.")
