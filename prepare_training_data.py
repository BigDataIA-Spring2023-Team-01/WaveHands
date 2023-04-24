# %%
import json
import os
import shutil

import numpy as np
import pandas as pd

# %%
main_path =  (r"data/kaggledataset/")
wlasl_df = pd.read_json(main_path + "WLASL_v0.3.json")
wlasl_df.head()

# %%
wlasl_df.shape

# %%
def get_videos_ids(json_list):
    video_ids = []
    for ins in json_list:
        video_id = ins['video_id']
        if os.path.exists(f'{main_path}videos/{video_id}.mp4'):
            video_ids.append(video_id)
    return video_ids

# %%
with open(main_path+'WLASL_v0.3.json', 'r') as data_file:
    json_data = data_file.read()

instance_json = json.loads(json_data)

# %%
get_videos_ids(instance_json[0]['instances'])

# %%
len(get_videos_ids(instance_json[0]['instances']))

# %%
wlasl_df["video_ids"] = wlasl_df["instances"].apply(get_videos_ids)

# %%
features_df = pd.DataFrame(columns=['gloss', 'video_id'])
for row in wlasl_df.iterrows():
    ids = get_videos_ids(row[1][1])
    word = [row[1][0]] * len(ids)
    df = pd.DataFrame(list(zip(word, ids)), columns=features_df.columns)
    features_df = features_df.append(df, ignore_index=True)

# %%
features_df

# %%
def move_videos_to_subdir(dataframe):
    for label in dataframe["gloss"].unique():
        dst_path = f'videos/{label}'
        os.makedirs(dst_path, exist_ok=True)
        
        for video in dataframe.loc[dataframe["gloss"] == label]["video_id"]:
            src = f'{main_path}videos/{video}.mp4'
            dst = dst_path + f'/{video}.mp4'
            shutil.copyfile(src, dst)


move_videos_to_subdir(features_df)

# %%
# os.listdir('videos/about/')


