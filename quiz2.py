import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
                             QSizePolicy, QToolButton, QWidget)


class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calculator(QWidget):
    NumDigitButtons = 10

    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)

        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''

        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)

        self.digitButtons = []

        for i in range(Calculator.NumDigitButtons): ## 숫자 버튼
            self.digitButtons.append(self.createButton(str(i),
                                                       self.digitClicked))

        self.pointButton = self.createButton(".", self.pointClicked)
        self.changeSignButton = self.createButton(u"\N{PLUS-MINUS SIGN}",
                                                  self.changeSignClicked)

        self.backspaceButton = self.createButton("BS",
                                                 self.backspaceClicked)
        self.clearButton = self.createButton("Clear", self.clearAll)
        #self.clearAllButton = self.createButton("Clear All", self.clearAll)

        self.divisionButton = self.createButton(u"\N{DIVISION SIGN}",
                                                self.multiplicativeOperatorClicked)
        self.timesButton = self.createButton(u"\N{MULTIPLICATION SIGN}",
                                             self.multiplicativeOperatorClicked)
        self.minusButton = self.createButton("-", self.additiveOperatorClicked)
        self.plusButton = self.createButton("+", self.additiveOperatorClicked)

        self.equalButton = self.createButton("=", self.equalClicked)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addWidget(self.display, 0, 0, 1, 4)

        mainLayout.addWidget(self.backspaceButton, 1, 0)
        mainLayout.addWidget(self.clearButton, 1, 1)
        mainLayout.addWidget(self.equalButton, 1, 2,1,2)

        for i in range(1, Calculator.NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3)
            mainLayout.addWidget(self.digitButtons[i], row, column)

        mainLayout.addWidget(self.plusButton, 2, 3)
        mainLayout.addWidget(self.divisionButton,5, 3)
        mainLayout.addWidget(self.timesButton, 4, 3)
        mainLayout.addWidget(self.minusButton, 3, 3)

        mainLayout.addWidget(self.digitButtons[0], 5, 0,1,2)
        mainLayout.addWidget(self.pointButton, 5, 2)

        self.setLayout(mainLayout)

        self.setWindowTitle("Calculator")

    def digitClicked(self):
        clickedButton = self.sender()  ## 이벤트 발생 버튼 정보
        digitValue = int(clickedButton.text())  ## 숫자

        if self.display.text() == '0' and digitValue == 0.0:  ## 0이면 return
            return

        if self.waitingForOperand:  ##  ex, 연산이 끝난후 숫자를 누르면 화면 clear 이후 숫자 입력시 값을 연결
            self.display.clear()
            self.waitingForOperand = False

        self.display.setText(self.display.text() + str(digitValue))

    def unaryOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if clickedOperator == "Sqrt":  ## 제곱급 함수(루트)
            if operand < 0.0:  ## 음수 일때
                self.abortOperation()  ## '####' 화면 표시
                return

            result = math.sqrt(operand)
        elif clickedOperator == u"x\N{SUPERSCRIPT TWO}":  ## 2의 제곱
            result = math.pow(operand, 2.0)
        elif clickedOperator == "1/x":  ## 분수
            if operand == 0.0:  ## 0으로 나눌때
                self.abortOperation()
                return

            result = 1.0 / operand

        self.display.setText(str(result))
        self.waitingForOperand = True  ## 연산이 끝나고 operand true

    def additiveOperatorClicked(self):  ## + -
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:  ## 이전 *, / operator 값이 있는 경우 앞에 연산을 계산 후 현재 누른 operator 값 저장
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(str(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''

        if self.pendingAdditiveOperator:  ## 이전 +, - operator 값이 있는 경우 앞에 연산을 계산 후 현재 누른 operator 값 저장
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.display.setText(str(self.sumSoFar))
        else:
            self.sumSoFar = operand

        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True

    def multiplicativeOperatorClicked(self):  ## * /
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:  ## 이전 *, / operator 값이 있는 경우 앞에 연산을 계산 후 현재 누른 operator 값 저장
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand

        ## ?? pendingMultiplicativeOperator가 없는 이유??

        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True

    def equalClicked(self):  ## = 연산 수행
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator: ## 이전 *, / operator 값이 있는 경우 앞에 연산을 계산 후 현재 누른 operator 값 저장
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''

        if self.pendingAdditiveOperator: ## 이전 +, - operator 값이 있는 경우 앞에 연산을 계산 후 현재 누른 operator 값 저장
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand

        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True ## 숫자 저장 true

    def pointClicked(self): ## 소수점
        if self.waitingForOperand:
            self.display.setText('0')

        if "." not in self.display.text():
            self.display.setText(self.display.text() + ".")

        self.waitingForOperand = False

    def changeSignClicked(self):
        text = self.display.text()
        value = float(text)

        if value > 0.0:
            text = "-" + text
        elif value < 0.0:
            text = text[1:]

        self.display.setText(text)

    def backspaceClicked(self):
        if self.waitingForOperand:
            return

        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.waitingForOperand = True

        self.display.setText(text)

    def clear(self):
        if self.waitingForOperand:
            return

        self.display.setText('0')
        self.waitingForOperand = True

    def clearAll(self):
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.display.setText('0')
        self.waitingForOperand = True

    def clearMemory(self):
        self.sumInMemory = 0.0

    def readMemory(self):
        self.display.setText(str(self.sumInMemory))
        self.waitingForOperand = True

    def setMemory(self):
        self.equalClicked()
        self.sumInMemory = float(self.display.text())

    def addToMemory(self):
        self.equalClicked()
        self.sumInMemory += float(self.display.text())

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button

    def abortOperation(self):
        self.clearAll()
        self.display.setText("####")

    def calculate(self, rightOperand, pendingOperator):
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == u"\N{MULTIPLICATION SIGN}":
            self.factorSoFar *= rightOperand
        elif pendingOperator == u"\N{DIVISION SIGN}":
            if rightOperand == 0.0:
                return False

            self.factorSoFar /= rightOperand

        return True


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())



