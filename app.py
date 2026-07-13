import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="천하제일 야바위 대회", page_icon="🔮", layout="centered")

# 세션 상태 초기화 (애니메이션 플래그 포함)
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "max_streak" not in st.session_state:
    st.session_state.max_streak = 0
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(1, 3)
if "game_status" not in st.session_state:
    st.session_state.game_status = "ready"
if "chosen_cup" not in st.session_state:
    st.session_state.chosen_cup = None
# 섞는 중인지 확인하는 플래그 (중요!)
if "shuffling" not in st.session_state:
    st.session_state.shuffling = False

# 컵 섞기 함수 (다음 판 버튼 누를 때 호출)
def shuffle_cups():
    st.session_state.shuffling = True  # 섞기 시작!
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

# 상단 레이아웃 (오른쪽 위에 최고 기록 배치)
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.title("🔮 야바위 대회")
    st.write("세 개의 컵 중 **보석이 든 진짜 컵**을 찾으세요!")

with header_col2:
    st.write("") 
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

# ✨ [애니메이션 효과 활성화!] (맨 앞의 #을 모두 지웠습니다.)
if st.session_state.shuffling:
    # 컵들이 싹 사라지고 로딩 애니메이션이 나옵니다!
    with st.spinner("🔮 타짜가 현란하게 컵을 섞는 중... 눈 떼지 마세요! 👀"):
        time.sleep(1.2) # 1.2초 동안 타임 루프 (섞는 연출)
    st.session_state.shuffling = False # 섞기 완료
    st.rerun() # 화면 새로고침해서 컵 다시 보여주기

# 컵 버튼 배치 (가로로 3개)
cup_cols = st.columns(3)

for i in range(1, 4):
    with cup_cols[i-1]:
        if st.session_state.game_status == "ready":
            st.button(f"🥤 {i}번 컵", on_click=choose_cup, args=(i,), use_container_width=True)
        else:
            # 중복 에러 해결: 버튼 텍스트 뒤에 숫자를 다르게 붙여서 중복 방지!
            if i == st.session_state.answer:
                st.button(f"💎 정답! ({i}번)", disabled=True, use_container_width=True)
            else:
                st.button(f"❌ 텅 빔 ({i}번)", disabled=True, use_container_width=True)

st.write("")

# 결과 메시지 출력
if st.session_state.game_status == "win":
    st.balloons()
    st.success(f"🎉 대박! 정답은 {st.session_state.answer}번 컵이었습니다!")
    st.button("다음 판 하기 ➡️", on_click=shuffle_cups, type="primary")

elif st.session_state.game_status == "lose":
    st.error(f"💥 맹탕! 보석은 {st.session_state.answer}번 컵에 있었습니다.")
    st.button("다시 도전하기 🔄", on_click=shuffle_cups, type="primary")