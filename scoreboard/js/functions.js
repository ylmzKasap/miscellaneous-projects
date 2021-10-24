var audioMixer = new Audio();

function increment(elem) {
    // Increment player score.
    let infoBox = elem.parentElement.parentElement;
    let scoreDiv = infoBox.getElementsByClassName("score")[0];
    let score = parseInt(scoreDiv.innerHTML);
    scoreDiv.innerHTML = score  + 1;
    calculate_height();

    audioMixer.src = 'sound/gogo.mp3';
    audioMixer.play();
}

function decrement(elem) {
    infoBox = elem.parentElement.parentElement;
    let scoreDiv = infoBox.getElementsByClassName("score")[0];
    let score = parseInt(scoreDiv.innerHTML);
    if (score > 0) {
        scoreDiv.innerHTML = score - 1;
        calculate_height();
        audioMixer.src = 'sound/nono.mp3';
        audioMixer.play();
    } else {
        delete_std(infoBox);
    }
}

function calculate_height() {
    // Get the sum of all scores.
    let container = document.getElementsByClassName('container')[0];
    let everyone = Array.from(container.getElementsByClassName('column'));
    let scoreSum = everyone.reduce((total, current) => {
        return total + parseInt(current.querySelector('.score').innerHTML);
    }, 0)

    for (let i = 0; i < everyone.length; i++) {
        let score = parseInt(everyone[i].querySelector('.score').innerHTML);
        if (scoreSum > 0) {
            var rateToSum = parseInt(score / (scoreSum / 2) * 87);
        } else {
            var rateToSum = 0;
        }
        everyone[i].style.height = `${rateToSum + 30}%`;
    }
}

function delete_std(elem) {
    if (confirm('Remove the student?')) {
        elem.remove();
    };
}

function order_scores() {
    let container = document.getElementsByClassName('container')[0];
    let everyone = container.getElementsByClassName('column');

    // Get every id and their score in an array.
    let scores = [];
    for (let i = 0; i < everyone.length; i++) {
        scores.push([`#${everyone[i].id}`, parseInt(everyone[i].querySelector('.score').innerHTML)]);
    }

    scores.sort((a, b) => b[1] - a[1]);

    // Helper function for styling.
    const standings = ['winner', 'second', 'third'];
    function set_standing_style(playerBox, standing) {
        let nameBox = playerBox.getElementsByClassName('name-box')[0];
        let scoreBox = playerBox.getElementsByClassName('score')[0];
        let toStyle = [playerBox, nameBox, scoreBox];
        for (let i = 0; i < toStyle.length; i++) {
            toStyle[i].classList.add(standing);
            toStyle[i].classList.remove(...standings.filter(x => x != standing));
        }
    }
    
    // Set order and style attributes.
    for (let i = 0; i < everyone.length; i++) {
        let player = container.querySelector(scores[i][0]);
        let nameBox = player.getElementsByClassName('name-box')[0];
        let scoreBox = player.getElementsByClassName('score')[0];
        player.style.order = i;

        // Styling of the winner.
        if (i == 0 && scores[i][1] != 0) {
            set_standing_style(player, 'winner');
            }
            // Styling of the second.
            else if (i == 1 && scores[i][1] != 0) {
                set_standing_style(player, 'second');
            }
            // Styling of the third.
            else if (i == 2 && scores[i][1] != 0) {
                set_standing_style(player, 'third');
            }
            // Styling of the rest.
            else {
                player.classList.remove(...standings);
                nameBox.classList.remove(...standings);
                scoreBox.classList.remove(...standings);

    }
}
}

function getWinner() {
    let container = document.getElementsByClassName('container')[0];
    let everyone = Array.from(container.getElementsByClassName('column'));
    let winner = everyone.filter(x => x.classList.contains('winner'))[0];
    if (winner) {
        var winnerName = winner.querySelector('.student-name').innerHTML;
    }
    let winnerPic = winnerName.toLocaleLowerCase().split(' ').join('-');
    
    let overlay = container.querySelector('#winnerOverlay');
    let winnerBox = overlay.querySelector('#winnerName');
    winnerBox.innerHTML = `<h1>${winnerName} wins!</h1>`;
    let imageBox = overlay.querySelector('.winImage');
    imageBox.src = `pictures/${winnerPic}.png`;

    function playAudio(audio){
        return new Promise(res => {
          audio.play();
          audio.onended = res;
        })
      }

    async function playTogether(){
        audioMixer.src = 'sound/drum-roll.mp3';
        await playAudio(audioMixer);
        audioMixer.src = 'sound/you-win.mp3';
        audioMixer.play();
    }
    playTogether();
    overlay.removeAttribute('style');
}

function quitOverlay() {
    let container = document.getElementsByClassName('container')[0];
    let overlay = container.querySelector('#winnerOverlay');
    overlay.setAttribute('style', 'display: none;');
    if (overlay.classList[0]) {
        overlay.removeAttribute('class');
    }
    function remove_elem(elem, className) {
        if (elem.classList.contains(className)) {
            elem.classList.remove(className);
        }
    }
    let imageBox = overlay.querySelector('#winImageBox');
    remove_elem(imageBox, 'rollingBack');
    let winImage = overlay.querySelector('.winImage');
    remove_elem(winImage, 'rolling');
    let nameBox = overlay.querySelector('#winnerName');
    remove_elem(nameBox, 'epicEmphasis');

    if (!audioMixer.paused) {
        audioMixer.src = '';
    }
}

function initiateEpicMode() {
    let container = document.getElementsByClassName('container')[0];
    let overlay = container.querySelector('#winnerOverlay');
    if (overlay.classList[0]) {
        overlay.removeAttribute('class');
    } else {
        overlay.setAttribute('class', 'onDrugs');
    }

    function add_or_remove(elem, className) {
        if (elem.classList.contains(className)) {
            elem.classList.remove(className);
        } else {
            elem.classList.add(className);
        }
    }

    let imageBox = overlay.querySelector('#winImageBox');
    add_or_remove(imageBox, 'rollingBack');

    let winImage = overlay.querySelector('.winImage');
    add_or_remove(winImage, 'rolling');

    let nameBox = overlay.querySelector('#winnerName');
    add_or_remove(nameBox, 'epicEmphasis');

    epicRegex = /.*epic-mode.mp3/;
    if (epicRegex.test(audioMixer.src)) {
        audioMixer.src = '';
    } else {
        audioMixer.src = 'sound/epic-mode.mp3';
        audioMixer.play();
    }
}