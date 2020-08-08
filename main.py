from config import config
import psycopg2
from tkinter import *
import GUI


def main():  # makes the program work
    conn = None
    root = Tk()
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        conn.set_session(autocommit=True)  # turns on the auto commit function
        cur = conn.cursor()

        root.title("Employee Attendance Management System")
        w = 600
        h = 570
        sw = (root.winfo_screenwidth() - w) / 2
        sh = (root.winfo_screenheight() - h) / 2
        root.geometry('%dx%d+%d+%d' % (w, h, sw, sh))
        GUI.CreateMenu(root, cur)  # Creates the menus for the window app
        GUI.CreateFrames(root, cur)  # Creates all the frames and widgets

        root.mainloop()  # Makes the program run

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Have a nice day.')


main()
