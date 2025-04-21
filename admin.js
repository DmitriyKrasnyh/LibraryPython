document.addEventListener('DOMContentLoaded', function() {
    loadUsers(); // Загружаем пользователей при загрузке страницы
    document.getElementById('userForm').onsubmit = function(event) {
        event.preventDefault(); // Предотвращаем обновление страницы
        addUser();
    };
});

function loadUsers() {
    var users = JSON.parse(localStorage.getItem('users') || '[]'); // Получаем пользователей или пустой массив
    users.forEach(function(user) {
        addUserToTable(user.username, user.password, user.isAdmin);
    });
}

function addUser() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var isAdmin = document.getElementById('isAdmin').checked; // Получаем состояние чекбокса

    if (username && password) {
        addUserToTable(username, password, isAdmin);
        saveUser({ username: username, password: password, isAdmin: isAdmin });
        document.getElementById('username').value = ''; // Очистка поля ввода
        document.getElementById('password').value = ''; // Очистка поля ввода
        document.getElementById('isAdmin').checked = false; // Сброс чекбокса
    } else {
        alert('Пожалуйста, заполните все поля.');
    }
}

function saveUser(user) {
    var users = JSON.parse(localStorage.getItem('users') || '[]');
    users.push(user);
    localStorage.setItem('users', JSON.stringify(users));
}

function addUserToTable(username, password, isAdmin) {
    var table = document.getElementById('usersTable').getElementsByTagName('tbody')[0];
    var newRow = table.insertRow();
    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1);
    var cell3 = newRow.insertCell(2);
    var cell4 = newRow.insertCell(3);

    cell1.textContent = username;
    cell2.textContent = password;
    cell3.textContent = isAdmin ? 'Да' : 'Нет'; // Показывать статус администратора
    cell4.innerHTML = '<button onclick="removeUser(this)">Удалить</button>';
}

function removeUser(btn) {
    var row = btn.parentNode.parentNode;
    var index = Array.prototype.indexOf.call(row.parentNode.children, row); // Получаем индекс удаляемой строки
    var users = JSON.parse(localStorage.getItem('users'));
    users.splice(index, 1);
    localStorage.setItem('users', JSON.stringify(users));
    row.parentNode.removeChild(row);
}
