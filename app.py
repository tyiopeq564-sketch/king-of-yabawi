import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="천하제일 야바위 대회", page_icon="🔮", layout="centered")

st.title("🔮 천하제일 야바위 대회")
st.write("눈앞에서 휙휙 섞이는 컵을 잘 보고 보석이 든 컵을 맞혀보세요!")
st.markdown("---")

# HTML + JavaScript 기반의 진짜 움직이는 게임 구현 (따옴표 에러 방지 처리)
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
            margin-top: 20px;
            min-height: 27px;
        }
    </style>
</head>
<body>

    <div class="scoreboard">
        <div class="score-box" style="background-color: #fab1a0; border-color: #e17055;">🔥 현재 연승: <span id="current-streak">0</span></div>
        <div class="score-box">👑 최고 기록: <span id="max-streak">0</span></div>
    </div>

    <div class="game-container" id="stage">
        <div class="cup-wrapper" id="cup0" onclick="clickCup(0)">
            <div class="item" id="item0">❌</div>
            <div class="cup" id="cup-img0">🥤</div>
        </div>
        <div class="cup-wrapper" id="cup1" onclick="clickCup(1)">
            <div class="item" id="item1">❌</div>
            <div class="cup" id="cup-img1">🥤</div>
        </div>
        <div class="cup-wrapper" id="cup2" onclick="clickCup(2)">
            <div class="item" id="item2">❌</div>
            <div class="cup" id="cup-img2">🥤</div>
        </div>
    </div>

    <button class="btn" id="start-btn" onclick="startShuffle()">🔮 컵 섞기 시작!</button>
    <div id="message">😏 쫄지 말고 [컵 섞기 시작]을 눌러봐!</div>

    <script>
        let streak = 0;
        let maxStreak = 0;
        let answer = 1;
        let positions = [0, 1, 2];
        let isShuffling = false;
        let isGameOver = true;
        
        const cardWidth = 100;
        
        function updatePositions() {
            const containerWidth = document.getElementById('stage').offsetWidth;
            const center = containerWidth / 2;
            
            positions.forEach((posIndex, cupIndex) => {
                const cup = document.getElementById('cup' + cupIndex);
                const leftPos = center + (posIndex - 1) * cardWidth - 40; 
                cup.style.left = leftPos + 'px';
            });
        }

        window.onload = () => {
            updatePositions();
            window.addEventListener('resize', updatePositions);
        };

        async function startShuffle() {
            if (isShuffling) return;
            
            isShuffling = true;
            isGameOver = false;
            document.getElementById('start-btn').disabled = true;
            document.getElementById('message').innerText = "👀 눈 떼지 마라! 컵 섞는다!!";
            
            for(let i=0; i<3; i++) {
                document.getElementById('cup-img' + i).classList.remove('lifted');
                document.getElementById('item' + i).style.display = 'none';
            }
            await new Promise(r => setTimeout(r, 400));

            answer = Math.floor(Math.random() * 3);
            for(let i=0; i<3; i++) {
                document.getElementById('item' + i).innerText = (i === answer) ? "💎" : "❌";
            }

            for (let k = 0; k < 8; k++) {
                let idx1 = Math.floor(Math.random() * 3);
                let idx2 = Math.floor(Math.random() * 3);
                while(idx1 === idx2) { idx2 = Math.floor(Math.random() * 3); }
                
                let temp = positions[idx1];
                positions[idx1] = positions[idx2];
                positions[idx2] = temp;
                
                updatePositions();
                await new Promise(r => setTimeout(r, 250));
            }
            
            isShuffling = false;
            document.getElementById('message').innerText = "👇 자, 보석이 든 컵을 골라봐!";
        }

        function clickCup(cupIndex) {
            if (isShuffling || isGameOver) return;
            isGameOver = true;
            
            for(let i=0; i<3; i++) {
                document.getElementById('cup-img' + i).classList.add('lifted');
                document.getElementById('item' + i).style.display = 'block';
            }
            
            if (cupIndex === answer) {
                streak++;
                if (streak > maxStreak) maxStreak = streak;
                document.getElementById('message').innerText = "🎉 대박 정답! 손기술 장난 아닌데?";
            } else {
                streak = 0;
                document.getElementById('message').innerText = "💥 맹탕! 타짜한테 당했쥬? 연승 리셋!";
            }
            
            document.getElementById('current-streak').innerText = streak;
            document.getElementById('max-streak').innerText = maxStreak;
            document.getElementById('start-btn').disabled = false;
            document.getElementById('start-btn').innerText = "🔄 한 판 더 하기";
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=380)