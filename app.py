import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="천하제일 야바위 대회", page_icon="🔮", layout="centered")

st.title("🔮 천하제일 야바위 대회")
st.write("눈앞에서 휙휙 섞이는 컵을 잘 보고 보석이 든 컵을 맞혀보세요!")
st.markdown("---")

# HTML + JavaScript 기반의 진짜 움직이는 게임 구현
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            text-align: center;
            background-color: transparent;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .scoreboard {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .score-box {
            background-color: #ffeaa7;
            padding: 10px 20px;
            border-radius: 10px;
            border: 2px solid #fdcb6e;
            font-weight: bold;
            min-width: 100px;
        }
        .game-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 180px;
            position: relative;
            margin: 20px auto;
            width: 90%;
            max-width: 500px;
        }
        .cup-wrapper {
            position: absolute;
            width: 80px;
            height: 120px;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
        }
        .cup {
            font-size: 60px;
            user-select: none;
            transition: transform 0.3s;
        }
        .cup.lifted {
            transform: translateY(-50px);
        }
        .item {
            font-size: 35px;
            position: absolute;
            bottom: 10px;
            z-index: -1;
            display: none;
        }
        .btn {
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .btn:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        #message {
            font-size: 18px;
            font-weight: bold;
            margin-