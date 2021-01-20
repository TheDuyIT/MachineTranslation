import os
import re


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
                    lst_vi.append(re.sub(" +", " ", vi))

                elif last_line_start == "T:":
                    lst_cn.append(re.sub(" +", " ", cn))

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
        num = 237
        print(lst_vi[num])
        # print(len(lst_cn))
        print("-------------------------")
        print(lst_cn[num])

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
                        lst_vi.append(re.sub(" +", " ", tmp))
                    else:
                        lst_cn.append(re.sub(" +", " ", tmp))
                    i += 1
        print(len(lst_vi))
        print(len(lst_cn))
        # print(lst_vi)
        # print("---------------------")
        # print(lst_cn)

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


if __name__ == "__main__":
    ROOT_DIR = os.getcwd()

    formatter = DataFormatter()
    loader = DataLoader()

    # data = loader.load_txt(os.path.join(ROOT_DIR, "../datasets/999letters.txt"))
    # dic = formatter.preprocess(data)
    data = loader.load_txt(os.path.join(ROOT_DIR, "../datasets/100_07.txt"))
    dic = formatter.preprocess_3k(data)

