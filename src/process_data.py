import os
import unicodedata


class DataFormatter:
    def __init__(self) -> None:
        super().__init__()

    def preprocess(self, data: str) -> tuple:
        lst_vi, lst_cn = [], []
        t_flag, v_flag = 0, 0
        vi, cn = None, None
        i = 0
        last_line_start = None
        for line in data.split("\n"):
            # if i > 214 and i < 222:
            #     print("i", i)
            #     print("len vi:", len(lst_vi), "len cn:", len(lst_cn))
            #     print("vi", line)
            if line.strip() == "":
                continue
            line_start = line[:2]

            if line_start == "T:" or line_start == "V:":
                if last_line_start == "V:":
                    lst_vi.append(vi)

                elif last_line_start == "T:":
                    lst_cn.append(cn)

                last_line_start = line[:2]

                if line_start == "T:":
                    t_flag = 1
                    v_flag = 0
                    cn = line[2:]
                else:
                    vi = line[2:]
                    t_flag = 0
                    v_flag = 1

            # if line.startswith("V:"):
            #     # v_flag = 1
            #     i += 1
            #     t_flag = 0
            #     if vi:
            #         lst_vi.append(vi)
            #     vi = line[2:]
            # elif line.startswith("T:"):
            #     i += 1
            #     # v_flag = 0
            #     t_flag = 1
            #     if cn:
            #         lst_cn.append(cn)
            #     cn = line[2:]
            else:
                if t_flag:  # cn
                    cn = cn + " " + line
                elif v_flag:  # vi
                    vi = vi + " " + line

        # print(len(lst_vi))
        num = 237
        print(lst_vi[num])
        # print(len(lst_cn))
        print("-------------------------")
        print(lst_cn[num])

    def preprocess_3k(self, data: str) -> tuple:
        pass


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

    data = loader.load_txt(os.path.join(ROOT_DIR, "../datasets/10007.txt"))
    dic = formatter.preprocess_3k(data)

