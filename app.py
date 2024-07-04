import streamlit.components.v1 as components
import datetime
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


@st.cache_data(ttl="4hr")
def get_arxiv_title_dict():
    return u.get_arxiv_title_dict()


if st.session_state.get("arxiv_title_dict") is None:
    st.session_state.arxiv_title_dict = get_arxiv_title_dict()


def main():
    st.write("# [📚➡📊] Arxiv Paper to Interactive Dashboard")
    st.caption("Turn any LLM related Arxiv whitepaper into an interactive data dashboard.")
    arxiv_title_dict = st.session_state.arxiv_title_dict
    arxiv_codes = sorted(list(arxiv_title_dict.keys()))[::-1]
    arxiv_code = st.selectbox("Arxiv Code", options=arxiv_codes, index=arxiv_codes.index("2406.19371"))


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
            script = u.get_arxiv_dashboard_script(arxiv_code, "script_content")
            summary = u.get_arxiv_dashboard_script(arxiv_code, "summary")
            if not script:
                ## Check if we got credits.
                request_count = u.get_daily_arxiv_request_count(datetime.datetime.now().strftime("%Y-%m-%d"))
                if request_count > 20:
                    st.error("Too many requests today. Please try again tomorrow!")
                    return

                res_str = run_instructor_query(
                    p.artifacts_system_prompt,
                    p.artifacts_user_prompt.format(title=title, content=content),
                    llm_model="claude-3-5-sonnet-20240620",
                    temperature=0.8
                )
                summary = res_str.split("<summary>")[1].split("</summary>")[0].strip()
                script = res_str.split("<script>")[1].split("</script>")[0].strip()
                u.save_arxiv_dashboard_script(arxiv_code, summary, script)

            output_placeholder.empty()

        html_content = html_template.format(title=title, summary=summary, script=script)
        components.html(html_content, height=1000, scrolling=True)


if __name__ == '__main__':
    main()