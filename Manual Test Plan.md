Manual Test Plan
==========

A Manual test plan including screenshots and the corresponding error and process.

Table of Contents
-----------------

  * [Prerequisites](#Prerequisites)
  * [Environment Setup and Configurations](#Environment)
  * [Error messages](#errors-and-process)
  * [Command Line Interface](#command-line-interface)
  * [Scraping process](#scraping-process)
  * [React Application](#react-application)



Prerequisites
------------

The application requires the following to run:
  * A Python development environment [PyCharm] or [PyDev for Eclipse]
  * Single-page application using frameworks like React



Environment
------------

1. clone the repository to local filesystem -- git clone https://gitlab.engr.illinois.edu/xinyu6/sp21-cs242-assignment2.git \
2. Open an IDE written in Python, such as PyCharm or PyDev for Eclipse, run the main.py file



Errors and Process
------------

If a book doesn't have a ISBN number, this error will appear: \
![title](MTP/isbn.png)

If the number of authors meet the requirement, this warning will appear:\
![title](MTP/author_number.png)

If the number of books meet the requirement, this warning will appear:\
![title](MTP/book_number_warning.png)



Command Line Interface
-------
This is the Command Line Interface if you just type "python main.py" in the terminal without any arguments:

![title](MTP/CLI.png)

Then if you type "python main.py -h" in the terminal, which give users explanations about the argument:
![title](MTP/CLI_help.png)

If a user gave an invalid url, this will appear:
![title](MTP/invalid_url.png)


Scraping process
-------

This is the scraping progress and errors showing when the scraper is running:
![title](MTP/process.png)

At the end, if users specify the output json file, this appears:
![title](MTP/jsonwriting.png)

And the according JSON file will be like this:
![title](MTP/json_out.png)

The database stored after scraping is:
![title](MTP/db.png)



React Application
-------

This is the main page when you start the react application where you can select the menu at the top and the API request type:
![title](MTP/home.png)

The request selector has the following value:
![title](MTP/requests.png)

There are 4 different types of API requests:
1. if the chosen request is PUT, you will get another selector showing below where you can select whether you want to update book or author:
![title](MTP/putAttr.png)
   Take book as an example, after choosing "Book Id", an input field will show up like following where you can type the book id:
   ![title](MTP/afterPutAttr.png)
   Then, after a valid book id is entered and click submit, a notification of success will show up:
   ![title](MTP/gettheput.png)
   And then an input group will show up where each field contains the information of the selected book:
   ![title](MTP/putinfo.png)
   After changing the field and click "Update" button, this message will show up and the database will be updated accordingly.
   ![title](MTP/putsuccess.png)
   
2. if the chosen request is GET, you will get another selector showing below where you can select whether you want to update book or author:
![title](MTP/getAttr.png)
   Take book as an example, after choosing "Book Id", an input field will show up like following where you can type the book id:
   ![title](MTP/afterGetAttr.png)
   Then, after a valid book id is entered and click submit, a notification of success will show up:
   ![title](MTP/getnotif.png)
   And then the information of the book matched the input field will show up:
   ![title](MTP/getsuccess.png)

3. if the chosen request is POST, you will get another selector showing below where you can select whether you want to update book or author:
   ![title](MTP/postAttr.png)
   If you choose "Book", an input group will show up where you can type the information of the book you want to create:
   ![title](MTP/postbook.png)
   If you choose "Author", another input group will show up where you can type the information of the author you want to create:
   ![title](MTP/postauthor.png)
   After filling out the fields and click "Submit" button, this message will show up and the database will be updated accordingly.
   ![title](MTP/postsuccess.png)
   
4. if the chosen request is DELETE, you will get another selector showing below where you can select whether you want to update book or author:
   ![title](MTP/deleteAttr.png)
   Take book as an example, after choosing "Book Id", an input field will show up like following where you can type the book id:
   ![title](MTP/afterDeleteAttr.png)
   Then, after a valid book id is entered and click submit, a notification of success will show up and the book will be deleted from the database:
   ![title](MTP/deletesucc.png)

Users can also choose "Top Books" and "Top Authors" on the top menu. 
If you click "Top Books", this is the page you will see after you click it:
![title](MTP/topbook.png)
You can specify the top k highest rating books in the input field, e.g. if you enter 3, the top 3 highest rating books will show up:
![title](MTP/topbookimage.png)

Same works for "Top Author". If you click "Top Books", this is the page you will see after you click it:
![title](MTP/topauthor.png)
You can specify the top k highest rating authors in the input field, e.g. if you enter 2, the top 2 highest rating authors will show up:
![title](MTP/topauthorimage.png)


[PyCharm]: https://www.jetbrains.com/pycharm/
[PyDev for Eclipse]: https://www.pydev.org/