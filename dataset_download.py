import kaggle
import os
import sqlite3


# # Authenticate and download dataset
kaggle.api.authenticate()
kaggle.api.dataset_download_files('risangbaskoro/wlasl-processed', path='data/ASL', unzip=True)

# Connect to metadata database and retrieve unique video IDs
conn = sqlite3.connect('data/metadata.db')
c = conn.cursor()
c.execute("SELECT DISTINCT video_id FROM ASL_Table")
video_ids = [id[0] for id in c.fetchall()]

# Delete videos not in list of retrieved IDs
videos_path = 'data/ASL/videos'
for file in os.listdir(videos_path):
    if file.endswith('.mp4'):
        file_id = file.split('.')[0]
        if file_id not in video_ids:
            os.remove(os.path.join(videos_path, file))

# Close database connection
conn.close()

print("Done")
