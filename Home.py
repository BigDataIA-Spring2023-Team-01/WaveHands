



# #-------------------------------------------------------------------------------------------------------------------------------
# #Fundamental template
# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )

# st.write("# WaveHands 👋")
# st.write("Bridging the gap between deaf and hearing world")


import os
import sqlite3
import shutil

#----------------------------------------------------TRANSFER FROM DOWNLOADS INTO DATA/ISL DIRECTORY--------------------
# import os
# import shutil

# #code to transfer file from downloads into dirctory in data
# downloads_path = "/Users/andy/Downloads/Indian"
# destination_path = "/Users/andy/Documents/GitHub/WaveHands/data/ISL"

# # Get a list of files in the downloads folder
# files = os.listdir(downloads_path)

# # Loop through each file in the downloads folder
# for file in files:
#     # Get the full path of the file
#     file_path = os.path.join(downloads_path, file)
#     # Check if the file is a directory
#     if os.path.isdir(file_path):
#         # If it is a directory, copy the entire directory to the destination folder
#         shutil.copytree(file_path, os.path.join(destination_path, file))
#     else:
#         # If it is a file, copy the file to the destination folder
#         shutil.copy(file_path, os.path.join(destination_path, file))


#------------------------------------------------TAKES ONE IMAGE EACH FOR EVERY FOLDER AND ADDS TO ISL/EXTRACTED---------------------------------
import os
import shutil

# source_dir = "/Users/andy/Documents/GitHub/WaveHands/data/ISL_ML"
# destination_dir = "/Users/andy/Documents/GitHub/WaveHands/data/ISL"

# # Loop over all subdirectories in the source directory
# for root, dirs, files in os.walk(source_dir):
#     for directory in dirs:
#         dir_path = os.path.join(root, directory)
#         file_names = os.listdir(dir_path)
#         if len(file_names) > 0:
#             # Get the first file in the directory
#             file_name = file_names[0]
#             # Create the destination directory path with the same subdirectory structure as the source directory
#             new_dir_path = os.path.join(destination_dir, os.path.relpath(dir_path, source_dir))
#             # Create the destination directory if it doesn't exist
#             os.makedirs(new_dir_path, exist_ok=True)
#             # Create the full source and destination file paths
#             src_path = os.path.join(dir_path, file_name)
#             dst_path = os.path.join(new_dir_path, file_name)
#             # Copy the file to the destination directory
#             shutil.copy(src_path, dst_path)

#------------------ same as above but without folder structure---------
# import os
# import shutil

# source_dir = "/Users/andy/Documents/GitHub/WaveHands/data/ISL_ML"
# dest_dir = "/Users/andy/Documents/GitHub/WaveHands/data/ISL"
# count = 1
# for dirpath, dirnames, filenames in os.walk(source_dir):
#     for filename in filenames:
#         if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
#             source_path = os.path.join(dirpath, filename)
#             dirname = os.path.basename(os.path.normpath(dirpath))
#             new_filename = f"{dirname}_{filename.replace(filename, str(count).zfill(3))}.jpeg"
#             dest_path = os.path.join(dest_dir, new_filename)
#             count += 1
#             if not os.path.exists(dest_path):
#                 shutil.copy(source_path, dest_path)
#                 break

#----------- ^^^^^^^^^^^^^ THIS IS THE CODE^^^^^^^^^^^^^^^^^^^^^^^^
   










# #-------------------------------------------------CONVERT ISL DATASET TO CSV----------------------
# import os
# import pandas as pd
# from tqdm import tqdm

# # Path to the dataset folder
# dataset_path = "/Users/andy/Documents/GitHub/WaveHands/data/ISL"

# # List all the image files in the dataset folder
# image_files = []
# for root, dirs, files in os.walk(dataset_path):
#     for file in files:
#         if file.endswith(".jpg"):
#             image_files.append(os.path.join(root, file))

# # Create a DataFrame to store the dataset information
# dataset_df = pd.DataFrame(columns=["image_path", "label"])

# # Loop through all the image files and extract the label information from the folder name
# for image_path in tqdm(image_files):
#     label = os.path.basename(os.path.dirname(image_path))
#     dataset_df = pd.concat([dataset_df, pd.DataFrame({"image_path": image_path, "label": label}, index=[0])], ignore_index=True)


# # Save the dataset information to a CSV file
# dataset_df.to_csv("/Users/andy/Documents/GitHub/WaveHands/data/ISL_extracted/dataset.csv", index=False)

#------------------------------------------------------------------------------------------------------------------------------

import os
import sqlite3

# Set up SQLite database
conn = sqlite3.connect('/Users/andy/Documents/GitHub/WaveHands/data/metadata.db')
c = conn.cursor()

# Create table if it does not exist
c.execute('CREATE TABLE IF NOT EXISTS ISL_Table (alphabet_digit TEXT, image_id TEXT, file_path TEXT)')

# Iterate through directory and insert records into table
for root, dirs, files in os.walk('/Users/andy/Documents/GitHub/WaveHands/data/ISL'):
    for file in files:
        # Extract alphabet_digit and image_id from filename
        filename_parts = os.path.splitext(file)[0].split('_')
        alphabet_digit = filename_parts[0]
        image_id = filename_parts[1]
        
        file_path = os.path.join(root, file)

        c.execute('INSERT INTO ISL_Table (alphabet_digit, image_id, file_path) VALUES (?, ?, ?)', (alphabet_digit, image_id, file_path))

# Commit changes and close database connection
conn.commit()
conn.close()




