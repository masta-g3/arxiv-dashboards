import streamlit.components.v1 as components
import streamlit as st

import utils as u
import prompts as p
from instruct import run_instructor_query

st.set_page_config(page_title="LLM Interactive Summaries", page_icon="📊", layout="wide")

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://unpkg.com/react@17.0.2/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@17.0.2/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/prop-types/prop-types.min.js"></script>
    <script src="https://unpkg.com/recharts/umd/Recharts.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
<style>
    body, html {{
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
        background-color: #FFF5E6;
    }}
    #header {{
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 100;
        background-color: #FF8C00;
        color: white;
        padding: 20px;
        text-align: center;
        font-size: 2em;
    }}
    #summary {{
        position: fixed;
        top: 70px; /* Adjust this value based on the height of your header */
        width: 100%;
        z-index: 100;
        background-color: #FFA500;
        color: white;
        padding: 15px;
        border-radius: 5px;
    }}
    #root {{
        padding: 20px;
        margin-top: 180px; /* Adjust this value based on the combined height of your header and summary */
    }}
</style>
</head>
<body>
    <div id="header">
        <h1>{title}</h1>
    </div>
    <div id="summary">
        {summary}
    </div>
    <div id="root"></div>
    <script>
        {script}
    </script>
</body>
</html>"""

def main():
    st.write("# 📚 Arxiv Notes to Interactive Dashboard Summary")
    arxiv_code = st.text_input("Arxiv Code", value="2406.19371")

    if st.button("Submit"):
        with st.spinner("Generating summary..."):
            output_placeholder = st.empty()
            u.log_request(arxiv_code)
            title = u.get_arxiv_title_dict()[arxiv_code]
            mini_content = u.get_recursive_summary(arxiv_code)[:1000] + "..."

        with st.spinner("Generating data dashboard..."):
            component_placeholder = output_placeholder.columns((1.2, 4, 3, 1.2))
            arxiv_link = u.get_img_link_for_blob(f"arxiv:{arxiv_code}")
            component_placeholder[2].image(arxiv_link)
            component_placeholder[1].write(f"**{title}**")
            component_placeholder[1].write(mini_content)

            content = u.get_extended_notes(arxiv_code, expected_tokens=3000)

            res_str = run_instructor_query(
                p.artifacts_system_prompt,
                p.artifacts_user_prompt.format(title=title, content=content),
                llm_model="claude-3-5-sonnet-20240620",
                temperature=0.8
            )

            output_placeholder.empty()
            summary = res_str.split("<summary>")[1].split("</summary>")[0]
            script = res_str.split("<script>")[1].split("</script>")[0]

        html_content = html_template.format(title=title, summary=summary, script=script)
        components.html(html_content, height=900, scrolling=True)


if __name__ == '__main__':
    main()