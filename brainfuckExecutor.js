class BrainfuckExecutor {
	initState(startingTape) {
		if (startingTape !== null) {
			if (Array.isArray(startingTape)) {
				startingTape = toStr(startingTape);
			}
			this.program1 = startingTape;
		} else {
			this.program1 = randomProgram();
		}
		this.state = {
			tape: toIntArr(this.program1),
			pointer: 0,
			head0: 0,
			head1: 0,
			loopStack: [],
			numReads: 0,
			maxReads: 2 ** 13
		};
		this.running = false;
		this.runInterval = null;
		console.log(this.program1);
	}

	initContent(layout) {
		this.textLayout = document.createElement('div');
		this.textLayout.style.position = 'relative';
		this.textLayout.style.marginTop = '100px';
		this.paransLabel = this.addLabel(" ".repeat(64), 0);
		this.pointerLabel = this.addLabel("v" + " ".repeat(63), 50);
		let bfText = toHumanReadableStr(this.program1, false);
		this.bfLabel = this.addLabel(bfText, 100);
		this.hLabel = this.addLabel("^" + " ".repeat(63), 150);

		layout.appendChild(this.textLayout);
	}

	updateState() {
		this.state = this.updateStateHelper(this.state);
		this.updateContent();
	}

	updateStateHelper({ tape, pointer, head0, head1, loopStack, numReads, maxReads }) {
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
					while (loopLevel > 0 && pointer < tape.length - 1 && numReads < maxReads) {
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
						pointer = -1;
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
		pointer = (pointer + 1) % tape.length;
		return { tape, pointer, head0, head1, loopStack, numReads, maxReads };
	}

	updateContent() {
		this.program1 = this.state.tape;
		this.bfLabel.innerText = toHumanReadableStr(this.program1, false);
		let pointer = this.state.pointer;
		if (pointer >= this.program1.length) {
			this.running = false;
			clearInterval(this.runInterval);
		}
		let numReads = this.state.numReads;
		console.log(numReads, pointer, this.program1);
		let h0 = this.state.head0;
		let h1 = this.state.head1;
		this.pointerLabel.innerText = "-".repeat(pointer) + "v" + "-".repeat(63 - pointer);

		const addressConvert = (i) => {
			if (i === h0 && i === h1) {
				return "^";
			} else if (i === h0) {
				return "0";
			} else if (i === h1) {
				return "1";
			} else {
				return "-";
			}
		};
		this.hLabel.innerText = Array.from({ length: 64 }, (_, i) => addressConvert(i)).join('');
		let loopStack = this.state.loopStack;
		this.paransLabel.innerText = Array.from({ length: 64 }, (_, i) => loopStack.includes(i) ? "[" : "-").join('');
	}

	addLabel(text, yDown) {
		let label = document.createElement('div');
		label.innerText = text;
		label.style.position = 'absolute';
		label.style.top = `${yDown}px`;
		label.style.fontFamily = 'Courier Prime, monospace';
		this.textLayout.appendChild(label);
		return label;
	}
	
	toggleRun() {
		if (this.running) {
			this.running = false;
			clearInterval(this.runInterval);
		} else {
			this.running = true;
			this.runInterval = setInterval(() => {
				this.updateState();
				this.updateContent();
			}, 100); // Adjust the interval as needed
		}
	}
};

// Example usage:
const contentController = new BrainfuckExecutor();
const initialState = [4, 9, 5, 1, 0, 3, 3, 1, 8, 1, 2, 8, 1, 6, 0, 4, 8, 4, 6, 9, 7, 6, 6, 8, 2, 10, 7, 10, 6, 6, 4, 10, 6, 3, 6, 9, 9, 10, 8, 3, 2, 6, 7, 6, 8, 8, 4, 1, 8, 6, 4, 0, 3, 3, 2, 4, 4, 0, 0, 6, 7, 7, 10, 7];
contentController.initState(initialState);
contentController.initContent(document.getElementById('app'));
document.getElementById('stepButton').addEventListener('click', () => {
		contentController.updateState();
		contentController.updateContent();
	});
	document.getElementById('runButton').addEventListener('click', () => {
		contentController.toggleRun();
	});
