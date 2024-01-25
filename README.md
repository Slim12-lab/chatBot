# План тестирования программы чат-бота

## 1. Тестирование авторизации:
   - *Ожидаемый результат:* Пользователь успешно авторизуется при вводе корректного логина и пароля.
   - *Реальный результат:* Бот подтверждает успешную авторизацию, и пользователю предлагаются доступные действия.

## 2. Тестирование постановки задачи:
   - *Ожидаемый результат:* Пользователь успешно поставляет задачу, и бот подтверждает успешное добавление задачи в базу данных.
   - *Реальный результат:* Задача успешно добавлена, и бот отправляет уведомление исполнителю.

## 3. Тестирование просмотра списка задач:
   - *Ожидаемый результат:* Бот выводит список задач пользователя с подробной информацией.
   - *Реальный результат:* Бот выводит корректный список задач пользователя.

## 4. Тестирование ввода исполнителя:
   - *Ожидаемый результат:* Пользователь успешно вводит порядковый номер исполнителя, и бот подтверждает выбор.
   - *Реальный результат:* Бот корректно обрабатывает введенные данные и добавляет задачу в базу данных.

## 5. Тестирование работы с базой данных:
   - *Ожидаемый результат:* Данные успешно добавляются, извлекаются и обновляются в базе данных в соответствии с логикой программы.
   - *Реальный результат:* База данных корректно взаимодействует с программой.

## 6. Тестирование отмены операции:
   - *Ожидаемый результат:* Команда /cancel успешно прерывает текущий процесс и возвращает пользователя в начальное состояние.
   - *Реальный результат:* Процесс успешно прерывается, и пользователь возвращается в начальное состояние.

## 7. Тестирование отправки уведомлений:
   - *Ожидаемый результат:* Уведомление о новой задаче успешно отправляется исполнителю с корректной информацией.
   - *Реальный результат:* Исполнитель получает уведомление с правильной информацией о задаче.

## 8. Тестирование негативных сценариев:
   - *Ожидаемый результат:* Программа корректно обрабатывает ошибки и исключения, предоставляя информативные сообщения об ошибках.
   - *Реальный результат:* Программа отлавливает и обрабатывает ошибки, предоставляя адекватные сообщения.

## 9. Тестирование устойчивости к изменениям в коде:
   - *Ожидаемый результат:* После внесения изменений в код программы, она продолжает корректно работать.
   - *Реальный результат:* Изменения в коде не приводят к сбоям, и программа продолжает корректную работу.

## 10. Тестирование безопасности:
    - *Ожидаемый результат:* Программа устойчива к возможным атакам и вредоносному вводу.
    - *Реальный результат:* Программа корректно обрабатывает входные данные и предотвращает атаки.

## 11. Тестирование взаимодействия с ботом:
    - *Ожидаемый результат:* Бот правильно реагирует на ввод пользователя и отправляет корректные ответы.
    - *Реальный результат:* Бот взаимодействует с пользователем в режиме реального времени и отвечает на ввод пользователя.

## 12. Тестирование работы с различными типами сообщений:
    - *Ожидаемый результат:* Программа корректно обрабатывает различные типы сообщений, такие как текстовые, команды и другие.
    - *Реальный результат:* Программа корректно реагирует на различные типы сообщений и выполняет соответствующие действия.
