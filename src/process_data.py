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
                    lst_vi.append(re.sub(" +", " ", vi).strip().lower())

                elif last_line_start == "T:":
                    lst_cn.append(re.sub(" +", " ", cn).strip().lower())

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
            lst_vi.append(re.sub(" +", " ", vi).strip().lower())

        elif last_line_start == "T:":
            lst_cn.append(re.sub(" +", " ", cn).strip().lower())
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
                        lst_vi.append(re.sub(" +", " ", tmp).strip().lower())
                    else:
                        lst_cn.append(re.sub(" +", " ", tmp).strip().lower())
                    i += 1
        return (lst_vi, lst_cn)

    def preprocess_6k_binh(self, data: str) -> tuple:
        xs = re.split("\n", data)
        lst_vi = []
        lst_cn = []
        for i in xs:
            # print(i)
            span = re.search(r"[\u4e00-\u9fff]+", i).span()
            lst_vi.append(re.sub(" +", " ", i[: span[0]]).strip().lower())

            lst_cn.append(re.sub(" +", " ", i[span[0] :]).strip().lower())
            # print(lst_vi[-1])
            # print(lst_cn[-1])
        # print(len(lst_vi))
        # print(len(lst_cn))
        # num = -1
        # print(lst_vi[num])
        # print(lst_cn[num])
        return (lst_vi, lst_cn)

    def preprocess_format_bai_hat(self, data: str) -> tuple:
        xs = re.split("\n\s*\n", data)
        lst_vi = []
        lst_cn = []
        for x in xs:
            x = x.split("\n")
            # print(x)
            lst_cn.append(x[0].strip().lower())
            lst_vi.append(x[1].strip().lower())

        return (lst_vi, lst_cn)

    def check_pdf(self, data: str) -> tuple:
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

    def process_duplicate(
        self, lst_vi_old: str, lst_vi_new: list, lst_cn_old: str, lst_cn_new: list
    ) -> tuple:
        lst_vi_old = self.np_load(lst_vi_old)
        # for i in lst_vi_old:
        #     print(i)
        # print("-----------------------------------------")
        lst_cn_old = self.np_load(lst_cn_old)
        # for i in lst_cn_old:
        #     print(i)
        assert len(lst_vi_new) == len(lst_cn_new), "New pairs not match length!"
        assert len(lst_vi_old) == len(lst_cn_old), "Old pairs not match length!"

        lst_vi = np.array(lst_vi_new + lst_vi_old)
        lst_cn = np.array(lst_cn_new + lst_cn_old)

        # num = 1233
        # print(lst_vi[num])
        # print(lst_cn[num])
        tmp = np.unique(lst_vi, return_counts=True, return_index=True)

        ind = tmp[1][tmp[2] == 2]

        lst_duplicate = lst_vi[ind]
        res_vi = []
        res_cn = []
        for i, val in enumerate(lst_vi_new):
            if val in lst_duplicate:
                continue
            res_vi.append(val)
            res_cn.append(lst_cn_new[i])
        num = 12
        # print(res_vi[num])
        # print(res_cn[num])
        return res_vi, res_cn

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

    lst_vi_name = "lst_vi_all_with6k_except_1001_dict"
    lst_cn_name = "lst_cn_all_with6k_except_1001_dict"
    # 999letters
    data = loader.load_txt(os.path.join(ROOT_DIR, "datasets/999letters.txt"))
    lst_vi, lst_cn = formatter.preprocess(data)
    loader.np_save(lst_cn, lst_cn_name, update=False)
    loader.np_save(lst_vi, lst_vi_name, update=False)
    print(len(loader.np_load(lst_cn_name)))
    print(len(loader.np_load(lst_vi_name)))
    print("----------------")
    # 3k datasets
    for name in os.listdir("datasets/"):
        if name.startswith("PDF"):
            print(name)
            path = os.path.join("datasets", name)
            data = loader.load_txt(path)
            lst_vi, lst_cn = formatter.preprocess_3k(data)
            loader.np_save(lst_cn, lst_cn_name)
            loader.np_save(lst_vi, lst_vi_name)
            print(len(loader.np_load(lst_cn_name)))
    print(len(loader.np_load(lst_vi_name)))
    
    # 3k augment
    path = "datasets/dataset/3000cau_final.txt"
    data = loader.load_txt(path)
    lst_vi, lst_cn = formatter.preprocess_format_bai_hat(data)
    lst_vi, lst_cn = loader.process_duplicate(lst_vi_name, lst_vi, lst_cn_name, lst_cn)
    loader.np_save(lst_cn, lst_cn_name)
    loader.np_save(lst_vi, lst_vi_name)
    print(len(loader.np_load(lst_cn_name)))
    print(len(loader.np_load(lst_vi_name)))

    # 1001letters
    # path = "datasets/1001letters_original.txt"
    # data = loader.load_txt(path)
    # lst_cn, lst_vi = formatter.preprocess_3k(data)
    # print(len(lst_cn))
    # print(len(lst_vi))
    # print(len(loader.np_load("lst_cn_1000_original")))
    # print(len(loader.np_load("lst_vi_1000_original")))
    # loader.np_save(lst_cn, "lst_cn_1000_original")
    # loader.np_save(lst_vi, "lst_vi_1000_original")
    # print(len(loader.np_load("lst_cn_1000_original")))
    # print(len(loader.np_load("lst_vi_1000_original")))

    # format bai hat
    for name in os.listdir("datasets/"):
        if name.startswith("format_bai_hat"):
            print(name)
            path = os.path.join("datasets", name)
            data = loader.load_txt(path)
            lst_vi, lst_cn = formatter.preprocess_format_bai_hat(data)
            loader.np_save(lst_cn, lst_cn_name)
            loader.np_save(lst_vi, lst_vi_name)
            print(len(loader.np_load(lst_cn_name)))
            print(len(loader.np_load(lst_vi_name)))

    # path = "datasets/format_bai_hat_Yeu_cau_chang_can_ly_do.txt"
    # data = loader.load_txt(path)
    # lst_vi, lst_cn = formatter.preprocess_format_bai_hat(data)
    # print(len(lst_vi))
    # print(len(lst_cn))
    # print(lst_vi[0])
    # print(lst_cn[0])
    # print(lst_vi[-1])
    # print(lst_cn[-1])
    # loader.np_save(lst_cn, lst_cn_name)
    # loader.np_save(lst_vi, lst_vi_name)
    # print(loader.np_load(lst_vi_name)[-1])
    # print(loader.np_load(lst_cn_name)[-1])

    # 6k Binh

    for name in os.listdir("datasets/"):
        if name.startswith("binh_"):
            print(name)
            path = os.path.join("datasets", name)
            data = loader.load_txt(path)

            lst_vi, lst_cn = formatter.preprocess_6k_binh(data)
            loader.np_save(lst_cn, lst_cn_name)
            loader.np_save(lst_vi, lst_vi_name)
            print(len(loader.np_load(lst_vi_name)))
            print(len(loader.np_load(lst_cn_name)))
            print(loader.np_load(lst_vi_name)[-1])
            print(loader.np_load(lst_cn_name)[-1])

    for name in os.listdir("datasets/vi_zh"):
        if name.startswith("vi-zh"):
            print(name)
            path = os.path.join("datasets/vi_zh", name)
            data = loader.load_txt(path)
            # print(data)
            lst_vi, lst_cn = formatter.preprocess_6k_binh(data)

            loader.np_save(lst_cn, lst_cn_name)
            loader.np_save(lst_vi, lst_vi_name)
            print(loader.np_load(lst_vi_name)[-1])
            print(loader.np_load(lst_cn_name)[-1])

