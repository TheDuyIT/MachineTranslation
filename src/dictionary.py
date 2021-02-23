import sys
import os

sys.path.append(os.getcwd())

from src.process_data import DataLoader, DataFormatter


class Dictionary:
    def __init__(self) -> None:
        self.data_loader = DataLoader()
        self.data_formatter = DataFormatter()

    def create_dict(self, data_path: str) -> dict:
        dic = dict()
        for name in os.listdir(data_path):
            if name.startswith("vi-zh"):
                # print(name)
                path = os.path.join(data_path, name)
                data = self.data_loader.load_txt(path)
                # print(data)
                lst_vi, lst_cn = self.data_formatter.preprocess_6k_binh(data)

                dic_tmp = dict(zip(lst_cn, lst_vi))
                dic.update(dic_tmp)
                print(len(dic.keys()))
        return dic


if __name__ == "__main__":
    dictionary = Dictionary()
    dictionary.create_dict("datasets/vi_zh")
