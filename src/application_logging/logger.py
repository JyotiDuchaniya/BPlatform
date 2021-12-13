from datetime import datetime


class App_Logger:
    def __init__(self):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

    def log(file_path, log_message):
        new= App_Logger()
        file_object= open(file_path, 'a+')
        file_object.write(
            str(new.date) + "/" + str(new.current_time) + "\t\t" + log_message +"\n")
