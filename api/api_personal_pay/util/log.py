from config.config import Config
import time


class Logger:
    @classmethod
    def log(cls, string):
        t = time.localtime(time.time())
        file_name = time.strftime("%Y%m%d", t)
        file = Config.ROOT_PATH + "/log/" + file_name + ".log"
        with open(file, 'a') as f:
            string = "\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + string
            f.write(string)
            print(string)
