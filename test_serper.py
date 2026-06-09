from crewai_tools import SerperDevTool

tool = SerperDevTool()

result = tool.run(
    search_query="Mesacol medicine"
)

print(result)