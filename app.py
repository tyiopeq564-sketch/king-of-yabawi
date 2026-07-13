import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="천하제일 야바위 대회", page_icon="🔮", layout="centered")

# 세션 상태(변수 저장) 초기화
if "streak" not in st.session_state:
    st.session_state.streak = 0  # 현재 연승 기록
if "max_streak" not in st.session_state:
    st.session_state.max_streak = 0  # 최고 연승 기록
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(1, 3)  # 보석이 든 컵 (1, 2, 3 중 하나)
if "game_status" not in st.session_state:
    st.session_state.game_status = "ready"  # ready, win, lose
if "chosen_cup" not in st.session_state:
    st.session_state.chosen_cup = None

# 게임 리셋 함수
def reset_game():
    st.session_state.answer = random.randint(1, 3)
    st.session_state.game_status = "ready"
    st.session_state.chosen_cup = None

# 컵 선택 시 작동하는 함수
def choose_cup(cup_num):
    st.session_state.chosen_cup = cup_num
    if cup_num == st.session_state.answer:
        st.session_state.game_status = "win"
        st.session_state.streak += 1
        if st.session_state.streak > st.session_state.max_streak:
            st.session_state.max_streak = st.session_state.streak
    else:
        st.session_state.game_status = "lose"
        st.session_state.streak = 0

# --- 화면 UI 시작 ---

# 👑 상단 레이아웃 (오른쪽 위에 최고 기록 배치)
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.title("🔮 야바위 대회")
    st.write("세 개의 컵 중 **보석이 든 진짜 컵**을 찾으세요!")

with header_col2:
    st.write("") # 줄바꿈용 빈칸
    # 오른쪽 상단에 강조된 최고 기록 배치
    st.markdown(
        f"""
        <div style="background-color: #ffeaa7; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #fdcb6e;">
            <span style="color: #d63031; font-weight: bold; font-size: 14px;">👑 HIGH SCORE</span><br>
            <span style="color: #2d3436; font-weight: bold; font-size: 20px;">{st.session_state.max_streak} 연승</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.markdown("---")

# 현재 점수판 표시
st.metric(label="🔥 나의 현재 기록", value=f"{st.session_state.streak} 연승")

# 킹받는 멘트 시스템
if st.session_state.streak == 0 and st.session_state.game_status == "ready":
    st.info("😏 어이 친구, 쫄지 말고 컵 하나 골라봐.")
elif st.session_state.streak >= 5:
    st.success("😎 뭐야..? 당신 장난 아닌데? 손기술 작두 탔네 탔어!")
elif st.session_state.streak >= 3:
    st.warning("👀 오... 집중력 좀 좋은데? 친구들이 슬슬 긴장하겠어.")

st.write("")

# 컵 버튼 배치 (가로로 3개)
cup_cols = st.columns(3)

for i in range(1, 4):
    with cup_cols[i-1]:
        if st.session_state.game_status == "ready":
            st.button(f"🥤 {i}번 컵", on_click=choose_cup, args=(i,), use_container_width=True)
        else:
            if i == st.session_state.answer:
                st.button(f"💎 (정답!)", disabled=True, use_container_width=True)
            else:
                st.button(f"❌ (텅 빔)", disabled=True, use_container_width=True)

st.write("")

# 결과 메시지 출력
if st.session_state.game_status == "win":
    st.balloons()
    st.success(f"🎉 대박! 정답은 {st.session_state.answer}번 컵이었습니다!")
    st.button("다음 판 하기 ➡️", on_click=reset_game, type="primary")

elif st.session_state.game_status == "lose":
    st.error(f"💥 맹탕! 보석은 {st.session_state.answer}번 컵에 있었습니다.")
    st.button("다시 도전하기 🔄", on_click=reset_game, type="primary")