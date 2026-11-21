import streamlit as st
import time

from pipeline import run_search, run_reader, run_writer, run_critic


# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------- CUSTOM CSS --------------------

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
    color: #ffffff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #9ca3af;
    font-size: 1.1rem;
}

.agent-card {
    background-color: #1a1d24;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #2d313a;
    margin-bottom: 10px;
}

div[data-testid="stMetric"] {
    background-color: #1a1d24;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #2d313a;
}

.stButton button {
    border-radius: 10px;
    height: 3rem;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR --------------------

with st.sidebar:

    st.markdown("## 🔬 Research AI")

    st.markdown("---")

    st.markdown("### Pipeline")

    st.markdown("""
    🔎 **Search Agent**

    📖 **Reader Agent**

    ✍️ **Writer Agent**

    🧐 **Critic Agent**
    """)

    st.markdown("---")

    st.markdown("### About")

    st.info(
        """
        This AI research pipeline uses multiple agents
        to search, extract, write, and review information
        about your research topic.
        """
    )

    st.markdown("---")

    st.caption("Powered by LangChain & AI Agents")


# -------------------- HEADER --------------------

st.markdown(
    '<h1 class="main-title">AI Research Assistant</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Your multi-agent research and report generation system</p>',
    unsafe_allow_html=True
)

st.markdown("---")


# -------------------- INPUT --------------------

st.markdown("### 📝 Research Topic")

topic = st.text_area(
    "What would you like to research?",
    placeholder="Example: Impact of artificial intelligence on healthcare...",
    height=100
)

col1, col2 = st.columns([1, 5])

with col1:

    research_button = st.button(
        "🚀 Start Research",
        type="primary",
        use_container_width=True
    )


# -------------------- PIPELINE --------------------

if research_button:

    if not topic.strip():

        st.warning("Please enter a research topic.")

    else:

        st.markdown("---")

        st.markdown("## 🧠 Research Pipeline")

        progress_bar = st.progress(0)

        status = st.status(
            "Initializing research pipeline...",
            expanded=True
        )

        results = {}

        try:

            # -------------------- STEP 1 --------------------

            status.update(
                label="🔎 Search Agent is working...",
                state="running"
            )

            status.write("Searching for reliable and recent information...")

            results["search_results"] = run_search(topic)

            progress_bar.progress(25)

            status.write("✅ Search completed successfully")


            # -------------------- STEP 2 --------------------

            status.write("📖 Reader Agent is scraping relevant resources...")

            results["scraped_content"] = run_reader(
                topic,
                results["search_results"]
            )

            progress_bar.progress(50)

            status.write("✅ Reading and extraction completed")


            # -------------------- STEP 3 --------------------

            status.write("✍️ Writer Agent is generating the research report...")

            results["report"] = run_writer(
                topic,
                results["search_results"],
                results["scraped_content"]
            )

            progress_bar.progress(75)

            status.write("✅ Report generated successfully")


            # -------------------- STEP 4 --------------------

            status.write("🧐 Critic Agent is reviewing the report...")

            results["feedback"] = run_critic(
                topic,
                results["report"]
            )

            progress_bar.progress(100)

            status.update(
                label="🎉 Research pipeline completed!",
                state="complete",
                expanded=False
            )


            # -------------------- SAVE RESULTS --------------------

            st.session_state["research_results"] = results
            st.session_state["research_topic"] = topic


        except Exception as e:

            status.update(
                label="❌ Research pipeline failed",
                state="error"
            )

            st.error(f"An error occurred: {e}")


# -------------------- DISPLAY RESULTS --------------------

if "research_results" in st.session_state:

    results = st.session_state["research_results"]

    topic = st.session_state["research_topic"]

    st.markdown("---")

    st.markdown("## 📊 Research Results")

    st.markdown(f"### 🎯 Topic: {topic}")


    # -------------------- METRICS --------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="Search Agent",
            value="Completed",
            delta="Success"
        )

    with col2:

        st.metric(
            label="Reader Agent",
            value="Completed",
            delta="Success"
        )

    with col3:

        st.metric(
            label="Writer Agent",
            value="Completed",
            delta="Success"
        )

    with col4:

        st.metric(
            label="Critic Agent",
            value="Completed",
            delta="Success"
        )


    st.markdown("---")


    # -------------------- TABS --------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Final Report",
        "🔎 Search Results",
        "📖 Scraped Content",
        "🧐 Critic Review"
    ])


    # -------------------- FINAL REPORT --------------------

    with tab1:

        st.markdown("### 📄 Final Research Report")

        st.markdown(results["report"])

        st.download_button(
            label="⬇️ Download Research Report",
            data=results["report"],
            file_name="research_report.md",
            mime="text/markdown"
        )


    # -------------------- SEARCH RESULTS --------------------

    with tab2:

        st.markdown("### 🔎 Search Agent Results")

        with st.expander("View Search Results", expanded=True):

            st.markdown(results["search_results"])


    # -------------------- SCRAPED CONTENT --------------------

    with tab3:

        st.markdown("### 📖 Reader Agent Output")

        with st.expander("View Scraped Content", expanded=True):

            st.markdown(results["scraped_content"])


    # -------------------- CRITIC --------------------

    with tab4:

        st.markdown("### 🧐 Critic Agent Review")

        st.markdown(results["feedback"])


    # -------------------- FOOTER --------------------

    st.markdown("---")

    st.markdown(
        """
        <div style="text-align:center; color:#6b7280;">
            Generated by AI Research Assistant
        </div>
        """,
        unsafe_allow_html=True
    )