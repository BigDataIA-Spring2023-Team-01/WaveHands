from cProfile import label
from diagrams import Diagram, Cluster
from diagrams import Edge
from diagrams.azure.general import Userresource # to denote user 
from diagrams.alibabacloud.communication import DirectMail # to denote streamlit cloud
from diagrams.elastic.elasticsearch import LogstashPipeline # to denote api 
from diagrams.onprem.container import Docker # to denote docker
from diagrams.custom import Custom # for custom logos : streamlit, whiper api, kaggle
from diagrams.aws.storage import S3 # to denote aws bucket
from diagrams.onprem.workflow import Airflow # to denote airflow 
from diagrams.onprem.compute import Server # to denote wordbook in streamlit 
from diagrams.onprem.ci import GithubActions # to denote dags
from diagrams.gcp.ml import SpeechToText as STT # streamlit HandSpeak 
from diagrams.gcp.ml import TextToSpeech as TTS # streamlit SIGNIT
from diagrams.aws.management import Cloudwatch # cloudwatch in AWS
from diagrams.gcp.storage import Storage as GCS # cloud storage 
 
with Diagram("Workflow Diagram", show=False, direction="LR"):
  user = Userresource("Users")
  with Cluster("Cloud"):
    with Cluster("Streamlit Cloud"):
      streamlit_app = Custom("Streamlit","./data/images/streamlit-logo.png")
      with Cluster("Streamlit"):
        login = Server("Login Dashboard")
        WB = Server("Word Book")
        Sign = TTS("SignIt")
        HS = STT("HandSpeak")

    with Cluster("Airflow"):
      af = Airflow("Airflow")
      dag1 = GithubActions("DAG 1")
      dag2 = GithubActions("DAG 2")

    with Cluster("API's"):
      api = LogstashPipeline("Fast API")
      wapi = Custom("Whisper API", "./data/images/download.png")
      mediapipe = Custom("Mediapipe", "./data/Images/mediapipe.png")

    with Cluster("AWS"):
      s3 = S3("Transcribed Texts")
      logs = Cloudwatch("User logs")

    with Cluster("Database"):
      db = GCS("Data Base")

    user >> streamlit_app
    Sign >> Edge(label="Upload Audio File  triggers") >> dag1
    api >> Edge(label="Fetches data") >> db
    WB >> Edge(label="Fetches sign language data based on input") >> api
    Sign >> Edge(label="Uploads YouTube link triggers") >> dag1  
    dag1 >> Edge(label="Transcribes the audio file") >> wapi
    wapi >> Edge(label="transcribed text in storage") >> s3

    HS >> Edge(label="triggers DAG 2") >> dag2
    dag2 >> Edge(label="Gesture recognisiton model") >> mediapipe
    mediapipe >> Edge(label="Stores data") >> s3

    login >> Edge(label="logs the user activity") >> logs


