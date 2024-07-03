from app import create_app
import configparser

# Load the configuration
config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=config.getint('settings', 'PORT'))
