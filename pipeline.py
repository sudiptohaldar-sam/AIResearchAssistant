from agents import build_reader_agent,build_search_agent,critic_chain,writer_chain
from rich import print

def run_research_pipeline(topic:str)->dict:
    state={}
    #search agent working
    print("\n"+"="*50)
    print("Step 1- search agent is working ...")
    print("="*50)

    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages":[("user",f"Give me detailed, reliable and recent details about:{topic}")]
    }) 
    state["search_results"]=search_result['messages'][-1].content
    print("\n Search result: ", state['search_results'])

    #step 2 - reader agent
    print("\n"+"="*50)
    print("Step 2- Reader agent is scraping top resource is working ...")
    print("="*50)

    reader_agent=build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [(
            "user",
            f"Based on the following results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search results:\n{state['search_results'][:400]}"
        )]
    })
    state['scraped_content']=reader_result['messages'][-1].content
    print("\n Scraped content:", state['scraped_content'])

    #step 3 - Writer agent
    print("\n"+"="*50)
    print("Step 3- The writer agent is drafting the report ...")
    print("="*50)
    research_combined=(
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"]=writer_chain.invoke({
         "topic":topic,
         "research":research_combined
    })
    print("\nFinal Report:",state['report'])

    #critic report
    print("\n"+"="*50)
    print("Step 4- Critic is reviewing the report ...")
    print("="*50)

    state['feedback']=critic_chain.invoke({
        "topic":topic,
        "research":state['report']
    })

    print("\nCritic report:",state['feedback'])

    return state

if __name__=="__main__":
    topic=input("\nEnter a research topic: ")
    run_research_pipeline(topic)

from agents import build_reader_agent, build_search_agent, critic_chain, writer_chain


def run_search(topic: str) -> str:
    agent = build_search_agent()
    result = agent.invoke({
        "messages": [("user", f"Give me detailed, reliable and recent details about: {topic}")]
    })
    return result["messages"][-1].content


def run_reader(topic: str, search_results: str) -> str:
    agent = build_reader_agent()
    result = agent.invoke({
        "messages": [(
            "user",
            f"Based on the following results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search results:\n{search_results[:400]}"
        )]
    })
    return result["messages"][-1].content


def run_writer(topic: str, search_results: str, scraped: str) -> str:
    research = (
        f"SEARCH RESULTS:\n{search_results}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{scraped}"
    )
    return writer_chain.invoke({"topic": topic, "research": research})


def run_critic(topic: str, report: str) -> str:
    return critic_chain.invoke({"topic": topic, "research": report})