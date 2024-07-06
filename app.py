import streamlit.components.v1 as components
import datetime
import streamlit as st

import utils as u
import prompts as p
from instruct import run_instructor_query

st.set_page_config(page_title="LLM Arxiv Paper to Data Dashboard", page_icon="🪄", layout="wide")

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
        border-radius: 10px;
    }}
    p {{
        font-size: 0.9em;
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
    top: 0px; /* Adjust this value based on the height of your header */
    left: 0;
    right: 0;
    margin: auto;
    width: 100%;
    z-index: 100;
    background-color: #FFA500;
    color: white;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.25);
    font-weight: bold;
    border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    #root {{
        padding: 20px;
        margin-top: 110px; /* Adjust this value based on the combined height of your summary */
    }}
</style>
</head>
<body>
    <div id="summary">
        {summary}
    </div>
    <div id="root"></div>
    <script>
        // Card component
        const Card = ({{ children, className, style }}) => (
            React.createElement('div', {{ className: `card ${{className}}`, style: {{ ...style, backgroundColor: '#FFF8E1', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', overflow: 'hidden', transition: 'all 0.3s ease-in-out' }} }}, children)
        );
        
        const CardContent = ({{ children, className }}) => (
            React.createElement('div', {{ className: `card-content ${{className}}`, style: {{ padding: '16px', color: '#333333' }} }}, children)
        );
        
        // Tabs components
        const Tabs = ({{ defaultValue, children, className }}) => {{
            const [activeTab, setActiveTab] = React.useState(defaultValue);
        
            const handleClick = (value) => {{
                setActiveTab(value);
            }};
        
            return React.createElement('div', {{ className }},
                React.createElement(TabsList, {{ activeTab, handleClick, className: "tabs-header" }}, 
                    React.Children.map(children, child => child.type === TabsTrigger ? React.cloneElement(child, {{ activeTab, handleClick }}) : null)
                ),
                React.Children.map(children, child => child.type === TabsContent ? React.cloneElement(child, {{ activeTab }}) : null)
            );
        }};
        
        const TabsList = ({{ children, activeTab, handleClick, className }}) => (
            React.createElement('div', {{
                className: `tabs-list ${{className}}`,
                style: {{
                    // position: 'fixed', // Make it fixed at the top
                    width: '100%',
                    display: 'flex',
                    justifyContent: 'space-around',
                    padding: '8px 0',
                    background: '#FFF8E1',
                    borderBottom: '3px solid #FF8C00',
                    zIndex: '101', // Ensure it's above other content, adjust as necessary
                }}
            }},
            React.Children.map(children, child =>
                React.cloneElement(child, {{ activeTab, handleClick }})
            ))
        );
        
        const TabsTrigger = ({{ value, children, activeTab, handleClick, className }}) => (
            React.createElement('button', {{
                className: `tabs-trigger ${{className}} ${{activeTab === value ? 'active' : ''}}`,
                onClick: () => handleClick(value),
                style: {{ padding: '8px 16px', cursor: 'pointer', borderBottom: activeTab === value ? '2px solid #FF8C00' : 'none', transition: 'all 0.3s ease-in-out' }}
            }}, children)
        );
        
        const TabsContent = ({{ value, children, activeTab, className }}) => (
            React.createElement('div', {{
                className: `tabs-content ${{className}}`,
                style: {{ display: activeTab === value ? 'block' : 'none', padding: '16px'}}
            }}, children)
        );
        {script}

        // Calculate margin-top
        const summaryText = document.getElementById('summary').innerText;
        
        const charsPerLine = 75;
        const numberOfLines = Math.ceil(summaryText.length / charsPerLine);
        
        const baseMargin = 110; // Base margin for 4 lines
        const additionalMarginPerTwoLines = 40; // Additional margin for every 2 lines above 4
        let marginTop = baseMargin;
        if (numberOfLines > 4) {{
            marginTop += Math.floor((numberOfLines - 4) / 2) * additionalMarginPerTwoLines;
        }}        
        document.getElementById('root').style.marginTop = `${{marginTop}}px`;
    </script>
</body>
</html>"""


@st.cache_data(ttl="4hr")
def get_arxiv_title_dict():
    return u.get_arxiv_title_dict()


if st.session_state.get("arxiv_title_dict") is None:
    st.session_state.arxiv_title_dict = get_arxiv_title_dict()


def main():
    st.write("# f(📃) ➡ [📊]")
    st.write("Turn any LLM related Arxiv whitepaper into an interactive data dashboard.")
    arxiv_title_dict = st.session_state.arxiv_title_dict
    arxiv_code_title_map = {f"{code} - {title}":code for code, title in arxiv_title_dict.items()}
    arxiv_codes_names = sorted(list(arxiv_code_title_map.keys()))[::-1]
    arxiv_code_name = st.selectbox("Arxiv Code", options=arxiv_codes_names, index=0, label_visibility="collapsed")
    arxiv_code = arxiv_code_title_map[arxiv_code_name]

    if st.button(" 🪄 Generate"):
        with st.spinner("**Generating interactive card (this might take a minute)...**"):
                output_placeholder = st.empty()
                u.log_request(arxiv_code)
                title = u.get_arxiv_title_dict()[arxiv_code]
                mini_content = u.get_recursive_summary(arxiv_code)[:1000] + "..."

                component_placeholder = output_placeholder.columns((1.2, 4, 3, 1.2))
                arxiv_link = u.get_img_link_for_blob(f"arxiv:{arxiv_code}")
                component_placeholder[2].image(arxiv_link)
                component_placeholder[1].write(f"#### {title}")
                component_placeholder[1].write(mini_content)

                content = u.get_extended_notes(arxiv_code, expected_tokens=3000)
                script = u.get_arxiv_dashboard_script(arxiv_code, "script_content")
                summary = u.get_arxiv_dashboard_script(arxiv_code, "summary")
                scratchpad = ""
                if not script:
                    # Check if we got credits.
                    request_count = u.get_daily_arxiv_request_count(datetime.datetime.now().strftime("%Y-%m-%d"))
                    if request_count > 50:
                        st.error("Too many requests today. Please try again tomorrow!")
                        return

                    res_str = run_instructor_query(
                        p.artifacts_system_prompt,
                        p.artifacts_user_prompt.format(title=title, content=content),
                        llm_model="claude-3-5-sonnet-20240620",
                        temperature=0.7
                    )
                    ## Check if it ends with </script> tag, otherwise append output to user prompt and rerun.
                    if not res_str.endswith("</script>"):
                        res_str += run_instructor_query(
                            p.artifacts_system_prompt,
                            p.artifacts_user_prompt.format(title=title, content=content) + res_str,
                            llm_model="claude-3-5-sonnet-20240620",
                            temperature=0.7
                        )

                    summary = res_str.split("<summary>")[1].split("</summary>")[0].strip()
                    script = res_str.split("<script>")[1].split("</script>")[0].strip()
                    u.save_arxiv_dashboard_script(arxiv_code, summary, scratchpad, script)

                output_placeholder.empty()

        html_content = html_template.format(title=title, summary=summary, script=script)
        @st.experimental_dialog(title, width="large")
        def render():
            components.html(html_content, height=700, scrolling=True)

        render()

    st.caption("🖤 Powered by Claude-3.5-Sonnet.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        st.error("An error occurred... Please try again.")