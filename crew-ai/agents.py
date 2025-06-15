from crewai import Agent, LLM
from tools import yt_tool
from dotenv import load_dotenv
from load_dotenv import load_dotenv
import os 
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-4o"


## Create a senior blog content researcher
blog_researcher=Agent(
    role='Blog Researcher from Youtube Videos',
    goal='get the relevant video transcription for the topic {topic} from the provided youtube channel', # Mục tiêu cụ thể (lấy transcript video theo chủ đề)
    verbose=True, # Hiển thị chi tiết quá trình làm việc
    memory=True, # Agent có thể nhớ thông tin từ các tương tác trước
    backstory=(
       "Expert in understanding videos in AI Data Science , Machine Learning And GEN AI and providing suggestion" 
    ), # Bối cảnh và chuyên môn của agent
    tools=[yt_tool],
    # llm= llm, 
    allow_delegation=True # Cho phép agent giao việc cho agent khác
)

## creating a senior blog writer agent with YT tool
# Chức năng: Agent này chuyên viết blog dựa trên thông tin đã nghiên cứu
# allow_delegation=False: Không cho phép giao việc (agent cuối cùng trong chuỗi)

blog_writer=Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the video {topic} from youtube video',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
    ), # Bối cảnh và chuyên môn của agent
    tools=[yt_tool],
    # llm= llm,
    allow_delegation=False


)




