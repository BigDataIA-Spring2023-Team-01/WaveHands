**WaveHands**


**Bridging the gap between the deaf and hearing world**
Although sign language is an effective means of communication, not everyone is familiar with it. Likewise, communicating with the hearing world might be difficult for those who are deaf or hard of hearing. 
WaveHands is a web application that utilizes advanced algorithms and machine learning to help bridge the communication gap between different communities. Specifically, it is designed to cater to the needs of the hearing-impaired community, making it easier for them to access and understand various forms of media.

Documentation : https://codelabs-preview.appspot.com/?file_id=1smHQI2--0jZQxkKMPynGA90ml7u-kTS-5YTe-TA1c4I/edit#0

Application Links : 
    Streamlit : http://34.136.86.232:8501/
    FastAPI : http://34.136.86.232:8000/docs
    Airflow : http://34.136.86.232:8080

Streamlit : 

Fast API: 

**Project Execution**
The Git repository contains all the necessary resources for this project. 
To begin, you will need to clone the repository and access it within your virtual environment.

Steps:
1. Open terminal
2. Browse the location where you want to clone the repository
3. Write the following command and press enter
``````````````````````````````````````````````````````````````````````````
    git clone https://github.com/BigDataIA-Spring2023-Team-01/SignIt.git
``````````````````````````````````````````````````````````````````````````
4. Now we need to run the following command which will download the dataset from kaggle that we are using to generate the sign language videos.

``````````````````````````
python3 db_metadata.py
``````````````````````````
````````````````````````````
python3 dataset_download.py
````````````````````````````

Note: This will download around 5GB of dataset to the data/ directory. This will be needed to create the sign language videos. Always run the above commands in sequence

5. We will run the docker compose command which will initiate all the containers and volumes needed and will startup the project

``````````````````````
docker-compose build
Docker-compose up -d
```````````````````````

Note: This assumes that you have docker desktop installed in your machine, if not please download docker desktop from the following website (Docker Desktop: https://www.docker.com/products/docker-desktop/) and startup the docker and docker-compose service using the below documentation : https://docs.docker.com/desktop/

In order to execute the project you would also need to make a .env file with the following requirements

```````````````````````````````````````````````
OPENAI_SECRET_KEY = <Your Whisper API Key>
STREAMLIT_URL = <To be taken from README.md>
```````````````````````````````````````````````

**Folder Structure:**

./streamlit
This folder contains the web application files.

./api
This folder contains the fast API functions
        
./pytest
This folder contains the testing file and use cases
        
./data
This folder contains the dataset, the missing alphabet's videos, and images used in the project     
        
./airflow
this folder contains code for airflow DAG for processing audio files and converting them to sign language
        
        
**Declaration**

Contribution

Anandita Deb : 25%

Cheril Yogi :25%

Shamin Chokshi :25%

Thejas Bharadwaj :25%

WE ATTEST THAT WE HAVEN'T USED ANY OTHER STUDENT'S WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.
