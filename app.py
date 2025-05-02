import streamlit as st
from main import ResearchResponse, llm, parser, search_tool, wiki_tool, save_tool

st.title("AI Research Assistant 🤖📄")

query = st.text_input("What can I help you research?")

if st.button("Run Research"):
    with st.spinner("Running tools..."):
        search_result = search_tool.run(query)
        wiki_result = wiki_tool.run(query)

    st.write("### 🔍 Search Results")
    st.write(search_result)
    
    st.write("### 📚 Wikipedia Results")
    st.write(wiki_result)

    input_text = f"""
    You are a research assistant generating a research paper.

    Here are search results:
    Search Tool: {search_result}

    Here are wikipedia results:
    Wiki Tool: {wiki_result}

    Please summarize these sources and output in this format:
    {parser.get_format_instructions()}
    """

    with st.spinner("Querying Llama..."):
        response = llm.invoke(input_text)

    try:
        structured_response = parser.parse(response.content)
        st.success("✅ Research completed!")

        st.write("### 📝 Summary")
        st.json(structured_response.dict())

        if st.button("Save to File"):
            result = save_tool.run(response.content)
            st.info(result)

    except Exception as e:
        st.error(f"Error parsing response: {e}")
        st.write("Raw LLM response:")
        st.text(response.content)
