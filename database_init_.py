import sqlite3
import os
import shutil

#Add ISL to Data folder
downloads_path = "../Downloads/Indian"
destination_path = "./data/ISL_ML"

# Get a list of files in the downloads folder
files = os.listdir(downloads_path)

# Loop through each file in the downloads folder
for file in files:
    # Get the full path of the file
    file_path = os.path.join(downloads_path, file)
    # Check if the file is a directory
    if os.path.isdir(file_path):
        # If it is a directory, copy the entire directory to the destination folder
        shutil.copytree(file_path, os.path.join(destination_path, file))
    else:
        # If it is a file, copy the file to the destination folder
        shutil.copy(file_path, os.path.join(destination_path, file))

#Add SSL to Data folder
downloads_path = "../Downloads/Spanish"
destination_path = "./data/SSL_ML"

# Get a list of files in the downloads folder
files = os.listdir(downloads_path)

# Loop through each file in the downloads folder
for file in files:
    # Get the full path of the file
    file_path = os.path.join(downloads_path, file)
    # Check if the file is a directory
    if os.path.isdir(file_path):
        # If it is a directory, copy the entire directory to the destination folder
        shutil.copytree(file_path, os.path.join(destination_path, file))
    else:
        # If it is a file, copy the file to the destination folder
        shutil.copy(file_path, os.path.join(destination_path, file))


source_dir = "./data/ISL_ML"
dest_dir = "./data/ISL"
count = 1
for dirpath, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".JPG"):
            source_path = os.path.join(dirpath, filename)
            dirname = os.path.basename(os.path.normpath(dirpath))
            new_filename = f"{dirname}_{filename.replace(filename, str(count).zfill(3))}.jpeg"
            dest_path = os.path.join(dest_dir, new_filename)
            count += 1
            if not os.path.exists(dest_path):
                shutil.copy(source_path, dest_path)
                break

source_dir = "./data/SSL_ML"
dest_dir = "./data/SSL"
count = 1
for dirpath, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".JPG"):
            source_path = os.path.join(dirpath, filename)
            dirname = os.path.basename(os.path.normpath(dirpath))
            new_filename = f"{dirname}_{filename.replace(filename, str(count).zfill(3))}.jpeg"
            dest_path = os.path.join(dest_dir, new_filename)
            count += 1
            if not os.path.exists(dest_path):
                shutil.copy(source_path, dest_path)
                break


conn = sqlite3.connect('./data/metadata.db')
c = conn.cursor()

# Create table if it does not exist
c.execute('CREATE TABLE IF NOT EXISTS ISL_Table (word TEXT, video_id TEXT, url TEXT)')

# Iterate through directory and insert records into table
for root, dirs, files in os.walk('./data/ISL'):
    for file in files:
        # Extract word and video_id from filename
        filename_parts = os.path.splitext(file)[0].split('_')
        word = filename_parts[0]
        video_id = filename_parts[1]
        
        url = os.path.join(root, file)

        c.execute('INSERT INTO ISL_Table (word, video_id, url) VALUES (?, ?, ?)', (word, video_id, url))


# Create table if it does not exist
c.execute('CREATE TABLE IF NOT EXISTS SSL_Table (word TEXT, video_id TEXT, url TEXT)')

# Iterate through directory and insert records into table
for root, dirs, files in os.walk('./data/SSL'):
    for file in files:
        # Extract word and video_id from filename
        filename_parts = os.path.splitext(file)[0].split('_')
        word = filename_parts[0]
        video_id = filename_parts[1]
        
        url = os.path.join(root, file)

        c.execute('INSERT INTO SSL_Table (word, video_id, url) VALUES (?, ?, ?)', (word, video_id, url))

# Commit changes and close database connection
conn.commit()
conn.close() 


