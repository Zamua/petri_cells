function executeSelfModifyingBrainfuck(tape, maxReads = 2 ** 13) {
  if (typeof tape === "string") {
    tape = toIntArr(tape);
  }
  let head0 = 0;
  let head1 = 0;
  const loopStack = [];
  let pointer = 0;
  let numReads = 0;

  while (pointer < tape.length && numReads < maxReads) {
    numReads++;
    const char = tape[pointer];
    switch (char) {
      case 1:
        head0 = (head0 - 1 + tape.length) % tape.length;
        break;
      case 2:
        head0 = (head0 + 1) % tape.length;
        break;
      case 3:
        head1 = (head1 - 1 + tape.length) % tape.length;
        break;
      case 4:
        head1 = (head1 + 1) % tape.length;
        break;
      case 5:
        tape[head0]--;
        break;
      case 6:
        tape[head0]++;
        break;
      case 7:
        tape[head1] = tape[head0];
        break;
      case 8:
        tape[head0] = tape[head1];
        break;
      case 9:
        if (tape[head0] === 0) {
          let loopLevel = 1;
          while (
            loopLevel > 0 &&
            pointer < tape.length - 1 &&
            numReads < maxReads
          ) {
            numReads++;
            pointer++;
            if (tape[pointer] === 9) {
              loopLevel++;
            } else if (tape[pointer] === 10) {
              loopLevel--;
            }
          }
        } else {
          loopStack.push(pointer);
        }
        break;
      case 10:
        if (tape[head0] !== 0) {
          if (loopStack.length === 0) {
            pointer = 0;
            continue;
          } else {
            pointer = loopStack[loopStack.length - 1];
          }
        } else {
          if (loopStack.length > 0) {
            loopStack.pop();
          }
        }
        break;
    }
    pointer++;
  }
  return tape;
}

function randomProgram(size = 64, minInt = 0, maxInt = 10) {
  const randProgram = Array.from(
    { length: size },
    () => Math.floor(Math.random() * (maxInt - minInt + 1)) + minInt,
  );
  return toStr(randProgram);
}

function toIntArr(asStr, bitOffset = 128) {
  return Array.from(asStr).map((char) => char.charCodeAt(0) - bitOffset);
}

function toStr(asIntArr, bitOffset = 128) {
  return String.fromCharCode(
    ...asIntArr.map((num) => Math.max(num + bitOffset, 0)),
  );
}

function crossReactPrograms(a, b) {
  a = toIntArr(a);
  b = toIntArr(b);
  const out = executeSelfModifyingBrainfuck(a.concat(b));
  const halfLen = Math.floor(out.length / 2);
  a = toStr(out.slice(0, halfLen));
  b = toStr(out.slice(halfLen));
  return [a, b];
}

function visualizeProgram(program, cellElement) {
  if (!cellElement) return;

  const canvas = document.createElement("canvas");
  canvas.width = 32;
  canvas.height = 32;
  canvas.style.width = "100%";
  canvas.style.height = "100%";
  const ctx = canvas.getContext("2d");

  const intArr = toIntArr(program);

  for (let i = 0; i < 64; i++) {
    const x = (i % 8) * 4;
    const y = Math.floor(i / 8) * 4;
    const color = intToColor(intArr[i]);
    ctx.fillStyle = color;
    ctx.fillRect(x, y, 4, 4);
  }

  cellElement.innerHTML = "";
  cellElement.appendChild(canvas);
  cellElement.style.aspectRatio = "1 / 1";
}

function intToColor(num) {
  const colorMapping = {
    0: "#F0F2F3",
    1: "#E64C3C",
    2: "#F29B11",
    3: "#F3CF3E",
    4: "#7A3E00",
    5: "#145A32",
    6: "#A2D9CD",
    7: "#1A5276",
    8: "#A3E4D7",
    9: "#8E44AD",
    10: "#AE7AC4",
  };

  if (num in colorMapping) {
    return colorMapping[num];
  } else if (num < 0) {
    const x = Math.max(0, 1 + num / 256);
    return `rgb(${x * 255},${x * 255},${x * 255})`;
  } else if (num > 10) {
    const x = Math.max(0, 1 - num / 256);
    const r = Math.max(0, x - 0.0390625) * 255;
    return `rgb(${r},${x * 255},${x * 255})`;
  }
}

function createGrid(width, height) {
  const container = document.getElementById("lifeBoard");
  container.innerHTML = "";

  const stepCounter = document.createElement("div");

  stepCounter.textContent = `Step: 0`;
  stepCounter.id = "stepCounter";
  stepCounter.style.textAlign = "center";
  stepCounter.style.fontSize = "18px";
  stepCounter.style.marginBottom = "10px";
  container.appendChild(stepCounter);

  const grid = document.createElement("div");
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = `repeat(${width}, 3.8vmin)`;
  grid.style.gridTemplateRows = `repeat(${height}, 3.8vmin)`;
  grid.style.gap = ".4vmin";
  grid.style.padding = ".4vmin";
  container.appendChild(grid);
  const cells = [];
  for (let i = 0; i < width * height; i++) {
    const cell = document.createElement("div");
    cell.style.backgroundColor = "#fff";
    cell.style.cursor = "pointer";
    cell.addEventListener("click", () => copyProgramToClipboard(i));
    grid.appendChild(cell);
    cells.push(cell);
  }
  return cells;
}

function copyProgramToClipboard(index) {
  const program = grid[Math.floor(index / WIDTH)][index % WIDTH];
  navigator.clipboard
    .writeText(program)
    .then(() => {
      alert("Program copied to clipboard!");
    })
    .catch((err) => {
      console.error("Failed to copy program: ", err);
    });
}

function updateGrid(grid, cells) {
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      visualizeProgram(grid[i][j], cells[i * grid[i].length + j]);
    }
  }
}

function initializeGrid(width, height) {
  return Array.from({ length: height }, () =>
    Array.from({ length: width }, () => randomProgram()),
  );
}

function updateState(grid) {
  const height = grid.length;
  const width = grid[0].length;

  for (let i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      const x2 = (i + Math.floor(Math.random() * 5) - 2 + height) % height;
      const y2 = (j + Math.floor(Math.random() * 5) - 2 + width) % width;
      const [newProgram1, newProgram2] = crossReactPrograms(
        grid[i][j],
        grid[x2][y2],
      );
      grid[i][j] = newProgram1;
      grid[x2][y2] = newProgram2;
    }
  }

  return grid;
}
const WIDTH = 20;
const HEIGHT = 20;
let grid = initializeGrid(WIDTH, HEIGHT);
const cells = createGrid(WIDTH, HEIGHT);
updateGrid(grid, cells);
let stepCount = 0;
let isRunning = false;

function step() {
  if (isRunning) {
    grid = updateState(grid);
    updateGrid(grid, cells);
    stepCount++;
    document.getElementById("stepCounter").textContent = `Step: ${stepCount}`;
    setTimeout(step, 0);
  }
}

document.getElementById("lifeSimRun").addEventListener("click", () => {
  isRunning = !isRunning;
  if (isRunning) {
    step();
  }
});

const program = randomProgram();
visualizeProgram(program);
