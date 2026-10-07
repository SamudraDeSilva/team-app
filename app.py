# %%
import os
import re
import time
from datetime import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from streamlit_gsheets import GSheetsConnection

# %%
import os
import re
import time
from datetime import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from streamlit_gsheets import GSheetsConnection

# --- CONFIGURATION ---
TEAM_STRUCTURE = {
    "TDU": ["Gang 1", "Gang 3", "Gang 4", "Gang 7", "Gang 19"],
    "LEW": ["LEG 1", "LEG 2"],
    "Lot B1": ["LEW CM & CS", "TDU"],
    "BT": ["Team 5", "Team 6", "Team 7", "Team 8"],
    "Drivers": ["Drivers"],
    "Assitive Operations": ["Burning Assisting - Team 2", "Ultrasonic Maintenance (Lillie Bridge)", "Ultrasonic Maintenance (Edgeweare)"],
    "AO - District Line": ["P&C Team 1", "P&C Team 2", "Re-Rail Team 3", "SS Faults Team"],
    "AO - Jubilee Line": ["Re-Rail Team 3", "SS Faults Team"],
    "AO - Nothern Line": ["Core P&C Team 1", "Core P&C Team 2", "Core Re-Rail Team 2", "SS Faults Team", "T002 L1 & L2", "Core Track Quality Team 1", "Core Track Quality Team 2"],
    "AO - Picadaly Line": ["Core P&C Team", "Re-Rail Team", "Block Joints Team", "Safety Standards Team", "Core Track Quality Team", "Core Track Quality Team 1", "Upgrade Team"],
    "Life Extension": ["Team 4", "Team 6"]
}

# Web page configuration optimized for mobile screens
st.set_page_config(page_title="Team Update Portal", page_icon="📝", layout="centered")

st.title("📝 Public Team Update Portal")
st.markdown("Anyone with this link can submit their daily metrics.")
st.markdown("---")

# 1. Establish the cloud database connection safely
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.warning("⚠️ Cloud database connection is setting up. Please ensure your configuration file is present.")

# 2. Team Selections Dropdowns
main_team = st.selectbox("Select Main Team:", list(TEAM_STRUCTURE.keys()))
sub_teams = TEAM_STRUCTURE.get(main_team, [])
sub_team = st.selectbox("Select Sub-Team:", sub_teams)

st.markdown("### Select & Log Metrics (Choose at least one)")

# 3. Checkboxes & Inputs Layout
col1, col2 = st.columns(2)

with col1:
    use_t002 = st.checkbox("T002")
    use_pwt = st.checkbox("PWT")
    use_spl = st.checkbox("SPL")
    use_drivers = st.checkbox("Drivers")

with col2:
    t002_val = st.text_input("T002 Count:", value="0", disabled=not use_t002, key="t002")
    pwt_val = st.text_input("PWT Count:", value="0", disabled=not use_pwt, key="pwt")
    spl_val = st.text_input("SPL Count:", value="0", disabled=not use_spl, key="spl")
    drivers_val = st.text_input("Drivers Count:", value="0", disabled=not use_drivers, key="drivers")

st.markdown("---")

# 4. Text & Submitter Input
update_text = st.text_area("Enter EOD Update:", placeholder="Type your core update points here...")
name_input = st.text_input("Your Name:")

# 5. Submission Engine
if st.button("Submit Details", type="primary", use_container_width=True):
    # Validation checks
    if not use_t002 and not use_pwt and not use_spl and not use_drivers:
        st.error("⚠️ Validation Error: You must check and log at least one metric!")
    elif not update_text or not name_input:
        st.error("⚠️ Error: All main fields (Update Text and Your Name) are required!")
    else:
        # Validate numbers
        metrics = [("T002", use_t002, t002_val), ("PWT", use_pwt, pwt_val), ("SPL", use_spl, spl_val), ("Drivers", use_drivers, drivers_val)]
        valid = True
        
        for name, checked, val in metrics:
            if checked and (not val.strip() or not val.strip().isdigit()):
                st.error(f"⚠️ Validation Error: The value for {name} must be a valid number!")
                valid = False
                break
                
        if valid:
            try:
                # Fetch current spreadsheet data from the cloud
                existing_data = conn.read(worksheet="Sheet1", ttl="0d")
                df = pd.DataFrame(existing_data)
            except Exception:
                # If sheet is empty, initialize columns
                df = pd.DataFrame(columns=["Date", "Time", "Main Team", "Sub Team", "Update Text", "T002", "PWT", "SPL", "Drivers", "Submitted By"])

            # Create the entry row
            new_row = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Main Team": main_team,
                "Sub Team": sub_team,
                "Update Text": update_text.strip(),
                "T002": int(t002_val) if use_t002 else 0,
                "PWT": int(pwt_val) if use_pwt else 0,
                "SPL": int(spl_val) if use_spl else 0,
                "Drivers": int(drivers_val) if use_drivers else 0,
                "Submitted By": name_input.strip()
            }
            
            # Append and update the cloud spreadsheet database
            updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.success("🎉 Data successfully submitted online! You can close this page.")


# %%
# --- CONFIGURATION ---
EXCEL_FILE_PATH = r"C:\Users\SamudraDeSilva\Downloads\Application\team_daily_updates.xlsx"

TEAM_STRUCTURE = {
    "TDU": ["Gang 1", "Gang 3", "Gang 4", "Gang 7", "Gang 19"],
    "LEW": ["LEG 1", "LEG 2"],
    "Lot B1": ["LEW CM & CS", "TDU"],
    "BT": ["Team 5", "Team 6", "Team 7", "Team 8"],
    "Drivers": ["Drivers"],
    "Assitive Operations": ["Burning Assisting - Team 2", "Ultrasonic Maintenance (Lillie Bridge)", "Ultrasonic Maintenance (Edgeweare)"],
    "AO - District Line": ["P&C Team 1", "P&C Team 2", "Re-Rail Team 3", "SS Faults Team"],
    "AO - Jubilee Line": ["Re-Rail Team 3", "SS Faults Team"],
    "AO - Nothern Line": ["Core P&C Team 1", "Core P&C Team 2", "Core Re-Rail Team 2", "SS Faults Team", "T002 L1 & L2", "Core Track Quality Team 1", "Core Track Quality Team 2"],
    "AO - Picadaly Line": ["Core P&C Team", "Re-Rail Team", "Block Joints Team", "Safety Standards Team", "Core Track Quality Team", "Core Track Quality Team 1", "Upgrade Team"],
    "Life Extension": ["Team 4", "Team 6"]
}

def update_sub_teams(event):
    selected_main = team_combo.get()
    sub_teams = TEAM_STRUCTURE.get(selected_main, [])
    sub_team_combo['values'] = sub_teams
    sub_team_combo.set('') 

def toggle_entry(chk_var, entry_widget):
    if chk_var.get() == 1:
        entry_widget.config(state="normal")
    else:
        entry_widget.delete(0, tk.END)
        entry_widget.config(state="disabled")

def submit_data():
    team = team_combo.get()
    sub_team = sub_team_combo.get()
    update = update_text.get("1.0", tk.END).strip()
    name = name_entry.get().strip()
    
    # Check if at least one metric checkbox is selected
    if t002_var.get() == 0 and pwt_var.get() == 0 and spl_var.get() == 0 and drv_var.get() == 0:
        messagebox.showerror("Validation Error", "You must select and log at least one metric (T002, PWT, SPL or Drivers)!")
        return

    # Extract numerical values and validate inputs
    t002_val = t002_entry.get().strip() if t002_var.get() == 1 else "0"
    pwt_val = pwt_entry.get().strip() if pwt_var.get() == 1 else "0"
    spl_val = spl_entry.get().strip() if spl_var.get() == 1 else "0"
    drv_val = drv_entry.get().strip() if drv_var.get() == 1 else "0"
    
    # Ensure selected fields are not empty and contain valid digits
    for label, check, val in [("T002", t002_var, t002_val), ("PWT", pwt_var, pwt_val), ("SPL", spl_var, spl_val), ("Drivers", drv_var, drv_val)]:
        if check.get() == 1:
            if not val:
                messagebox.showerror("Validation Error", f"Please enter a number for the selected metric: {label}")
                return
            if not val.isdigit():
                messagebox.showerror("Validation Error", f"The value for {label} must be a valid number!")
                return
                
    if not team or not sub_team or not update or not name:
        messagebox.showerror("Error", "All main fields (Teams, Update, Name) are required!")
        return
        
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Main Team": team,
        "Sub Team": sub_team,
        "Update Text": update,
        "T002 Count": int(t002_val),
        "PWT Count": int(pwt_val),
        "SPL Count": int(spl_val),
        "Driver Count": int(drv_val),
        "Submitted By": name
    }
    
    new_df = pd.DataFrame([new_row])
    
    try:
        if os.path.exists(EXCEL_FILE_PATH):
            existing_df = pd.read_excel(EXCEL_FILE_PATH)
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            updated_df = new_df
            
        updated_df.to_excel(EXCEL_FILE_PATH, index=False)
        
        # Reset input widgets for next log
        update_text.delete("1.0", tk.END)
        name_entry.delete(0, tk.END)
        
        t002_var.set(0)
        pwt_var.set(0)
        spl_var.set(0)
        drv_var.set(0)
        toggle_entry(t002_var, t002_entry)
        toggle_entry(pwt_var, pwt_entry)
        toggle_entry(spl_var, spl_entry)
        toggle_entry(drv_var, drv_entry)
        
        messagebox.showinfo("Success", "Update and mandatory metrics saved successfully!")
        
    except PermissionError:
        messagebox.showerror("Error", "Cannot update file! Please close your Excel sheet first.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# --- SAFE GUI WINDOW SETUP FOR JUPYTER ---
if 'root' in globals():
    try:
        if root.winfo_exists():
            root.destroy()
    except Exception:
        pass

root = tk.Tk()
root.title("Team Update Portal")
root.geometry("420x650")

root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

# 1. Main Team & Sub Team Dropdowns
tk.Label(root, text="Select Main Team:", font=("Arial", 10, "bold")).pack(pady=4)
team_combo = ttk.Combobox(root, values=list(TEAM_STRUCTURE.keys()), state="readonly", width=35)
team_combo.pack(pady=3)
team_combo.bind("<<ComboboxSelected>>", update_sub_teams)

tk.Label(root, text="Select Sub-Team:", font=("Arial", 10, "bold")).pack(pady=4)
sub_team_combo = ttk.Combobox(root, values=[], state="readonly", width=35)
sub_team_combo.pack(pady=3)

# 2. MANDATORY Metric Checkboxes + Entries Area
tk.Label(root, text="Select and Log Metrics:", font=("Arial", 10, "bold")).pack(pady=10)

metric_frame = tk.Frame(root)
metric_frame.pack(pady=5)

# T002 Row
t002_var = tk.IntVar()
t002_chk = tk.Checkbutton(metric_frame, text="T002 *", variable=t002_var, font=("Arial", 10, "bold"), command=lambda: toggle_entry(t002_var, t002_entry))
t002_chk.grid(row=0, column=0, sticky="w", padx=10, pady=4)
t002_entry = tk.Entry(metric_frame, width=15, state="disabled")
t002_entry.grid(row=0, column=1, padx=10, pady=4)

# PWT Row
pwt_var = tk.IntVar()
pwt_chk = tk.Checkbutton(metric_frame, text="PWT *", variable=pwt_var, font=("Arial", 10, "bold"), command=lambda: toggle_entry(pwt_var, pwt_entry))
pwt_chk.grid(row=1, column=0, sticky="w", padx=10, pady=4)
pwt_entry = tk.Entry(metric_frame, width=15, state="disabled")
pwt_entry.grid(row=1, column=1, padx=10, pady=4)

# SPL Row
spl_var = tk.IntVar()
spl_chk = tk.Checkbutton(metric_frame, text="SPL *", variable=spl_var, font=("Arial", 10, "bold"), command=lambda: toggle_entry(spl_var, spl_entry))
spl_chk.grid(row=2, column=0, sticky="w", padx=10, pady=4)
spl_entry = tk.Entry(metric_frame, width=15, state="disabled")
spl_entry.grid(row=2, column=1, padx=10, pady=4)

# DRV Row
drv_var = tk.IntVar()
drv_chk = tk.Checkbutton(metric_frame, text="Driver *", variable=drv_var, font=("Arial", 10, "bold"), command=lambda: toggle_entry(drv_var, drv_entry))
drv_chk.grid(row=3, column=0, sticky="w", padx=10, pady=4)
drv_entry = tk.Entry(metric_frame, width=15, state="disabled")
drv_entry.grid(row=3, column=1, padx=10, pady=4)

# 3. Update Text Box
tk.Label(root, text="Enter EOD Update:", font=("Arial", 10, "bold")).pack(pady=5)
update_text = tk.Text(root, height=6, width=40)
update_text.pack(pady=3)

# 4. Name Input
tk.Label(root, text="Your Name:", font=("Arial", 10, "bold")).pack(pady=5)
name_entry = tk.Entry(root, width=35)
name_entry.pack(pady=3)

# 5. Submit Button
submit_btn = tk.Button(root, text="Submit to Excel", command=submit_data, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=25)
submit_btn.pack(pady=15)

root.mainloop()



