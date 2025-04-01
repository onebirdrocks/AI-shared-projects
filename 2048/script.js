const gameBoard = document.getElementById('game-board');
const newGameButton = document.getElementById('new-game');

let board = [];
const size = 4;

let moveCount = 0;
const moveCountElement = document.getElementById('move-count');

let totalScore = 0;
const totalScoreElement = document.getElementById('total-score');

let audioContext;

function createAudioContext() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playMoveSound() {
    createAudioContext();
    
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(440, audioContext.currentTime); // A4音
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.1);
}

function playScoreSound() {
    createAudioContext();
    
    const oscillator1 = audioContext.createOscillator();
    const oscillator2 = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator1.connect(gainNode);
    oscillator2.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator1.type = 'sine';
    oscillator2.type = 'square';
    
    oscillator1.frequency.setValueAtTime(523.25, audioContext.currentTime); // C5音
    oscillator2.frequency.setValueAtTime(659.25, audioContext.currentTime); // E5音
    
    gainNode.gain.setValueAtTime(0.4, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
    
    oscillator1.start(audioContext.currentTime);
    oscillator2.start(audioContext.currentTime);
    oscillator1.stop(audioContext.currentTime + 0.3);
    oscillator2.stop(audioContext.currentTime + 0.3);
}

function initializeGame() {
    board = Array(size).fill().map(() => Array(size).fill(0));
    addNewTile();
    addNewTile();
    moveCount = 0;
    moveCountElement.textContent = moveCount;
    totalScore = 0;
    totalScoreElement.textContent = totalScore;
    updateBoard(); // 移到这里，确保在添加新方块后更新棋盘
}

function addNewTile() {
    const emptyTiles = [];
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            if (board[i][j] === 0) {
                emptyTiles.push({i, j});
            }
        }
    }
    if (emptyTiles.length > 0) {
        const {i, j} = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
        board[i][j] = {
            value: Math.random() < 0.9 ? 2 : 4,
            isNew: true,
            merged: false
        };
    }
}

function updateBoard() {
    gameBoard.innerHTML = '';
    
    // 创建格子背景
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const gridCell = document.createElement('div');
            gridCell.className = 'grid-cell';
            gameBoard.appendChild(gridCell);
        }
    }
    
    // 创建方块
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const tile = board[i][j];
            if (tile !== 0) {
                const tileElement = document.createElement('div');
                tileElement.className = 'tile';
                tileElement.textContent = tile.value;
                tileElement.setAttribute('data-value', tile.value);
                tileElement.style.top = `${i * 100 + 15}px`;
                tileElement.style.left = `${j * 100 + 15}px`;
                if (tile.isNew) {
                    tileElement.classList.add('new');
                }
                if (tile.merged) {
                    tileElement.classList.add('merged');
                }
                gameBoard.appendChild(tileElement);
            }
        }
    }
}

function move(direction) {
    let moved = false;
    const newBoard = JSON.parse(JSON.stringify(board));

    // 重置所有方块的状态
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            if (newBoard[i][j] !== 0) {
                newBoard[i][j].merged = false;
                newBoard[i][j].isNew = false;
            }
        }
    }

    function moveInDirection(row, col, rowStep, colStep) {
        if (newBoard[row][col] === 0) return false;
        let newRow = row + rowStep;
        let newCol = col + colStep;
        while (newRow >= 0 && newRow < size && newCol >= 0 && newCol < size) {
            if (newBoard[newRow][newCol] === 0) {
                newBoard[newRow][newCol] = newBoard[row][col];
                newBoard[row][col] = 0;
                row = newRow;
                col = newCol;
                moved = true;
            } else if (newBoard[newRow][newCol].value === newBoard[row][col].value && !newBoard[newRow][newCol].merged) {
                newBoard[newRow][newCol] = {
                    value: newBoard[newRow][newCol].value * 2,
                    merged: true,
                    isNew: false
                };
                totalScore += newBoard[newRow][newCol].value;
                newBoard[row][col] = 0;
                moved = true;
                playScoreSound();
                break;
            } else {
                break;
            }
            newRow += rowStep;
            newCol += colStep;
        }
    }

    if (direction === 'up') {
        for (let col = 0; col < size; col++) {
            for (let row = 1; row < size; row++) {
                moveInDirection(row, col, -1, 0);
            }
        }
    } else if (direction === 'down') {
        for (let col = 0; col < size; col++) {
            for (let row = size - 2; row >= 0; row--) {
                moveInDirection(row, col, 1, 0);
            }
        }
    } else if (direction === 'left') {
        for (let row = 0; row < size; row++) {
            for (let col = 1; col < size; col++) {
                moveInDirection(row, col, 0, -1);
            }
        }
    } else if (direction === 'right') {
        for (let row = 0; row < size; row++) {
            for (let col = size - 2; col >= 0; col--) {
                moveInDirection(row, col, 0, 1);
            }
        }
    }

    if (moved) {
        board = newBoard;
        addNewTile();
        updateBoard();
        updateMoveCount();
        totalScoreElement.textContent = totalScore;
        playMoveSound();
    }
}

function updateMoveCount() {
    moveCount++;
    moveCountElement.textContent = moveCount;
}

document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case 'ArrowUp':
            move('up');
            break;
        case 'ArrowDown':
            move('down');
            break;
        case 'ArrowLeft':
            move('left');
            break;
        case 'ArrowRight':
            move('right');
            break;
    }
});

let startX, startY, endX, endY;
const minSwipeDistance = 50; // 小滑动距离,单位为像素
let isDragging = false; // 新增: 用于跟踪是否正在拖动

function handleSwipe() {
    const deltaX = endX - startX;
    const deltaY = endY - startY;
    
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
        // 水平滑动
        if (Math.abs(deltaX) > minSwipeDistance) {
            if (deltaX > 0) {
                move('right');
            } else {
                move('left');
            }
        }
    } else {
        // 垂直滑动
        if (Math.abs(deltaY) > minSwipeDistance) {
            if (deltaY > 0) {
                move('down');
            } else {
                move('up');
            }
        }
    }
}

// 修改鼠标事件监听器
gameBoard.addEventListener('mousedown', (e) => {
    startX = e.clientX;
    startY = e.clientY;
    isDragging = true;
});

gameBoard.addEventListener('mousemove', (e) => {
    if (isDragging) {
        endX = e.clientX;
        endY = e.clientY;
    }
});

gameBoard.addEventListener('mouseup', () => {
    if (isDragging) {
        handleSwipe();
        isDragging = false;
    }
});

gameBoard.addEventListener('mouseleave', () => {
    if (isDragging) {
        handleSwipe();
        isDragging = false;
    }
});

// 保留触摸事件监听器
gameBoard.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
}, false);

gameBoard.addEventListener('touchend', (e) => {
    endX = e.changedTouches[0].clientX;
    endY = e.changedTouches[0].clientY;
    handleSwipe();
}, false);

newGameButton.addEventListener('click', initializeGame);

initializeGame();