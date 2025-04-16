from UI.mainframe import mainframe


import sys
sys.path.append('/home/user/Documents/Studium/pyvisa')

if __name__ == "__main__":
    app = mainframe()
    app.mainloop()