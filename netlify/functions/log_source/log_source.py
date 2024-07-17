from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/log_source', methods=['POST'])
def log_source():
    try:
        token = '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'

        data = request.get_json()
        source = data.get('client_payload', {}).get('source')

        if not source:
            return jsonify({'error': 'Source parameter not found'}), 400

        github_url = 'https://api.github.com/repos/<username>/<repository>/dispatches'

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
        }

        payload = {
            'event_type': 'log_source',
            'client_payload': {'source': source}
        }

        response = requests.post(github_url, headers=headers, json=payload)
        response.raise_for_status()

        return jsonify({'message': 'Logging triggered successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
