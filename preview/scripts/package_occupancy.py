"""Copy the occupancy exercise assets and create its learner download."""
from pathlib import Path
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[2]
source = root / "course/notebooks/module-5"
target = root / "preview/public/notebooks/module-5"
(target / "public").mkdir(parents=True, exist_ok=True)
for name in ["occupancy.py", "occupancy_reuse.py"]:
    shutil.copyfile(source / name, target / name)
shutil.copyfile(source / "occupancy.py", target / "public/occupancy.py")
shutil.copyfile(source / "public/occupancy.csv", target / "public/occupancy.csv")
files = ["occupancy.py", "occupancy_reuse.py", "public/occupancy.csv",
         "OCCUPANCY-SOURCES.md", "licenses/marimo-studio-LICENSE.txt"]
with ZipFile(target / "occupancy-course.zip", "w", ZIP_DEFLATED) as archive:
    for name in files:
        archive.write(source / name, "occupancy-course/" + name)
print("Packaged occupancy notebooks and data.")
