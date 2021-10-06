# توضیح کلی
رباتی مخصوص تنظیم یادداشت و یادآوری (تکلیف) برای روز مشخص

# نحوه نصب

این ربات با استفاده از یک لایبری غیر رسمی نوشته شده است
- [SkPy](https://github.com/Terrance/SkPy#readme)

برای کارکرد ربات باید چند پکیج را نصب داشته باشید از جمله لایبری بالا

```
pip install Skpy
```
```
python -m pip install mysql-connector-python
```
```
pip install beautifulsoup4
```
```
pip install responses
```

# تنظیم یوزرنیم و پسورد

یک اکانت اسکایپ بسازید و ایمیل و پسورد و آن را در سورس مشخص کنید

```python
user = "example@gmqail.com"
password = "password"
ADMIN_LIVE_ID = "live:.cid.df869b09bdca9259"
````


# کارکرد

![image](https://user-images.githubusercontent.com/90097342/136155872-60750784-1298-4d85-8ab2-c2954e49a822.png)

# لیست دستورات ربات

###### لیست تکالیف ههمان روز
```
تکلیف
```

###### لیست تمامی تکالیف آینده

```
!all
```

###### اضافه کردن تکلیف
```
!add
date
Something
test
```
