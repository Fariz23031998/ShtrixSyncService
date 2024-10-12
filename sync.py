import os
from datetime import datetime
import time


with open("config.txt", encoding='utf-8') as config_file:
    config = eval(config_file.read())

shtrix_file_list = config["regos_shtrix_files"]
check_time = config["check_time"]


class UpdateTxt:
    def __init__(self):
        with open("log.txt", "w", encoding="windows-1251") as log_file:
            log_file.write(f"File created at {self.get_date()}\n")

    def get_date(self):
        now = datetime.now()
        return now.strftime("%m/%d/%Y %H:%M:%S")

    def write_log_file(self, text):
        with open("log.txt", "a", encoding='utf-8') as file:
            file.write(text + '\n')


    def check_files(self):
        for shtrix_file in shtrix_file_list:
            if os.path.exists(shtrix_file):
                print(shtrix_file)
                self.compare_files(shtrix_file)


    def read_regos_txt(self, file_name):
        with open(file_name, "r", encoding="windows-1251") as file:
            lines = file.readlines()

        result = {line.strip().split(';')[7]: line.strip().split(';')[1:] for line in lines}

        return result

    def write_lines(self, updated_file, lists):
        with open(updated_file, "w", encoding="windows-1251") as updated_file:
            updated_file.writelines(line + "\n" for line in lists)

    def compare_files(self, shtrix_file):
        old_shtrix_file = f"old_{shtrix_file}"
        updated_shtrix_file = f"updated_{shtrix_file}"
        new_file_dict = self.read_regos_txt(shtrix_file)

        if os.path.exists(old_shtrix_file):
            new_lines = []
            old_file_dict = self.read_regos_txt(old_shtrix_file)
            for code, line in new_file_dict.items():
                line.insert(0, code)
                string_line = ";".join(line)
                if code in old_file_dict:
                    old_file_dict[code].insert(0, code)
                    # print(line == old_file_dict[code])
                    # print(line)
                    # print(old_file_dict[code])
                    if line != old_file_dict[code]:
                        new_lines.append(string_line)
                else:
                    new_lines.append(string_line)

            print(new_lines)
            if new_lines:
                self.write_lines(updated_shtrix_file, new_lines)

            self.write_log_file(f"Created {updated_shtrix_file} file that contains {len(new_lines)} "
                                f"new or updated items. ({self.get_date()})")

            os.remove(old_shtrix_file)
            os.rename(shtrix_file, old_shtrix_file)

        else:
            all_lines = []
            for code, line in new_file_dict.items():
                line.insert(0, code)
                string_line = ";".join(line)
                all_lines.append(string_line)

            self.write_lines(updated_shtrix_file, all_lines)
            self.write_log_file(f"Created {updated_shtrix_file} file that contains {len(all_lines)} "
                                f"new items. ({self.get_date()})")
            os.rename(shtrix_file, old_shtrix_file)


update_txt = UpdateTxt()

while True:
    update_txt.check_files()
    time.sleep(check_time)
