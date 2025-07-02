# Python script to automate file management tasks such as organizing files into directories based on their extensions, renaming files, and deleting old files.
import os
import shutil


# Define the path to your download directory
downloads_folder = r"C:\\Users\\Unity\\Downloads"


# Define target folders for different file types
folders = {
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    'documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'videos': ['.mp4', '.avi', '.mov'],
    'audio': ['.mp3', '.wav', '.flac'],
    'archives': ['.zip', '.rar', '.tar'],
    'scripts': ['.py', '.sh', '.js'],
    'installers': ['.exe', '.msi'],
    'others': []
}

# Create target folders if they don't exist
for folder in folders:
    folder_path = os.path.join(downloads_folder, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# Loop through files in the downloads folder
for filename in os.listdir(downloads_folder):
    file_path = os.path.join(downloads_folder, filename)

    # Skip directories
    if os.path.isdir(file_path):
        continue

    # Get file extension
    file_extension = os.path.splitext(filename)[1].lower()
    
    # Check file extension and move to the appropriate folder
    moved = False
    for folder, extensions in folders.items():
        if file_extension in extensions:
            target_folder = os.path.join(downloads_folder, folder)
            target_path = os.path.join(target_folder, filename)
            
            try:
                # Avoid overwriting existing files
                if os.path.exists(target_path):
                    print(f'File {filename} already exists in {folder} folder')
                else:
                    shutil.move(file_path, target_path)
                    print(f'Moved {filename} to {folder} folder')
                moved = True
                break
            except Exception as e:
                print(f'Error moving {filename}: {e}')
    
    # Move unrecognized files to 'others' folder
    if not moved and file_extension:
        others_folder = os.path.join(downloads_folder, 'others')
        target_path = os.path.join(others_folder, filename)
        try:
            if os.path.exists(target_path):
                print(f'File {filename} already exists in others folder')
            else:
                shutil.move(file_path, target_path)
                print(f'Moved {filename} to others folder')
        except Exception as e:
            print(f'Error moving {filename}: {e}')

print("File organization completed!")