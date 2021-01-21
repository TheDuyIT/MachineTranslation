import os
from os import path
import re
import numpy as np
from numpy.lib.npyio import load


class DataFormatter:
    def __init__(self) -> None:
        super().__init__()

    def preprocess(self, data: str) -> tuple:
        lst_vi, lst_cn = [], []
        t_flag, v_flag = 0, 0
        vi, cn = None, None
        last_line_start = None
        for line in data.split("\n"):
            if line.strip() == "":
                continue
            line_start = line[:2]

            if line_start == "T:" or line_start == "V:":
                if last_line_start == "V:":
                    lst_vi.append(re.sub(" +", " ", vi).strip())

                elif last_line_start == "T:":
                    lst_cn.append(re.sub(" +", " ", cn).strip())

                last_line_start = line[:2]

                if line_start == "T:":
                    t_flag = 1
                    v_flag = 0
                    cn = line[2:]
                else:
                    vi = line[2:]
                    t_flag = 0
                    v_flag = 1
            else:
                if t_flag:  # cn
                    cn = cn + " " + line
                elif v_flag:  # vi
                    vi = vi + " " + line
        # Last sentences save
        if last_line_start == "V:":
            lst_vi.append(re.sub(" +", " ", vi).strip())

        elif last_line_start == "T:":
            lst_cn.append(re.sub(" +", " ", cn).strip())
        # print(lst_cn[238])
        # print(lst_vi[238])
        # print(len(lst_vi))
        # print(len(lst_cn))
        return (lst_vi, lst_cn)

    def preprocess_3k(self, data: str) -> tuple:
        # print(data)
        xs = re.split("\n\s*\n", data)
        # print(xs)
        lst_vi = []
        lst_cn = []
        i = 0
        for x in xs:
            x = x.strip()
            if not x == "":
                if x.isnumeric():
                    i = 0
                    # print("---------------------")
                else:
                    if i == 2:
                        continue
                    tmp = " ".join(x.split("\n"))

                    if i == 0:
                        lst_vi.append(re.sub(" +", " ", tmp).strip())
                    else:
                        lst_cn.append(re.sub(" +", " ", tmp).strip())
                    i += 1
        return (lst_vi, lst_cn)

    def check(self, data: str) -> tuple:
        # print(data)
        xs = re.split("\n\s*\n", data)
        i = 0
        for x in xs:
            x = x.strip()
            if not x == "":
                if x.isnumeric():
                    if i != 3:
                        print(x)
                    i = 0
                    # print(x)
                else:
                    i += 1


class DataLoader:
    def __init__(self) -> None:
        super().__init__()

    def load_txt(self, path: str) -> str:
        assert isinstance(path, str), "Path must be str!"
        if not os.path.exists(path):
            raise Exception(f"Path {path} not exists!")

        with open(path, "rb") as f:
            data = f.read()
            data = data.decode("utf-8")
        return data

    def np_save(self, data: list, name: str, update=True) -> None:
        """Save list
        Args:
            data (list): [list to save]
            name (str): [name to save]
            update (bool, optional): [If true, file will be updated. if false, file will be replaced]. Defaults to True.
        """
        path_save = os.path.join("outputs/", name + ".npy")
        if update:
            if os.path.exists(path_save):
                data = self.np_load(name) + data
                np.save(path_save, np.array(data))
                return
        np.save(path_save, np.array(data))

    def np_load(self, name: str) -> list:
        path = os.path.join("outputs/", name + ".npy")
        return np.load(path).tolist()


if __name__ == "__main__":
    ROOT_DIR = os.getcwd()

    formatter = DataFormatter()
    loader = DataLoader()
    """
    # 999letters
    data = loader.load_txt(os.path.join(ROOT_DIR, "datasets/999letters.txt"))
    lst_vi, lst_cn = formatter.preprocess(data)
    loader.np_save(lst_cn, "lst_cn", update=False)
    loader.np_save(lst_vi, "lst_vi", update=False)
    print(len(loader.np_load("lst_cn")))
    print(len(loader.np_load("lst_vi")))

    # 3k datasets
    for name in os.listdir("datasets/"):
        if name.startswith("PDF"):
            print(name)
            path = os.path.join("datasets", name)
            data = loader.load_txt(path)
            lst_vi, lst_cn = formatter.preprocess_3k(data)
            loader.np_save(lst_cn, "lst_cn")
            loader.np_save(lst_vi, "lst_vi")
            print(len(loader.np_load("lst_cn")))
            print(len(loader.np_load("lst_vi")))
    """
    # 1001letters
    path = "datasets/1001letters_original.txt"
    data = loader.load_txt(path)
    lst_cn, lst_vi = formatter.preprocess_3k(data)
    print(len(lst_cn))
    print(len(lst_vi))
    print(len(loader.np_load("lst_cn_1000_original")))
    print(len(loader.np_load("lst_vi_1000_original")))
    loader.np_save(lst_cn, "lst_cn_1000_original")
    loader.np_save(lst_vi, "lst_vi_1000_original")
    print(len(loader.np_load("lst_cn_1000_original")))
    print(len(loader.np_load("lst_vi_1000_original")))

