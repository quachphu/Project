from crewai import Crew,Process
from agents import blog_researcher,blog_writer
from tasks import research_task,write_task


# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[blog_researcher, blog_writer], # Danh sách các agents trong crew
  tasks=[research_task, write_task], # Danh sách các tác vụ cần thực hiện
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=True, #  Crew có thể nhớ thông tin giữa các lần chạy
  cache=True, # Lưu cache để tăng tốc độ xử lý
  max_rpm=100, # Giới hạn 100 requests per minute đến API
  share_crew=True # Cho phép chia sẻ thông tin giữa các agents
)

## start the task execution process with enhanced feedback
result=crew.kickoff(inputs={'topic':'AI VS ML VS DL vs Data Science'})
print(result)