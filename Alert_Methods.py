import datetime
from Alert_Database import Alert_Database
import redis

class Alert_Methods:

    def sort_reminders(self):
        #sort the reminders by their datetime object

    def send_reminder(self):
        #runs constantly to send then delete reminders that are at the time to be used