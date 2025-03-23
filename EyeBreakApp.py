import tkinter as tk
import random
from plyer import notification

EYEWORKTIME = 20 * 60 # 20 minutes in seconds
EYEBREAKTIME = 20 # 20 seconds

class EyeBreakApp:
    """ A simple GUI application to remind users to take breaks for their eyes.
    It allows users to set a timer for work and break intervals, and provides a list of tasks to perform during breaks.
    based on the practice of every 20 minutes of work, take a 20-second break and look at something 20 feet away.
    It also allows users to suggest other tasks to do during breaks.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Break Reminder")
        self.root.geometry("400x400")
        self.running = False
        self.time_remaining = EYEWORKTIME 
        self.break_duration = EYEBREAKTIME
        
        # future updates could include connecting this to a database or file to save tasks
        self.tasks = ["Stretch", "Jumping Jacks", "Drink Water", "Clean Desk"]

        # UI Components
        self.label = tk.Label(root, text=self.format_time(self.time_remaining), font=("Helvetica", 48))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.pack()

        self.task_listbox = tk.Listbox(root, height=5)
        self.task_listbox.pack()

        self.load_tasks()

        self.task_entry = tk.Entry(root)
        self.task_entry.pack()

        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.remove_task_button = tk.Button(root, text="Remove Selected Tasks", command=self.remove_task)
        self.remove_task_button.pack()

    def format_time(self, seconds):
        minutes, sec = divmod(seconds, 60)
        return f"{minutes:02}:{sec:02}"

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)
    
    def add_task(self):
        task = self.task_entry.get() 
        if task: 
            self.tasks.append(task)
            self.load_tasks()
            self.task_entry.delete(0, tk.END)
    
    def remove_task(self):
        selected = self.task_listbox.curselection()
        if selected: 
            self.tasks.pop(selected[0])
            self.load_tasks()
    
    def start_timer(self):
        if not self.running:
            self.running = True
            self.countdown()
    def stop_timer(self):
        self.running = False
    
    def countdown(self):
        if self.running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.label.config(text=self.format_time(self.time_remaining))
            self.root.after(1000, self.countdown)
        elif self.running: 
            self.notify_break()
            self.time_remaining = self.break_duration
            self.break_countdown()
        
    def break_countdown(self):
        if self.time_remaining > 0: 
            self.label.config(text=f"Break: {self.format_time(self.time_remaining)}")
            self.time_remaining -= 1
            self.root.after(1000, self.break_countdown)
        else:
            self.time_remaining = EYEWORKTIME 
            self.countdown()
    def notify_break(self):
        task = random.choice(self.tasks)
        notification.notify(
            title="Eye Break Reminder",
            message=f"Time to {task}!",
            timeout=10
        )
        self.label.config(text=f"Break: {task}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EyeBreakApp(root)
    root.mainloop()
