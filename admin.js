document.addEventListener('DOMContentLoaded', function () {
    loadUsers();
    loadResults();
    document.getElementById('userForm').onsubmit = function (event) {
        event.preventDefault();
        addUser();
    };
});

function loadUsers() {
    fetch('http://localhost:5000/get_users')
        .then(response => response.json())
        .then(users => {
            if (Array.isArray(users)) {
                const tableBody = document.querySelector('#usersTable tbody');
                tableBody.innerHTML = '';
                users.forEach(user => addUserToTable(user));
            } else {
                alert('Ошибка загрузки пользователей: некорректный формат данных.');
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке пользователей:', error);
            alert('Ошибка загрузки пользователей.');
        });
}

function addUser() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const isAdmin = document.getElementById('isAdmin').checked;

    if (!username || !password) {
        alert('Пожалуйста, заполните все поля.');
        return;
    }

    fetch('http://localhost:5000/add_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, isAdmin })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ Пользователь успешно добавлен!');
                loadUsers();
                document.getElementById('userForm').reset();
            } else {
                alert('❌ Ошибка при добавлении пользователя.');
            }
        })
        .catch(error => {
            console.error('Ошибка добавления пользователя:', error);
            alert('❌ Не удалось добавить пользователя.');
        });
}

function addUserToTable(user) {
    const table = document.getElementById('usersTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();
    newRow.setAttribute('data-username', user.username);

    newRow.insertCell(0).textContent = user.id || '—';
    newRow.insertCell(1).textContent = user.username || '—';
    newRow.insertCell(2).textContent = user.password || '—';

    // ФИО — сделаем редактируемым
    const fullNameCell = newRow.insertCell(3);
    fullNameCell.innerHTML = `<input type="text" value="${user.full_name || ''}" onchange="updateUserField('${user.username}', 'full_name', this.value)">`;

    // Номер группы — тоже редактируемый
    const groupCell = newRow.insertCell(4);
    groupCell.innerHTML = `<input type="text" value="${user.group_name || ''}" onchange="updateUserField('${user.username}', 'group_name', this.value)">`;

    newRow.insertCell(5).textContent = user.is_admin ? 'Да' : 'Нет';
    newRow.insertCell(6).textContent = user.created_at ? new Date(user.created_at).toLocaleString() : '—';

    const actionsCell = newRow.insertCell(7);
    actionsCell.innerHTML = `
        <button onclick="removeUser('${user.username}')" style="background-color: #f44336; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">
            Удалить
        </button>
    `;
}

function removeUser(username) {
    if (!confirm(`Вы уверены, что хотите удалить пользователя "${username}"?`)) {
        return;
    }

    fetch(`http://localhost:5000/delete_user?username=${encodeURIComponent(username)}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ Пользователь удален!');
                const row = document.querySelector(`#usersTable tbody tr[data-username="${username}"]`);
                if (row) {
                    row.remove();
                }
            } else {
                alert('❌ Ошибка при удалении пользователя.');
            }
        })
        .catch(error => {
            console.error('Ошибка при удалении пользователя:', error);
            alert('❌ Не удалось удалить пользователя.');
        });
}

function updateUserField(username, field, newValue) {
    fetch('http://localhost:5000/update_user', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            field: field,
            value: newValue
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ Поле обновлено.');
            } else {
                alert('❌ Ошибка при обновлении поля.');
            }
        })
        .catch(error => {
            console.error('Ошибка при обновлении поля:', error);
            alert('❌ Не удалось обновить поле.');
        });
}

function loadResults() {
    fetch('http://localhost:5000/get_results')
        .then(response => response.json())
        .then(data => {
            if (data.success && Array.isArray(data.results)) {
                const tableBody = document.querySelector('#resultsTable tbody');
                tableBody.innerHTML = '';
                data.results.forEach(result => {
                    const row = tableBody.insertRow();
                    const fullName = result.users?.full_name || result.users?.username || 'Неизвестно';

                    row.insertCell(0).textContent = fullName;
                    row.insertCell(1).textContent = result.test_id;
                    row.insertCell(2).textContent = result.score;
                    row.insertCell(3).textContent = new Date(result.passed_at).toLocaleString();
                });
            } else {
                alert('Ошибка загрузки результатов.');
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке результатов:', error);
            alert('Ошибка при получении результатов тестирования.');
        });
}
