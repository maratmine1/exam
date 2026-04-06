async function loadCars() {
    const btn = document.getElementById('loadCarsBtn');
    const tbody = document.querySelector('#carsTable tbody');
    const errorBlock = document.getElementById('carsError');

    btn.disabled = true;
    errorBlock.textContent = '';
    tbody.innerHTML = '';

    try {
        const response = await fetch('/cars');
        if (!response.ok) {
            throw new Error('Ошибка загрузки списка автомобилей');
        }
        const data = await response.json();
        data.forEach((car) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${car.id}</td>
                <td>${car.model}</td>
                <td>${car.number}</td>
                <td>${car.is_reserved ? 'Да' : 'Нет'}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        errorBlock.textContent = e.message;
    } finally {
        btn.disabled = false;
    }
}

async function submitCarInfoForm(event) {
    event.preventDefault();

    const form = document.getElementById('carInfoForm');
    const resultBlock = document.getElementById('carInfoResult');
    const errorBlock = document.getElementById('carInfoError');

    resultBlock.textContent = '';
    errorBlock.textContent = '';

    const phone = form.phone.value.trim();
    const smsCode = form.smsCode.value.trim();

    if (!phone || !smsCode) {
        errorBlock.textContent = 'Введите телефон и СМС код.';
        return;
    }

    try {
        const response = await fetch('/car-info', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({phone, sms_code: smsCode})
        });

        if (response.status === 401) {
            const data = await response.json();
            throw new Error(data.detail || 'Неверная пара телефон + СМС код');
        }

        if (!response.ok) {
            throw new Error('Ошибка запроса к серверу');
        }

        const car = await response.json();
        resultBlock.innerHTML = `
            <div><strong>Модель автомобиля:</strong> ${car.car_model}</div>
            <div><strong>Номер автомобиля:</strong> ${car.car_number}</div>
            <div><strong>Уровень топлива:</strong> ${car.fuel_level}</div>
        `;
    } catch (e) {
        errorBlock.textContent = e.message;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document
        .getElementById('loadCarsBtn')
        .addEventListener('click', loadCars);

    document
        .getElementById('carInfoForm')
        .addEventListener('submit', submitCarInfoForm);
});

