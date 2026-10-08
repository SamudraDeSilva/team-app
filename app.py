# %%
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- CONFIGURATION ---

EXCEL_FILE_PATH = r"C:\Users\SamudraDeSilva\Downloads\Application\team_daily_updates.xlsx"

TEAM_STRUCTURE = {
    "Dev Team": ["dev 1", "dev 2"],
    "Team Alpha": ["ap 1", "ap 2"],
    "Marketing Sync": ["mkt 1", "mkt 2"],
    "Operations": ["ops 1", "ops 2"],
    "Sales": ["sales 1", "sales 2"]
}

# Web page configuration optimized for desktop and mobile screens
st.set_page_config(page_title="Local Team Update Portal", page_icon="📝", layout="centered")

st.title("📝 Local Team Update Portal")
st.markdown("This portal runs locally and saves records directly to your C: drive.")
st.markdown("---")

# 1. Team Selections Dropdowns
main_team = st.selectbox("Select Main Team:", list(TEAM_STRUCTURE.keys()))
sub_teams = TEAM_STRUCTURE.get(main_team, [])
sub_team = st.selectbox("Select Sub-Team:", sub_teams)

st.markdown("### Select & Log Metrics (Choose at least one)")

# 2. Checkboxes & Inputs Layout
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

# 3. Text & Submitter Input
update_text = st.text_area("Enter EOD Update:", placeholder="Type your core update points here...")
name_input = st.text_input("Your Name:")

# 4. Local Submission Engine
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
            
            new_df = pd.DataFrame([new_row])
            
            try:
                # Appending directly to your hard drive file
                if os.path.exists(EXCEL_FILE_PATH):
                    existing_df = pd.read_excel(EXCEL_FILE_PATH)
                    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                else:
                    updated_df = new_df
                    
                updated_df.to_excel(EXCEL_FILE_PATH, index=False)
                st.success(f"🎉 Success! Row saved directly onto your computer at: {EXCEL_FILE_PATH}")
                
            except PermissionError:
                st.error("🔒 File Lock Error: Please close your Excel sheet so this application can save data to it.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
Use code with caution.

Step 2: How to Launch the App Locally

Close your browser tabs for GitHub and Streamlit Cloud—you do not need them anymore.
1. Open your terminal or command prompt window.
2. Navigate to your application folder:cmd
cd C:\Users\SamudraDeSilva\Downloads\Application
Use code with caution.
3. Launch the web app using Streamlit:cmd
streamlit run app.py
Use code with caution.

Step 3: Sharing the Link with Your Team

When you run that command, look at your terminal screen. It will display two URLs:
• Local URL: http://localhost:8501 (This is for your eyes only on your computer).
• Network URL: http://192.168.X.X:8501 (This is your local web app link).
To let anyone add details: Copy that Network URL and send it to your team or drop it in your WhatsApp groups. As long as your computer stays turned on and your teammates are connected to the same company office Wi-Fi/network router, clicking that link will open your web form on their devices, and hitting submit will save the data rows straight into your desktop Excel file.
Did launching the script using streamlit run app.py generate the Network URL in your terminal successfully?
AI responses may include mistakes. Learn more

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
            
