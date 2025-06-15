from crewai import Task
from tools import yt_tool
from agents import blog_researcher,blog_writer

## Research Task
research_task = Task(
  description=(
    "Identify the video {topic}."
    "Get detailed information about the video from the channel video."
  ),
  expected_output='A comprehensive 3 paragraphs long report based on the {topic} of video content.',
  tools=[yt_tool],
  agent=blog_researcher,
)

# Writing task with language model configuration
# async_execution=False: Quan trọng! Đảm bảo tác vụ này chạy tuần tự, chờ research_task hoàn thành trước
write_task = Task(
  description=(
    "get the info from the youtube channel on the topic {topic}."
  ),
  expected_output='Summarize the info from the youtube channel video on the topic{topic} and create the content for the blog',
  tools=[yt_tool],
  agent=blog_writer, 
  async_execution=False, # Cái này đảm bảo rằng tác vụ viết sẽ chờ đợi kết quả từ tác vụ nghiên cứu trước khi thực hiện
  output_file='new-blog-post.md'  # cái này là ví dụ về tùy chỉnh đầu ra (output customization)  Lưu kết quả vào file Markdown
)