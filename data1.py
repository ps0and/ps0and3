import streamlit as st
from streamlit_ace import st_ace
import pandas as pd
import io
import sys

# 실행 함수
def code_runner(code_input):
    output_buffer = io.StringIO()
    result, status = "", "success"
    try:
        sys.stdout = output_buffer
        exec_globals = {}
        exec(code_input, exec_globals)
        result = output_buffer.getvalue() or "출력된 내용이 없습니다."
    except Exception as e:
        result = f"{e.__class__.__name__}: {e}"
        status = "error"
    finally:
        sys.stdout = sys.__stdout__
    return result, status

# 출력 함수
def display_output(result, status):
    if status == "success":
        st.markdown(f"```bash\n{result}\n```")
    else:
        st.markdown("##### ❌ 실행 중 오류 발생")
        st.markdown(
            f"<pre style='color: red; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>{result}</pre>",
            unsafe_allow_html=True
        )

# 공통 코드 블록 UI
def code_block(problem_number, title, starter_code, prefix=""):
    key_prefix = f"{prefix}{problem_number}"
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"##### 📥 코드 입력 ")
        code_input = st_ace(
            value=starter_code,
            language='python',
            theme='github',
            height=250,
            key=f"{key_prefix}_editor"
        )

    with c2:
        st.markdown("##### 📤 실행 결과")
        if st.button("▶️ 코드 실행하기", key=f"{key_prefix}_run"):
            result, status = code_runner(code_input)
            display_output(result, status)
def diagnostic_evaluation():
    st.subheader("📝 진단 평가")
    st.write("아래 두 문제를 풀어 제출해주세요.")

    # 폼 정의
    with st.form("diag_form"):
        q1 = st.text_input(
            "(1) Hello를 출력하는 코드",
            placeholder="힌트: print"
        )
        q2 = st.text_input(
            "(2) 한 줄로: 숫자 5를 a에, 3을 b에 할당하고 두 수의 합을 출력하는 코드를 작성하세요.",
            placeholder="예: a=5; print(a)"
        )
        submitted = st.form_submit_button("제출")

    # 제출 버튼을 눌렀을 때만 실행
    if submitted:
        # 정답 판별
        correct1 = q1.strip().replace('"', "'") == "print('Hello')"
        clean_q2 = q2.replace(" ", "")
        correct2 = (
            "a=5" in clean_q2 and
            "b=3" in clean_q2 and
            "print(a+b)" in clean_q2
        )

        # 결과 안내 및 차시 추천
        if not correct1:
            st.info("👉 추천 학습 시작: Day 1")
            return 1
        elif not correct2:
            st.info("👉 추천 학습 시작: Day 2")
            return 2
        else:
            st.info("👉 추천 학습 시작: Day 3")
            return 3 

# ✅ 메인 화면
def show():
    diagnostic_evaluation()
    st.divider()
    st.header("🗓️ 1Day")
    st.subheader("파이썬 기초: 자료형, 변수, 리스트")
    st.write("수학을 코딩하기 위해서는 코딩에 대한 기본 문법을 알고 있어야 합니다.")
    st.write("코딩 시작합니다.")
    st.divider()

    st.subheader("🎥 수업 영상 보기")
    st.subheader("📌 학습 목표")
    st.write("""
    - 파이썬의 기본 자료형과 변수의 사용법을 익힐 수 있다.
    - 리스트의 생성과 요소 접근 방법을 실습할 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 자료형")
    st.write("""          
    - 문자열: 메일 제목, 메시지 내용 등 따옴표('')로 감싸서 입력 Ex.```'Hello World'```
    - 숫자열: 물건의 가격, 학생의 성적 Ex. ```52, 12```
    - 불: 친구의 로그인 상태 Ex. ```True, False```""")
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 출력: print() 함수")
    st.write("""          
    - ```print()``` 함수의 괄호 안에 출력하고 싶은 내용을 적습니다.
    - ```print(1,'a')``` 함수의 괄호 안에 출력하고 싶은 내용을 쉼표로 연결해서 여러 개 적어도 됩니다.""")
    
    st.markdown(""" ###### 💻 :blue[[문제 1]] 아래와 같이 print 함수를 이용해서 다양한 자료형을 출력해보세요""")
    code_block(1, "print 함수", "print('hello', 320)\nprint(21)", prefix="d1_")

    # 사칙연산 정리표
    data = {
        "연산 종류": ["덧셈", "뺄셈", "곱셈", "나눗셈", "정수 나눗셈", "나머지", "거듭제곱"],
        "연산자": ["+", "-", "*", "/", "//", "%", "**"],
        "예시 코드": ["3 + 2", "5 - 2", "4 * 2", "10 / 4", "10 // 4", "10 % 4", "2 ** 3"],
        "결과": [5, 3, 8, 2.5, 2, 2, 8],
        "설명": [
            "두 수를 더함",
            "앞 수에서 뒤 수를 뺌",
            "두 수를 곱함",
            "실수 나눗셈 결과",
            "몫만 구함 (소수점 버림)",
            "나눗셈의 나머지 계산",
            "제곱 (2의 3제곱)"
        ]
    }
    df = pd.DataFrame(data)
    st.subheader("🧮 파이썬 사칙연산 정리표")
    st.dataframe(df, use_container_width=True)
    st.markdown(""" ###### 💻 :blue[[문제 2]] 아래와 같이 숫자의 연산을 출력해보세요""")
    code_block(2, "연산 출력", "print('5+7=', 5+7)\nprint('5**2=', 5**2)", prefix="d1_")
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 변수와 입력")
    st.write("""          
    - 변수는 값을 저장할 때 사용하는 식별자
    - ```변수 = 값``` (값을 변수에 할당합니다.)
    - ```=``` 기호는 '같다'의 의미가 아니라 우변의 값을 좌변에 '할당하겠다'의 의미""")
    st.markdown("""###### 💻 :blue[[문제 3]] 아래와 같이 x라는 변수에 숫자나 문자를 할당하고 변수를 출력해보세요""")
    code_block(3, "변수 사용", "pi = 3.14\nprint(pi)", prefix="d1_")
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 리스트(list) 및 인덱스(index)")
    st.write("""          
    - 리스트란 숫자나 문자 등의 자료를 모아서 사용할 수 있게 해주는 특별한 자료
        - 리스트는 대괄호 [ ] 내부에 여러 종류의 자료를 넣어 선언합니다.
        - [요소, 요소, ..., 요소]
    """)
    st.code("""
list = [12, '문자열', True]
print(list)
# 출력: [12, '문자열', True]
    """)
    st.write("""          
    - 파이썬은 인덱스를 0부터 셉니다.
    - 리스트의 특정 위치(인덱스)를 출력하려면 대괄호를 사용합니다.
    """)
    st.image("image/data1_img1.png")
    st.code("""
list = [12, '문자열', True]
print(list[0])  
# 출력: 12
    """)
    st.write("""
    - append() 함수는 리스트에 요소를 추가합니다.
    """)
    st.code("""
list = ['a', 'b', 'c']
list.append('d')
print(list)  
# 출력: ['a', 'b', 'c', 'd']
    """)
    st.markdown("""###### 💻 :blue[[문제 4]] 리스트에 자료를 추가하고 특정 요소를 출력해보세요""")
    with st.expander("💡 힌트 보기"):
        st.markdown("`list.append()`를 사용하여 리스트에 요소를 추가하고 `list[]`를 사용하여 특정 요소를 출력합니다.")
    code_block(4, "리스트 사용", "list =", prefix="d1_")
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.markdown("##### 🌈 :rainbow[[수준별 문제]] 파이썬 기초 실습")

    level = st.radio(
        "난이도를 선택하세요!",
        ("하", "중", "상"),
        horizontal=True,
        key="d1_select_level"
    )

    if level == "하":
        # 문제 1(자료형+print) 변형
        q_title = "문자열과 숫자 출력"
        q_problem = "문자열 'Hello Python!'과 숫자 100을 한 줄씩 각각 출력해보세요."
        starter_code = "print()\nprint()"
        answer_code = "print('Hello Python!')\nprint(100)"
    elif level == "중":
        # 문제 4(리스트/append) 변형
        q_title = "리스트 요소 추가 및 출력"
        q_problem = "빈 리스트를 만들고, 숫자 5와 10을 차례대로 추가한 뒤 전체 리스트와 첫 번째 요소를 출력해보세요."
        starter_code = "my_list = []\n# 여기에 코드 추가\n"
        answer_code = (
            "my_list = []\n"
            "my_list.append(5)\n"
            "my_list.append(10)\n"
            "print(my_list)\n"
            "print(my_list[0])"
        )
    else:  # 상
        # 문제 3(변수, 연산, print) 변형 + 논리적 추론 추가
        q_title = "변수와 연산, 조건문"
        q_problem = (
            "두 변수 a=7, b=3을 선언하고 두 변수의 합, 곱을 출력하세요. "
            "그리고 a가 b보다 크면 True, 아니면 False를 출력해보세요."
        )
        starter_code = "a = 7\nb = 3\n# 여기에 코드 추가\n"
        answer_code = (
            "a = 7\nb = 3\n"
            "print(a + b)\n"
            "print(a * b)\n"
            "print(a > b)"
        )

    st.markdown(f"**[{level}] {q_title}**  \n{q_problem}")

    with st.expander("💡 정답 코드 보기"):
        st.code(answer_code, language='python')

    code_block("data1_level", f"수준별 파이썬 ({level})", starter_code, prefix=f"d1_sel_{level}_")

if __name__ == "__main__":
    show()