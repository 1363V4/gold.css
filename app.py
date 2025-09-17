from pathlib import Path
from sanic import Sanic


static_dir = Path().cwd() / 'static'
html_files = list(static_dir.glob("*.html"))

app = Sanic("gold")

app.static('/static/', './static/')
app.static('/', './static/index.html', name="index")

for html_file in html_files:
    app.static(f'/{html_file.name}', html_file, name=html_file.name)

if __name__ == "__main__":
    app.run(auto_reload=True)
