# Funções para checagem de arquivos
import os
def file_exists(path): return os.path.isfile(path)
def dir_exists(path): return os.path.isdir(path)