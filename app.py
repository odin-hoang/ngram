from flask import Flask, request, jsonify
from autocomplete import AutoComplete
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
ac = AutoComplete()
@app.route('/api/suggest', methods=['POST'])
def suggest():
    try:
        keywords = request.form['keywords']
        if keywords == '':
            return jsonify([]), 200
        keywords = keywords.split()
        print('keywords: %s' % keywords)
        last_word = keywords[-1]
        if last_word:
            last_word = last_word
        else:
            last_word = None
        print('last word: %s' % last_word)
        suggestion = ac.get_suggestions(keywords, ac.n_grams, ac.vocabulary, start_with=last_word)
        suggestion2 = ac.get_suggestions(keywords, ac.n_grams, ac.vocabulary)
        print(suggestion)
        return jsonify(suggestion2 + suggestion ), 200
    except Exception as e:
        print(e)
        return jsonify({'error': e}), 500

if __name__ == '__main__':
    app.run(debug=True)