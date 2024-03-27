from flask import Flask, render_template, request
import helper
from repository import GitHubRepository

app = Flask(__name__)

'''REST API with Python Flask'''
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        repositories = []
        for i in range(1, 6):  # Loop through up to 5 pairs of inputs
            username = request.form.get(f'username{i}')
            repository = request.form.get(f'repository{i}')
            if username and repository:
                repositories.append(GitHubRepository(username, repository))
        
        statistics = helper.get_statistics(repositories)
        return render_template('statistics.html', statistics=statistics)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
