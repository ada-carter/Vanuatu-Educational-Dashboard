import streamlit as st
import pandas as pd
import plotly.express as px
import os
from data_loader import load_data
from visualizations import *
from detailed_enrollment_visualizations import *  # Import the new script
import plotly.graph_objects as go
import json
import numpy as np

# Page configuration
st.set_page_config(layout="wide", page_title="Vanuatu Education Report")

# Add flag image to the top left
st.image("data/Flag_of_Vanuatu.svg", width=50)
# Load data 
try:
    data = load_data()
    # Exclude national row in "Enrollment by School Type" if present
    for key in ["Enrollment by School Type"]:
        if "Province" in data[key].columns:
            data[key] = data[key][data[key]["Province"] != "National"]
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Report Header and Executive Summary
col1, col2 = st.columns([3, 1])

with col1:
    st.title("State of Education in Vanuatu: Comprehensive Analysis")
    st.markdown("*EDUC 310 Final Project - Ada Carter University of Washington*")
    
    # -----------------------------------------------------------------------------
    # Executive Summary
    # -----------------------------------------------------------------------------
    st.header("Executive Summary")
    st.markdown("""
    ### Executive Summary
    Vanuatu's education system has been the focus of ongoing reforms aimed at enhancing teaching quality, strengthening multilingual pedagogies, integrating traditional ecological knowledge (TEK), and improving student learning outcomes. Positioned within a broader context of cultural and linguistic diversity, as well as unique environmental challenges, these reforms have sought to address high attrition rates and notable disparities in educational access between provinces.

    **Key Findings**  
    1. **Decolonizing Educational Frameworks**  
       - Vanuatu's postcolonial journey includes a gradual shift toward valuing vernacular languages, Bislama, 
         and culturally grounded curricula. Early-childhood instruction in local languages supports student engagement 
         and literacy development. Over time, these policies reflect an effort to decolonize education by embracing 
         indigenous languages and knowledge.  

    2. **Curriculum and TEK Integration**  
       - Recent curriculum reforms emphasize learner-centered methods and the inclusion of TEK. These changes help reinforce 
         cultural identity and environmental stewardship, reflecting a broader move toward holistic, context-relevant education. 
         By embedding local knowledge of ecosystems and practices into lessons, schools foster students' connection to their 
         heritage and surroundings.  

    3. **Teacher Development and Sustainability**  
       - Professional development initiatives have led to improved teaching quality and inclusive practices. However, 
         challenges persist, especially for rural and remote schools, highlighting the need for sustained investment 
         and follow-up support. Limited resources and geographic isolation mean that ongoing mentorship and equitable 
         distribution of materials remain critical for long-term success.

    Additional sections below detail Vanuatu's historical and policy context, language-in-education practices, 
    gender equity considerations, resource distribution, demographic trends, and recommendations for future 
    directions.
    """)

with col2:
    # Create iframe for OpenStreetMap - zoomed in on Vanuatu
    st.markdown("""
    <iframe width="100%" height="800" frameborder="0" scrolling="no" marginheight="10" marginwidth="0"
    src="https://www.openstreetmap.org/export/embed.html?bbox=166.0,-20.0,169.0,-14.0&layer=mapnik&marker=-16.5,167.5">
    </iframe>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Expanded Introduction and Historical Context
# -----------------------------------------------------------------------------
st.subheader("Introduction and Historical Background")

col1, col2 = st.columns([1,1])

with col1:
    # Create language distribution pie chart
    language_data = pd.DataFrame({
        'Language': ['Indigenous Languages', 'Bislama', 'English', 'French'],
        'Percentage': [82.6, 14.5, 2.1, 0.8]
    })

    fig = px.pie(
        language_data, 
        values='Percentage', 
        names='Language',
        title='Language Distribution in Vanuatu (2020)',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_x=0.5,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    ### Introduction and Historical Background
    Vanuatu stands out as a nation with an exceptional level of linguistic diversity; with an estimated 138 indigenous languages, it has the world's highest linguistic density​ of over 82% of the population primarily speaks one of these 100+ indigenous languages, alongside Bislama (a creole lingua franca blending colonial and indigenous influences). Despite this rich linguistic tapestry, Vanuatu officially recognizes only three languages: English, French, and Bislama. This discrepancy between a diverse spoken landscape and a limited set of official languages presents inherent challenges in the education system. The disparity complicates standardized instruction and curriculum development. Creating educational materials and training teachers to effectively teach in so many languages is a complex undertaking. This can lead to inequities in access and outcomes, potentially marginalizing students who do not speak the official languages. The challenge lies in finding innovative, culturally sensitive approaches that harness linguistic diversity while ensuring all students have access to quality education.
    """)

st.markdown("""

""")

st.markdown("""
### Independence Movement and Self-Reliance Ideology
Vanuatu's 1970s independence movement was deeply influenced by socialist and anti‑colonial ideas. The leading party, Vanua'aku Pati (VP), espoused a philosophy of self‑reliance and Melanesian socialism as an alternative to colonial dependency. Father Walter Lini—an Anglican priest and the first Prime Minister—was a key figure who openly embraced socialist ideals in a Melanesian context (Premdas, 1987). He drew inspiration from leaders like Tanzania's Julius Nyerere, frequently praising "the good thoughts" of his "comrade Nyerere" in speeches (Premdas, 1987). Lini's concept of Melanesian socialism blended communal indigenous values with Christian and socialist principles, emphasizing collective welfare, egalitarian decision-making, and local empowerment (Premdas, 1987). This ideological foundation framed education as a tool for nation‑building and self‑determination, rejecting the notion that development should mirror former colonial powers' models.
""")

# Create tabs for detailed education reforms content
reform_era_tabs = st.tabs([
    "Radical Reforms (1980s)", 
    "Lini's Influence", 
    "Evolution & Challenges",
    "Kastom & Modern Values",
    "Reform Legacy"
])

with reform_era_tabs[0]:
    st.markdown("""
    Upon achieving independence in 1980, the new government moved swiftly to reshape the education system along self‑reliant lines. The dual British–French colonial school networks were unified under a national Ministry of Education, and officials aimed to indigenize curricula and expand access (David, 2020). Prime Minister Lini's first education plan made primary schooling compulsory for ages 6–11 and targeted a 20% increase in primary schools (David, 2020). 
    
    Crucially, these quantitative goals were tied to a radical qualitative shift: colonial curricula were to be overhauled to serve local needs (David, 2020). It was "no longer a question of bringing children the 'enlightenment' of British or French education, but of preparing them to take charge of their country" (David, 2020). Schools were encouraged to teach practical skills and local content so that graduates could use their knowledge for rural community development rather than migrating to towns (David, 2020). 
    
    Education was seen as a "lever of development" to foster self‑sufficient villages—for example, by training youth to become farmers, artisans, or entrepreneurs who would revitalize the local economy (David, 2020). This early post‑independence vision explicitly linked education with economic self‑reliance and the reduction of colonial‑era inequalities.
    """)

with reform_era_tabs[1]:
    st.markdown("""
    ### Vanua'aku Pati and Father Lini's Influence
    The socialist-oriented Vanua'aku Pati government under Father Walter Lini was the driving force behind these transformative policies. Lini's personal influence ensured that Melanesian socialism was more than rhetoric—it informed concrete reforms in schooling, land, and local governance (Premdas, 1987). For instance, the VP's development slogan of the 1980s centered on achieving economic self-reliance, and education was reoriented to support this national goal (David, 2020)​. Lini believed education should produce citizens capable of "self-help" and stewardship of their resources, reflecting both Marxist and Christian principles of social justice (David, 2020). Under his leadership, the government promoted vernacular literacy programs and rural training centers to reach communities outside the formal school system (McCormick, 2016; Premdas, 1987)​. Organizations such as the Vanuatu Rural Development Training Centres Association (VRDTCA) emerged to provide non-formal education in villages, teaching basic vocational skills to those with little formal schooling. By empowering local people through education, Lini and the Vanua'aku Pati saw themselves as fostering a "Melanesian renaissance"—a revival of indigenous values and knowledge suppressed under colonial rule (McCormick, 2016; Premdas, 1987).
    """)

with reform_era_tabs[2]:
    st.markdown("""
    ### Challenges and Evolution of Education Policy
    Despite the bold start, implementing these radical reforms proved challenging over time. Vanuatu's small size and colonial legacy created practical constraints that tempered the revolution in education. Scholars note that formal, Western-style educational planning often clashed with local cultural realities; the process "has often been subverted by tensions based in local cultural contexts" (Hindson, 1995)​. In the early 1980s, political strains including a secessionist revolt on Espiritu Santo in 1980 and later frequent changes of government hindered steady progress in the education sector (Hindson, 1995). The inherited bilingual system (with distinct English and French streams) also complicated unified policy-making (Hindson, 1995). As the 1990s unfolded, economic austerity under the Comprehensive Reform Program (1997) reduced public spending, affecting schools and staffing. Many of Lini's socialist initiatives (e.g. cooperatives and communal development schemes) waned amid a turn to market-oriented policies. 
    Yet the core ideals did not disappear. Community-based education efforts and church-run schools continued to instill values of service and self-help at the local level.By the early 21st century, the government re-emphasized education access and equity — notably introducing fee-free primary education in 2010 to uphold the principle that basic education is a universal right (School‑Community Relations and Fee‑Free Education Policy in Vanuatu, n.d.)​. The balance between the revolutionary zeal and practical realities led to a hybrid approach: while standard curricula and donor-driven projects took root, Vanuatu also sought to preserve the spirit of independence-era reforms wherever possible.
    """)

st.markdown("### Timeline of Key Educational Developments")
# Prepare timeline data with key events only
timeline_data = [
    {"year": "1980", "numeric_year": 1980, "short_label": "Independence", 
     "event": "Independence achieved; dual British-French school systems unified"},
    {"year": "1985", "numeric_year": 1985, "short_label": "Vernacular programs", 
     "event": "Vernacular literacy programs and rural training centers established"},
    {"year": "1997", "numeric_year": 1997, "short_label": "Economic reforms", 
     "event": "Comprehensive Reform Program introduces economic austerity"},
    {"year": "2010", "numeric_year": 2010, "short_label": "Fee-free education", 
     "event": "Fee-free primary education introduced"},
    {"year": "2012", "numeric_year": 2012, "short_label": "Traditional economy", 
     "event": "National Council of Chiefs advocates for 'traditional economy' in curriculum"},
    {"year": "2015", "numeric_year": 2015, "short_label": "Vernacular integration", 
     "event": "Increased integration of vernacular languages in early education"}
]

# Convert list to DataFrame and sort chronologically
timeline_df = pd.DataFrame(timeline_data)
timeline_df = timeline_df.sort_values('numeric_year')

fig = go.Figure()
# Create alternating positions above and below the timeline
for i, row in timeline_df.iterrows():
    y_val = 0.5 if i % 2 == 0 else -0.5
    
    # Define text position before using it
    text_pos = "top center" if i % 2 == 0 else "bottom center"
    
    # Add marker and label
    fig.add_trace(go.Scatter(
        x=[row["numeric_year"]],
        y=[y_val],
        mode="markers+text",
        marker=dict(
            size=14,
            color="#2b5797",
            line=dict(width=2, color="DarkSlateGrey")
        ),
        text=[row["short_label"]],
        textposition=text_pos,
        hovertext=f"<b>{row['year']}</b><br>{row['event']}",
        hoverinfo="text"
    ))
    text_pos = "top center" if i % 2 == 0 else "bottom center"
    
    # Add dotted line connector
    fig.add_shape(
        type="line",
        x0=row["numeric_year"],
        y0=0,
        x1=row["numeric_year"],
        y1=y_val,
        line=dict(color="gray", width=1, dash="dot")
    )
    
    # Add marker and label
    fig.add_trace(go.Scatter(
        x=[row["numeric_year"]],
        y=[y_val],
        mode="markers+text",
        marker=dict(
            size=14,
            color="#2b5797",
            line=dict(width=2, color="DarkSlateGrey")
        ),
        text=[row["short_label"]],
        textposition=text_pos,
        hovertext=f"<b>{row['year']}</b><br>{row['event']}",
        hoverinfo="text"
    ))

# Define timeline bounds
min_year = timeline_df['numeric_year'].min() - 2
max_year = timeline_df['numeric_year'].max() + 2

# Draw the main timeline
fig.add_shape(
    type="line",
    x0=min_year,
    y0=0,
    x1=max_year,
    y1=0,
    line=dict(color="gray", width=2)
)

# Update layout for a more compact display - removed decade markers and year labels
fig.update_layout(
    template="simple_white",
    showlegend=False,
    xaxis=dict(
        title="Year",
        range=[min_year, max_year],
        tickmode="linear",
        dtick=10,
        zeroline=False,
        showticklabels=False  # Hide the year labels on the x-axis
    ),
    yaxis=dict(visible=False, range=[-0.8, 0.8]),
    margin=dict(l=20, r=20, t=30, b=50),
    height=350,
    hoverlabel=dict(bgcolor="white", font_size=14)
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("""
### Kastom, Melanesian Values, and Contemporary Reforms

In the 21st century, Vanuatu's education policy continues to be shaped by the ideals of self-determination and respect for kastom (customary culture). The discourse of decolonizing education remains prominent, invoked by policymakers and civil society alike (McCormick, 2016). Recent national plans explicitly reference the importance of indigenous knowledge and languages in schooling.

In 2012, the National Council of Chiefs (Malvatumauri) successfully advocated for recognizing the "traditional economy"—subsistence agriculture, customary exchanges, and indigenous skills—as a foundation for the national curriculum and development strategy (McCormick, 2016). This shows a continued effort to value local ways of learning and living alongside formal education.

As a result, early-grade instruction in many schools now includes vernacular languages and cultural content, helping bridge students' community life with academic learning. Such measures echo the original post-independence aim of aligning education with Melanesian values. Studies confirm that the "decolonising discourses of self‑reliance" from the independence era still inform Vanuatu's education and development policies today (McCormick, 2016).

In practice, schools are encouraged to work with local communities, use local examples in teaching, and produce graduates who are not only globally competent but also firmly rooted in their culture and capable of contributing to their villages.

### Legacy of Early Reforms and Key Modern Figures

The legacy of Vanuatu's early socialist education reforms is visible in contemporary policy and leadership. Concepts like **self-reliance**, **community participation**, and **social equity** remain cornerstones of educational planning. Modern leaders and scholars have rejuvenated these themes in current initiatives.

For instance, politician Ralph Regenvanu has championed the preservation of kastom and promoted the idea of a kastom-based education as part of a broader "traditional economy" revival (McCormick, 2016). Likewise, educators at tertiary institutions such as the University of the South Pacific continue to emphasize Melanesian pedagogy—teaching methods that integrate storytelling, communal activities, and respect for elders—reflecting Vanuatu's cultural context.

The Ministry of Education's vision statement today still calls for students to gain "the skills, values, and confidence to be self‑reliant," underscoring continuity with the independence generation's goals. In recent years, Vanuatu has navigated global education agendas (e.g., the Sustainable Development Goals) on its own terms: policymakers engage with international standards but filter them through local priorities of resilience and self-determination (McCormick, 2016).

In summary, while the revolutionary zeal of the 1970s–80s has been tempered by experience, Vanuatu's 21st-century education system remains guided by the ethos of Melanesian socialism—valuing communal welfare, cultural pride, and the capacity for Ni-Vanuatu to shape their own future through education (McCormick, 2016).
""")

# -----------------------------------------------------------------------------
# Vanuatu in Global Context (HPI and Comparisons)
# -----------------------------------------------------------------------------
st.header("Vanuatu in Global Context")
try:
    hpi_data = pd.read_csv("data/hpi.csv")
except Exception as e:
    st.error(f"Error loading HPI data: {e}")
    hpi_data = None

st.markdown("""
Vanuatu consistently ranks high in the Happy Planet Index (HPI), reflecting relatively strong well-being outcomes paired with a low ecological footprint. In contrast, countries with high per-capita consumption (like the United States) often rank lower. This suggests that Vanuatu's focus on social cohesion, cultural vitality, and environmental stewardship aligns with broader measures of sustainable well-being. Educational policy in Vanuatu contributes to this balance by emphasizing community and environment, rather than purely economic metrics.
""")

if hpi_data is not None:
    metrics = {
        'HPI': {
            'description': 'Happy Planet Index - measures sustainable wellbeing for all', 
            'inverse': False
        },
        'Life Expectancy in Years': {
            'description': 'Average number of years a person is expected to live', 
            'inverse': False
        },
        'Ladder Of Life': {
            'description': 'Subjective wellbeing score (0-10)', 
            'inverse': False
        },
        'Ecological Footprint': {
            'description': 'Per capita Ecological Footprint (global hectares) - lower is better', 
            'inverse': True
        }
    }
    
    available_countries = sorted(hpi_data['country'].unique().tolist())
    default_country = "United States" if "United States" in available_countries else available_countries[0]
    user_country = st.selectbox(
        "Select a country for comparison:", 
        available_countries, 
        index=available_countries.index(default_country)
    )
    
    metric_tabs = st.tabs(list(metrics.keys()))
    
    for i, (metric, info) in enumerate(metrics.items()):
        with metric_tabs[i]:
            metric_data = hpi_data.copy().dropna(subset=[metric])
            
            # Format numbers for display
            if metric == 'HPI':
                metric_data[metric] = metric_data[metric].apply(lambda x: float(f"{x:.1f}"))
            
            metric_data['ranking'] = metric_data[metric].rank(
                ascending=info['inverse'], 
                method='min'
            ).astype(int)
            
            # Get reference data
            vanuatu_data = metric_data[metric_data['country'] == 'Vanuatu'].copy()
            user_country_data = metric_data[metric_data['country'] == user_country].copy()
            other_data = metric_data[~metric_data['country'].isin(['Vanuatu', user_country])]
            
            total_countries = len(metric_data)
            vanuatu_rank = int(vanuatu_data['ranking'].iloc[0]) if not vanuatu_data.empty else "N/A"
            user_country_rank = int(user_country_data['ranking'].iloc[0]) if not user_country_data.empty else "N/A"
            
            col1, col2 = st.columns([2,1])
            
            with col1:
                st.write(f"**{info['description']}**")
                if vanuatu_rank != "N/A":
                    st.write(f"Vanuatu ranks **{vanuatu_rank}** out of {total_countries} countries")
                if user_country_rank != "N/A":
                    st.write(f"{user_country} ranks **{user_country_rank}** out of {total_countries} countries")
                
                # Get top/bottom 10 countries for plotting
                if info['inverse']:
                    plot_data = other_data.nsmallest(10, metric).copy()
                else:
                    plot_data = other_data.nlargest(10, metric).copy()
                
                # Always include Vanuatu and selected country
                for special_data in [vanuatu_data, user_country_data]:
                    if not special_data.empty:
                        plot_data = pd.concat([plot_data, special_data])
                
                # Sort the data
                plot_data = plot_data.sort_values(metric, ascending=info['inverse'])
                
                # Create the bar chart
                color_scale = px.colors.sequential.YlGn_r if info['inverse'] else px.colors.sequential.YlGn
                fig = px.bar(
                    plot_data,
                    x='country',
                    y=metric,
                    title=f'{"Lowest" if info["inverse"] else "Highest"} Values for {metric}',
                    color=metric,
                    color_continuous_scale=color_scale
                )
                
                fig.update_layout(
                    showlegend=False,
                    xaxis=dict(
                        tickangle=45,
                        tickmode='array',
                        tickvals=plot_data['country'],
                        ticktext=[
                            f'<b>{c}</b>' if c in ['Vanuatu', user_country] else c 
                            for c in plot_data['country']
                        ]
                    ),
                    height=500,
                    margin=dict(b=100)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("Rankings (sorted by performance):")
                
                # Prepare dataset for display
                display_data = metric_data[['country', metric, 'ranking']].copy()
                # Format numbers based on metric type
                if metric == 'HPI':
                    display_data[metric] = display_data[metric].apply(lambda x: '{:.1f}'.format(float(x)))
                else:
                    display_data[metric] = display_data[metric].apply(lambda x: '{:.2f}'.format(float(x)))
                
                display_data['ranking'] = display_data['ranking'].astype(int)
                display_data = display_data.sort_values('ranking')
                
                # Calculate Vanuatu's row number
                vanuatu_idx = display_data.index[display_data['country'] == 'Vanuatu'].tolist()[0]
                
                def highlight_countries(row):
                    color = ''
                    if row['country'] == 'Vanuatu':
                        color = 'background-color: #F3E5F5'
                    elif row['country'] == user_country:
                        color = 'background-color: #FFF3E0'
                    return [color] * len(row)
                
                # Style the dataframe
                styled_df = display_data.style.apply(highlight_countries, axis=1)
                
                element = st.dataframe(
                    styled_df,
                    hide_index=True,
                    use_container_width=True,
                    height=400
                )
                
                # Use JavaScript to scroll to Vanuatu's position
                row_height = 35  # Approximate height of each row in pixels
                scroll_position = max(0, (vanuatu_idx * row_height) - 200)
                st.markdown(
                    f"""
                    <script>
                        const element = document.querySelector('.stDataFrame div[data-testid="stDataFrame"] div');
                        element.scrollTop = {scroll_position};
                    </script>
                    """,
                    unsafe_allow_html=True
                )
                
                st.caption("Table automatically scrolls to Vanuatu's position. Vanuatu and selected country are highlighted.")


# -----------------------------------------------------------------------------
# Curriculum Reforms, TEK, and Teacher Development (Inserted from Report)
# -----------------------------------------------------------------------------
st.subheader("Curriculum Reforms and TEK Integration")
st.markdown("""
Recent curriculum reforms aim to improve teaching quality and student engagement by promoting learner-centered pedagogies (Cassity, Cheng, & Wong, 2021; Cassity, Chainey, Cheng, & Wong, 2022; Cassity, Wong, Wendiady, & Chainey, 2023). Key elements of these reforms include:

- **Professional Development of Teachers**: Training modules designed to strengthen lesson planning, encourage collaborative learning, and incorporate local cultural contexts​. This ongoing professional development has improved instructional quality, although consistent follow-up is needed to support teachers in remote areas (Cassity et al., 2023)​
- **Language Transition Skills**: Programs supporting teachers and students in navigating the transition from vernacular languages and Bislama in early years to English or French in later grades, aligning with national bilingual policies​. These help bridge early learning in mother tongues with proficiency in the official languages.
- **Inclusion of Traditional Ecological Knowledge (TEK)**: Efforts to embed local knowledge of ecosystems, agriculture, and cultural practices into science and social studies content. This approach fosters cultural pride, community engagement, and environmental awareness​. For example, lessons incorporate knowledge of medicinal plants or traditional farming techniques (McCarter & Gavin, 2011), connecting students with indigenous wisdom as part of their formal learning.

However, challenges such as limited locally-developed resources, geographical isolation, and variable post-training support underline the need for more sustainable, consistently funded professional learning frameworks (Cassity et al., 2023)​. Ensuring that curriculum reforms take hold across all islands will require continued collaboration between the Ministry of Education, communities, and international partners.
""")

st.subheader("Language-in-Education Practices")
st.markdown("""
#### Bislama and Vernacular Languages
Research has shown the importance of mother-tongue instruction in Vanuatu's early education. Daly and Barbour (2019) show that teachers and community members find vernacular-based instruction crucial for early engagement and literacy, although pressures from national exams and global forces still push the use of English or French in later grades​. Vandeputte-Tavo (2013) observes that acceptance of Bislama as a medium of instruction varies; debates continue over whether Bislama should serve as a primary language of instruction or only as a support language​. Willans (2015) documents practical strategies teachers use to blend local languages with English or French to ensure comprehension, essentially code-switching to help students grasp content​.

#### Multilingualism in Practice
While official policy supports local languages in education, classroom practices differ widely. Some teachers struggle with limited teaching materials in vernacular languages, while others successfully integrate community knowledge and languages to make lessons more relevant and inclusive. Multilingual education in Vanuatu is therefore implemented unevenly: in some schools, young children learn to read and write in their native tongue before adding English or French; in others, the colonial languages dominate from the start. The tension between policy and practice in multilingual education reflects ongoing negotiation between the advantages of mother-tongue instruction and the perceived socioeconomic opportunities tied to English and French​. Strengthening teacher training and providing resources in local languages are seen as vital steps to move multilingual education forward (Willans, 2013, 2015).
""")

st.subheader("Decolonization of Schooling in Vanuatu")
st.markdown("""
#### Colonial Legacy and Independence
Vanuatu's education system was shaped by its unique colonial history as an Anglo-French Condominium. At independence in 1980, the new nation inherited two separate school systems – one English-medium (British) and one French-medium – which created linguistic and cultural divisions in Ni-Vanuatu society. Francophone and Anglophone communities often attended different schools with different curricula, leading to cleavages in educational experience​. After independence, the government recognized that these parallel colonial-era structures were inefficient and divisive, and it began efforts to unify the education administration. Over time, the formerly separate British and French education bureaucracies merged under a single Ministry of Education, culminating in the Education Act of 2014 which formally established one national system instead of two​. This was a crucial step in decolonizing Vanuatu's schooling. Nonetheless, remnants of the dual system persist, most visibly in the continued use of English and French as parallel languages of instruction in schools.

#### Vernacular Languages and Culturally Relevant Curriculum
A cornerstone of decolonizing education in Vanuatu has been the promotion of indigenous languages and knowledge in the classroom. Since independence, educators and policymakers have debated how to reduce reliance on colonial languages (English and French) and better integrate Bislama and vernacular languages (the mother tongues of Ni-Vanuatu) into schooling​. In the late 1990s, this debate led to concrete action. The Education Master Plan 2000–2010 recommended introducing local languages in early education, prompting the government to draft a National Vernacular Education Policy in 1999. Pilot programs were launched in which children were taught in their mother tongue during the first years of primary school, with English or French introduced later​. This marked a radical shift from the colonial model where European languages dominated from Grade 1. By the mid-2010s, the Ministry of Education formally encouraged bilingual literacy: children start schooling in a vernacular language or Bislama, then gradually transition to English or French in later grades​.

This bilingual policy is decolonizing in that it validates Ni-Vanuatu linguistic heritage within formal education, rather than privileging only the former colonial tongues.

#### Indigenous Knowledge and "Kastom" in Schools
Alongside language changes, Vanuatu has sought to indigenize the curriculum by incorporating kastom (traditional knowledge, values, and practices) into education. There was growing recognition that Western-style schooling had marginalized local culture, leading to calls for contextualizing the curriculum to Vanuatu's realities​. Researchers noted that the lack of vernacular language use and local content in schools contributed to the erosion of traditional knowledge in communities. In response, the Vanuatu Cultural Centre and education authorities initiated curriculum reforms around 2010 to infuse courses with traditional ecological knowledge, local history, music, and arts​. 

These efforts aimed to ensure that what students learn in school resonates with their heritage and community life.
""")

# Add tabbed interface with key reforms
reform_tabs = st.tabs(["Unified Administration", "Language Policy", "Bilingual Curriculum", "Integration of Kastom"])

with reform_tabs[0]:
    st.markdown("""
    ### Unified Education Administration (1980s–2010s)
    Merging the dual French/English school systems into one national system under the Ministry of Education, culminating 
    in the Education Act 2014. This eliminated parallel curricula and governance, creating a more cohesive national 
    education structure.
    """)

with reform_tabs[1]:
    st.markdown("""
    ### National Language Policy (1999–2005)
    Development of a vernacular language in education policy to introduce indigenous languages (and Bislama, the lingua franca) 
    as languages of instruction in early primary grades. By using children's first languages in schooling, this policy aims to 
    improve literacy and preserve local languages that were previously excluded from formal classrooms.
    """)

with reform_tabs[2]:
    st.markdown("""
    ### Bilingual Curriculum Reform (2010s)
    Implementation of a new bilingual national curriculum that balances English and French and incorporates vernacular instruction. 
    Students now begin learning in their mother tongue or Bislama, then gradually transition to English or French, an approach 
    designed to strengthen foundational learning and bridge to colonial languages.
    """)

with reform_tabs[3]:
    st.markdown("""
    ### Integration of Kastom and Local Content (2010–present)
    Ongoing revision of curricula to include traditional knowledge, cultural skills, and local examples across subjects. 
    The National Curriculum Framework emphasizes Vanuatu's cultural heritage, and partnerships with the Vanuatu Cultural 
    Centre have helped produce teaching resources on kastom. For instance, local stories and environmental knowledge are 
    used to contextualize literacy and science lessons, validating indigenous perspectives in formal education.
    """)

st.subheader("Education for Resilience and Sustainable Development")
st.markdown("""
Vanuatu's extreme vulnerability to natural hazards (cyclones, earthquakes, volcanic activity) demands robust disaster risk reduction (DRR) education​. Yet historically, formal curricula introduced topics like climate change and disaster preparedness only in later years of schooling, limiting exposure for younger students. Experts suggest that integrating resilience concepts and traditional knowledge at earlier grade levels could strengthen community-level preparedness and adaptive capacity​. For example, lessons for primary-age children can include identifying traditional environmental warning signs and practicing safety drills, so that resilience becomes part of foundational learning.

Incorporating traditional ecological knowledge (TEK) into sustainability education is also seen as vital. McCarter and Gavin (2011) emphasize including ethnobiological knowledge—such as medicinal plants and local agricultural practices—as part of the mainstream curriculum​. This approach enriches science education, fosters local pride, and addresses real-world community challenges by linking classroom learning to the students' own environment. By learning how past generations managed natural resources and coped with environmental stress, students gain tools that are directly relevant to issues like climate change and food security.
""")

st.subheader("Marine Resources and Curriculum Integration")
st.markdown("""
Another critical aspect of sustainable education in Vanuatu is the integration of marine resources and maritime knowledge into curricula. As an island nation, Vanuatu’s economy and cultural practices are closely tied to the ocean, and educational programs have increasingly reflected this connection. For instance, the Vanuatu Maritime College, established in 1999, provides competency‐based training in near‐coastal seamanship, fishing operations, and marine safety, thereby aligning vocational education with the country’s maritime needs (FAO, n.d.-a). These programs range from rural fishing skills to certification of crew for international shipping, ensuring that local people can acquire skills for employment in fishing industries and seafaring careers without leaving Vanuatu (FAO, n.d.-b).
At the primary and secondary school levels, efforts have been made to include marine conservation and resource management in the curriculum. A Teachers’ Resource Kit on Fisheries for Vanuatu (introduced in 2017) integrates fisheries and marine ecology topics into lessons, linking national curriculum objectives with local knowledge of ocean life (SPCCFPSTORE1.blob.core.windows.net, n.d.-a). The kit provides information sheets and activity guides on subjects such as fish species, aquaculture, sustainable fishing practices, and the impacts of climate change on marine ecosystems (SPCCFPSTORE1.blob.core.windows.net, n.d.-b). Community and NGO-led initiatives also complement formal curricula in promoting ocean literacy. For example, conservation groups carry out school programs that teach children—through games and interactive sessions—the importance of protecting marine environments from overfishing and other human-induced changes (OceansWatch.org, n.d.).
""")


# -----------------------------------------------------------------------------
# Population Trends Section
# -----------------------------------------------------------------------------
st.header("Population Trends")
try:
    population_data = pd.read_csv("data/Population.csv")
    
    # Add toggle for school-age only view
    school_age_only = st.checkbox("Show only school-age population (0-19 years)", value=True)
    
    col1, col2 = st.columns([2,1])
    with col1:
        pop_fig = create_population_trend_visualization(population_data, school_age_only)
        st.plotly_chart(pop_fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        **Population Growth Analysis**
        
The population trends in Vanuatu show consistent growth, with a significant portion under 19 years of age. Nearly half of the population is school-aged (0–19), underscoring the urgent need for accessible, high-quality education to serve this youthful demographic. Notably, growth is especially robust in rural areas, which raises logistical challenges for resource distribution and school provisioning in the outer islands. Over the years, increased demand for schooling has put pressure on the teacher workforce and educational infrastructure. Key statistics as of 2020 include: a total population of about 300,000; roughly 144,746 individuals aged 0–19 (approximately 48% of the population); and about 28% population growth since 2009. These trends highlight why expanding educational access remains a top priority. A growing cohort of children each year requires more teachers, classrooms, and learning materials, particularly in remote areas.

        """)
        
        # Calculate and display key statistics
        total_growth = (population_data['Total Population'].iloc[-1] / population_data['Total Population'].iloc[0] - 1) * 100
        school_age_pop = population_data[['0--4', '5--9', '10--14', '15--19']].sum(axis=1).iloc[-1]
        school_age_percent = (school_age_pop / population_data['Total Population'].iloc[-1]) * 100
        
        latest_year = population_data['Year'].max()
        st.markdown(f"""
        **Key Statistics ({latest_year}):**
        - Total Population: {population_data['Total Population'].iloc[-1]:,.0f}
        - School-age Population (0-19): {school_age_pop:,.0f}
        - School-age percentage: {school_age_percent:.1f}%
        - Population growth (2009-2020): {total_growth:.1f}%
        """)

except Exception as e:
    st.error(f"Error loading population data: {e}")

st.header("Higher Education in Vanuatu")

# Create tabs for institution-specific details
tabs = st.tabs([
    "National University of Vanuatu", 
    "USP – Emalus Campus", 
    "Other Institutions"
])

with tabs[0]:
    st.markdown("""
    ### National University of Vanuatu (NUV)
    
    Established under Act No. 34 of 2019 and officially published in January 2020, the National University of Vanuatu (NUV) is a public institution located in Port Vila. NUV consolidates existing post‐secondary entities (such as teacher training, technical, and nursing colleges) to provide comprehensive academic programs. Collaborative degree programs with international partners ensure adherence to global academic standards.
    """)

with tabs[1]:
    st.markdown("""
    ### University of the South Pacific (USP) – Emalus Campus
    
    The University of the South Pacific (USP) is a regional institution jointly owned by 12 Pacific countries. Its Emalus Campus in Port Vila, operating since 1989, offers a primary focus on legal studies alongside additional disciplines through flexible learning approaches. The campus contributes to regional higher education by providing both undergraduate and postgraduate courses.
    """)

with tabs[2]:
    st.markdown("""
    ### Other Recognized Higher Education Institutions in Vanuatu
    
    Vanuatu is also home to several accredited institutions offering vocational and specialized training:
    
    - **Vanuatu Institute of Teacher Education (VITE)** – Founded in 1962, offering diploma programs in teacher education.
    - **Vanuatu Institute of Technology (VIT)** – Established in 1970, delivering certificate and diploma courses in technical and vocational fields.
    - **Vanuatu College of Nursing Education (VCNE)** – Provides a 3-year Diploma in General Nursing with a midwifery component.
    - **Vanuatu Agriculture College (VAC)** – Offers certificate and diploma programs in agriculture.
    - **Vanuatu Maritime College (VMC)** – Established in 1999, specializing in maritime and seafaring skills.
    - **Talua Theological Training Institute (TTTI)** – Since 1986, offering academic programs in theological studies.
    - **Australia-Pacific Technical College (APTC)** – A regional vocational training provider supported by the Australian Government.
    """)

# Persistent Timeline Section (displayed below the tabs)
st.markdown("### Timeline of Higher Education Development in Vanuatu")

# Data for timeline
institutions_data = pd.DataFrame({
    'Institution': ['VITE', 'VIT', 'USP', 'TTTI', 'USP Emalus', 'VMC', 'APTC', 'NUV'],
    'Year': [1962, 1970, 1968, 1986, 1989, 1999, 2006, 2019],
    'Type': ['Specialized', 'Technical', 'Regional University', 'Specialized', 'Regional Campus', 'Technical', 'Technical', 'National University'],
    'Full_Name': [
        'Vanuatu Institute of Teacher Education',
        'Vanuatu Institute of Technology',
        'University of the South Pacific',
        'Talua Theological Training Institute',
        'USP – Emalus Campus',
        'Vanuatu Maritime College',
        'Australia-Pacific Technical College',
        'National University of Vanuatu'
    ]
})

# Color mapping for institution types
color_map = {
    "Specialized": "#1f77b4",
    "Technical": "#ff7f0e",
    "Regional University": "#2ca02c",
    "National University": "#d62728",
    "Regional Campus": "#9467bd"
}

fig = go.Figure()

# Sort data by year to ensure chronological order
institutions_data = institutions_data.sort_values('Year')

# Add markers for each institution on the timeline
for i, row in institutions_data.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['Year']],
        y=[0],
        mode="markers+text",
        marker=dict(
            size=16,
            color=color_map[row['Type']],
            line=dict(width=2, color="DarkSlateGrey")
        ),
        text=[row['Institution']],
        textposition="top center",
        name=row['Institution'],
        hovertemplate=f"<b>{row['Full_Name']}</b><br>Established: {row['Year']}<extra></extra>"
    ))

# Define timeline bounds
min_year = institutions_data['Year'].min() - 5
max_year = institutions_data['Year'].max() + 5

# Draw the main timeline line
fig.add_shape(
    type="line",
    x0=min_year,
    y0=0,
    x1=max_year,
    y1=0,
    line=dict(color="gray", width=2)
)

# Add decade markers with minimal design elements
for decade in range((institutions_data['Year'].min() // 10) * 10, institutions_data['Year'].max() + 10, 10):
    fig.add_shape(
        type="line",
        x0=decade,
        y0=-0.05,
        x1=decade,
        y1=0.05,
        line=dict(color="gray", width=1)
    )
    fig.add_annotation(
        x=decade,
        y=-0.1,
        text=str(decade),
        showarrow=False,
        font=dict(size=10, color="gray")
    )

fig.update_layout(
    template="simple_white",
    title="Timeline of Higher Education Institutions in Vanuatu",
    showlegend=False,
    xaxis=dict(
        title="Year",
        range=[min_year, max_year],
        tickmode="linear",
        dtick=5,
        zeroline=False
    ),
    yaxis=dict(visible=False),
    margin=dict(l=20, r=20, t=50, b=50),
    height=300
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
The development of higher education in Vanuatu has accelerated in recent years, marked most prominently by the establishment of the National University of Vanuatu (NUV). Officially created by Act No. 34 of 2019 and opened in early 2020, NUV is a public institution in Port Vila that consolidates existing post-secondary programs (such as teacher training, technical institutes, and nursing colleges) under one umbrella. NUV also engages in collaborative degree programs with international partners to ensure its offerings meet global academic standards. This milestone reflects Vanuatu's effort to build domestic tertiary capacity and reduce reliance on regional universities abroad (Figure 2 – Timeline of Higher Education Institutions in Vanuatu is referenced here).

#### Access and Affordability
Access to higher education in Vanuatu has historically been limited, but it is gradually improving. Only a small fraction of students progress from secondary school to the tertiary level, due in part to the sharp pyramid shape of the education system. For example, around 8,000 children start primary Grade 1 each year, but only on the order of a few hundred complete Year 13, and an even smaller number enroll in university studies. In concrete terms, Ministry of Education data indicate that in 2019 only 1,064 students were enrolled in Year 13, compared with 8,150 who began in Year 1 in 2007—an approximately 87% attrition rate through the end of secondary (Trauma.massey.ac.nz, n.d.).

Cost has been a major barrier to tertiary participation. Studying abroad (in Fiji, Australia, or France, for instance) incurs high expenses that most Ni-Vanuatu families cannot afford. The government and international donors provide a limited number of scholarships each year (about 40–50) to help bridge this gap. Recognizing the demand, the Vanuatu government has made it a priority to expand local tertiary opportunities so that more students can study "at home" at lower cost. The establishment of NUV and the strengthening of vocational colleges are expected to reduce the need for expensive overseas study, allowing hundreds of students to earn degrees in-country each year.

#### Challenges in Higher Education
Despite recent progress, Vanuatu's higher education system faces several challenges. There are capacity and quality concerns, including a shortage of local faculty with Ph.D. qualifications, limited research output, and a nascent quality assurance framework for programs. Infrastructure limitations are evident as well: universities and colleges have limited classroom space, libraries, and laboratory facilities, constraining the learning environment. Another challenge is alignment with national needs—ensuring that graduates are trained in priority sectors like engineering, medicine, agriculture, and technical sciences that are critical for Vanuatu's development. Moreover, brain drain remains an issue: it is estimated that approximately 80% of Ni-Vanuatu who graduate overseas do not return to work in the domestic public sector, representing a loss of talent for the country.

#### Role of Regional Universities and Workforce Development
For decades, regional universities played an outsized role in shaping Vanuatu's skilled workforce. The University of the South Pacific (USP), for example, with its Emalus Campus in Port Vila, has produced many of Vanuatu's leaders in education, government, and business. Similarly, francophone Ni-Vanuatu have often studied at universities in New Caledonia, Tahiti, or France, given the historical ties. By developing NUV, Vanuatu hopes to retain more talent and tailor higher education to the local context. Courses can be designed to address Vanuatu's unique environment and needs (for instance, programs in disaster risk management or sustainable agriculture that directly apply to local challenges). The establishment of a National University is also a step toward educational sovereignty, a move away from complete reliance on regional institutions and toward building home-grown capacity. With a youthful population (nearly half of Ni-Vanuatu are under 20), investment in tertiary education is crucial for the nation's future, providing advanced skills and knowledge to drive development.
""")

# -----------------------------------------------------------------------------
# Province Data Visualizations Section
# -----------------------------------------------------------------------------
st.header("Province Data Visualizations")

try:
    # Load detailed enrollment data
    detailed_enrollment = data["Detailed Enrollment"]
    detailed_enrollment = preprocess_data(detailed_enrollment)

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Total Enrollment", "Enrollment by Level", "Gender Distribution", "Grade Trends", "Total vs Secondary"
    ])

    with tab1:
        # Total Enrollment by Province
        fig1 = create_total_enrollment_bar_chart(detailed_enrollment)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        # Enrollment by Education Level
        fig2 = create_enrollment_type_pie_chart(detailed_enrollment)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        # Gender Distribution by Education Level
        fig3 = create_gender_distribution_bar_chart(detailed_enrollment)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        # Enrollment Trend by Grade
        fig4 = create_grade_enrollment_line_chart(detailed_enrollment)
        if fig4:
            st.plotly_chart(fig4, use_container_width=True)

    with tab5:
        # Total vs Secondary Enrollment
        fig5 = create_total_vs_secondary_scatter(detailed_enrollment)
        if fig5:
            st.plotly_chart(fig5, use_container_width=True)

except Exception as e:
    st.error(f"Error in Province Data Visualizations: {e}")


# -----------------------------------------------------------------------------
# 3. Gender Equity in Education
# -----------------------------------------------------------------------------
st.header("Gender Equity in Education")
st.subheader("Gender Distribution Analysis")

col1, col_spacer, col2 = st.columns([2, 0.1, 1.9])

with col1:
    try:
        enrollment_details = data["Detailed Enrollment"]
        fig = create_gender_ratio_plot(enrollment_details, "enrollment")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating gender ratio plot: {e}")

with col2:
    # Create tabs to organize the content more effectively
    gender_tabs = st.tabs(["Overview", "Primary Education", "Secondary Education", "Challenges"])
    
    with gender_tabs[0]:
        st.markdown("""
        **Gender Equity Assessment**  
        
        The research base on gender-specific outcomes in Vanuatu shows generally balanced enrollment rates at primary level 
        with some variations at secondary level. Recent policies have helped improve gender parity, though cultural 
        and socioeconomic factors still create barriers in some contexts.
        """)
    
    with gender_tabs[1]:
        st.markdown("""
        **Primary Education**
        
        Parity has largely been achieved in primary schooling (Education.gov.vu, n.d.-a). After some fluctuations 
        (such as a slight dip in girls' enrollment after 2015, possibly due to economic pressures following disasters), 
        the overall gender parity index in basic education has improved.
        """)
        
    with gender_tabs[2]:
        st.markdown("""
        **Secondary Education**
        
        Recent data indicate that at the junior secondary level, girls' enrollment and retention can even surpass 
        that of boys in some cohorts (Education.gov.vu, n.d.-b). In secondary schools there have been years where 
        slightly more females are enrolled than males and females' drop-out rates are consistently lower than males 
        (Education.gov.vu, n.d.-c). This trend of boys leaving school earlier is partly attributable to different 
        social pressures on males (e.g., entering work) and initiatives encouraging girls' education.
        """)
        
    with gender_tabs[3]:
        st.markdown("""
        **Ongoing Challenges**
        
        Disparities still emerge in later schooling, where economic factors, cultural expectations, or early marriage 
        and pregnancy can disproportionately affect girls' continued education. Studies have found that adolescent 
        pregnancy is a major reason for female students dropping out in Vanuatu (Warwick.ac.uk, 2010a; 2010b).
        
        The rate of teen pregnancy in Vanuatu is high compared to other Pacific countries, and once an unmarried girl 
        becomes pregnant, it is often considered shameful or impractical for her to return to school (Warwick.ac.uk, 2010c). 
        
        Additionally, customary norms in some communities still encourage girls to marry at a young age, which can 
        interrupt or terminate their schooling (Naidu, 2010).
        """)

# -----------------------------------------------------------------------------
# 4. Teaching Resources
# -----------------------------------------------------------------------------
st.header("Teaching Resources")
st.subheader("Teacher Distribution and Qualifications")

col1, col2 = st.columns([2,1])
with col1:
    teacher_data = data["Teachers Distribution"]
    fig = create_teacher_distribution(teacher_data)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Create tabs for better organization of the content
    teacher_tabs = st.tabs(["Overview", "Challenges", "Initiatives"])
    
    with teacher_tabs[0]:
        st.markdown("""
        **Teaching Resource Distribution**
        
        Vanuatu faces significant disparities in teacher allocation between urban and rural areas. 
        Recent studies (Cassity et al., 2021-2023) show professional development programs have 
        improved teaching quality, but geographical isolation limits ongoing support for 
        remote teachers.
        """)
    
    with teacher_tabs[1]:
        st.markdown("""
        **Key Challenges**
        
        • **Rural retention**: Higher turnover and vacancy rates in remote islands
        • **Qualifications gap**: Lower proportion of certified teachers in remote areas
        • **Resource shortages**: Limited textbooks in English/French and fewer in local languages
        • **Follow-up support**: Teachers attend training but receive minimal mentoring afterward
        """)
        
    with teacher_tabs[2]:
        st.markdown("""
        **Current Initiatives**
        
        • Volunteer teacher deployment to understaffed schools
        • Housing/salary incentives for remote postings
        • Technology solutions for remote training where feasible
        • Development of vernacular teaching materials through cultural centers
        
        *Addressing these disparities is crucial for equitable education across provinces.*
        """)

# -----------------------------------------------------------------------------
# 5. Age Distribution and Educational Access
# -----------------------------------------------------------------------------
st.header("Age Distribution and Educational Access")
st.subheader("Age-based Enrollment Patterns")

col1, col2 = st.columns([3,1])
with col1:
    age_data = data["Age Distribution"]
    fig = create_age_distribution_analysis(age_data) 
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    **Age Distribution Insights**  
    """)
    
    # Create expandable sections for better organization
    with st.expander("Key Patterns", expanded=True):
        st.markdown("""
        - Early childhood enrollment (under 3) can be sporadic, though many provinces have 
          started to introduce preschool programs in vernacular languages
        - Core age groups (3-4 years) typically see the highest enrollment rates for early learning
        - Over-age enrollment (>6 years in early grades) remains an issue
        - Year-over-year trends indicate gradual improvements in early enrollment
        """)
    
    with st.expander("Detailed Analysis"):
        st.markdown("""
        Early childhood enrollment has historically been low but is improving with new vernacular language programs. The 3-4 year age group now sees better participation rates.

        A persistent challenge is over-age enrollment where children significantly older than expected (e.g., 8-9 year olds in Grade 1-2) are present due to late school entry or repetition.
        
        Dropout rates increase in upper primary and lower secondary years due to:
        - Financial pressures
        - Cultural factors (subsistence work, early marriage)
        - Academic barriers (examination hurdles)
        
        While policies now favor automatic promotion and fee-free basic education, the effects of previous selection practices remain visible in the enrollment patterns.
        """)

# -----------------------------------------------------------------------------
# Insights and Interventions
# -----------------------------------------------------------------------------
st.header("Insights and Interventions")
st.markdown("""
Integrating traditional ecological knowledge (TEK) and local languages from the earliest stages of education can help children and families see schooling as culturally relevant, potentially mitigating late entry and dropout. When the curriculum reflects students' home culture and language, parents are often more supportive of sending young children to school on time, and students themselves feel a greater sense of belonging. Early childhood programs that use local language and culturally familiar content have shown promise in easing the transition into formal education. Additionally, flexible initiatives like "second-chance education" or community-based classes allow over-age learners to re-enter schooling or gain basic literacy outside the formal system. Vanuatu's strong tradition of community involvement is an asset here: villages, chiefs, and church groups have been mobilized in some areas to encourage every child of school age to attend. Going forward, continued monitoring of age-specific enrollment patterns through the Vanuatu Education Management Information System (OpenVEMIS) will be important to identify where progress is being made and where gaps remain.
""")

# -----------------------------------------------------------------------------
# Recommendations and Future Directions
# -----------------------------------------------------------------------------
st.header("Recommendations and Future Directions")
st.markdown("""
Based on the comprehensive analysis above and the findings of multiple studies, the following actions are recommended to strengthen education in Vanuatu:

### Short-term Recommendations

1. **Sustain Teacher Professional Development**: Establish localized mentoring and refresher courses, ensuring teachers in remote areas have consistent, ongoing support. This could involve experienced mentors traveling to outer islands periodically, and creating peer support networks using radio or mobile phone communication for teachers to share experiences.

2. **Enhance Resource Distribution**: Prioritize the distribution of bilingual and vernacular-language teaching materials to underserved provinces. In the immediate term, an audit of textbook availability by language and location should be conducted, with emergency supplies sent to schools that lack core materials.

### Medium-term Strategies

1. **Integrate TEK and Resilience Education**: Strengthen curriculum content around disaster preparedness and climate change at earlier grade levels. Collaborate with local experts and community elders to formalize TEK-based lesson plans so that traditional knowledge (e.g., safe building practices, food preservation methods) becomes part of the taught curriculum.

2. **Improve Data Monitoring**: Invest in the Vanuatu Education Management Information System (OpenVEMIS) to ensure up-to-date and accurate data on enrollment, teacher qualifications, and learning outcomes. Better data will enable more responsive policy adjustments and resource allocation to where needs are greatest.

### Long-term Vision

1. **Consolidate Multilingual Education**: Continue refining language-in-education policy to balance the benefits of vernacular instruction with the economic and global opportunities linked to English and French. This could mean extending bilingual education into higher grade levels and providing pathways for students to become truly trilingual (local language, Bislama, and English/French) by the end of secondary school.

2. **Develop Culturally Anchored Curriculum**: Embed local customs, traditional authority structures, and ecological knowledge across subjects to reinforce community identity and sustainable development. A long-term goal is a curriculum that fully reflects Vanuatu's unique cultural context while equipping students with skills for the modern world. This includes engaging community leaders in curriculum development and review, and periodically updating content to include regional cultural diversity.

Implementing these recommendations will require concerted effort from government agencies, educators, communities, and development partners. Vanuatu's experience since independence shows that educational change is most effective when it involves local voices and adapts global ideas to local realities. By building on the progress made and addressing the gaps with culturally informed strategies, Vanuatu can continue to move toward an inclusive and resilient education system for all Ni-Vanuatu.
""")

# -----------------------------------------------------------------------------
# Methodology and Data Sources
# -----------------------------------------------------------------------------
st.header(" Methodology and Data Sources")
st.markdown("""
**Methodology Overview**: This report synthesizes findings from peer-reviewed studies, government policy documents, and educational data analyses. A mixed-methods approach was used, combining quantitative data (enrollment figures, demographic trends, etc.) with qualitative insights (historical and cultural context).

**Quantitative Analysis**: Enrollment numbers, teacher distribution data, age breakdowns, and well-being indices (e.g., HPI rankings) were analyzed using descriptive statistics, trend analysis, and comparative charts. Using python 3.11.2.

**Qualitative Insights**: Literature on colonial/postcolonial influences, language policy, indigenous knowledge integration, and gender factors provided contextual understanding of ongoing reforms and challenges. Interviews and focus group findings from prior studies (e.g., the Barriers to Education Study 2020) were considered to incorporate community perspectives on issues like dropout causes and resource needs.

**Data Sources**: Key sources of data and information included:
- Vanuatu Ministry of Education and Training (MoET) statistics (for enrollment by year and province, teacher postings, age distributions, etc., including the OpenVEMIS database)
- Happy Planet Index (HPI) rankings and associated indicators for well-being and sustainability
- National census data and population projections (2009–2020) for understanding demographic pressures
- Policy documents such as the Vanuatu Education and Training Sector Strategic Plan 2020–2030 (MoET, 2020) and historical plans (e.g., Education Master Plans) for official targets and frameworks
- Academic journals and reports covering Vanuatu's education (e.g., Comparative Education, International Education Journal, regional conference papers) for analysis of policy implementation and case studies

**Limitations**: Some limitations should be acknowledged. Geographic constraints and infrastructural limitations can lead to gaps in data collection, particularly in remote islands where record-keeping is challenging and surveys are infrequent. Thus, some statistics (e.g., dropout rates or literacy levels) may be estimated with a margin of error. Also, while policies and reforms are well-documented on paper, real-world implementation varies considerably and can be underreported in official statistics. This analysis tried to account for that by including qualitative evidence from specific communities. Nonetheless, the diversity of Vanuatu's islands means educational experiences are not uniform, and exceptions to the general trends discussed may exist.
""")

st.markdown("""
### References 

**Application Form for Diploma in General Nurse Training. (n.d.).** [PDF document]. Retrieved from https://17965218293175009171.googlegroups.com/attach/2ab0d763a40a4/Aplication_Form%20English%20.pdf?part=0.2&vt=ANaJVrEVkJgPvom3cpgumGB4X6c7nkYTUeriTo_ZkxeYqQY78hbrwmfjUpdhH8gva8-Xl1L_HICxmDmFnt8FQUzYzzd0ryfUIXcp2DMvG4B4qaxMr5LQeDM#:~:text=LOCATION%3A%20The%20Vanuatu%20College%20of,all%20the%20people%20in%20Vanuatu

**Cassity, E., Chainey, J., Cheng, J., & Wong, D. (2022).** *Teacher development multi-year study series. 
Vanuatu: Interim report 2.* Australian Council for Educational Research. https://doi.org/10.37517/978-1-74286-659-8  

**Cassity, E., Cheng, J., & Wong, D. (2021).** *Teacher development multi-year study series. Vanuatu: 
Interim report 1.* Australian Council for Educational Research. https://doi.org/10.37517/978-1-74286-672-7  

**Cassity, E., Wong, D., Wendiady, J., & Chainey, J. (2023).** *Teacher development multi-year study series. 
Vanuatu: Final report.* Australian Council for Educational Research. https://doi.org/10.37517/978-1-74286-729-8  

**Cypher Learning. (n.d.).** LMS Best practice: $3.3 million saved with AI-powered course creation. Retrieved from https://www.cypherlearning.com/best-practices/vanuatu-institute-of-technology#:~:text=Image%3A%202024%20Customer%20of%20the,skilled%20labour%20force%20across%20Vanuatu

**Daly, N., & Barbour, J. (2019).** 'Because, they are from here. It is their identity, and it is important': 
teachers' understanding of the role of translation in vernacular language maintenance in Malekula, Vanuatu. 
*International Journal of Bilingual Education and Bilingualism, 24,* 1414–1430. https://doi.org/10.1080/13670050.2019.1604625  

**David, G. (2020).** Vanuatu's 40th anniversary: Review of the first decade of political independence from 1980 to 1990. 
*Pacific Geographies, (54),* 15–24. https://doi.org/10.23791/541524

**DFAT (Australian Government). (2007).** Vanuatu: The Unfinished State – Drivers of Change. Canberra: AusAID/DFAT analysis report.

**FAO. (n.d.-a).** Major fields of interest: Vanuatu Maritime College. Retrieved from https://www.fao.org/4/x7308e/x7308e1n.htm#:~:text=Major%20Fields%20of%20Interest%3A

**FAO. (n.d.-b).** Fishing: Maritime training details. Retrieved from https://www.fao.org/4/x7308e/x7308e1n.htm#:~:text=Fishing%3A

**François, A., Lacrampe, S., Franjieh, M., & Schnell, S. (Eds.). (2015).** *The languages of Vanuatu: Unity and diversity.* 
Canberra, Australia: Asia-Pacific Linguistics, Australian National University.

**Government of Vanuatu, Ministry of Education and Training (MoET). (2020).** Vanuatu Education and Training Sector Strategic Plan 2020–2030. Port Vila: MoET.

**Hindson, C. E. (1995).** Educational planning in Vanuatu – an alternative analysis. *Comparative Education, 31(3),* 
327–338. https://doi.org/10.1080/03050069529010  

**MastersPortal. (n.d.).** Vanuatu Institute of Technology | University Info. Retrieved from https://www.mastersportal.com/universities/14651/vanuatu-institute-of-technology.html#:~:text=VIT%20has%20rich%20roots%20reaching,dual%20language%20programs%20in%201980

**McCarter, J., & Gavin, M. (2011).** Perceptions of the value of traditional ecological knowledge to formal 
school curricula: opportunities and challenges from Malekula Island, Vanuatu. *Journal of Ethnobiology and 
Ethnomedicine, 7,* 38–38. https://doi.org/10.1186/1746-4269-7-38  

**McCormick, A. (2016).** Vanuatu education policy post-2015: "Alternative", decolonising processes for 
"development". *International Education Journal: Comparative Perspectives, 15(3),* 16–29.  

**Ministry of Education and Training. (n.d.-a).** Tertiary Education. Retrieved from https://moet.gov.vu/index.php?id=tertiary-education#:~:text=The%20USP%20Emalus%20campus%20is,for%20local%20and%20overseas%20students

**Ministry of Education and Training. (n.d.-b).** Australia-Pacific Technical College overview. Retrieved from https://moet.gov.vu/index.php?id=tertiary-education#:~:text=The%20APTC%20offers%20Australian%20Certificate,Hospitality%20and%20Community%20Services%20areas

**Ministry of Education and Training. (2024).** JAHVC and VAC Cooperation Framework. Retrieved from https://moet.gov.vu/docs/press-releases/ministry/JAHVC%20and%20VAC%20Cooperation%20Framework_08_2024.pdf#:~:text=On%20August%208%2C%202024%2C%20Vanuatu,Director

**Ministry of Education and Training (MoET). (n.d.).** Non-Governmental Organizations in Education – VRDTCA (Vanuatu Rural Development Training Centres Association). Retrieved from https://moet.gov.vu/

**Naidu, S. (2010).** Right to education for all children in Vanuatu – Are girls getting a fair chance? University of Warwick Legal Studies.
Retrieved from https://warwick.ac.uk/fac/soc/law/elj/lgd/2010_2/naidu/

**National University of Vanuatu. (n.d.-a).** Overview. Retrieved from https://www.univ.edu.vu/en/structure/overview#:~:text=The%20Act%20n%C2%B034%20of%202019,on%20the%2024th%20January%202020

**National University of Vanuatu. (n.d.-b).** Programs and partnerships. Retrieved from https://www.univ.edu.vu/en/structure/overview#:~:text=,Jaur%C3%A8s%20University%20%28Bachelor%20in%20tourism

**OceansWatch.org. (n.d.).** Marine conservation education programs in Vanuatu. Retrieved from OceansWatch.org

**Paviour-Smith, M. (2005).** "Is it Aulua or education dressed up in "kastom"? Ongoing negotiation of literacy and identity in a Ni-Vanuatu community. Current Issues in Language Planning, 6(2), 224–238.

**Pierce, C., & Hemstock, S. (2021).** Resilience in Formal School Education in Vanuatu: A Mismatch with 
National, Regional and International Policies. *Journal of Education for Sustainable Development, 15,* 
206–233. https://doi.org/10.1177/09734082211031350  

**Pierce, C., & Hemstock, S. (2022).** Cyclone Harold and the role of traditional knowledge in fostering resilience in Vanuatu. 
*Australasian Journal of Disaster and Trauma Studies, 26(1),* 41–56. Retrieved from http://trauma.massey.ac.nz/issues/2022-1/AJDTS_26_1_Pierce.pdf

**Premdas, R. R. (1987).** Melanesian socialism: Vanuatu's quest for self‑definition and problems of implementation. 
*Pacific Studies, 11(1),* 107–127.

**School‑Community Relations and Fee‑Free Education Policy in Vanuatu. (n.d.).** *Pacific Affairs, 92(1),* 71–91. 
Retrieved from https://www.jstor.org/stable/48541517

**SPCCFPSTORE1.blob.core.windows.net. (n.d.-a).** Teachers' Resource Kit on Fisheries for Vanuatu (Introduction). Retrieved from SPCCFPSTORE1.blob.core.windows.net

**SPCCFPSTORE1.blob.core.windows.net. (n.d.-b).** Teachers' Resource Kit on Fisheries for Vanuatu (Activity guides). Retrieved from SPCCFPSTORE1.blob.core.windows.net

**Talua Theological Training Institute. (n.d.).** About/History. Retrieved from https://ttti.edu.vu/about/history/#:~:text=Presbyterian%20Bible%20College%20on%20Tangoa,course%20to%20train%20lay%20people

**Tamtam, H. L. (2008).** The status of English as a language of education and communication in Vanuatu [Conference paper]. Commonwealth of Learning (COL) Oasis repository.

**Trauma.massey.ac.nz. (n.d.).** Education statistics from Vanuatu MOET. Retrieved from Trauma.massey.ac.nz

**University of the South Pacific. (n.d.).** History. Retrieved from https://en.wikipedia.org/wiki/University_of_the_South_Pacific#:~:text=,106%20%20An%20extension

**Urban Coconuts. (n.d.).** Theological education in Vanuatu. Retrieved from https://urbancoconuts.org/theological-education/#:~:text=Talua%20Theological%20Training%20Institute%20is,and%20it%20is%20still%20expanding

**USP Emalus. (n.d.).** Emalus Campus overview. Retrieved from https://www.usp.ac.fj/emalus/#:~:text=Emalus%20campus%20in%20Port%20Vila,six%20schools%C2%A0and%20two%20interdisciplinary%20colleges

**Vandeputte-Tavo, L. (2013).** Bislama in the educational system? Debate around the legitimacy of a 
creole at school in a post-colonial country. *Current Issues in Language Planning, 14,* 254–269. 
https://doi.org/10.1080/14664208.2013.837217  

**Vanuatu Agriculture College. (n.d.).** Provider profile and courses. Retrieved from https://vqa.edu.vu/index.php/registered-providers-providers-side/276-vanuatu-agriculture-college#:~:text=,Diploma%20of%20Agriculture

**Vanuatu College of Nursing Education. (n.d.).** Registered provider info. Retrieved from https://vqa.edu.vu/index.php/registered-providers-providers-side/278-vanuatu-college-of-nursing-education#:~:text=Latest%20%20Info

**Vanuatu Institute of Technology. (n.d.).** Provider profile. Retrieved from https://vqa.edu.vu/index.php/registered-providers-providers-side/242-vanuatu-institute-of-technology#:~:text=,Computer%20Operations

**Vanuatu Ministry of Education. (2010).** National Curriculum Review Report [Unpublished policy document].

**Vanuatu National Council of Chiefs (Malvatumauri). (2012).** Alternative Indicators of Well-Being for Melanesia: Vanuatu Pilot Study Report. Port Vila: Malvatumauri Press.

**Warwick.ac.uk. (2010a).** Vanuatu educational gender equity data. Retrieved from Warwick.ac.uk

**Warwick.ac.uk. (2010b).** Adolescent pregnancy statistics in Vanuatu. Retrieved from Warwick.ac.uk

**Warwick.ac.uk. (2010c).** Girls' education barriers in Vanuatu. Retrieved from Warwick.ac.uk

**Willans, F. (2013).** The engineering of plurilingualism following a blueprint for multilingualism: The case of Vanuatu's 
education language policy. *TESOL Quarterly, 47(3),* 546–573. https://doi.org/10.1002/tesq.113

**Willans, F. (2014).** Moving multilingual education forward in Vanuatu: Rethinking the familiar stories about language and education (Summary report of PhD research, University of Oxford).

**Willans, F. (2015).** Traces of globalised discourses within and around spaces for multilingualism: 
prospects for education policy change in Vanuatu. *Current Issues in Language Planning, 16,* 113–97. 
https://doi.org/10.1080/14664208.2014.947021  
""")

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
*Report prepared using data from the Vanuatu Ministry of Education*  
Last updated: 2023
""")
