function toIntArr(asStr, bitOffset = 128) {
  return Array.from(asStr).map((char) => char.charCodeAt(0) - bitOffset);
}

function toStr(asIntArr, bitOffset = 128) {
  return asIntArr
    .map((num) => String.fromCharCode(Math.max(num + bitOffset, 0)))
    .join("");
}

function executeSelfModifyingBrainfuck(tape, maxReads = 2 ** 13) {
  if (typeof tape === "string") {
    tape = toIntArr(tape);
  }
  let head0 = 0;
  let head1 = 0;
  let loopStack = [];
  let pointer = 0;
  let numReads = 0;
  while (pointer < tape.length && numReads < maxReads) {
    numReads += 1;
    let char = tape[pointer];
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
        tape[head0] -= 1;
        break;
      case 6:
        tape[head0] += 1;
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
            numReads += 1;
            pointer += 1;
            if (tape[pointer] === 9) {
              loopLevel += 1;
            } else if (tape[pointer] === 10) {
              loopLevel -= 1;
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
    pointer += 1;
  }
  return tape;
}

function randomProgram(size = 64, minInt = 0, maxInt = 10) {
  return toStr(
    Array.from(
      { length: size },
      () => Math.floor(Math.random() * (maxInt - minInt + 1)) + minInt,
    ),
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
    } else if (-10 <= _int && _int < 0) {
      return String(-_int);
    } else if (10 < _int && _int <= 26 + 10) {
      return String.fromCharCode(_int + 65 - 11);
    } else if (-26 - 10 <= _int && _int < -10) {
      return String.fromCharCode(-_int + 97 - 11);
    } else if (_int > 26 + 10) {
      return withBolds ? "<b>%</b>" : "%";
    } else if (_int < -26 - 10) {
      return withBolds ? "<b>&</b>" : "&";
    }
  }
  return intArr.map(intToHrChar).join("");
}

function crossReactPrograms(a, b) {
  a = toIntArr(a);
  b = toIntArr(b);
  let out = executeSelfModifyingBrainfuck(a.concat(b));
  let halfLen = Math.floor(out.length / 2);
  a = out.slice(0, halfLen);
  b = out.slice(halfLen);
  a = toStr(a);
  b = toStr(b);
  return [a, b];
}
