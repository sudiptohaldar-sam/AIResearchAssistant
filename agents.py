from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import searcher, scrape_web
import os
from dotenv import load_dotenv
load_dotenv()

llm=ChatGroq(model="openai/gpt-oss-120b",max_tokens=1200)

#1st agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[searcher],
        system_prompt=(
            "You are a web research assistant. Use ONLY the `searcher` tool. "
            "Never call any other tool such as `open` or `browser`."
        )
    )

#2nd agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_web],
        system_prompt=(
            "You read web pages. To read any URL, call the `scrape_web` tool "
            "with the URL as a plain string, exactly as given. "
            "Never call `open`, `browser`, or any tool not provided."
        )
    )

#writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a research writer. Turn the given research into a short report with this structure:

        ## Introduction
        Briefly introduce the topic and what the report covers.

        ## Main Body
        Organize the key findings into clear points. Use only the provided research.

        ## Conclusion
        Summarize the key takeaways.

        Don't invent facts. Keep the tone clear and professional."""
    ),
    (
        "human",
        "Topic: {topic}\n\nResearch:\n{research}"
    ),
])

writer_chain=writer_prompt | llm | StrOutputParser()

#critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a strict research critic. Review the given research on the topic and evaluate it on:
accuracy, depth, relevance, clarity, and use of sources.

Respond in this format:

Score: x/10

Strengths:
- ...

Weaknesses:
- ...

Suggestions:
- ...

Onr line verdict:
- ...

Be honest and specific. Don't inflate the score. Only a 9 or 10 should be given to excellent, well-sourced research."""
    ),
    (
        "human",
        "Topic: {topic}\n\nResearch:\n{research}"
    ),
])

critic_chain=critic_prompt | llm | StrOutputParser()
