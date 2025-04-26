from app import create_app
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
