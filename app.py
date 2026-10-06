import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Hunter 🐍",
    page_icon="🐍",
    layout="centered",
)

st.markdown("""
<style>
    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 20px;
        max-width: 950px;
    }

    .title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 20px;
    }
</style>

<div class="title">🐍 SNAKE HUNTER 🍎</div>
<div class="subtitle">Classic Snake • Neon Edition</div>
""", unsafe_allow_html=True)


GAME = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: transparent;
    font-family: Arial, sans-serif;
    color: white;
}

.container {
    max-width: 850px;
    margin: auto;
}

.hud {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 10px;
}

.card {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 10px;
    text-align: center;
}

.label {
    font-size: 11px;
    color: #94a3b8;
    text-transform: uppercase;
}

.value {
    font-size: 22px;
    font-weight: bold;
}

.game {
    position: relative;
    background: #020617;
    border-radius: 20px;
    overflow: hidden;
    border: 2px solid #06b6d4;
    box-shadow:
        0 0 30px rgba(6,182,212,.25),
        inset 0 0 30px rgba(0,0,0,.5);
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    touch-action: none;
}

.overlay {
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(2,6,23,.85);
}

.panel {
    text-align: center;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 24px;
    padding: 35px;
    width: 90%;
    max-width: 450px;
}

.panel h1 {
    font-size: 35px;
    margin: 10px;
}

.panel p {
    color: #cbd5e1;
}

button {
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    margin: 5px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    background: linear-gradient(135deg,#06b6d4,#2563eb);
}

button:hover {
    transform: scale(1.05);
}

.secondary {
    background: #1e293b;
}

.controls {
    display: grid;
    grid-template-columns: repeat(3, 60px);
    justify-content: center;
    gap: 7px;
    margin-top: 12px;
}

.controls button {
    height: 50px;
    padding: 0;
    font-size: 20px;
}

.empty {
    visibility: hidden;
}

.help {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    margin-top: 10px;
}

@media(max-width:600px) {

    .hud {
        grid-template-columns: repeat(2,1fr);
    }

    .controls {
        grid-template-columns: repeat(3,55px);
    }

}

</style>
</head>


<body>

<div class="container">

    <div class="hud">

        <div class="card">
            <div class="label">Score</div>
            <div id="score" class="value">0</div>
        </div>

        <div class="card">
            <div class="label">Best</div>
            <div id="best" class="value">0</div>
        </div>

        <div class="card">
            <div class="label">Level</div>
            <div id="level" class="value">1</div>
        </div>

        <div class="card">
            <div class="label">Speed</div>
            <div id="speed" class="value">1.0x</div>
        </div>

    </div>


    <div class="game">

        <canvas id="canvas" width="720" height="720"></canvas>

        <div class="overlay" id="overlay">

            <div class="panel">

                <div style="font-size:60px;">
                    🐍🍎
                </div>

                <h1 id="title">
                    SNAKE HUNTER
                </h1>

                <p id="message">
                    Ăn táo và trở thành con rắn dài nhất!
                </p>

                <button id="start">
                    BẮT ĐẦU
                </button>

                <button
                    class="secondary"
                    id="resetBest">
                    XÓA KỶ LỤC
                </button>

            </div>

        </div>

    </div>


    <div class="controls">

        <button class="empty">•</button>

        <button onclick="changeDirection('up')">
            ▲
        </button>

        <button class="empty">•</button>

        <button onclick="changeDirection('left')">
            ◀
        </button>

        <button onclick="changeDirection('down')">
            ▼
        </button>

        <button onclick="changeDirection('right')">
            ▶
        </button>

    </div>


    <div class="help">
        🎮 WASD / Mũi tên để di chuyển • SPACE để tạm dừng
    </div>

</div>


<script>

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");


const GRID = 24;

const CELL =
    canvas.width / GRID;


let snake;

let apple;

let direction;

let nextDirection;

let score;

let level;

let running = false;

let paused = false;

let timer;


let best =
    Number(localStorage.getItem(
        "snakeBest"
    ) || 0);


document.getElementById("best")
    .textContent = best;


/* =========================
   RESET GAME
========================= */

function resetGame() {

    snake = [

        {x:12,y:12},

        {x:11,y:12},

        {x:10,y:12},

        {x:9,y:12}

    ];


    direction = {
        x:1,
        y:0
    };


    nextDirection = {
        x:1,
        y:0
    };


    score = 0;

    level = 1;

    paused = false;


    createApple();

    updateHUD();

    draw();

}


/* =========================
   CREATE APPLE
========================= */

function createApple() {

    do {

        apple = {

            x: Math.floor(
                Math.random() * GRID
            ),

            y: Math.floor(
                Math.random() * GRID
            )

        };

    }

    while (
        snake.some(
            part =>
            part.x === apple.x &&
            part.y === apple.y
        )
    );

}


/* =========================
   CHANGE DIRECTION
========================= */

function changeDirection(dir) {

    const directions = {

        up: {
            x:0,
            y:-1
        },

        down: {
            x:0,
            y:1
        },

        left: {
            x:-1,
            y:0
        },

        right: {
            x:1,
            y:0
        }

    };


    const newDirection =
        directions[dir];


    if (
        newDirection.x === -direction.x &&
        newDirection.y === -direction.y
    ) {
        return;
    }


    nextDirection =
        newDirection;


    if (!running) {

        startGame();

    }

}


/* =========================
   START
========================= */

function startGame() {

    resetGame();

    running = true;

    document
        .getElementById("overlay")
        .style.display = "none";


    startTimer();

}


/* =========================
   TIMER
========================= */

function startTimer() {

    clearInterval(timer);


    const speed =
        Math.max(
            55,
            150 - (level - 1) * 10
        );


    timer =
        setInterval(
            gameLoop,
            speed
        );

}


/* =========================
   GAME LOOP
========================= */

function gameLoop() {

    if (!running || paused) {
        return;
    }


    direction =
        nextDirection;


    const head = {

        x: snake[0].x +
            direction.x,

        y: snake[0].y +
            direction.y

    };


    /* WALL COLLISION */

    if (
        head.x < 0 ||
        head.x >= GRID ||
        head.y < 0 ||
        head.y >= GRID
    ) {

        gameOver();

        return;

    }


    /* BODY COLLISION */

    for (
        let i = 0;
        i < snake.length;
        i++
    ) {

        if (
            head.x === snake[i].x &&
            head.y === snake[i].y
        ) {

            gameOver();

            return;

        }

    }


    snake.unshift(head);


    /* EAT APPLE */

    if (
        head.x === apple.x &&
        head.y === apple.y
    ) {

        score += 10;


        level =
            Math.floor(score / 50) + 1;


        createApple();

        startTimer();

    }

    else {

        snake.pop();

    }


    updateHUD();

    draw();

}


/* =========================
   GAME OVER
========================= */

function gameOver() {

    running = false;

    clearInterval(timer);


    if (score > best) {

        best = score;

        localStorage.setItem(
            "snakeBest",
            best
        );

    }


    updateHUD();


    document.getElementById(
        "title"
    ).textContent =
        "GAME OVER 💥";


    document.getElementById(
        "message"
    ).textContent =
        "Điểm của bạn: " +
        score +
        " • Kỷ lục: " +
        best;


    document.getElementById(
        "start"
    ).textContent =
        "CHƠI LẠI";


    document.getElementById(
        "overlay"
    ).style.display =
        "flex";

}


/* =========================
   PAUSE
========================= */

function togglePause() {

    if (!running) {
        return;
    }


    paused = !paused;


    document.getElementById(
        "title"
    ).textContent =
        paused
        ? "TẠM DỪNG ⏸️"
        : "SNAKE HUNTER";


    if (paused) {

        document.getElementById(
            "overlay"
        ).style.display =
            "flex";

    }

    else {

        document.getElementById(
            "overlay"
        ).style.display =
            "none";

    }

}


/* =========================
   HUD
========================= */

function updateHUD() {

    document.getElementById(
        "score"
    ).textContent =
        score;


    document.getElementById(
        "best"
    ).textContent =
        best;


    document.getElementById(
        "level"
    ).textContent =
        level;


    document.getElementById(
        "speed"
    ).textContent =
        (
            1 +
            (level - 1) * 0.12
        ).toFixed(1) + "x";

}


/* =========================
   DRAW BACKGROUND
========================= */

function drawBackground() {

    ctx.fillStyle =
        "#020617";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /* GRID */

    ctx.strokeStyle =
        "rgba(148,163,184,0.08)";

    ctx.lineWidth = 1;


    for (
        let i=0;
        i<=GRID;
        i++
    ) {

        ctx.beginPath();

        ctx.moveTo(
            i * CELL,
            0
        );

        ctx.lineTo(
            i * CELL,
            canvas.height
        );

        ctx.stroke();


        ctx.beginPath();

        ctx.moveTo(
            0,
            i * CELL
        );

        ctx.lineTo(
            canvas.width,
            i * CELL
        );

        ctx.stroke();

    }

}


/* =========================
   DRAW APPLE
========================= */

function drawApple() {

    const x =
        apple.x * CELL +
        CELL / 2;

    const y =
        apple.y * CELL +
        CELL / 2;


    ctx.shadowColor =
        "#ef4444";

    ctx.shadowBlur = 20;


    ctx.fillStyle =
        "#ef4444";


    ctx.beginPath();

    ctx.arc(
        x,
        y + 2,
        CELL * 0.32,
        0,
        Math.PI * 2
    );

    ctx.fill();


    /* HIGHLIGHT */

    ctx.shadowBlur = 0;

    ctx.fillStyle =
        "rgba(255,255,255,.7)";


    ctx.beginPath();

    ctx.arc(
        x - 5,
        y - 5,
        4,
        0,
        Math.PI * 2
    );

    ctx.fill();


    /* STEM */

    ctx.strokeStyle =
        "#78350f";

    ctx.lineWidth = 4;

    ctx.beginPath();

    ctx.moveTo(
        x,
        y - CELL * .28
    );

    ctx.lineTo(
        x + 3,
        y - CELL * .43
    );

    ctx.stroke();

}


/* =========================
   DRAW SNAKE
========================= */

function drawSnake() {

    snake.forEach(
        (part,index) => {

            const padding = 2;

            const x =
                part.x * CELL +
                padding;

            const y =
                part.y * CELL +
                padding;

            const size =
                CELL -
                padding * 2;


            if (index === 0) {

                ctx.shadowColor =
                    "#22c55e";

                ctx.shadowBlur = 18;

                ctx.fillStyle =
                    "#22c55e";

            }

            else {

                ctx.shadowBlur = 8;

                ctx.fillStyle =
                    "#16a34a";

            }


            ctx.beginPath();

            ctx.roundRect(
                x,
                y,
                size,
                size,
                7
            );

            ctx.fill();


            ctx.shadowBlur = 0;


            /* EYES */

            if (index === 0) {

                ctx.fillStyle =
                    "white";


                let eye1;
                let eye2;


                if (direction.x !== 0) {

                    eye1 = {
                        x:
                            x +
                            (direction.x > 0
                            ? size*.7
                            : size*.3),

                        y:
                            y +
                            size*.3
                    };


                    eye2 = {
                        x:
                            x +
                            (direction.x > 0
                            ? size*.7
                            : size*.3),

                        y:
                            y +
                            size*.7
                    };

                }

                else {

                    eye1 = {
                        x:
                            x +
                            size*.3,

                        y:
                            y +
                            (direction.y > 0
                            ? size*.7
                            : size*.3)
                    };


                    eye2 = {
                        x:
                            x +
                            size*.7,

                        y:
                            y +
                            (direction.y > 0
                            ? size*.7
                            : size*.3)
                    };

                }


                ctx.beginPath();

                ctx.arc(
                    eye1.x,
                    eye1.y,
                    3,
                    0,
                    Math.PI*2
                );

                ctx.arc(
                    eye2.x,
                    eye2.y,
                    3,
                    0,
                    Math.PI*2
                );

                ctx.fill();


                ctx.fillStyle =
                    "#020617";


                ctx.beginPath();

                ctx.arc(
                    eye1.x,
                    eye1.y,
                    1.5,
                    0,
                    Math.PI*2
                );

                ctx.arc(
                    eye2.x,
                    eye2.y,
                    1.5,
                    0,
                    Math.PI*2
                );

                ctx.fill();

            }

        }
    );

}


/* =========================
   DRAW
========================= */

function draw() {

    drawBackground();

    drawApple();

    drawSnake();

}


/* =========================
   KEYBOARD
========================= */

document.addEventListener(
    "keydown",
    function(event) {

        const key =
            event.key.toLowerCase();


        if (
            key === "arrowup" ||
            key === "w"
        ) {

            event.preventDefault();

            changeDirection("up");

        }


        else if (
            key === "arrowdown" ||
            key === "s"
        ) {

            event.preventDefault();

            changeDirection("down");

        }


        else if (
            key === "arrowleft" ||
            key === "a"
        ) {

            event.preventDefault();

            changeDirection("left");

        }


        else if (
            key === "arrowright" ||
            key === "d"
        ) {

            event.preventDefault();

            changeDirection("right");

        }


        else if (
            event.code === "Space"
        ) {

            event.preventDefault();

            togglePause();

        }

    }
);


/* =========================
   BUTTONS
========================= */

document.getElementById(
    "start"
).onclick = startGame;


document.getElementById(
    "resetBest"
).onclick = function() {

    best = 0;

    localStorage.setItem(
        "snakeBest",
        "0"
    );

    updateHUD();

};


/* =========================
   INITIALIZE
========================= */

resetGame();

</script>

</body>
</html>
"""


components.html(
    GAME,
    height=850,
    scrolling=False
)
