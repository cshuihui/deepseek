::@Ϊ����
@echo off

cd /d "%~dp0..\"
:: ..\��ʾ��һ��
::%0������ǰ�������ļ������� script.bat����
::d��drive������ȡ���������� C:����
::p��path������ȡ����·������ \Users\Name\Desktop\����
::0��ָ����ǰ�ű���
::����Ч�������ص�ǰ�������ļ����ڵľ���·����ĩβ����б�� \����

call .venv\Scripts\activate.bat

streamlit run deepseek\streamlit_learn.py

:: ��ͣ���ڣ���ֹ�Զ��ر�
pause
