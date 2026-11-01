(function () {
    const form = document.getElementById('sortForm');
    const numbersInput = document.getElementById('numbers');
    const randomBtn = document.getElementById('randomBtn');

    // "Random numbers": fill the box with random values and sort them
    randomBtn.addEventListener('click', function () {
        const values = [];
        for (let i = 0; i < 10; i++) {
            values.push(Math.floor(Math.random() * 99) + 1);
        }
        numbersInput.value = values.join(', ');
        form.submit();
    });

    // Clicking another algorithm card sorts the same numbers again
    form.querySelectorAll('input[name="algorithm"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            if (numbersInput.value.trim() !== '') { form.submit(); }
        });
    });

    const box = document.getElementById('syAnim');
    if (!box) { return; }   // nothing sorted yet, no animation to run

    const frames = JSON.parse(box.dataset.frames);

    const tilesBox = document.getElementById('syTiles');
    const capEl = document.getElementById('syCaption');
    const cmpEl = document.getElementById('syCmp');
    const swpEl = document.getElementById('sySwp');
    const stepEl = document.getElementById('syStep');
    const restartBtn = document.getElementById('syRestart');
    const backBtn = document.getElementById('syBack');
    const playBtn = document.getElementById('syPlay');
    const nextBtn = document.getElementById('syNext');
    const scrub = document.getElementById('syScrub');
    const speedSel = document.getElementById('sySpeed');

    const count = frames[0].values.length;
    let index = 0;
    let timer = null;
    let shown = null;      // the values currently drawn, used to spot swaps

    scrub.max = frames.length - 1;
    if (count > 16) { tilesBox.classList.add('sy-dense'); }

    // one cell per number: the tile, its index and a pointer label
    const cells = [];
    for (let i = 0; i < count; i++) {
        const cell = document.createElement('div');
        cell.className = 'sy-cell';
        const tile = document.createElement('div');
        tile.className = 'sy-tile';
        const idx = document.createElement('div');
        idx.className = 'sy-idx';
        idx.textContent = i;
        const tag = document.createElement('div');
        tag.className = 'sy-tag';
        cell.appendChild(tile);
        cell.appendChild(idx);
        cell.appendChild(tag);
        tilesBox.appendChild(cell);
        cells.push({ cell: cell, tile: tile, tag: tag });
    }

    function tileState(frame, i) {
        if (frame.swap.indexOf(i) !== -1) { return 'sy-swap'; }
        if (frame.compare.indexOf(i) !== -1) { return 'sy-compare'; }
        if (frame.pivot === i) { return 'sy-pivot'; }
        if (frame.marker.indexOf(i) !== -1) { return 'sy-marker'; }
        if (frame.done.indexOf(i) !== -1) { return 'sy-done'; }
        return '';
    }

    // two tiles trade places: slide them across, one over and one under
    function animateSwap(a, b, duration) {
        const dx = cells[b].cell.offsetLeft - cells[a].cell.offsetLeft;
        const lift = 22;
        const tileA = cells[a].tile;
        const tileB = cells[b].tile;
        tileA.style.zIndex = 3;
        tileB.style.zIndex = 2;
        tileA.animate([
            { transform: 'translate(' + dx + 'px, 0)' },
            { transform: 'translate(' + (dx / 2) + 'px, -' + lift + 'px)' },
            { transform: 'translate(0, 0)' }
        ], { duration: duration, easing: 'ease-in-out' });
        tileB.animate([
            { transform: 'translate(' + (-dx) + 'px, 0)' },
            { transform: 'translate(' + (-dx / 2) + 'px, ' + lift + 'px)' },
            { transform: 'translate(0, 0)' }
        ], { duration: duration, easing: 'ease-in-out' }).onfinish = function () {
            tileA.style.zIndex = '';
            tileB.style.zIndex = '';
        };
    }

    // one tile gets a new value (merge sort writing): a quick pop
    function animatePop(i, duration) {
        cells[i].tile.animate([
            { transform: 'scale(0.6)' },
            { transform: 'scale(1.15)' },
            { transform: 'scale(1)' }
        ], { duration: duration, easing: 'ease-out' });
    }

    function render() {
        const frame = frames[index];
        const interval = Number(speedSel.value);
        const duration = Math.max(120, Math.min(450, interval * 0.8));

        cells.forEach(function (c, i) {
            c.tile.className = 'sy-tile ' + tileState(frame, i);
            c.tile.textContent = frame.values[i];
            c.tag.textContent = frame.tags[i] ? '▲ ' + frame.tags[i] : '';
        });

        if (shown) {
            const changed = [];
            for (let i = 0; i < count; i++) {
                if (shown[i] !== frame.values[i]) { changed.push(i); }
            }
            if (changed.length === 2 &&
                shown[changed[0]] === frame.values[changed[1]] &&
                shown[changed[1]] === frame.values[changed[0]]) {
                animateSwap(changed[0], changed[1], duration);
            } else if (changed.length === 1) {
                animatePop(changed[0], duration);
            }
        }
        shown = frame.values.slice();

        capEl.textContent = frame.text;
        cmpEl.textContent = frame.comparisons;
        swpEl.textContent = frame.swaps;
        scrub.value = index;
        stepEl.textContent = 'Step ' + (index + 1) + ' of ' + frames.length;
    }

    function pause() {
        clearInterval(timer);
        timer = null;
        playBtn.textContent = '▶ Play';
    }

    function tick() {
        if (index < frames.length - 1) {
            index++;
            render();
        } else {
            pause();
        }
    }

    function play() {
        if (index >= frames.length - 1) { index = 0; shown = null; render(); }
        clearInterval(timer);
        timer = setInterval(tick, Number(speedSel.value));
        playBtn.textContent = '⏸ Pause';
    }

    playBtn.addEventListener('click', function () {
        if (timer) { pause(); } else { play(); }
    });

    nextBtn.addEventListener('click', function () {
        pause();
        if (index < frames.length - 1) { index++; render(); }
    });

    backBtn.addEventListener('click', function () {
        pause();
        if (index > 0) { index--; render(); }
    });

    restartBtn.addEventListener('click', function () {
        index = 0;
        shown = null;
        render();
        play();
    });

    scrub.addEventListener('input', function () {
        pause();
        index = Number(scrub.value);
        render();
    });

    speedSel.addEventListener('change', function () {
        if (timer) { play(); }
    });

    render();
    play();
})();