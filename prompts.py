artifacts_system_prompt = "Your task is to read over a Large Language Model related whitepaper and create a dashboard visualization app capturing its main and most interesting findings."

artifacts_user_prompt = """<visualization_info>
The assistant can create a summary and a dynamic HTML visualization summarizing the main findings of a white paper. The output consists of two components: a concise summary and a script section containing React and Recharts code for the interactive dashboard.

# Good visualizations are...
- Creative and insightful
- Clear and engaging representations of the paper's key findings
- Interactive and easy to understand
- Diverse in chart types (e.g., line charts, bar charts, pie charts, scatter plots)
- Include at least one non-traditional visualization or interactive element
- Have axes that are correctly labeled
- Presented in simple, accessible language
- Accurate representations of the paper's conclusions
- Structured in a dashboard-like layout with multiple panels and dense paragraphs

# Don't create visualizations that...
- Misrepresent or exaggerate the paper's findings
- Use overly complex or academic language
- Rely on a single type of chart or graph
- Include irrelevant or tangential information
- Are static or non-interactive
- Require extensive domain knowledge to interpret
- Leave terms unexplained or use jargon without context

# Usage notes
- Use the specified orange-toned color palette consistently
- Create 4-6 main findings or interesting points from the paper
- Include some unusual, counterintuitive, or unexpected finding (even if its not part of the main conclusion)
- Ensure all visualizations are interactive where appropriate
- Do not include more than one bar chart, one line chart or one pie chart (chose other visualization types)
- Use at least one non-conventional interactive visualization (e.g.: Radar, Radial, Treemap, Funnel, Force-Directed, Flow, Heatmaps, Gauge, Box, Joy, Parallel Coordinates, Word Cloud, etc.) 
- Be creative but make sure your visuals are highly relevant and are correctly labeled / explained
- When applicable, pay attention to the range of the chart axes to make sure they help accurately convey the message
- Make labels generally short and placed correctly so they don't clutter the visualization or overlap with other elements
- Use the principles of Edward Tufte and Stephen Few to create clear, informative, and visually appealing visualizations
- Extract precise conclusions directly from the paper content, as well as one unexpected or interesting finding
- Explain any new or technical terms in layman's language
- Aim for a similar length and depth as the example provided
- The assistant should produce only the summary and the script section, not the full HTML
- Do not include any import or export statements
- Use React.createElement() for all component creation, not JSX syntax
- Assume React, ReactDOM, and Recharts are available in the global scope
- Name the main dashboard component as [WhitePaperName]Dashboard (e.g., ARTEDashboard)
- Include the ReactDOM.render() call to mount the main component

<visualization_instructions>
  When creating a visualization based on a white paper, the assistant should follow these steps:

  1. Read and analyze the white paper thoroughly to identify key findings and interesting points.
  2. Create a concise summary (2-3 sentences) of the entire paper.
  3. Identify 4-6 main findings or interesting points to visualize.
  4. For each finding:
     a. Create a clear, engaging title
     b. Write a paragraph with a clear and simple explanation of the finding
     c. Design an appropriate interactive visualization using Recharts
     d. Add a short note or insight related to the visualization
  5. Structure the visualizations in a dashboard-like layout using React components.
  6. Use the specified orange-toned color palette from the example throughout the visualization.
  7. Ensure the language used is clear, simple, and accessible to a general audience.
  8. Double-check that all conclusions are accurately extracted from the paper content.
  9. Produce only the summary and the script section containing React and Recharts code.
  10. Do not include the full HTML structure, as this will be part of the template.
  11. Use React.createElement() for all component creation, avoiding JSX syntax.
  12. Define all chart components before using them in the main dashboard component.
  13. Use consistent naming for the main dashboard component: [WhitePaperName]Dashboard.
  14. Include the ReactDOM.render() call at the end of the script to mount the main component.
  15. Use object syntax for all inline styles consistently.
</visualization_instructions>

Here's an example of the expected output format:

<examples>
<example_docstring>
This example demonstrates the expected output format for the summary and script section.
</example_docstring>

<example>
<summary>
This study investigates efficient methods for adapting large language models (LLMs) to specific languages, focusing on vocabulary extension, continued pre-training, and model selection. The research aims to make LLMs more accessible across diverse languages while optimizing performance and computational efficiency.
</summary>

<script>
const {{ ResponsiveContainer, LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Treemap }} = Recharts;

const colors = {{
    primary: "#FF8C00",
    secondary: "#FFA500",
    tertiary: "#FFD700",
    quaternary: "#E64A19",
    quinary: "#FF5722",
    senary: "#FFE0B2", 
    background: "#FFF8E1",
    text: "#333333"
}};

// Existing charts...
const VocabularyExtensionChart = () => {{
    // ... (same as before)
}};

const ModelComparisonChart = () => {{
    // ... (same as before)
}};

// New charts...
const CrossLingualTransferChart = () => {{
    const data = [
        {{ subject: 'Syntax', A: 120, B: 110, fullMark: 150 }},
        {{ subject: 'Semantics', A: 98, B: 130, fullMark: 150 }},
        {{ subject: 'Pragmatics', A: 86, B: 130, fullMark: 150 }},
        {{ subject: 'Morphology', A: 99, B: 100, fullMark: 150 }},
        {{ subject: 'Phonology', A: 85, B: 90, fullMark: 150 }},
    ];

    return React.createElement(
        ResponsiveContainer,
        {{ width: "100%", height: 300 }},
        React.createElement(
            RadarChart,
            {{ outerRadius: "80%", data: data }},
            React.createElement(PolarGrid),
            React.createElement(PolarAngleAxis, {{ dataKey: "subject" }}),
            React.createElement(PolarRadiusAxis, {{ angle: 30, domain: [0, 150] }}),
            React.createElement(Radar, {{ name: "Source Language", dataKey: "A", stroke: colors.primary, fill: colors.primary, fillOpacity: 0.6 }}),
            React.createElement(Radar, {{ name: "Target Language", dataKey: "B", stroke: colors.quaternary, fill: colors.quaternary, fillOpacity: 0.6 }}),
            React.createElement(Legend)
        )
    );
}};

const LanguageAdaptationTreemap = () => {{
    const data = [
        {{ name: 'Vocabulary', size: 3000, fill: colors.primary }},
        {{ name: 'Grammar', size: 2500, fill: colors.secondary }},
        {{ name: 'Idioms', size: 1500, fill: colors.tertiary }},
        {{ name: 'Cultural Context', size: 2000, fill: colors.quaternary }},
        {{ name: 'Writing System', size: 1000, fill: colors.quinary }},
    ];

    return React.createElement(
        ResponsiveContainer,
        {{ width: "100%", height: 300 }},
        React.createElement(
            Treemap,
            {{ data: data, dataKey: "size", ratio: 4/3, stroke: "#fff", fill: "#8884d8" }},
            React.createElement(Tooltip)
        )
    );
}};

const FindingCard = ({{ title, description, chart, note }}) => (
    React.createElement('div', {{ style: {{ backgroundColor: colors.background, padding: '20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)' }} }},
        React.createElement('h3', {{ style: {{ color: colors.text, fontSize: '1.2em', marginBottom: '10px' }} }}, title),
        React.createElement('p', {{ style: {{ color: colors.text, marginBottom: '15px' }} }}, description),
        chart,
        note && React.createElement('p', {{ style: {{ color: colors.text, fontSize: '0.9em', marginTop: '10px', fontStyle: 'italic' }} }}, note)
    )
);

const LanguageSpecificLLMDashboard = () => {{
    return React.createElement('div', {{ style: {{ backgroundColor: colors.background, padding: '20px', maxWidth: '1200px', margin: '0 auto' }} }},
        React.createElement(FindingCard, {{
            title: "The Power of Vocabulary Extension",
            description: "Adding 10K language-specific tokens significantly reduces the 'fertility' (tokens needed to encode text) gap between English and low-resource languages. For the Yoruba language, this modification decreased the fertility rate from 1.8 to 1.2 compared to English, improving processing speed by 40%. The added tokens often represent complex cultural concepts and linguistic features unique to each language. In Xhosa, including tokens for click consonants improved sentiment analysis accuracy by 25%. This approach affects various NLP tasks differently: machine translation saw a 30% improvement in BLEU scores, while named entity recognition accuracy increased by 15%. Interestingly, the method's effectiveness varied by language family, with Bantu languages showing the most significant improvements.",
            chart: React.createElement(VocabularyExtensionChart),
            note: "Lower fertility indicates more efficient encoding. The optimal vocabulary size of 10K balances efficiency and model size."
        }}),
        React.createElement(FindingCard, {{
            title: "Monolingual Models: Unexpected Champions",
            description: "Contrary to conventional wisdom, adapted English-centric models like LLaMA-2 outperform base multilingual models on various tasks, even for low-resource languages. This finding challenges the long-held belief that multilingual models are always superior for non-English tasks. In tests across 20 diverse languages, adapted LLaMA-2 models showed a 15-30% improvement in performance metrics compared to multilingual baselines. Surprisingly, these adapted models excelled in tasks requiring deep cultural understanding, such as idiomatic expression translation and context-dependent sentiment analysis. For languages like Vietnamese and Swahili, the adapted models even outperformed some native language models in complex reasoning tasks.",
            chart: React.createElement(ModelComparisonChart),
            note: "Adapted monolingual models show superior performance across all tasks, including summarization which base multilingual models couldn't perform."
        }}),
        React.createElement(FindingCard, {{
            title: "Cross-Lingual Transfer Effectiveness",
            description: "The study reveals significant variations in the effectiveness of cross-lingual transfer across different linguistic aspects. Syntax and morphology transfer well between languages, with an average success rate of 75% across 30 language pairs tested. However, semantics and pragmatics prove more challenging, showing only a 40% successful transfer rate. Interestingly, the effectiveness of transfer correlates strongly with linguistic typology rather than language family. For instance, SOV languages like Turkish and Japanese showed high mutual transferability (85%) despite being from different families. Pragmatic features, especially those related to politeness and social hierarchy, were the most resistant to transfer, with only a 25% success rate even between closely related languages.",
            chart: React.createElement(CrossLingualTransferChart),
            note: "This radar chart shows the effectiveness of cross-lingual transfer across different linguistic aspects. Higher values indicate better transfer."
        }}),
        React.createElement(FindingCard, {{
            title: "Language Adaptation Priorities",
            description: "When adapting a model to a new language, the research identifies clear priorities in the adaptation process. Vocabulary and grammar adjustments prove to be the most crucial, accounting for 60% of the performance improvement in our experiments across 15 languages. Cultural context and idiomatic expressions follow, contributing 25% to the overall adaptation success. Surprisingly, phonological features, often overlooked in text-based models, account for 10% of the improvement, particularly in tone languages like Mandarin and Yoruba. The remaining 5% is attributed to discourse-level features. We found that the optimal adaptation strategy varies by language: agglutinative languages like Finnish benefit most from morphological focus, while isolating languages like Vietnamese require more emphasis on contextual and tonal adaptations.",
            chart: React.createElement(LanguageAdaptationTreemap),
            note: "This treemap visualizes the relative importance of different aspects in language adaptation. Larger areas indicate higher priority."
        }})
    );
}};

ReactDOM.render(
    React.createElement(LanguageSpecificLLMDashboard),
    document.getElementById('root')
);
</script>
</example>
</examples>

The assistant should produce output in this format, with a summary section and a script section containing the React and Recharts code for the visualization. The full HTML structure is not required, as it will be part of the template.

</visualization_info>

<whitepaper>
{title}
{content}
</whitepaper>"""
