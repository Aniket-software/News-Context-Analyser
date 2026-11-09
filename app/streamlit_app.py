
import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from claim_analyzer import ClaimAnalyzer


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Context | Intelligence & Research",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# STYLING
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --paper: #F5F4F0;
    --white: #FFFFFF;
    --ink: #202522;
    --muted: #858B84;
    --line: #E5E4DE;
    --green: #526C5B;
    --green-light: #E9EFE9;
    --red: #A45E55;
    --red-light: #F5EAE8;
    --blue: #526A80;
}

.stApp {
    background: var(--paper);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1280px;
    padding-top: 3rem;
    padding-bottom: 4rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: #202923;
    border-right: 1px solid #303A33;
    min-width: 220px;
    max-width: 220px;
}

[data-testid="stSidebar"] > div:first-child {
    width: 220px;
}

[data-testid="stSidebar"] * {
    color: #E8EAE5 !important;
}

.sidebar-brand {
    font-family: 'Playfair Display', serif;
    font-size: 29px;
    color: #F3F0E8;
    margin-top: 12px;
}

.sidebar-subtitle {
    color: #A6B0A5 !important;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
}

.sidebar-section {
    color: #91A094 !important;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin-top: 48px;
    margin-bottom: 12px;
}

.sidebar-item {
    color: #D7DED6 !important;
    font-size: 13px;
    padding: 11px 12px;
    border-radius: 4px;
    background: #303B33;
    margin-bottom: 8px;
}

.sidebar-note {
    color: #A6B0A5 !important;
    font-size: 11px;
    line-height: 1.8;
}

/* Header */

.topline {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid var(--line);
    padding-bottom: 17px;
    margin-bottom: 34px;
}

.topline-label {
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 700;
    color: #777E75;
}

.topline-status {
    font-size: 12px;
    color: #294D37;
    background: #E1EADF;
    padding: 9px 13px;
    border: 1px solid #B9CBB8;
    border-radius: 3px;
    letter-spacing: 1px;
    font-weight: 700;
    white-space: nowrap;
}

.eyebrow {
    color: var(--green);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(38px, 5vw, 57px);
    font-weight: 500;
    letter-spacing: -1.8px;
    line-height: 1.12;
    color: #252C26;
    margin-bottom: 13px;
}

.hero-description {
    max-width: 660px;
    color: #727970;
    font-size: 14px;
    line-height: 1.9;
    margin-bottom: 32px;
}

/* Sections */

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 25px;
    font-weight: 500;
    color: #29322B;
    margin-bottom: 5px;
}

.section-description {
    color: #82877F;
    font-size: 12px;
    margin-bottom: 20px;
}

.section-number {
    color: #8B978B;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

/* Input */

.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1px solid #DFE1D9 !important;
    border-radius: 3px !important;
    color: #29322B !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
    padding: 16px !important;
}

.stTextArea textarea:focus {
    border-color: #788B79 !important;
    box-shadow: 0 0 0 1px #788B79 !important;
}

/* Buttons */

.stButton button,
.stFormSubmitButton button {
    background: #29372E !important;
    border: 1px solid #29372E !important;
    color: #FFFFFF !important;
    border-radius: 3px !important;
    min-height: 43px;
    padding: 0 23px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: .4px;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #405747 !important;
    border-color: #405747 !important;
}

/* Metrics */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 3px;
    padding: 20px;
}

[data-testid="stMetricLabel"] {
    color: #7E867C;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif;
    color: #29372E;
    font-size: 29px;
}

/* Verdict */

.finding-card {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-left: 4px solid var(--green);
    padding: 25px 28px;
    margin: 15px 0 25px 0;
}

.finding-label {
    font-size: 10px;
    color: #838B80;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.finding-value {
    font-family: 'Playfair Display', serif;
    color: #29372E;
    font-size: 32px;
    font-weight: 500;
}

.finding-caption {
    color: #82877F;
    font-size: 12px;
    margin-top: 8px;
    line-height: 1.7;
}

/* Evidence */

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 3px;
    margin-bottom: 10px;
}

[data-testid="stExpander"] summary {
    font-size: 13px;
    font-weight: 600;
    color: #29372E;
    padding: 12px;
}

[data-testid="stExpander"] summary:hover {
    color: var(--green);
}

/* Progress bar */

[data-testid="stProgressBar"] > div > div {
    background-color: #526C5B;
}

/* Footer */

hr {
    border: none;
    border-top: 1px solid var(--line);
    margin: 29px 0;
}

.footer {
    border-top: 1px solid var(--line);
    padding-top: 22px;
    margin-top: 50px;
    color: #969A91;
    font-size: 10px;
    letter-spacing: 1px;
    text-align: center;
}

/* Hide default Streamlit elements */

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

.stDeployButton {
    display: none;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

@st.cache_resource
def load_analyzer():
    return ClaimAnalyzer()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">Context.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Research & Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">01 &nbsp; Claim Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">ABOUT THE PROJECT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-note">'
        'An experimental research tool combining text classification, '
        'semantic search and natural language inference to examine '
        'news claims against a retrieved article collection.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">ANALYSIS PIPELINE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-note">'
        '01 &nbsp; Machine learning classification<br><br>'
        '02 &nbsp; Semantic evidence retrieval<br><br>'
        '03 &nbsp; Natural language inference<br><br>'
        '04 &nbsp; Evidence assessment'
        '</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown("""
<div class="topline">
    <div class="topline-label">CONTEXT / CLAIM ANALYSIS</div>
    <div class="topline-status">RESEARCH WORKSPACE</div>
</div>

<div class="eyebrow">INDEPENDENT ANALYSIS WORKSPACE</div>

<div class="hero-title">
    Every claim has<br>another side.
</div>

<div class="hero-description">
    Examine news statements through machine learning and retrieved
    evidence. Explore what supports a claim, what challenges it,
    and where the available context falls short.
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CLAIM INPUT
# --------------------------------------------------

st.markdown(
    '<div class="section-number">01 / SUBMISSION</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">What are we examining?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Enter a headline, statement or factual claim for analysis.'
    '</div>',
    unsafe_allow_html=True
)

with st.form("claim_form"):

    claim = st.text_area(
        "NEWS CLAIM",
        placeholder=(
            "For example: North Korea experienced rising fuel prices "
            "after UN sanctions."
        ),
        height=125,
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button(
        "RUN ANALYSIS   →"
    )


# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------

if submitted:

    if not claim.strip():

        st.warning("Please enter a claim before continuing.")

    else:

        try:

            with st.spinner("Retrieving and examining evidence..."):

                analyzer = load_analyzer()
                result = analyzer.analyze_claim(claim.strip())

            st.session_state["analysis_result"] = result

        except Exception as error:

            st.error(f"Analysis failed: {error}")


# --------------------------------------------------
# REPORT
# --------------------------------------------------

if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]

    st.markdown("<hr>", unsafe_allow_html=True)

    # FINDINGS

    st.markdown(
        '<div class="section-number">02 / FINDINGS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Analysis report</div>',
        unsafe_allow_html=True
    )

    st.markdown("**Claim under examination**")
    st.write(result["claim"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "ML classification",
            result["ml_prediction"]
        )

    with col2:
        st.metric(
            "Model confidence",
            f'{result["ml_confidence"] * 100:.2f}%'
        )

    with col3:
        st.metric(
            "Articles retrieved",
            result["total_evidence"]
        )

    # OVERALL ASSESSMENT

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-number">03 / OVERALL ASSESSMENT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="finding-card">
            <div class="finding-label">PRELIMINARY EVIDENCE VERDICT</div>
            <div class="finding-value">{result["overall_verdict"]}</div>
            <div class="finding-caption">
                Assessment based on the stance of retrieved articles.
                This is not an independent confirmation of factual truth.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # EVIDENCE SUMMARY

    st.markdown(
        '<div class="section-title">Evidence breakdown</div>',
        unsafe_allow_html=True
    )

    summary = result["stance_summary"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Entailment", summary["entailment"])
    col2.metric("Contradiction", summary["contradiction"])
    col3.metric("Neutral", summary["neutral"])

    # SOURCE REVIEW

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-number">04 / SOURCE REVIEW</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Retrieved articles</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Explore the original headlines, publication details and '
        'model-assessed relationship to the submitted claim.'
        '</div>',
        unsafe_allow_html=True
    )

    for index, item in enumerate(
        result["retrieved_evidence"],
        start=1
    ):

        title = item.get("title", "Untitled article")
        date = item.get("date", "Date unavailable")
        subject = item.get("subject", "Unknown category")

        stance = item["stance"].upper()

        with st.expander(
            f"ARTICLE {index:02d}  /  {stance}  —  {title}"
        ):

            # ARTICLE INFORMATION

            st.markdown(f"**{title}**")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.caption("PUBLICATION DATE")
                st.write(date)

            with col2:
                st.caption("CATEGORY")
                st.write(subject)

            with col3:
                st.caption("DATASET LABEL")

                label = (
                    "Real"
                    if item["dataset_label"] == 1
                    else "Fake"
                )

                st.write(label)

            st.divider()

            # SEMANTIC SIMILARITY

            st.markdown("**SEMANTIC SIMILARITY**")

            similarity = max(
                0.0,
                min(1.0, item["similarity"])
            )

            st.progress(similarity)

            st.write(f"{similarity:.2%}")

            st.divider()

            # ARTICLE CONTENT

            st.markdown("**ARTICLE CONTENT**")

            st.write(item["article"])

            st.divider()

            # NLI ASSESSMENT

            st.markdown("**NLI MODEL ASSESSMENT**")

            scores = item["nli_scores"]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Entailment",
                    f'{scores.get("entailment", 0) * 100:.2f}%'
                )

            with col2:
                st.metric(
                    "Contradiction",
                    f'{scores.get("contradiction", 0) * 100:.2f}%'
                )

            with col3:
                st.metric(
                    "Neutral",
                    f'{scores.get("neutral", 0) * 100:.2f}%'
                )

    # METHODOLOGY

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("**Methodology & limitations**")

    st.caption(
        "The classification model learns patterns from its training "
        "dataset. Retrieved articles come from the project's existing "
        "corpus. Similarity is not proof of relevance or truth, and "
        "NLI scores are model estimates rather than factual probabilities. "
        "The overall verdict is generated using simple stance-counting "
        "rules. Independent, up-to-date source verification is not "
        "currently implemented."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    CONTEXT. &nbsp; / &nbsp; AI NEWS CONTEXT & CLAIM ANALYSER
    <br><br>
    EXPERIMENTAL RESEARCH SOFTWARE
</div>
""", unsafe_allow_html=True)
