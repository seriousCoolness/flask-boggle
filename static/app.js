const guessForm = $("#guess-form");
const guessInput = $("#guess-input");
const guessResponse = $("#guess-response");
const scoreCounter = $("#score-counter");
const timeCounter = $("#time-counter");

let score = 0;
let timer = 60;
let gameOver = false;
let pageReady = false;
let word_list = [];

let timerInterval = null;

async function onGuessSubmit(evt) 
{
    evt.preventDefault();
    
    if(!pageReady || timer <= 0 || !window.location.pathname.includes('/board')) { return; }
    
    const word_guess = guessInput.val().toLowerCase().split(' ')[0];
    const res = await sendGuess(word_guess);

    displayResult(word_guess, res.data.result);    
}
guessForm.on("submit", onGuessSubmit);


async function sendGuess(form_guess) { return await axios.postForm('/submit', { guess: form_guess }); }

async function sendRecords() { return await axios.post('/records', { score: score }); }

function displayResult(guess, result) 
{
    if(result == "ok")
    {
        if(!word_list.find((word) => word.toLowerCase() == guess.toLowerCase()))
        {
            guessResponse.text(`${guess.substring(0,1).toUpperCase() + guess.substring(1).toLowerCase()} is on the board!`);
            addScore(guess.length);
            word_list.push(guess.toLowerCase());
        }
        else
            guessResponse.text(`${guess.substring(0,1).toUpperCase() + guess.substring(1).toLowerCase()} has already been used...`);
    }
    else if(result == "not-on-board")
        guessResponse.text(`${guess.substring(0,1).toUpperCase() + guess.substring(1).toLowerCase()} was not on the board.`);
    else if(result == "not-word")
        guessResponse.text(`${guess.substring(0,1).toUpperCase() + guess.substring(1).toLowerCase()} isn't a recognized word...`);  
}


function addScore(points) 
{
    score += points;
    scoreCounter.text(`Points: ${score}`);
    sessionStorage.setItem("cookieScore", score);
}


function loadScoreAndTime()
{
    pageReady = true;
    score = sessionStorage.getItem("cookieScore") != null ? parseInt(sessionStorage.getItem("cookieScore")) : 0;
    timer = sessionStorage.getItem("cookieTime") != null ? parseInt(sessionStorage.getItem("cookieTime")) : 60;
    timerInterval = setInterval(tickSecond, 1000);

    if(timer <= 0)
    {
        gameOver = true;
        $("#game-section").hide();
        $("#final-score").text(`Final Score: ${score}`);
    }
    else
    {
        scoreCounter.text(`Points: ${score}`);
        timeCounter.text(`Time: ${timer}`);
    }
}
$(document).ready(loadScoreAndTime);

async function tickSecond()
{
    if(pageReady && window.location.pathname.includes('/board'))
    {
        if(timer > 0)
        {
            timer += -1;
            timeCounter.text(`Time: ${timer}`);
            sessionStorage.setItem("cookieTime", timer);
        }
        else if (sessionStorage.getItem('submittedRecords') != true)
        {
            clearInterval(timerInterval);
            $("#game-section").hide();
            $("#final-score").text(`Final Score: ${score}`);
            sessionStorage.setItem("cookieTime", 0);
            res = await sendRecords(score);
            sessionStorage.setItem('submittedRecords', true);
        }
    }
}

function startGame(evt)
{
    if(sessionStorage.getItem("cookieTime") != null && sessionStorage.getItem("cookieTime") <= 0)
        sessionStorage.clear();
}
$("#start-game").on("submit", startGame);