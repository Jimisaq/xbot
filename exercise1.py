# Simple Backup Script: Backs up files modified in the last 3 minutes

import os      # For file system operations (checking if files/folders exist)
import shutil  # For copying files
import time    # For getting current time and file modification times


source_folder = r"C:\Users\Unity\Desktop\Source"  # Folder to monitor for changes
backup_folder = r"C:\Users\Unity\Desktop\Backup"     # Where backup copies will be stored

print(f"Monitoring: {source_folder}")
print(f"Backing up to: {backup_folder}")

# Step 2: Create the backup folder if it doesn't exist yet
if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)
    print("Created backup folder")

# Function to backup recently modified files
def backup_recent_files():
    # Get current time in seconds since 1970 (Unix timestamp)
    current_time = time.time()
    
    # Calculate what time it was 3 minutes ago (180 seconds)
    three_minutes_ago = current_time - 180
    
    print("\nChecking for recently modified files...")
    files_backed_up = 0
    
    # Step 4: Look at each file in the source folder
    for filename in os.listdir(source_folder):
        # Build the full path to the file
        file_path = os.path.join(source_folder, filename)
        
        # Skip folders
        if os.path.isdir(file_path):
            continue
            
        # Get when this file was last modified
        file_modified_time = os.path.getmtime(file_path)
        
        # Check if the file was modified in the last 3 minutes
        if file_modified_time > three_minutes_ago:
            # Create the path where we'll save the backup copy
            backup_path = os.path.join(backup_folder, filename)
            
            try:
                # Copy the file (shutil.copy2 preserves file timestamps)
                shutil.copy2(file_path, backup_path)
                print(f"✓ Backed up: {filename}")
                files_backed_up += 1
                
            except Exception as error:
                print(f"✗ Failed to backup {filename}: {error}")
    
    # Show summary
    if files_backed_up == 0:
        print("No recently modified files found")
    else:
        print(f"Successfully backed up {files_backed_up} file(s)")

# Step 5: Run the backup once when script starts
print("Starting initial backup check...")
backup_recent_files()

# Step 6: Keep running the backup check every 3 minutes
print("\nScript will now check for new files every 3 minutes...")
print("Press Ctrl+C to stop")

try:
    while True:
        time.sleep(180)  # Wait 3 minutes (180 seconds)
        backup_recent_files()
        
except KeyboardInterrupt:
    print("\nBackup monitoring stopped by user")