import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox, PhotoImage
from tkinter.font import Font
import json
import os
from datetime import datetime
import webbrowser
import logging

# File to store tickets
TICKET_FILE = 'tickets.json'

class Ticket:
    def __init__(self, title, description, phone_number, creation_date=None, notes=None, is_open=True, status="open"):
        self.title = title
        self.description = description
        self.phone_number = phone_number
        self.notes = notes if notes is not None else []
        self.is_open = is_open
        self.status = status
        self.creation_date = creation_date or datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    
    def set_status(self, new_status):
        self.status = new_status

    def add_note(self, note):
        note_entry = {'note': note, 'timestamp': datetime.now().strftime('%m-d-%Y %H:%M:%S')}
        self.notes.append(note_entry)

    def close(self):
        self.is_open = False

    def __str__(self):
        notes_str = ''
        for note in self.notes:
            notes_str += 'Note ({}): {}\n        '.format(note['timestamp'], note['note'])
        status = "Open" if self.is_open else "Closed"
        
        # Display the title on the first line and the rest of the information on the next lines
        return f'[{status}] {self.creation_date} - {self.title} - {self.phone_number}\n    Description: {self.description}\n    Notes:\n    {notes_str if notes_str else "No notes"}\n'

def open_github():
    webbrowser.open('https://github.com/erfwerm')  # Open the GitHub page in a web browser
    logging.info("Github page for Erfwerm opened! Woo!")


def setup_logging():
    logging.basicConfig(filename='action_log.log', level=logging.INFO, 
                        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

setup_logging()

def show_about_this():
    about_window = tk.Toplevel(root)
    about_window.title("About this program")
    about_window.geometry("700x400")  

    image_path = "jayburgerssmall.png"  
    img = PhotoImage(file=image_path)
    img_label = tk.Label(about_window, image=img)
    img_label.image = img  
    img_label.pack(side="top", pady=10)

    about_text = """I created this program because I am learning Python.\nI also work in an office daily and decided I need  help organizing.\n\nI wrote most of the back end of this program.\nVersion 1 was all text based. Then I used AI to help learn GUI.\nFrom there I just went nuts and started to see what else it could teach me.\n"""
    about_label = tk.Label(about_window, text=about_text, justify=tk.LEFT)
    about_label.pack(side="top", padx=10, pady=10)


###### TICKET FUNCTIONS ######

def load_tickets():
    if not os.path.exists(TICKET_FILE):
        return []
    with open(TICKET_FILE, 'r') as file:
        tickets_data = json.load(file)
        if not tickets_data:
            return []
        loaded_tickets = []
        for data in tickets_data:
            ticket = Ticket(
                data['title'],
                data['description'],
                data['phone_number'],
                data['creation_date'],
                notes=data.get('notes', []),
                is_open=data['is_open'],
                status=data.get('status', 'open')  # Load the status, default to 'open' if not found
            )
            loaded_tickets.append(ticket)
            logging.info("Tickets Loaded successfully")
        return loaded_tickets
        

def save_tickets(tickets):
    logging.info("Tickets Saved successfully")
    with open(TICKET_FILE, 'w') as file:
        json.dump([{
            'title': ticket.title,
            'description': ticket.description,
            'phone_number': ticket.phone_number,
            'notes': ticket.notes,
            'is_open': ticket.is_open,
            'status': ticket.status,
            'creation_date': ticket.creation_date
        } for ticket in tickets], file)

    
def display_tickets(tickets, display_area):
    display_area.delete('1.0', tk.END)
    display_area.insert(tk.END, f'\n-------------- OPEN TICKETS ----------------\n')
    if not tickets or all(not ticket.is_open for ticket in tickets):
        display_area.insert(tk.END, 'No Open Tickets found\n')
        for index, ticket in enumerate(tickets):
            if not ticket.is_open:
                display_area.insert(tk.END, f'Ticket ID: {index} - {ticket}\n\n')
        return
    for index, ticket in enumerate(tickets):
        if ticket.is_open:
            display_area.insert(tk.END, f'Ticket ID: {index} - {ticket}\n\n')


def display_closed_tickets(tickets, display_area):
    display_area.delete('1.0', tk.END)
    display_area.insert(tk.END, f'\n-------------- CLOSED TICKETS ----------------\n')
    for index, ticket in enumerate(tickets):
        if not ticket.is_open:
            display_area.insert(tk.END, f'Ticket ID: {index} - {ticket}\n\n')


def update_ticket_title(tickets, display_area):
    ticket_id = simpledialog.askinteger("Update Title", "Enter ticket ID:", parent=root)
    if ticket_id is None or ticket_id < 0 or ticket_id >= len(tickets):
        messagebox.showwarning("Invalid Input", "Invalid ticket ID.")
        return

    new_title = simpledialog.askstring("Update Title", "Enter new title:", parent=root)
    if new_title:
        tickets[ticket_id].title = new_title
        logging.info(f"Ticket title updated {new_title}")
        save_tickets(tickets)
        display_all_tickets(tickets, display_area)
    else:
        messagebox.showinfo("Info", "Update cancelled or invalid title.")


def update_ticket_description(tickets, display_area):
    ticket_id = simpledialog.askinteger("Update Description", "Enter ticket ID:", parent=root)
    if ticket_id is None or ticket_id < 0 or ticket_id >= len(tickets):
        messagebox.showwarning("Invalid Input", "Invalid ticket ID.")
        return

    new_description = simpledialog.askstring("Update Description", "Enter new description:", parent=root)
    if new_description:
        tickets[ticket_id].description = new_description
        logging.info(f"Ticket description updated {new_description}")
        save_tickets(tickets)
        display_all_tickets(tickets, display_area)
    else:
        messagebox.showinfo("Info", "Update cancelled or invalid description.")


def update_ticket_phone(tickets, display_area):
    ticket_id = simpledialog.askinteger("Update Phone", "Enter ticket ID:", parent=root)
    if ticket_id is None or ticket_id < 0 or ticket_id >= len(tickets):
        messagebox.showwarning("Invalid Input", "Invalid ticket ID.")
        return

    new_phone = simpledialog.askstring("Update Phone", "Enter new phone (optional):", parent=root)
    if new_phone is not None:
        tickets[ticket_id].phone_number = new_phone
        logging.info(f"Ticket phone updated {new_phone}")
        save_tickets(tickets)
        display_all_tickets(tickets, display_area)
    else:
        messagebox.showinfo("Info", "Update cancelled.")


def display_all_tickets(tickets, display_area):
    display_area.delete('1.0', tk.END)

    # Sort tickets by creation date in descending order
    sorted_tickets = sorted(tickets, key=lambda ticket: datetime.strptime(ticket.creation_date, '%m-%d-%Y %H:%M:%S'), reverse=True)

    # Display Open Tickets
    display_area.insert(tk.END, f'\n-------------- OPEN TICKETS ----------------\n')
    open_tickets = [ticket for ticket in sorted_tickets if ticket.status == "open" and ticket.is_open]
    if not open_tickets:
        display_area.insert(tk.END, 'No Open Tickets found\n\n')
    for ticket in open_tickets:
        display_area.insert(tk.END, f'Ticket ID: {tickets.index(ticket)} - {ticket}\n\n')

    # Display Pending Tickets
    display_area.insert(tk.END, f'\n-------------- PENDING TICKETS ----------------\n')
    pending_tickets = [ticket for ticket in sorted_tickets if ticket.status == "pending"]
    if not pending_tickets:
        display_area.insert(tk.END, 'No Pending Tickets found\n\n')
    for ticket in pending_tickets:
        display_area.insert(tk.END, f'Ticket ID: {tickets.index(ticket)} - {ticket}\n\n')

    # Display Closed Tickets
    display_area.insert(tk.END, f'\n-------------- CLOSED TICKETS ----------------\n')
    closed_tickets = [ticket for ticket in sorted_tickets if not ticket.is_open]
    if not closed_tickets:
        display_area.insert(tk.END, 'No Closed Tickets found\n\n')
    for ticket in closed_tickets:
        display_area.insert(tk.END, f'Ticket ID: {tickets.index(ticket)} - {ticket}\n\n')


def create_ticket_form(tickets, display_area):
    form_window = tk.Toplevel(root)
    form_window.title("New Ticket")
    form_window.geometry("600x400")  # Adjust size as needed

    # Labels and Entry Widgets
    tk.Label(form_window, text="Title:").grid(row=0, column=0, sticky="nw")
    title_entry = tk.Entry(form_window, width=30)
    title_entry.grid(row=0, column=1)

    tk.Label(form_window, text="Phone Number:").grid(row=1, column=0, sticky="nw")
    phone_entry = tk.Entry(form_window, width=30)
    phone_entry.grid(row=1, column=1)

    tk.Label(form_window, text="Description:").grid(row=2, column=0, sticky="nw")
    description_text = tk.Text(form_window, width=60, height=20)
    description_text.grid(row=2, column=1)


    # Submit Button
    def submit_ticket():
        title = title_entry.get()
        description = description_text.get("1.0", tk.END).strip()  # Get text from description_text
        phone_number = phone_entry.get()
        if title and description:
            tickets.append(Ticket(title, description, phone_number))
            logging.info(f"Ticket Added {title}")
            save_tickets(tickets)
            display_all_tickets(tickets, display_area)
            form_window.destroy()
        else:
            messagebox.showwarning("Invalid Input", "Title and description cannot be empty.", parent=form_window)

    submit_button = tk.Button(form_window, text="Submit", command=submit_ticket)
    submit_button.grid(row=3, column=1, sticky="e")

def create_ticket_gui(tickets, display_area):
    create_ticket_form(tickets, display_area)


def set_ticket_to_pending(tickets, display_area):
    ticket_id = simpledialog.askinteger("Set to Pending", "Enter ticket ID:", parent=root)
    if ticket_id is not None and 0 <= ticket_id < len(tickets):
        tickets[ticket_id].set_status("pending")
        logging.info(f"Changed ticket to pending {ticket_id}")
        save_tickets(tickets)
        display_all_tickets(tickets, display_area)


def reopen_ticket_from_pending(tickets, display_area):
    ticket_id = simpledialog.askinteger("Reopen Ticket", "Enter ticket ID:", parent=root)
    if ticket_id is not None and 0 <= ticket_id < len(tickets):
        tickets[ticket_id].set_status("open")
        logging.info(f"Reopened ticket from pending {ticket_id}")
        save_tickets(tickets)
        display_all_tickets(tickets, display_area)


def add_note_to_ticket_gui(tickets, display_area):
    ticket_id = simpledialog.askinteger("Input", "Enter ticket ID:", parent=root)
    note = simpledialog.askstring("Input", "Enter note:", parent=root)
    display_area.focus_set()
    if ticket_id is not None and note:
        tickets[ticket_id].add_note(note)
        logging.info(f"Ticket updated {ticket_id} {note}")
        display_all_tickets(tickets, display_area)


def close_ticket_gui(tickets, display_area):
    ticket_id = simpledialog.askinteger("Input", "Enter ticket ID:", parent=root)
    if ticket_id is not None:
        if messagebox.askyesno("Confirm", "Are you sure you want to close this ticket?"):
            tickets[ticket_id].close()
            tickets[ticket_id].set_status("closed")  # Update the status to 'closed'
            logging.info(f"Ticket closed {ticket_id}")
            save_tickets(tickets)
            display_all_tickets(tickets, display_area)




def reopen_ticket_gui(tickets, display_area):
    ticket_id = simpledialog.askinteger("Input", "Enter ticket ID:", parent=root)
    display_area.focus_set()
    if ticket_id is not None and 0 <= ticket_id < len(tickets):
        ticket = tickets[ticket_id]
        if not ticket.is_open:
            ticket.is_open = True 
            logging.info(f"Ticket opened {ticket_id}")
            save_tickets(tickets)  
            display_all_tickets(tickets, display_area)
        else:
            messagebox.showinfo("Info", "This ticket is already open.")
    else:
        messagebox.showinfo("Info", "Invalid ticket ID.")

def create_toolbar(root, tickets, display_area):
    toolbar = ttk.Frame(root)
    new_button = ttk.Button(toolbar, text="New Ticket", command=lambda: create_ticket_gui(tickets, display_area))
    new_button.grid(row=0, column=0, padx=2, pady=2)
    update_button = ttk.Button(toolbar, text="Update Ticket", command=lambda: add_note_to_ticket_gui(tickets, display_area))
    update_button.grid(row=0, column=2, padx=2, pady=2)
    close_button = ttk.Button(toolbar, text="Close Ticket", command=lambda: close_ticket_gui(tickets, display_area))
    close_button.grid(row=0, column=4, padx=2, pady=2)
    save_button = ttk.Button(toolbar, text="Save", command=lambda: save_tickets(tickets))
    save_button.grid(row=0, column=6, padx=2, pady=2)
    refresh_button = ttk.Button(toolbar, text="Refresh", command=lambda: display_all_tickets(tickets, display_area))
    refresh_button.grid(row=0, column=8, padx=2, pady=2)
    toolbar.grid(row=0, column=0, sticky="ew")

def create_status_bar(root):
    status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
    status_bar.grid(row=2, column=0, sticky="ew")
    return status_bar

def update_status(status_bar, message):
    status_bar.config(text=message)

###### VIEW MODES ######

def set_sepia_mode(display_area):
    logging.info("Changed mode to sepia")
    display_area.config(bg='#f4ecd8', fg='#4e463f')

def set_pastel_mode(display_area):
    logging.info("Changed mode to pastel")
    display_area.config(bg='#ffefd5', fg='#a1c3d1')

def set_solarized_mode(display_area):
    logging.info("Changed mode to solarized")
    display_area.config(bg='#fdf6e3', fg='#657b83')

def set_high_contrast_mode(display_area):
    logging.info("Changed mode to high contrast")
    display_area.config(bg='#ffffff', fg='#000000')

def set_neon_mode(display_area):
    logging.info("Changed mode to neon")
    display_area.config(bg='#2c2c54', fg='#00ff00')

def set_bold_on(display_area):
    logging.info("Bold is now ON")
    display_area.config(weight='bold')

def set_bold_off(display_area):
    logging.info("Bold is now OFF")
    display_area.config(weight=' ')

def change_text_color(display_area, color):
    logging.info("Changing font color")
    display_area.config(fg=color)

def set_dark_mode(display_area):
    logging.info("Changed mode to dark mode")
    display_area.config(bg='black', fg='green')

def set_light_mode(display_area):
    logging.info("Changed mode to light mode")
    display_area.config(bg='white', fg='black')


###### SEARCH FUNCTIONS ######

def search_open_tickets(tickets, display_area):
    search_term = simpledialog.askstring("Search", "Enter ticket title to search for:", parent=root)
    if search_term:
        search_term = search_term.lower()
        logging.info(f"Searching for ticket : {search_term}")
        matching_tickets = [ticket for ticket in tickets if ticket.is_open and search_term in ticket.title.lower()]
        display_search_results(matching_tickets, display_area)


def search_open_tickets_by_description(tickets, display_area):
    search_term = simpledialog.askstring("Search", "Enter description to search for:", parent=root)
    if search_term:
        search_term = search_term.lower()
        logging.info(f"Searching for ticket : {search_term}")
        matching_tickets = [ticket for ticket in tickets if ticket.is_open and search_term in ticket.description.lower()]
        display_search_results(matching_tickets, display_area)


def search_open_tickets_by_phone(tickets, display_area):
    search_term = simpledialog.askstring("Search", "Enter phone number to search for:", parent=root)
    if search_term:
        search_term = search_term.lower()
        logging.info(f"Searching for ticket : {search_term}")
        matching_tickets = [ticket for ticket in tickets if ticket.is_open and search_term in ticket.phone_number.lower()]
        display_search_results(matching_tickets, display_area)


def display_search_results(tickets, display_area):
    display_area.delete('1.0', tk.END)
    if not tickets:
        display_area.insert(tk.END, 'No matching tickets found\n')
        return
    for index, ticket in enumerate(tickets):
        display_area.insert(tk.END, f'Ticket ID: {index} - {ticket}\n\n')

###### MENU ######

def create_menu(root, tickets, display_area):
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    ticket_menu = tk.Menu(menu_bar, tearoff=0)


    set_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Set", menu=set_menu)
    set_menu.add_command(label="Update Ticket", command=lambda: add_note_to_ticket_gui(tickets, display_area))
    set_menu.add_command(label="Close Ticket", command=lambda: close_ticket_gui(tickets, display_area))
    set_menu.add_command(label="Reopen Ticket", command=lambda: reopen_ticket_gui(tickets, display_area))
    set_menu.add_separator()
    set_menu.add_command(label="Set Ticket to Pending", command=lambda: set_ticket_to_pending(tickets, display_area))
    set_menu.add_command(label="Reopen Pending Ticket", command=lambda: reopen_ticket_from_pending(tickets, display_area))
    set_menu.add_separator()
    set_menu.add_command(label="Edit Title", command=lambda: update_ticket_title(tickets, display_area))
    set_menu.add_command(label="Edit Description", command=lambda: update_ticket_description(tickets, display_area))
    set_menu.add_command(label="Edit Phone Number", command=lambda: update_ticket_phone(tickets, display_area))

    search_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Search", menu=search_menu)
    search_menu.add_command(label="Search by title", command=lambda: search_open_tickets(tickets, display_area))
    search_menu.add_command(label="Search by phone", command=lambda: search_open_tickets_by_phone(tickets, display_area))
    search_menu.add_command(label="Search by description", command=lambda: search_open_tickets_by_description(tickets, display_area))

    menu_bar.add_cascade(label="Show", menu=ticket_menu)
    ticket_menu.add_command(label="Show Open Tickets", command=lambda: display_tickets(tickets, display_area))
    ticket_menu.add_command(label="Show Closed Tickets", command=lambda: display_closed_tickets(tickets, display_area))
    ticket_menu.add_command(label="Show ALL Tickets", command=lambda: display_all_tickets(tickets, display_area))
  
    mode_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Mode", menu=mode_menu)
    mode_menu.add_command(label="Dark Mode", command=lambda: set_dark_mode(display_area))
    mode_menu.add_command(label="Light Mode", command=lambda: set_light_mode(display_area))
    mode_menu.add_command(label="Sepia Mode", command=lambda: set_sepia_mode(display_area))
    mode_menu.add_command(label="Pastel Mode", command=lambda: set_pastel_mode(display_area))
    mode_menu.add_command(label="Neon Mode", command=lambda: set_neon_mode(display_area))
    mode_menu.add_command(label="Solarized Mode", command=lambda: set_solarized_mode(display_area))
    mode_menu.add_command(label="High Contrast Mode", command=lambda: set_high_contrast_mode(display_area))

    settings_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Toggle Bold Font", command=lambda: toggle_bold_font(display_area))
    settings_menu.add_command(label="Increase Font Size", command=lambda: increase_font_size(display_area))
    settings_menu.add_command(label="Decrease Font Size", command=lambda: decrease_font_size(display_area))
    settings_menu.add_command(label="Align Text Left", command=lambda: align_text_left(display_area))
    settings_menu.add_command(label="Align Text Center", command=lambda: align_text_center(display_area))
    settings_menu.add_command(label="Align Text Right", command=lambda: align_text_right(display_area))
    settings_menu.add_separator()
    settings_menu.add_command(label="Text Color", command=lambda: change_text_color(display_area, color= simpledialog.askstring("Input", "Font color : ", parent=root)))
    settings_menu.add_separator()
    settings_menu.add_command(label="Reset to Default", command=lambda: reset_default_settings(display_area))

    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="GitHub Page", command=open_github)
    help_menu.add_command(label="About This Program", command=show_about_this)

    menu_bar.add_command(label="View Log", command=view_log)


###### FONT SETTINGS ######

def increase_font_size(display_area):
    global larger_font
    size = larger_font.actual()["size"] + 2
    logging.info(f"Changing font size to : {size}")
    larger_font.config(size=size)
    display_area.config(font=larger_font)


def decrease_font_size(display_area):
    global larger_font
    size = max(larger_font.actual()["size"] - 2, 8) 
    logging.info(f"Changing font size to : {size}")
    larger_font.config(size=size)
    display_area.config(font=larger_font)


def align_text_left(display_area):
    logging.info("Aligning text to the left")
    display_area.tag_configure("left", justify='left')
    display_area.tag_add("left", "1.0", "end")


def align_text_center(display_area):
    logging.info("Aligning text to the center")
    display_area.tag_configure("center", justify='center')
    display_area.tag_add("center", "1.0", "end")


def align_text_right(display_area):
    logging.info("Aligning text to the right")
    display_area.tag_configure("right", justify='right')
    display_area.tag_add("right", "1.0", "end")


def reset_default_settings(display_area):
    global larger_font
    logging.info("Resetting all settings")
    larger_font.config(family="Helvetica", size=12, weight="normal")
    display_area.config(font=larger_font, bg='black', fg='green')
    align_text_left(display_area)


def toggle_bold_font(display_area):
    global larger_font
    new_weight = "bold" if larger_font.actual()["weight"] == "normal" else "normal"
    larger_font.config(weight=new_weight)
    display_area.config(font=larger_font)


def center_window(root, width=800, height=600):
    '''This function centers the program window on the screen'''
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

def view_log():
    log_window = tk.Toplevel(root)
    log_window.title("Action Log")
    log_window.geometry("600x400")

    text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD)
    text_area.pack(expand=True, fill=tk.BOTH)

    def clear_log():
        open('action_log.log', 'w').close()
        text_area.delete('1.0', tk.END)

    with open('action_log.log', 'r') as file:
        log_content = file.read()
        text_area.insert(tk.END, log_content)

    clear_button = tk.Button(log_window, text="Clear Log", command=clear_log)
    clear_button.pack()

###### Main Program ######

# Create the main window
root = tk.Tk()
root.title("Ticket System")

# Define custom fonts
heading_font = Font(family="Arial", size=16, weight="bold")
body_font = Font(family="Arial", size=12)
larger_font = Font(family="Helvetica", size=12, weight="normal")  # Define larger_font


# Configure the grid
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frames for better layout
top_frame = ttk.Frame(root)
top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

bottom_frame = ttk.Frame(root)
bottom_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

# Create a scrolled text widget for the main display area
main_display = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, font=body_font)
main_display.pack(expand=True, fill=tk.BOTH)

# Load tickets
tickets = load_tickets()

# Create the toolbar and status bar
create_toolbar(root, tickets, main_display)
create_menu(root, tickets, main_display)
status_bar = create_status_bar(root)

# Display all tickets and update status
display_all_tickets(tickets, main_display)
update_status(status_bar, "Loaded tickets successfully")

# Center the window and start loop
center_window(root, 800, 600)
root.mainloop()

# Save tickets on close
save_tickets(tickets)

