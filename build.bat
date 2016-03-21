rmdir /s /q build
rmdir /s /q dist
pyinstaller --hidden-import cssselect ffcrawler.py
copy ffc_* dist\ffcrawler
