from pathlib import Path

content = r'''import streamlit as st

# Optional backend integration
try:
    from graph_engine import get_recommendations
    BACKEND_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    BACKEND_AVAILABLE = False
    get_recommendations = None


def get_mock_recommendations(user_skills):
    """Demo recommendations used when the FalkorDB backend is unavailable."""
    all_jobs = [
        {
            "job_title": "Data Scientist",
            "required": ["Python", "SQL", "Machine Learning"],
            "courses": {
                "Machine Learning": "Machine Learning Basics",
                "Python": "Python for Data Science",
                "SQL": "SQL Fundamentals",
            },
        },
        {
            "job_title": "Business Intelligence Analyst",
            "required": ["SQL", "Power BI", "Excel"],
            "courses": {
                "Power BI": "Power BI Fundamentals",
                "Excel": "Advanced Excel for Analytics",
                "SQL": "SQL for Business Analysis",
            },
        },
        {
            "job_title": "Data Analyst",
            "required": ["Python", "SQL", "Excel", "Power BI"],
            "courses": {
                "Power BI": "Power BI Fundamentals",
                "Python": "Python Data Analysis",
                "SQL": "SQL Fundamentals",
            },
        },
        {
            "job_title": "Python Developer",
            "required": ["Python", "SQL"],
            "courses": {
                "SQL": "SQL Fundamentals",
            },
        },
    ]

    user_skill_set = set(user_skills)
    results = []

    for job in all_jobs:
        required = set(job["required"])
        matched = sorted(user_skill_set.intersection(required))
        missing = sorted(required.difference(user_skill_set))

        if matched:
            match_percent = round(100 * len(matched) / len(required))
            courses = [
                job["courses"][skill]
                for skill in missing
                if skill in job["courses"]
            ]
            results.append(
                {
                    "job_title": job["job_title"],
                    "match_percent": match_percent,
                    "matched_skills": matched,
                    "missing_skills": missing,
                    "recommended_courses": courses,
                }
            )

    return sorted(
        results,
        key=lambda item: item["match_percent"],
        reverse=True,
    )


def convert_backend_result(result):
    """Convert Member 1's backend dictionary to the UI's list format."""
    if not isinstance(result, dict) or result.get("error"):
        return []

    converted = []
    for job in result.get("jobs", []):
        converted.append(
            {
                "job_title": job.get("title", "Unknown role"),
                "match_percent": job.get("match_percent", 0),
                "matched_skills": job.get("matched_skills", []),
                "missing_skills": job.get("missing_skills", []),
                "recommended_courses": [
                    course.get("title", "")
                    for course in result.get("courses", [])
                    if course.get("skill") in job.get("missing_skills", [])
                ],
            }
        )
    return converted


def main():
    st.set_page_config(
        page_title="GraphHire - FalkorDB Job Matching",
        page_icon="🕸️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

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
            display: inline-block;
            margin: 2px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-header">🕸️ GraphHire</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-header">Graph-powered career matching for students • Powered by FalkorDB</div>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("👤 Student Profile")
        student_profiles = {
            "Select a Profile...": [],
            "Alex Chen (Data Science Senior)": [
                "Python", "SQL", "Machine Learning"
            ],
            "Jordan Lee (Business Analyst)": [
                "Excel", "Power BI", "SQL"
            ],
            "Sam Taylor (Software Engineer Entry)": ["Python", "SQL"],
            "Custom Profile": [],
        }

        selected_profile = st.selectbox(
            "Load Profile Preset",
            options=list(student_profiles.keys()),
            index=0,
        )

        available_skills = [
            "Python",
            "SQL",
            "Excel",
            "Power BI",
            "Machine Learning",
        ]
        selected_skills = st.multiselect(
            "Configure profile skills:",
            options=available_skills,
            default=student_profiles[selected_profile],
            key=f"skill_select_{selected_profile}",
        )

        st.divider()
        find_jobs = st.button(
            "🚀 Find My Best Jobs",
            type="primary",
            use_container_width=True,
        )

        if BACKEND_AVAILABLE:
            st.caption("FalkorDB backend module found")
        else:
            st.caption("Demo mode: backend module not found")

    if find_jobs:
        if not selected_skills:
            st.info("💡 Please select at least one skill to match jobs.")
            return

        with st.spinner("Analyzing skills and finding opportunities..."):
            try:
                # The backend currently accepts a student name, not a skill list.
                # Use the demo data for custom skill combinations; use the backend
                # for the preloaded Asha profile when it is available.
                if BACKEND_AVAILABLE and selected_profile == "Alex Chen (Data Science Senior)":
                    backend_result = get_recommendations("Asha")
                    recommendations = convert_backend_result(backend_result)
                    if not recommendations:
                        recommendations = get_mock_recommendations(selected_skills)
                else:
                    recommendations = get_mock_recommendations(selected_skills)
            except Exception as error:
                st.warning(
                    "The FalkorDB backend could not be reached. Showing demo recommendations instead."
                )
                st.caption(f"Technical details: {error}")
                recommendations = get_mock_recommendations(selected_skills)

        if not recommendations:
            st.info(
                "🔍 No matching job roles found. Try selecting additional skills."
            )
            return

        total_evaluated = len(recommendations)
        top_match_score = max(
            (job.get("match_percent", 0) for job in recommendations),
            default=0,
        )

        st.markdown("### 📊 Search Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Roles Evaluated", total_evaluated)
        col2.metric("Top Match Score", f"{top_match_score}%")
        col3.metric("Active Skills Queried", len(selected_skills))

        st.divider()
        st.markdown("### 🎯 Recommended Opportunities")

        for index, job in enumerate(recommendations, start=1):
            title = job.get("job_title", "Unknown Role")
            match_percent = float(job.get("match_percent", 0))
            matched_skills = job.get("matched_skills", [])
            missing_skills = job.get("missing_skills", [])
            courses = job.get("recommended_courses", [])

            with st.container(border=True):
                col_info, col_score = st.columns([3, 1])
                with col_info:
                    st.subheader(f"{index}. {title}")
                with col_score:
                    st.metric("Match Score", f"{match_percent:.0f}%")

                st.progress(
                    min(max(match_percent / 100.0, 0.0), 1.0)
                )

                col_matched, col_missing, col_courses = st.columns(3)

                with col_matched:
                    st.write("**Matched Skills**")
                    if matched_skills:
                        chips = "".join(
                            f'<span class="skill-chip-matched">✓ {skill}</span>'
                            for skill in matched_skills
                        )
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.caption("None")

                with col_missing:
                    st.write("**Missing Skills**")
                    if missing_skills:
                        chips = "".join(
                            f'<span class="skill-chip-missing">✗ {skill}</span>'
                            for skill in missing_skills
                        )
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.caption("None — perfect match!")

                with col_courses:
                    st.write("**Recommended Courses**")
                    if courses:
                        chips = "".join(
                            f'<span class="course-chip">📚 {course}</span>'
                            for course in courses
                        )
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.caption("No skill-gap courses needed")

    else:
        st.info(
            "👈 Select a profile or skills in the sidebar, then click "
            "**Find My Best Jobs** to start."
        )


if __name__ == "__main__":
    main()
'''
path = Path("/mnt/data/app.py")
path.write_text(content, encoding="utf-8")
import ast
ast.parse(content)
print(f"Created and syntax-checked: {path}")
