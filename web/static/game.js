const EMPTY = 0;
const PLAYER = 1;
const COMPUTER = 2;

const STORAGE_KEY = "ticTacToeGame";

let gameId;
let field;
let gameFinished;
let isWaiting;

const cells = document.querySelectorAll(".cell");
const statusElement = document.getElementById("status");
const newGameButton = document.getElementById("new-game");

function createGameId() {
    if (typeof crypto.randomUUID === "function") {
        return crypto.randomUUID();
    }

    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);

    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;

    const hex = Array.from(
        bytes,
        (byte) => byte.toString(16).padStart(2, "0")
    );

    return (
        hex.slice(0, 4).join("") + "-" +
        hex.slice(4, 6).join("") + "-" +
        hex.slice(6, 8).join("") + "-" +
        hex.slice(8, 10).join("") + "-" +
        hex.slice(10, 16).join("")
    );
}

function startNewGame() {
    gameId = createGameId();

    field = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ];

    gameFinished = false;
    isWaiting = false;

    saveGame();

    statusElement.textContent = "Твой ход";

    renderField();
}


function loadGame() {
    const savedGame = localStorage.getItem(STORAGE_KEY);

    if (savedGame === null) {
        startNewGame();
        return;
    }

    try {
        const data = JSON.parse(savedGame);

        if (
            typeof data.gameId !== "string" ||
            !isValidField(data.field)
        ) {
            startNewGame();
            return;
        }

        gameId = data.gameId;
        field = data.field;
        gameFinished = false;
        isWaiting = false;

        updateGameStatus();
        renderField();

    } catch (error) {
        startNewGame();
    }
}


function saveGame() {
    localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
            gameId: gameId,
            field: field,
        })
    );
}


function isValidField(value) {
    if (!Array.isArray(value) || value.length !== 3) {
        return false;
    }

    return value.every(
        (row) =>
            Array.isArray(row) &&
            row.length === 3 &&
            row.every(
                (cell) =>
                    cell === EMPTY ||
                    cell === PLAYER ||
                    cell === COMPUTER
            )
    );
}


function renderField() {
    cells.forEach((cell) => {
        const row = Number(cell.dataset.row);
        const column = Number(cell.dataset.column);

        const value = field[row][column];

        if (value === PLAYER) {
            cell.textContent = "X";

        } else if (value === COMPUTER) {
            cell.textContent = "O";

        } else {
            cell.textContent = "";
        }

        cell.disabled =
            value !== EMPTY ||
            gameFinished ||
            isWaiting;
    });
}


async function makeMove(row, column) {
    if (gameFinished || isWaiting) {
        return;
    }

    if (field[row][column] !== EMPTY) {
        return;
    }

    field[row][column] = PLAYER;
    isWaiting = true;

    statusElement.textContent =
        "Компьютер думает...";

    renderField();

    try {
        const response = await fetch(
            `/game/${gameId}`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({
                    id: gameId,
                    field: field,
                }),
            }
        );

        const data = await response.json();

        if (!response.ok) {
            field[row][column] = EMPTY;
            isWaiting = false;

            statusElement.textContent =
                data.error ?? "Произошла ошибка";

            renderField();

            return;
        }

        field = data.field;
        isWaiting = false;

        updateGameStatus();
        saveGame();
        renderField();

    } catch (error) {
        field[row][column] = EMPTY;
        isWaiting = false;

        statusElement.textContent =
            "Не удалось связаться с сервером";

        renderField();
    }
}


function updateGameStatus() {
    const winner = getWinner();

    if (winner === PLAYER) {
        gameFinished = true;

        statusElement.textContent =
            "Ты победил!";

        return;
    }

    if (winner === COMPUTER) {
        gameFinished = true;

        statusElement.textContent =
            "Компьютер победил";

        return;
    }

    if (isFieldFull()) {
        gameFinished = true;

        statusElement.textContent =
            "Ничья";

        return;
    }

    gameFinished = false;

    statusElement.textContent =
        "Твой ход";
}


function getWinner() {
    const lines = [
        [field[0][0], field[0][1], field[0][2]],
        [field[1][0], field[1][1], field[1][2]],
        [field[2][0], field[2][1], field[2][2]],

        [field[0][0], field[1][0], field[2][0]],
        [field[0][1], field[1][1], field[2][1]],
        [field[0][2], field[1][2], field[2][2]],

        [field[0][0], field[1][1], field[2][2]],
        [field[0][2], field[1][1], field[2][0]],
    ];

    for (const line of lines) {
        if (
            line[0] !== EMPTY &&
            line[0] === line[1] &&
            line[1] === line[2]
        ) {
            return line[0];
        }
    }

    return null;
}


function isFieldFull() {
    return field.every(
        (row) =>
            row.every(
                (cell) => cell !== EMPTY
            )
    );
}


cells.forEach((cell) => {
    cell.addEventListener("click", () => {
        const row = Number(cell.dataset.row);
        const column = Number(cell.dataset.column);

        makeMove(row, column);
    });
});


newGameButton.addEventListener(
    "click",
    startNewGame
);


loadGame();