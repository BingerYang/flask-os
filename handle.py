import os
import shutil
import zipfile

path_project = "flask_os/conf/project.zip"
path_script = "project"


def zip_decode():
    print(os.path.exists(path_project))
    with zipfile.ZipFile(path_project) as zf:
        zf.extractall(path_script)
        print(os.path.exists(path_script))
        print("extract zipfile to: ", path_script)


def zip_encode():
    if os.path.exists(path_script):
        with zipfile.ZipFile(path_project, "w", zipfile.ZIP_DEFLATED) as zip_f:
            for root, dirs, files in os.walk(path_script):
                if root.endswith("__MACOSX"):
                    continue
                for file in files:
                    if file.startswith("."):
                        continue
                    zip_f.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path_script))
            shutil.rmtree(path_script)
            print("write zipfile to: ", path_project, "clear: ", path_script)


if __name__ == "__main__":
    zip_decode()
