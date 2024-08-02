# CountdownTimer
# 倒计时

这个 Python 脚本实现了一个简单的倒计时器应用，使用 `tkinter` 库创建了一个图形用户界面（GUI）。用户可以设置倒计时的时长，开始倒计时，并控制倒计时的暂停、重启和继续。

### 功能

- **设置时长**: 通过弹出对话框输入时、分、秒。可以直接修改上次设置的时长。
- **开始按钮**: 开始倒计时，显示倒计时数字。每次点击 "开始" 后，计时器从零开始计算。
- **暂停按钮**: 暂停倒计时，点击后可以随时恢复倒计时。
- **重启按钮**: 重置倒计时到上次设置的时长并立即开始。
- **结束提示**: 倒计时结束后，显示提示消息，包含倒计时的最终时间。

### 使用说明

1. **运行程序**: 启动 Python 脚本，主窗口会显示初始倒计时 "00:00:00"。
2. **设置时长**: 点击 "时长" 按钮，输入所需的倒计时时间（时、分、秒）。设置完成后，倒计时窗口会显示更新后的时长。
3. **开始倒计时**: 点击 "开始" 按钮，倒计时开始并显示倒计时的剩余时间。
4. **暂停倒计时**: 点击 "暂停" 按钮，可以暂停倒计时。再次点击 "开始" 按钮时，计时会从暂停的状态继续。
5. **重启倒计时**: 点击 "重启" 按钮，将倒计时重置为上次设置的时间，并立即开始倒计时。
6. **倒计时结束**: 当倒计时结束时，显示提示消息，并包括倒计时的最终时间。

### 依赖

- `tkinter`: 用于创建图形用户界面。

### 安装

确保已安装 Python 和 `tkinter`，并运行脚本来启动倒计时器应用。
