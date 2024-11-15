import mysql.connector
from tkinter import *
from tkinter import messagebox

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="piyush",
        database="feedback_db"
    )

'''CREATE DATABASE feedback_db;
USE feedback_db;

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(255),
    feedback TEXT
);'''

# Add feedback to the database
def add_feedback():
    student_id = entry_student_id.get()
    feedback = entry_feedback.get("1.0", END)

    if student_id and feedback.strip():
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO feedback (student_id, feedback) VALUES (%s, %s)", (student_id, feedback))
        db.commit()
        cursor.close()
        db.close()

        entry_student_id.delete(0, END)
        entry_feedback.delete("1.0", END)
        messagebox.showinfo("Success", "Feedback added successfully!")
    else:
        messagebox.showwarning("Input Error", "Please enter Student ID and Feedback.")

# View feedback for a student
def view_feedback():
    student_id = entry_student_id.get()
    if student_id:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT feedback FROM feedback WHERE student_id = %s", (student_id,))
        feedbacks = cursor.fetchall()
        cursor.close()
        db.close()

        listbox_feedback.delete(0, END)
        if feedbacks:
            for i, feedback in enumerate(feedbacks, 1):
                listbox_feedback.insert(END, f"{i}. {feedback[0]}")
        else:
            listbox_feedback.insert(END, "No feedback found.")
    else:
        messagebox.showwarning("Input Error", "Please enter a Student ID to view feedback.")

# Update feedback
def update_feedback():
    student_id = entry_student_id.get()
    selected_index = listbox_feedback.curselection()
    if student_id and selected_index:
        feedback_id = selected_index[0] + 1
        new_feedback = entry_feedback.get("1.0", END)

        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("UPDATE feedback SET feedback = %s WHERE student_id = %s AND id = %s", (new_feedback, student_id, feedback_id))
        db.commit()
        cursor.close()
        db.close()

        messagebox.showinfo("Success", "Feedback updated successfully!")
    else:
        messagebox.showwarning("Selection Error", "Select a feedback to update.")

# Delete feedback
def delete_feedback():
    student_id = entry_student_id.get()
    selected_index = listbox_feedback.curselection()
    if student_id and selected_index:
        feedback_id = selected_index[0] + 1

        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM feedback WHERE student_id = %s AND id = %s", (student_id, feedback_id))
        db.commit()
        cursor.close()
        db.close()

        listbox_feedback.delete(selected_index)
        messagebox.showinfo("Success", "Feedback deleted successfully!")
    else:
        messagebox.showwarning("Selection Error", "Select a feedback to delete.")

# Initialize GUI
root = Tk()
root.title("Student Feedback System")
root.geometry("400x400")

# Student ID Entry
Label(root, text="Student ID:").pack()
entry_student_id = Entry(root)
entry_student_id.pack()

# Feedback Entry
Label(root, text="Feedback:").pack()
entry_feedback = Text(root, height=5, width=30)
entry_feedback.pack()

# Buttons
Button(root, text="Add Feedback", command=add_feedback).pack(pady=5)
Button(root, text="View Feedback", command=view_feedback).pack(pady=5)
Button(root, text="Update Feedback", command=update_feedback).pack(pady=5)
Button(root, text="Delete Feedback", command=delete_feedback).pack(pady=5)

# Feedback Listbox
Label(root, text="Feedbacks:").pack()
listbox_feedback = Listbox(root, width=50)
listbox_feedback.pack()

root.mainloop()
