from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import os

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def index():
    return 'Сервер подключен через Supabase REST API!'


@app.route('/get_users', methods=['GET'])
def get_users():
    response = requests.get(f"{SUPABASE_URL}/rest/v1/users", headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'success': False, 'error': response.text}), 500


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    username = request.args.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Не указан логин'}), 400

    response = requests.delete(
        f"{SUPABASE_URL}/rest/v1/users",
        headers=HEADERS,
        params={"username": f"eq.{username}"}
    )
    if response.status_code in [200, 204]:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': response.text}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    params = {
        "username": f"eq.{username}",
        "password": f"eq.{password}"
    }
    response = requests.get(f"{SUPABASE_URL}/rest/v1/users", headers=HEADERS, params=params)

    if response.status_code == 200:
        users = response.json()
        if users:
            user = users[0]
            return jsonify({
                'success': True,
                'user_id': user['id'],
                'isAdmin': user['is_admin'],
                'fullName': user['full_name'],
                'groupName': user['group_name']
            })
        else:
            return jsonify({'success': False, 'message': 'Неверный логин или пароль'}), 401
    else:
        return jsonify({'success': False, 'message': 'Ошибка соединения с базой'}), 500


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('isAdmin', False)
    full_name = data.get('full_name', 'Не указано')
    group_name = data.get('group_name', 'Не указано')

    user_data = {
        "username": username,
        "password": password,
        "full_name": full_name,
        "group_name": group_name,
        "is_admin": is_admin
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/users",
        headers=HEADERS,
        json=user_data
    )

    if response.status_code in [200, 201]:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': response.text}), 400


@app.route('/questions', methods=['GET'])
def get_questions():
    test_id = request.args.get('test_id')
    if not test_id:
        return jsonify({'success': False, 'message': 'test_id не указан'}), 400

    questions_response = requests.get(
        f"{SUPABASE_URL}/rest/v1/questions",
        headers=HEADERS,
        params={"test_id": f"eq.{test_id}"}
    )

    if questions_response.status_code != 200:
        return jsonify({'success': False, 'message': 'Ошибка получения вопросов'}), 500

    questions = questions_response.json()
    result = []

    for q in questions:
        question_id = q['id']
        answers_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/answers",
            headers=HEADERS,
            params={"question_id": f"eq.{question_id}"}
        )

        if answers_response.status_code != 200:
            return jsonify({'success': False, 'message': 'Ошибка получения ответов'}), 500

        answers = answers_response.json()
        result.append({
            'id': q['id'],
            'question': q['question_text'],
            'correct_answer': q['correct_answer'],
            'answers': [a['answer_text'] for a in answers]
        })

    return jsonify({'success': True, 'questions': result})


@app.route('/save_result', methods=['POST'])
def save_result():
    data = request.json
    user_id = data.get('user_id')
    test_id = int(data.get('test_id'))
    grade = int(data.get('grade'))
    total_questions = int(data.get('total_questions', 7))
    correct_answers = int(data.get('correct_answers', grade if grade <= 5 else 0))
    passed = grade >= 3
    passed_at = datetime.utcnow().isoformat()

    if not user_id or not test_id or not grade:
        return jsonify({'success': False, 'message': 'Некорректные данные для сохранения.'}), 400

    result_data = {
        "user_id": user_id,
        "test_id": test_id,
        "score": grade,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "passed": passed,
        "passed_at": passed_at
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/results",
        headers=HEADERS,
        json=result_data
    )

    if response.status_code in [200, 201]:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': response.text}), 400


@app.route('/get_results', methods=['GET'])
def get_results():
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/results?select=*,users(username,full_name)",
        headers=HEADERS
    )
    if response.status_code == 200:
        results = response.json()
        return jsonify({'success': True, 'results': results})
    else:
        return jsonify({'success': False, 'error': response.text}), 500


@app.route('/update_user', methods=['PATCH'])
def update_user():
    data = request.json
    username = data.get('username')
    field = data.get('field')
    value = data.get('value')

    if not username or not field:
        return jsonify({'success': False, 'message': 'Некорректные данные'}), 400

    response = requests.patch(
        f"{SUPABASE_URL}/rest/v1/users",
        headers=HEADERS,
        params={"username": f"eq.{username}"},
        json={field: value}
    )

    if response.status_code in [200, 204]:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': response.text}), 400