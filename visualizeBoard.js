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

function toHumanReadableStr(inputArg, withBolds = true) {
  let intArr = inputArg;
  if (typeof inputArg === "string") {
    intArr = toIntArr(inputArg);
  }

  function intToHrChar(_int) {
    const bfMapping = {
      0: "0",
      1: "<",
      2: ">",
      3: "{",
      4: "}",
      5: "-",
      6: "+",
      7: ".",
      8: ",",
      9: "[",
      10: "]",
    };
    if (_int in bfMapping) {
      return bfMapping[_int];
    } else if (_int >= -10 && _int < 0) {
      return String(-_int);
    } else if (_int > 10 && _int <= 36) {
      return String.fromCharCode(_int + 65 - 11);
    } else if (_int >= -36 && _int < -10) {
      return String.fromCharCode(-_int + 97 - 11);
    } else if (_int > 36) {
      return withBolds ? "<b>%</b>" : "%";
    } else if (_int < -36) {
      return withBolds ? "<b>&</b>" : "&";
    }
  }

  return intArr.map(intToHrChar).join("");
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

// Add visualization to the lifeBoard div
function visualizeProgram(program, cellElement) {
  if (!cellElement) return; // Add this check

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
  cellElement.style.aspectRatio = "1 / 1"; // Add this line to ensure square cells
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
  container.innerHTML = ""; // Clear existing content

  // Create step counter
  const stepCounter = document.createElement("div");
  stepCounter.id = "stepCounter";
  stepCounter.style.textAlign = "center";
  stepCounter.style.fontSize = "18px";
  stepCounter.style.marginBottom = "10px";
  container.appendChild(stepCounter);

  // Create grid
  const grid = document.createElement("div");
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = `repeat(${width}, 40px)`;
  grid.style.gridTemplateRows = `repeat(${height}, 40px)`;
  grid.style.gap = "1px";
  grid.style.backgroundColor = "#ccc";
  grid.style.padding = "1px";
  grid.style.width = "100%";
  grid.style.height = "calc(100vh - 30px)"; // Adjust for step counter
  grid.style.overflow = "hidden";
  container.appendChild(grid);
  const cells = [];
  for (let i = 0; i < width * height; i++) {
    const cell = document.createElement("div");
    cell.style.backgroundColor = "#fff";
    grid.appendChild(cell);
    cells.push(cell);
  }
  return cells;
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
    Array.from({ length: width }, () => randomProgram())
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
        grid[x2][y2]
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
updateGrid(grid, cells);

function step() {
  grid = updateState(grid);
  updateGrid(grid, cells);
  stepCount++;
  document.getElementById("stepCounter").textContent = `Step: ${stepCount}`;
  setTimeout(step, 0);
}

step();

// Example usage
const program = randomProgram();
visualizeProgram(program);
