import streamlit as st
import pandas as pd

# Fallback/Import handling for backend integration
try:
    from graph_engine import get_recommendations
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False


def main():
    # Page Configuration
    st.set_page_config(
        page_title="GraphHire - FalkorDB Job Matching",
        page_icon="🕸️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom Styling for polished Hackathon Look
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #64748B;
            margin-bottom: 1.5rem;
        }
        .job-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .skill-chip-matched {
            background-color: #DEF7EC;
            color: #03543F;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.82rem;
            font-weight: 500;
            display: inline-block;
            margin: 2px;
        }
        .skill-chip-missing {
            background-color: #FDE8E8;
            color: #9B1C1C;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.82rem;
            font-weight: 500;
            display: inline-block;
            margin: 2px;
        }
        .course-chip {
            background-color: #E1EFFE;
            color: #1E429F;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.82rem;
            font-weight: 500;
            display: inline-block;
            margin: 2px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header Section
    st.markdown('<div class="main-header">🕸️ GraphHire</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Graph-Powered Knowledge Matching for Next-Gen Student Careers • Powered by FalkorDB</div>',
        unsafe_allow_html=True,
    )

    # Sidebar: Student Profile Selector & Controls
    with st.sidebar:
        st.header("👤 Student Profile")
        student_profiles = {
            "Select a Profile...": [],
            "Alex Chen (Data Science Senior)": [
                "Python",
                "SQL",
                "Machine Learning",
            ],
            "Jordan Lee (Business Analyst)": ["Excel", "Power BI", "SQL"],
            "Sam Taylor (Software Engineer Entry)": ["Python", "SQL"],
            "Custom Profile": [],
        }

        selected_profile = st.selectbox(
            "Load Profile Preset",
            options=list(student_profiles.keys()),
            index=0,
        )

        # Skill Selection Options
        default_skills = (
            student_profiles[selected_profile] if selected_profile else []
        )
        available_skills = [
            "Python",
            "SQL",
            "Excel",
            "Power BI",
            "Machine Learning",
        ]

        st.subheader("🛠️ Select Skills")
        selected_skills = st.multiselect(
            "Configure profile skills:",
            options=available_skills,
            default=default_skills,
            key=f"skill_select_{selected_profile}",
        )

        st.divider()
        find_jobs = st.button(
            "🚀 Find My Best Jobs", type="primary", use_container_width=True
        )

        st.caption("FalkorDB Graph Engine Integration Active")

    # Display Warning if Backend Import Failed
    if not BACKEND_AVAILABLE:
        st.warning(
            "⚠️ `graph_engine.py` with `get_recommendations()` was not detected. Running in mock mode."
        )

    # Execution State & Job Recommendations
    if find_jobs:
        if not selected_skills:
            st.info("💡 Please


select at least one skill to match jobs.")
            return

        with st.spinner("Analyzing FalkorDB knowledge graph..."):
            try:
                if BACKEND_AVAILABLE:
                    # Invoke actual function from Member 1's backend module
                    raw_recommendations = get_recommendations(selected_skills)
                else:
                    # Mock response strictly formatted according to backend contract
                    raw_recommendations = get_mock_recommendations(
                        selected_skills
                    )

            except Exception as e:
                st.error(
                    f"❌ **Backend Connection Error**: Failed to retrieve recommendations from FalkorDB graph engine."
                )
                st.caption(f"Error details: {str(e)}")
                return

        # Handle Empty Results
        if not raw_recommendations:
            st.info(
                "🔍 No matching job roles found for the selected skills. Try selecting additional skills."
            )
            return

        # Summary Section / Metrics
        total_evaluated = len(raw_recommendations)
        top_match_score = max(
            [r.get("match_percent", 0) for r in raw_recommendations], default=0
        )

        st.markdown("### 📊 Search Summary")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Roles Evaluated", total_evaluated)
        with col_m2:
            st.metric("Top Match Score", f"{top_match_score}%")
        with col_m3:
            st.metric("Active Skills Queried", len(selected_skills))

        st.divider()
        st.markdown("### 🎯 Recommended Opportunities")

        # Render Job Recommendation Cards
        for idx, job in enumerate(raw_recommendations, 1):
            title = job.get("job_title", "Unknown Role")
            match_pct = float(job.get("match_percent", 0))
            matched_skills = job.get("matched_skills", [])
            missing_skills = job.get("missing_skills", [])
            recommended_courses = job.get("recommended_courses", [])

            with st.container():
                col_info, col_score = st.columns([3, 1])

                with col_info:
                    st.subheader(f"{idx}. {title}")

                with col_score:
                    st.metric("Match Score", f"{match_pct:.0f}%")

                st.progress(min(max(match_pct / 100.0, 0.0), 1.0))

                col_k1, col_k2, col_k3 = st.columns(3)

                with col_k1:
                    st.write("**Matched Skills**")
                    if matched_skills:
                        chips = "".join(
                            [
                                f'<span class="skill-chip-matched">✓ {s}</span>'
                                for s in matched_skills
                            ]
                        )
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.caption("None")

                with col_k2:
                    st.write("**Missing Skills**")
                    if missing_skills:
                        chips = "".join(
                            [
                                f'<span class="skill-chip-missing">✗ {s}</span>'
                                for s in missing_skills
                            ]
                        )
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.caption("None (Perfect Match)")

                with col_k3:
                    st.write("**Recommended Courses**")
                    if recommended_courses:
                        chips = "".join(
                            [
                                f'<span class="course-chip">📚 {c}</span>'
                                for c in recommended_courses
                            ]
                        )
                        st.markdown(chips, unsafe_allow_html=True)
                    else:


st.caption("No gap fill needed")

                st.markdown("<br>", unsafe_allow_html=True)

    else:
        # Initial Landing View
        st.info("👈 Select your profile or skills in the sidebar and click **Find My Best Jobs** to start.")


def get_mock_recommendations(user_skills):
    """Fallback handler mimicking Member 1's backend return structure."""
    all_jobs = [
        {
            "job_title": "Data Scientist",
            "required": ["Python", "SQL", "Machine Learning"],
            "courses": {
                "Machine Learning": "Stanford Machine Learning (Coursera)",
                "Python": "Python for Data Science (EDX)",
                "SQL": "Complete SQL Bootcamp (Udemy)",
            },
        },
        {
            "job_title": "Business Intelligence Analyst",
            "required": ["SQL", "Power BI", "Excel"],
            "courses": {
                "Power BI": "Microsoft Power BI Data Analyst (Coursera)",
                "Excel": "Advanced Excel for Analytics (LinkedIn Learning)",
                "SQL": "SQL for Business Analysis (Udemy)",
            },
        },
        {
            "job_title": "Data Analyst",
            "required": ["Python", "SQL", "Excel", "Power BI"],
            "courses": {
                "Power BI": "Power BI Fundamentals (DataCamp)",
                "Python": "Python Data Analysis (DataCamp)",
            },
        },
    ]

    results = []
    user_skill_set = set(user_skills)

    for job in all_jobs:
        req_set = set(job["required"])
        matched = list(user_skill_set.intersection(req_set))
        missing = list(req_set.difference(user_skill_set))

        if matched:
            match_pct = round((len(matched) / len(req_set)) * 100)
            courses = [
                job["courses"][s] for s in missing if s in job["courses"]
            ]

            results.append(
                {
                    "job_title": job["job_title"],
                    "match_percent": match_pct,
                    "matched_skills": matched,
                    "missing_skills": missing,
                    "recommended_courses": courses,
                }
            )

    return sorted(results, key=lambda x: x["match_percent"], reverse=True)


if __name__ == "__main__":
    main()
