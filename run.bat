::@为隐藏
@echo off

cd /d "%~dp0deepseek"

::%0：代表当前批处理文件本身（如 script.bat）。
::%~dp0：
::d（drive）：提取驱动器（如 C:）。
::p（path）：提取完整路径（如 \Users\Name\Desktop\）。
::0：指代当前脚本。
::最终效果：返回当前批处理文件所在的绝对路径（末尾带反斜杠 \）。

call .venv\Scripts\activate.bat

streamlit run deepseek\streamlit_learn.py

:: 暂停窗口，防止自动关闭
pause
