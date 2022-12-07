from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt
app = QApplication([])

# 创建窗口
window = QWidget()
window.setWindowTitle('扫雷')
window.setGeometry(100, 100, 400, 400)

# 创建按钮
buttons = []
for i in range(10):
  row = []
  for j in range(10):
    button = QPushButton('', window)
    button.setGeometry(i * 40, j * 40, 40, 40)
    row.append(button)
  buttons.append(row)

# 打开格子
def uncover(row, col):
  button = buttons[row][col]
  button.setEnabled(False)
  mineCount = countMines(row,col)
  # 将雷数显示在按钮上
  button.setText(str(mineCount))

# 处理按钮点击事件
def handleButtonClick(row, col):
  button = buttons[row][col]

  # 检查是否为地雷
  if isMine(row, col):
    endGame('lose')
    return
  else:
  # 打开格子
    uncover(row, col)
      # 如果周围没雷，则继续自动点周围的区域
    if countMines(row,col)== 0:
      for i in range(row-1, row+2):
        for j in range(col-1, col+2):
          if i >= 0 and i < 10 and j >= 0 and j < 10 and buttons[i][j].isEnabled():
            handleButtonClick(i, j)
    if checkVictory():
      endGame('win')
  # 为每个按钮连接点击事件处理器


def handleButtonRightClick(row, col):
  button = buttons[row][col]

  # 如果按钮已经被打开，则不做任何处理
  if not button.isEnabled():
    return

  # 如果按钮已经被标记，则取消标记
  if button.text() == 'F':
    button.setText('')
  # 否则标记为“排雷”
  else:
    button.setText('F')




for i in range(10):
  for j in range(10):
    button = buttons[i][j]
    button.clicked.connect(lambda _, row=i, col=j: handleButtonClick(row, col))
    button.setContextMenuPolicy(Qt.CustomContextMenu)
    button.customContextMenuRequested.connect(lambda pos, row=i, col=j: handleButtonRightClick(row, col))

# 设置随机雷区
import random

mines = [] # 存储地雷的位置

# 随机选择10个格子作为地雷
for i in range(10):
  row = random.randint(0, 9)
  col = random.randint(0, 9)
  mines.append((row, col))

# 检查是否为地雷
def isMine(row, col):
  return (row, col) in mines

# 计算周围雷数
def countMines(row, col):
  count = 0
  for i in range(row-1, row+2):
    for j in range(col-1, col+2):
      if i >= 0 and i < 10 and j >= 0 and j < 10 and isMine(i, j):
        count += 1
  return count


  

# 检查游戏是否已经胜利
def checkVictory():
  for i in range(10):
    for j in range(10):
      button = buttons[i][j]
      if button.isEnabled() and not isMine(i, j):
        return False
  return True
# 结束游戏
def endGame(result):
  # 禁用所有按钮
  for row in buttons:
    for button in row:
      button.setEnabled(False)

  # 显示结果
  if result == 'win':
    print('恭喜你，你赢了！')
  else:
    print('很抱歉，你输了。')

window.show()
app.exec_()