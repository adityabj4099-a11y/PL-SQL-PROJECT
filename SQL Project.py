import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management System")
        self.root.geometry("1200x700+100+50")
        self.root.resizable(False, False)

        # Title
        title = tk.Label(self.root, text="Student Record Management System",
                         bg="#4db851", fg="white", font=("Elephant", 36, "bold"),
                         bd=4, relief="raised", pady=10)
        title.pack(side="top", fill="x")

        # Option Frame
        optFrame = tk.Frame(self.root, bd=4, relief="ridge", bg="#f0f0f0")
        optFrame.place(width=300, height=550, x=30, y=120)

        buttons = [
            ("Add Student", self.addFrameFun),
            ("Search Student", self.searchFrameFun),
            ("Update Record", self.updFrameFun),
            ("Show All", self.showAll),
            ("Remove Student", self.delFrameFun)
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = tk.Button(optFrame, text=text, command=cmd,
                            bg="#2196f3", fg="white", bd=3, relief="raised",
                            font=("Arial", 16, "bold"), width=18, height=2)
            btn.grid(row=i, column=0, padx=20, pady=12)
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1976d2"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2196f3"))

        # Detail Frame
        self.detFrame = tk.Frame(self.root, bd=4, relief="ridge", bg="#fff9c4")
        self.detFrame.place(width=840, height=550, x=350, y=120)

        tk.Label(self.detFrame, text="Record Details",
                 font=("Arial", 28, "bold"), bg="#fff9c4").pack(side="top", fill="x", pady=10)

        self.tabFun()

        # Keep track of current active frame
        self.currentFrame = None

    # --- Table ---
    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="#b2ebf2")
        tabFrame.place(width=800, height=420, x=20, y=80)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        style.configure("Treeview", font=("Arial", 14), rowheight=28)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")
        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("roll", "name", "fname", "sub", "grade"))
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("roll", text="Roll No")
        self.table.heading("name", text="Name")
        self.table.heading("fname", text="Father Name")
        self.table.heading("sub", text="Subject")
        self.table.heading("grade", text="Grade")
        self.table["show"] = "headings"

        self.table.column("roll", width=100, anchor="center")
        self.table.column("name", width=180, anchor="w")
        self.table.column("fname", width=180, anchor="w")
        self.table.column("sub", width=120, anchor="center")
        self.table.column("grade", width=80, anchor="center")

        self.table.pack(fill="both", expand=1, padx=5, pady=5)

    # --- Utility to close current frame ---
    def close_current_frame(self):
        if self.currentFrame:
            self.currentFrame.destroy()
            self.currentFrame = None

    # --- DATABASE CONNECTION ---
    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="12345", database="rec")
        self.cur = self.con.cursor()

    # --- ADD STUDENT ---
    def addFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#96b4fa")
        self.currentFrame.place(width=450, height=450, x=400, y=140)

        entries = [
            ("Roll No:", "rollNo"), ("Name:", "name"), ("Father Name:", "fname"),
            ("Subject:", "sub"), ("Grade:", "grade")
        ]
        self.addVars = {}
        for i, (lbl, var) in enumerate(entries):
            tk.Label(self.currentFrame, text=lbl, font=("arial", 15, "bold"), bg="#96b4fa").grid(row=i, column=0, padx=20, pady=12, sticky="w")
            ent = tk.Entry(self.currentFrame, width=25, font=("arial", 15, "bold"), bd=3)
            ent.grid(row=i, column=1, padx=10, pady=12)
            self.addVars[var] = ent

        tk.Button(self.currentFrame, text="Enter", command=self.addFun,
                  bd=3, relief="raised", font=("Arial", 20, "bold"), width=18).grid(row=len(entries), column=0, columnspan=2, pady=10)
        tk.Button(self.currentFrame, text="❌ Back", command=self.close_current_frame,
                  bd=3, relief="raised", font=("Arial", 15, "bold"), width=12, bg="red", fg="white").grid(row=len(entries)+1, column=0, columnspan=2, pady=10)

    def addFun(self):
        rn = self.addVars["rollNo"].get()
        name = self.addVars["name"].get()
        fname = self.addVars["fname"].get()
        sub = self.addVars["sub"].get()
        grade = self.addVars["grade"].get()
        if rn and name and fname and sub and grade:
            try:
                rNo = int(rn)
                self.dbFun()
                self.cur.execute(
                    "insert into student(rollNo,name,fname,sub,grade) values(%s,%s,%s,%s,%s)",
                    (rNo, name, fname, sub, grade)
                )
                self.con.commit()
                messagebox.showinfo("Success", f"Student {name} with Roll_No.{rNo} is Registered!")
                self.close_current_frame()
                self.showAll()
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "Please Fill All Input Fields!")

    # --- SEARCH STUDENT ---
    def searchFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#96b4fa")
        self.currentFrame.place(width=450, height=270, x=400, y=140)

        tk.Label(self.currentFrame, text="Search By:", font=("arial", 15, "bold"), bg="#96b4fa").grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.option = ttk.Combobox(self.currentFrame, width=20, values=("rollNo", "name", "sub"), font=("Arial", 15, "bold"))
        self.option.set("Select Option")
        self.option.grid(row=0, column=1, padx=10, pady=15)

        tk.Label(self.currentFrame, text="Value:", font=("arial", 15, "bold"), bg="#96b4fa").grid(row=1, column=0, padx=20, pady=15, sticky="w")
        self.value = tk.Entry(self.currentFrame, width=22, font=("arial", 15, "bold"), bd=3)
        self.value.grid(row=1, column=1, padx=10, pady=15)

        tk.Button(self.currentFrame, text="Search", command=self.searchFun,
                  bd=3, relief="raised", font=("Arial", 20, "bold"), width=18).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.currentFrame, text="❌ Back", command=self.close_current_frame,
                  bd=3, relief="raised", font=("Arial", 15, "bold"), width=12, bg="red", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

    def searchFun(self):
        opt = self.option.get()
        val = self.value.get()
        if opt == "rollNo" and val.isdigit():
            rn = int(val)
            try:
                self.dbFun()
                self.cur.execute("select * from student where rollNo=%s", (rn,))
                row = self.cur.fetchone()
                self.table.delete(*self.table.get_children())
                if row:
                    self.table.insert('', tk.END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found!")
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        elif opt in ["name", "sub"]:
            try:
                self.dbFun()
                query = f"select * from student where {opt}=%s"
                self.cur.execute(query, (val,))
                data = self.cur.fetchall()
                self.table.delete(*self.table.get_children())
                if data:
                    for i in data:
                        self.table.insert('', tk.END, values=i)
                else:
                    messagebox.showinfo("Info", "No record found!")
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "Please select a valid Search Option!")

    # --- UPDATE STUDENT ---
    def updFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#96b4fa")
        self.currentFrame.place(width=450, height=280, x=400, y=140)

        tk.Label(self.currentFrame, text="Field:", font=("arial", 15, "bold"), bg="#96b4fa").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.option = ttk.Combobox(self.currentFrame, width=20, values=("name", "sub", "grade"), font=("Arial", 15, "bold"))
        self.option.set("Select Field")
        self.option.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.currentFrame, text="New Value:", font=("arial", 15, "bold"), bg="#96b4fa").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.value = tk.Entry(self.currentFrame, width=22, font=("arial", 15, "bold"), bd=3)
        self.value.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.currentFrame, text="Roll_No:", font=("arial", 15, "bold"), bg="#96b4fa").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.roll = tk.Entry(self.currentFrame, width=22, font=("arial", 15, "bold"), bd=3)
        self.roll.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.currentFrame, text="Update", command=self.updFun,
                  bd=3, relief="raised", font=("Arial", 20, "bold"), width=18).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.currentFrame, text="❌ Back", command=self.close_current_frame,
                  bd=3, relief="raised", font=("Arial", 15, "bold"), width=12, bg="red", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

    def updFun(self):
        opt = self.option.get()
        val = self.value.get()
        rNo = self.roll.get()
        if opt in ["name", "sub", "grade"] and rNo.isdigit():
            try:
                rn = int(rNo)
                self.dbFun()
                query = f"update student set {opt}=%s where rollNo=%s"
                self.cur.execute(query, (val, rn))
                self.con.commit()
                messagebox.showinfo("Success", f"Record updated for Roll_No.{rn}")
                self.close_current_frame()
                self.showAll()
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "All fields required!")

    # --- SHOW ALL ---
    def showAll(self):
        try:
            self.dbFun()
            self.cur.execute("select * from student")
            data = self.cur.fetchall()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('', tk.END, values=i)
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # --- DELETE STUDENT ---
    def delFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#96b4fa")
        self.currentFrame.place(width=450, height=220, x=400, y=140)

        tk.Label(self.currentFrame, text="Roll_No:", font=("arial", 15, "bold"), bg="#96b4fa").grid(row=0, column=0, padx=20, pady=25, sticky="w")
        self.rollNo = tk.Entry(self.currentFrame, width=22, font=("arial", 15, "bold"), bd=3)
        self.rollNo.grid(row=0, column=1, padx=10, pady=25)

        tk.Button(self.currentFrame, text="Delete", command=self.delFun,
                  bd=3, relief="raised", font=("Arial", 20, "bold"), width=18).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.currentFrame, text="❌ Back", command=self.close_current_frame,
                  bd=3, relief="raised", font=("Arial", 15, "bold"), width=12, bg="red", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    def delFun(self):
        rNo = self.rollNo.get()
        if rNo.isdigit():
            rn = int(rNo)
            try:
                self.dbFun()
                self.cur.execute("delete from student where rollNo=%s", (rn,))
                self.con.commit()
                messagebox.showinfo("Success", f"Student with Roll_No.{rn} is Removed")
                self.close_current_frame()
                self.showAll()
                self.con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "Enter valid Roll_No!")


# Run App
root = tk.Tk()
StudentApp(root)
root.mainloop()