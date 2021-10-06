from skpy import SkypeEventLoop, SkypeNewMessageEvent
import re
from datetime import datetime, timedelta
from time import time
from converter import gregorian_to_jalali
import mysql.connector
# convert to jalali date


def jalaliDate(obj):
    y, m, d = obj.strftime('%Y'), obj.strftime(
        '%m'), obj.strftime('%d')
    res = gregorian_to_jalali(int(y), int(m), int(d))
    return f"{res[0]}-{res[1]}-{res[2]}"


# varabile
user = "" # Skype skype 
password = "" # Password skype
# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="homework"
)
mycursor = db.cursor()
# check connetction status
print(db)

# Skype Events


class SkypeHomeworkBot(SkypeEventLoop):
    def __init__(self):
        super(SkypeHomeworkBot, self).__init__(user, password)
        print("Bot is online!")

    #
    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent)\
                and not event.msg.userId == self.userId \
                and "دفتر" in event.msg.content:
            event.msg.chat.sendMsg("✨لیست دفترهای لازم برای سال تحصیلی نهم به شرح زیر می باشد (pointdownindex)   :\n\n(1f4da_books)  ادبیات: 80 برگ\n(1f4da_books)  فیزیک: 60 برگ\n(1f4da_books)  ریاضی: 100 برگ\n(1f4da_books)  هندسه: اگر خواستیم میتوانیم تهیه کنیم\n(1f4da_books)  عربی: لازم ندارد.\n(1f4da_books)  علوم: نمیخواهد ولی اگر دفترچه نوت برداری داشته باشیم خوب هست\n(1f4da_books)  توحید: 100 برگ")

        # Homework
        if isinstance(event, SkypeNewMessageEvent) \
                and not event.msg.userId == self.userId \
                and re.match(r"^تکلیف", event.msg.content):
            todayDate = jalaliDate(datetime.utcfromtimestamp(int(time())))
            try:
                mycursor.execute(
                    f"SELECT * FROM info where date='{todayDate}'")
                myresult = mycursor.fetchall()
                homeWorkName = [data[0] for data in myresult]
                homeWorkTitle = [data[2] for data in myresult]
                allHomework = ''
                for text in zip(homeWorkName, homeWorkTitle):
                    allHomework += f"(pointleftindex) {text[1]}: {text[0]}\n"
                if len(allHomework) <= 0:
                    allHomework = "تکلیفی برای تحویل امروز نیست! برای دیدن تمامی تکالیف آینده دستور !all را بزنید"
                event.msg.chat.sendMsg(
                    f"✨تکالیفی که امروز مورخ {todayDate} مهلت تحویل هست، به شرح زیر می باشد (pointdownindex):\n\n{allHomework}")
            except mysql.connector.Error as err:
                event.msg.chat.sendMsg(
                    f"خطا در اتصال به دیتابیس!\n{err}")

        if isinstance(event, SkypeNewMessageEvent) \
                and not event.msg.userId == self.userId \
                and event.msg.content == "!all":
            mycursor.execute(
                f"SELECT * FROM info")
            myresult = mycursor.fetchall()
            allHomework = ''
            for i in range(1, len(myresult)):
                date = jalaliDate(datetime.utcfromtimestamp(
                    int(time())) + timedelta(days=i))
                try:
                    mycursor.execute(
                        f"SELECT * FROM info where date='{date}'")
                    myresult = mycursor.fetchall()
                    homeWorkName = [data[0] for data in myresult]
                    homeWorkTitle = [data[2] for data in myresult]
                    if not not myresult:
                        allHomework += f"تکالیف مورخ {date}\n"
                        for text in zip(homeWorkName, homeWorkTitle):
                            allHomework += f"(pointleftindex) {text[1]}: {text[0]}\n"
                        allHomework += "\n"
                except mysql.connector.Error as err:
                    event.msg.chat.sendMsg(
                        f"خطا در اتصال به دیتابیس!\n{err}")
            event.msg.chat.sendMsg(
                f"✨(1f4d7_greenbook) تمامی تکالیف آینده به شرح زیر می باشد:\n\n{allHomework}")

        if isinstance(event, SkypeNewMessageEvent) \
                and not event.msg.userId == self.userId \
                and re.match(r"^ping", event.msg.content):
            print(event.msg.userId)
            event.msg.chat.sendMsg(
                "✅")

        # Add homework

        # !add
        # date
        # homeWorkName
        # homeWorkTitle
        if isinstance(event, SkypeNewMessageEvent) \
                and not event.msg.userId == self.userId \
                and event.msg.userId == "live:.cid.df869b09bdca9259"\
                and re.match(r"^!add[\n\n]", event.msg.content):
            result = re.split("\n", event.msg.content)
            sql = f"INSERT INTO info (date,title,name) VALUES ('{result[1]}','{result[3]}','{result[2]}')"
            try:
                mycursor.execute(sql)
                db.commit()
                event.msg.chat.sendMsg(
                    f"(like)  با موفقیت تکلیف درس {result[3]} با عنوان {result[2]} برای تاریخ {result[1]} تنظیم شد!")
            # db error
            except mysql.connector.Error as err:
                event.msg.chat.sendMsg(
                    f"خطا در اتصال به دیتابیس!\n{err}")


sk = SkypeHomeworkBot()
sk.loop()
