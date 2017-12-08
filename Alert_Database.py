import redis
import threading
import Reminder_2
import ast
import datetime
from datetime import timedelta



class Alert_Database:

    def __init__(self, reminders):
        # Create base database for reminders
        self.r = redis.Redis()
        self.lock = threading.RLock()

        # Create initial id_num to act as key for reminders in database
        self.id_num = 0
        self.expired = []

    def get_reminders(self):
        reminders = self.r.keys()
        base_results = reminders[0: 10]
        results = []

        for i in range(0, len(base_results)):
            # Converts the each into a string
            key = base_results[i].decode("utf-8")
            info = self.r.get(base_results[i]).decode("utf-8")
            info = {key: ast.literal_eval(info)}

            results.append(info)

        return results

    def new_reminder(self, time, message):
        # reminder_instance is the object.
        # Take the time and text and put it into one object, then pull the values when needed
        reminder_instance = Reminder_2.Reminder2(time, message)

        # Adds the new reminder to the database.
        self.r.set(self.id_num, reminder_instance.reminder)
        print("Reminder successfully added. The reminder's ID is", self.id_num, ".")

        # It might be a good idea to sort the reminders by time
        # self.r.sort(self.r, by=ast.literal_eval(self.r.get(*).decode("utf-8")[0]))

        # Increment id_num to prepare for next reminder
        self.id_num += 1

    def delete_reminder(self, numID):
        # use for drop
        # numID is the unique identifying number

        selected_entry = self.r.get(numID)
        print(selected_entry)
        if selected_entry is None:
            response = "I'm sorry. " + str(numID) + " is not a valid reminder code."
        else:
            selected_entry = selected_entry.decode("utf-8")

            # Request for confirmation of deletion.
            user_input = input("Are you sure you want to delete the reminder, " + selected_entry + " ?")
            if user_input != "y" and user_input != "n":
                response = "Sorry, that is not a valid response."
            else:
                if user_input == "y":
                    self.r.delete(numID)
                    response = "Reminder deleted."
                if user_input == "n":
                    response = "Deletion canceled."
        print(response)
        return response

    def scan_reminders(self):
        self.expired = []
        for rem in self.r.keys():
            r_info = self.r.get(rem).decode("utf-8")
            r_time = list(ast.literal_eval(r_info))
            print(r_time)
            rem_t = datetime.datetime.strptime(r_time[0], "%H:%M:%S")
            rem_time = timedelta(hours=rem_t.hour, minutes=rem_t.minute, seconds=rem_t.second)
            pass_time_one = datetime.datetime.strptime("00:01:00", "%H:%M:%S").time()
            pass_time_two = datetime.datetime.strptime("23:59:00", "%H:%M:%S").time()
            time_diff = (datetime.datetime.now() - rem_time).time()
            if time_diff < pass_time_one or time_diff > pass_time_two:
                self.expired.append(rem)
        if len(self.expired) != 0:
            self.send_reminder()

    def send_reminder(self):
        for re in self.expired:
            print(re)
            print("this is send")
