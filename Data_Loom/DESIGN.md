This is a flask app using html, css, javascript, jinja, sql, and python with numpy, pandas,
and bokeh for the plotting. What I envisioned for this app was a playground for users to
upload their own datasets with areas to easily create plots and line plots and other visualization plots,
to modify and or combine to create other new datasets, and a area where users can play with
small neuro networks. That being said, This app does none of that right now.
All the app is able l to do is create a new user and a database for the user to store their uploaded
data files and creates two two table with random data sets so the user can play with plotting without
having to upload any files, which is good because I was unable to get the file uploading to work. I
have working code that takes a csv file puts it in a pandas data-frame and then inserts it into the
users database, but could not the the file downloading to work with. I converted the csv file to a pandas data frame before I inserted it into the database because I was planning on having an intermittent step to display the data frame so the user could visually check the data before inserting it into the database, I also found it easier to insert into the database as data frame —>database than csv —> database.
I choose numpy, pandas, bokeh for my plotting because I have worked with it before so it was familiar
to me. I could get the plotting to work but only with pre made random datasets and not with any of the
data queried from the user database db.
Most of my design decisions came about just trying to get stuff to work. It’s a sad comfort to know
that developing with html, css, javascript, juqery is the same unmitigated nightmare now as it was
10 years ago. It would have been somewhat easier to do the whole thing as a python app using tkinter
library as the UI but the app I envisioned was web based so anyone could have access to it. I also
took me well out of my comfort zone to do a web app and I learned a ton on the way. Using predominately
javascript probably would have been a better course to really get this app running how I wanted it to
run but it was too late to to go that direction once I came to that realization. It doesn’t work as
I intended but it’s a good start and I plan on continuing to work on it through out the summer and
plan on having a working version running on my server here at home. I would like to write more on the app
but now I'm completely brain fried and am going to spend the week after I submit this just sitting
on the deck and watching the traffic go by.
I apologize in advance to whoever has to weed thru my code.
