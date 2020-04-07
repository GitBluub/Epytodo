from app import app_factory, app
from app import views

def main():
    epytodo = app_factory()
    epytodo.run(debug=True)
'''
if __name__ == "__main__":
    main()
'''

app.run(debug=True)