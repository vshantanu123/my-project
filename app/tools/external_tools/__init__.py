# from langchain.tools import tool
# from langchain_community.tools import WikipediaQueryRun
# from langchain_community.utilities import WikipediaAPIWrapper
#
# from app.utils.applogger import logger
#
#
# @tool(description="Search Wikipedia for information if not available in the other tools.")
# async def search_wikipedia(user_query: str):
#     """
#         Search Wikipedia for information if not available in the other tools.
#     :param user_query:
#     :return:
#     """
#     logger.info(f"user query {user_query}")
#     logger.info(f"calling from search_wikipedia ")
#     wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
#     wikipedia_result = wikipedia.run(user_query)
#     logger.info(f"return result from wikipedia search")
#     return wikipedia_result
#
#
# def get_external_tools():
#     return [search_wikipedia]
