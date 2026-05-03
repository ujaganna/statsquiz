import streamlit as st
import time
import sqlite3
import pandas as pd
import random
import math
import json
import datetime
import statistics

def norm_cdf(x):
    """Standard normal CDF using math.erfc — no scipy needed."""
    return 0.5 * math.erfc(-x / math.sqrt(2))

# Database setup
DATABASE_NAME = 'stats_quiz.db'

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS quiz_data (
            roll_number TEXT PRIMARY KEY,
            question_params TEXT,
            student_answers TEXT,
            marks INTEGER,
            last_saved_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- Question Generation Functions ---

def generate_q1():
    data = [random.randint(1, 25) for _ in range(10)]
    mean_val = round(sum(data) / len(data), 2)
    question_text = (
        f"**Question 1:**\n"
        f"Compute the **Mean** of the following 10 integers:\n\n"
        f"`{data}`\n\n"
        f"*(Round your answer to 2 decimal places.)*"
    )
    return {
        "type": "Mean",
        "params": {"data": data},
        "question": question_text,
        "answer": mean_val,
        "col_names": ["q1_data"]
    }

def generate_q2():
    data = sorted([random.randint(1, 25) for _ in range(10)])
    median_val = round(statistics.median(data), 2)
    question_text = (
        f"**Question 2:**\n"
        f"Compute the **Median** of the following 10 integers:\n\n"
        f"`{data}`\n\n"
        f"*(Round your answer to 2 decimal places.)*"
    )
    return {
        "type": "Median",
        "params": {"data": data},
        "question": question_text,
        "answer": median_val,
        "col_names": ["q2_data"]
    }

def generate_q3():
    # Ensure a clear single mode
    base = [random.randint(1, 25) for _ in range(7)]
    mode_val = random.randint(1, 25)
    while base.count(mode_val) >= 2:
        mode_val = random.randint(1, 25)
    data = base + [mode_val, mode_val, mode_val]
    random.shuffle(data)
    question_text = (
        f"**Question 3:**\n"
        f"Compute the **Mode** of the following 10 integers:\n\n"
        f"`{data}`\n\n"
        f"*(Enter the most frequently occurring value.)*"
    )
    return {
        "type": "Mode",
        "params": {"data": data},
        "question": question_text,
        "answer": float(mode_val),
        "col_names": ["q3_data"]
    }

def generate_q4():
    data = [random.randint(1, 25) for _ in range(10)]
    std_val = round(statistics.stdev(data), 2)
    question_text = (
        f"**Question 4:**\n"
        f"Compute the **Sample Standard Deviation** of the following 10 integers:\n\n"
        f"`{data}`\n\n"
        f"*(Round your answer to 2 decimal places.)*"
    )
    return {
        "type": "SampleStdDev",
        "params": {"data": data},
        "question": question_text,
        "answer": std_val,
        "col_names": ["q4_data"]
    }

def generate_q5():
    data = [random.randint(1, 25) for _ in range(10)]
    p25 = round(float(pd.Series(data).quantile(0.25)), 2)
    question_text = (
        f"**Question 5:**\n"
        f"Compute the **25th Percentile (Q1)** of the following 10 integers:\n\n"
        f"`{data}`\n\n"
        f"*(Round your answer to 2 decimal places. Use linear interpolation method.)*"
    )
    return {
        "type": "Percentile25",
        "params": {"data": data},
        "question": question_text,
        "answer": p25,
        "col_names": ["q5_data"]
    }

def generate_q6():
    n = random.randint(3, 6)
    # x must be <= n
    x = random.randint(min(3, n), min(5, n))
    prob = round(math.comb(n, x) * (0.5 ** n), 2)
    question_text = (
        f"**Question 6:**\n"
        f"In a toss of **{n} fair coins**, what is the probability of getting **exactly {x} heads**?\n\n"
        f"*(Round your answer to 2 decimal places.)*"
    )
    return {
        "type": "BinomialProbability",
        "params": {"n": n, "x": x},
        "question": question_text,
        "answer": prob,
        "col_names": ["q6_n", "q6_x"]
    }

def generate_q7():
    mu = round(random.uniform(0.09, 0.16), 2)
    sigma = round(random.uniform(0.20, 0.30), 2)
    z_val = round(random.uniform(0.05, 0.15), 2)
    # P(X > z_val) = 1 - Phi((z_val - mu) / sigma)
    z_score = (z_val - mu) / sigma
    prob = round(1 - norm_cdf(z_score), 2)
    question_text = (
        f"**Question 7:**\n"
        f"A stock has a **mean return of {mu}** and a **standard deviation of {sigma}**.\n\n"
        f"Calculate the probability that the return is **more than {z_val}**.\n\n"
        f"*(Assume returns are normally distributed. Round your answer to 2 decimal places.)*"
    )
    return {
        "type": "NormalProbability",
        "params": {"mu": mu, "sigma": sigma, "z_val": z_val},
        "question": question_text,
        "answer": prob,
        "col_names": ["q7_mu", "q7_sigma", "q7_z_val"]
    }

def generate_q8():
    mu = random.randint(55, 65)
    x = random.randint(15, 99)
    sigma = random.randint(5, 10)
    z = round((x - mu) / sigma, 2)
    question_text = (
        f"**Question 8:**\n"
        f"Compute the **Z-score**, given:\n"
        f"- Mean (μ) = {mu}\n"
        f"- X value = {x}\n"
        f"- Standard Deviation (σ) = {sigma}\n\n"
        f"*(Round your answer to 2 decimal places.)*"
    )
    return {
        "type": "ZScore",
        "params": {"mu": mu, "x": x, "sigma": sigma},
        "question": question_text,
        "answer": z,
        "col_names": ["q8_mu", "q8_x", "q8_sigma"]
    }

def generate_all_questions():
    return [
        generate_q1(),
        generate_q2(),
        generate_q3(),
        generate_q4(),
        generate_q5(),
        generate_q6(),
        generate_q7(),
        generate_q8(),
    ]

# --- App Layout ---

st.set_page_config(layout="wide", page_title="Statistics Quiz")
st.title("Statistics Quiz")

# Session state initialization
for key, default in [
    ('roll_number_submitted', False),
    ('roll_number', ""),
    ('question_data', {}),
    ('student_answers', {}),
    ('quiz_completed', False),
    ('marks', None),
    ('last_autosave_time', datetime.datetime.now()),
    ('saved_student_answers', {}),
    ('quiz_completed_pending_confirmation', False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# --- Roll Number Input ---
if not st.session_state.roll_number_submitted:
    with st.form("roll_number_form"):
        st.session_state.roll_number = st.text_input("Enter your Roll Number:", key="roll_input").strip()
        submit_roll = st.form_submit_button("Start Quiz / Admin Login")

        if submit_roll:
            if not st.session_state.roll_number:
                st.error("Roll number cannot be empty.")
            elif st.session_state.roll_number == "admin001":
                st.session_state.roll_number_submitted = True
                st.rerun()
            else:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("SELECT * FROM quiz_data WHERE roll_number = ?", (st.session_state.roll_number,))
                existing_entry = c.fetchone()
                conn.close()

                if existing_entry:
                    st.error(f"Roll number '{st.session_state.roll_number}' already exists. Please contact support if this is an error.")
                else:
                    st.session_state.roll_number_submitted = True
                    st.session_state.question_data = {"dummy": "data"}
                    st.rerun()

# --- Admin Dashboard ---
elif st.session_state.get("roll_number", "") == "admin001":
    st.header("Admin Dashboard")

    if 'admin_clear_data_confirm' not in st.session_state:
        st.session_state.admin_clear_data_confirm = False
    if 'admin_clear_data_ok' not in st.session_state:
        st.session_state.admin_clear_data_ok = False

    if not st.session_state.admin_clear_data_confirm:
        if st.button("Clear All Student Data", key="clear_data_btn"):
            st.session_state.admin_clear_data_confirm = True
    else:
        st.warning("Are you sure you want to clear all student data? This cannot be undone.")
        col_ok, col_cancel = st.columns(2)
        with col_ok:
            if st.button("OK", key="clear_data_ok"):
                st.session_state.admin_clear_data_ok = True
        with col_cancel:
            if st.button("Cancel", key="clear_data_cancel"):
                st.session_state.admin_clear_data_confirm = False
                st.session_state.admin_clear_data_ok = False
                st.info("Clear data cancelled.")

    if st.session_state.admin_clear_data_ok:
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("DELETE FROM quiz_data WHERE roll_number != 'admin001'")
            conn.commit()
            st.success("All student data cleared.")
        except Exception as e:
            st.error(f"Error clearing data: {e}")
        finally:
            conn.close()
        st.session_state.admin_clear_data_confirm = False
        st.session_state.admin_clear_data_ok = False

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT roll_number, marks, last_saved_at FROM quiz_data WHERE roll_number != 'admin001' ORDER BY last_saved_at DESC")
    students = c.fetchall()
    conn.close()

    if students:
        st.subheader("Student Submissions")
        student_df = pd.DataFrame(students, columns=["Roll Number", "Score", "Answered At"])
        selected_student = st.selectbox("Select a student to view details:", student_df["Roll Number"].tolist())
        st.dataframe(student_df)
        if selected_student:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM quiz_data WHERE roll_number = ?", (selected_student,))
            student_row = c.fetchone()
            conn.close()
            if student_row:
                st.markdown(f"### Details for {selected_student}")
                st.markdown(f"**Answered At:** {student_row['last_saved_at']}")
                st.markdown(f"**Score:** {student_row['marks']}")
                st.markdown("**Answers:**")
                answers = json.loads(student_row['student_answers']) if student_row['student_answers'] else {}
                params = json.loads(student_row['question_params']) if student_row['question_params'] else {}
                for idx, (k, v) in enumerate(answers.items()):
                    st.markdown(f"Q{int(idx)+1}: {v}")
                st.markdown("**Question Parameters:**")
                st.json(params)
    else:
        st.info("No student submissions yet.")

# --- Student Quiz Logic ---
elif st.session_state.get("roll_number_submitted", False):
    # Timer setup
    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = datetime.datetime.now()
    if 'quiz_end_time' not in st.session_state:
        st.session_state.quiz_end_time = st.session_state.quiz_start_time + datetime.timedelta(minutes=20)

    now = datetime.datetime.now()
    time_left = st.session_state.quiz_end_time - now
    minutes, seconds = divmod(max(0, int(time_left.total_seconds())), 60)
    st.warning(f"⏱️ Time left: {minutes:02d}:{seconds:02d}")

    if time_left.total_seconds() <= 0 and not st.session_state.get('quiz_completed', False):
        st.session_state.quiz_completed = True
        st.session_state.quiz_completed_pending_confirmation = False
        st.info("Time is up! Quiz auto-submitted.")

    # Generate questions once per student session
    if not st.session_state.question_data or st.session_state.question_data == {"dummy": "data"}:
        st.session_state.question_data = generate_all_questions()
        st.session_state.student_answers = {str(i): "" for i in range(len(st.session_state.question_data))}
        st.session_state.last_autosave_time = datetime.datetime.now()
        st.session_state.saved_student_answers = {}

    st.subheader("Quiz Questions")

    current_student_answers_display = {}
    for i, q in enumerate(st.session_state.question_data):
        st.markdown(q["question"])
        current_student_answers_display[str(i)] = st.text_input(
            "Your Answer:",
            value=st.session_state.student_answers.get(str(i), ""),
            key=f"q_{i}",
            disabled=st.session_state.get('quiz_completed', False)
        )
        st.markdown("---")

    st.session_state.student_answers = current_student_answers_display

    # Autosave logic
    if not st.session_state.quiz_completed and not st.session_state.quiz_completed_pending_confirmation:
        current_time = datetime.datetime.now()
        answers_changed = (st.session_state.student_answers != st.session_state.saved_student_answers)
        time_for_autosave = (current_time - st.session_state.last_autosave_time).total_seconds() >= 10

        if answers_changed and time_for_autosave:
            conn = get_db_connection()
            c = conn.cursor()

            flat_question_params = {}
            for q_idx, q_data in enumerate(st.session_state.question_data):
                for param_name in q_data.get('col_names', []):
                    original_param_key = param_name.split('_', 1)[1]
                    val = q_data['params'].get(original_param_key, None)
                    flat_question_params[param_name] = json.dumps(val) if isinstance(val, list) else val

            question_params_json = json.dumps(flat_question_params)
            student_answers_json = json.dumps(st.session_state.student_answers)
            last_saved = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                c.execute(
                    "INSERT OR REPLACE INTO quiz_data (roll_number, question_params, student_answers, marks, last_saved_at) VALUES (?, ?, ?, ?, ?)",
                    (st.session_state.roll_number, question_params_json, student_answers_json, st.session_state.marks, last_saved)
                )
                conn.commit()
                st.session_state.last_autosave_time = current_time
                st.session_state.saved_student_answers = st.session_state.student_answers.copy()
                st.success(f"Autosaved progress at {last_saved}!")
            except sqlite3.Error as e:
                st.error(f"Error autosaving progress: {e}")
            finally:
                conn.close()

    # Submit / Confirm section
    if not st.session_state.quiz_completed and time_left.total_seconds() > 0:
        if not st.session_state.quiz_completed_pending_confirmation:
            if st.button("Complete Quiz", key="submit_quiz_button"):
                st.session_state.quiz_completed_pending_confirmation = True
        else:
            st.warning("Are you sure you want to submit the quiz? You cannot change your answers after submission.")
            col_ok, col_cancel = st.columns(2)
            with col_ok:
                if st.button("OK, Submit Quiz", key="confirm_submit"):
                    st.session_state.quiz_completed_pending_confirmation = False
                    st.session_state.quiz_completed = True
                    st.session_state.quiz_end_time = now

                    # Scoring with ±0.05 tolerance for 2-decimal answers
                    score = 0
                    for i, q in enumerate(st.session_state.question_data):
                        correct_answer = q["answer"]
                        student_answer_str = st.session_state.student_answers.get(str(i), "").strip()
                        try:
                            student_answer = float(student_answer_str)
                            tolerance = 0.05  # All answers are 2 decimal places
                            if abs(student_answer - correct_answer) <= tolerance:
                                score += 1
                        except ValueError:
                            pass

                    st.session_state.marks = score
                    st.success(f"Quiz completed! Your score: {score} out of {len(st.session_state.question_data)}")

                    # Save final score
                    conn = get_db_connection()
                    c = conn.cursor()
                    last_saved = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    flat_question_params = {}
                    for q_idx, q_data in enumerate(st.session_state.question_data):
                        for param_name in q_data.get('col_names', []):
                            original_param_key = param_name.split('_', 1)[1]
                            val = q_data['params'].get(original_param_key, None)
                            flat_question_params[param_name] = json.dumps(val) if isinstance(val, list) else val

                    try:
                        c.execute(
                            "INSERT OR REPLACE INTO quiz_data (roll_number, question_params, student_answers, marks, last_saved_at) VALUES (?, ?, ?, ?, ?)",
                            (st.session_state.roll_number, json.dumps(flat_question_params), json.dumps(st.session_state.student_answers), score, last_saved)
                        )
                        conn.commit()
                        st.info("Final score and answers saved to database.")
                    except sqlite3.Error as e:
                        st.error(f"Error saving final score: {e}")
                    finally:
                        conn.close()

                    # Show results
                    st.subheader("Correct Answers:")
                    for i, q in enumerate(st.session_state.question_data):
                        student_ans = st.session_state.student_answers.get(str(i), 'Not answered')
                        correct_ans = q['answer']
                        try:
                            is_correct = abs(float(student_ans) - correct_ans) <= 0.05
                            result_icon = "✅" if is_correct else "❌"
                        except (ValueError, TypeError):
                            result_icon = "❌"

                        st.markdown(f"**Question {i+1}:** {result_icon}")
                        st.markdown(f"- Your Answer: `{student_ans}`")
                        st.markdown(f"- Correct Answer: `{correct_ans:.2f}`")
                        st.markdown("---")

            with col_cancel:
                if st.button("Cancel", key="cancel_submit"):
                    st.session_state.quiz_completed_pending_confirmation = False
                    st.info("Submission cancelled. You can continue answering.")

    elif st.session_state.quiz_completed:
        st.subheader("Quiz Results")
        st.success(f"You scored **{st.session_state.marks}** out of **{len(st.session_state.question_data)}** questions.")

        st.subheader("Answer Review:")
        for i, q in enumerate(st.session_state.question_data):
            student_ans = st.session_state.student_answers.get(str(i), 'Not answered')
            correct_ans = q['answer']
            try:
                is_correct = abs(float(student_ans) - correct_ans) <= 0.05
                result_icon = "✅" if is_correct else "❌"
            except (ValueError, TypeError):
                result_icon = "❌"
            st.markdown(f"**Q{i+1}** {result_icon} — Your: `{student_ans}` | Correct: `{correct_ans:.2f}`")

    # Force rerun every second for timer
    if not st.session_state.get('quiz_completed', False) and time_left.total_seconds() > 0:
        time.sleep(1)
        st.rerun()
