// script.js
document.addEventListener("scroll", function() {
    const logoBar = document.querySelector('.logo-bar');
    if (window.scrollY > 50) {
        logoBar.classList.add('scrolled');
    } else {
        logoBar.classList.remove('scrolled');
    }
});
document.addEventListener("DOMContentLoaded", function () {
    // قائمة الأصوات المتاحة
    const sounds = [
        new Audio('/static/sound1.mp3'),
        new Audio('/static/sound2.mp3'),
        new Audio('/static/sound3.mp3'),
        new Audio('/static/sound4.mp3'),
        new Audio('/static/sound5.mp3')
    ];

    // دالة لتشغيل صوت عشوائي مع احتمال 50%
    function playRandomSound() {
        // 50% احتمال لتشغيل الصوت
        if (Math.random() > 0.5) {
            // اختيار صوت عشوائي من القائمة
            const randomIndex = Math.floor(Math.random() * sounds.length);
            const selectedSound = sounds[randomIndex];
            selectedSound.play();
        }
    }

    // الحصول على جميع الخيارات من نوع radio
    const radioButtons = document.querySelectorAll('input[type="radio"]');

    // إضافة حدث change على كل خيار
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            playRandomSound(); // تشغيل صوت عشوائي عند تغيير الاختيار
        });
    });

    // التعامل مع زر التبديل بين الوضع الداكن والفاتح
    const toggleButton = document.getElementById('toggleButton');
    const funnyForm = document.getElementById('funnyForm');
    const resultMessage = document.getElementById('resultMessage');
    const resultContainer = document.querySelector('.result-container');
    const restartButton = document.getElementById('restartButton');

    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            document.body.classList.toggle('dark-mode');
            document.querySelector('.container').classList.toggle('dark-mode');
            document.querySelector('.logo-bar').classList.toggle('dark-mode');
        });
    }

    if (funnyForm) {
        funnyForm.addEventListener('submit', function (event) {
            event.preventDefault();
            
            const formData = {
                age: parseInt(document.getElementById('age').value),
                gender: document.querySelector('input[name="gender"]:checked')?.value,
                profession: document.getElementById('profession')?.value,
                marital_status: document.getElementById('marital_status')?.value,
                satisfied_life: document.querySelector('input[name="satisfied_life"]:checked')?.value,
                dropped_activities: document.querySelector('input[name="dropped_activities"]:checked')?.value,
                feel_life_empty: document.querySelector('input[name="feel_life_empty"]:checked')?.value,
                bored: document.querySelector('input[name="bored"]:checked')?.value,
                feel_helpless: document.querySelector('input[name="feel_helpless"]:checked')?.value,
                afraid_bad_happening: document.querySelector('input[name="afraid_bad_happening"]:checked')?.value,
                hopeful_about_future: document.querySelector('input[name="hopeful_about_future"]:checked')?.value,
                spend_time_happily: document.querySelector('input[name="spend_time_happily"]:checked')?.value,
                feel_energy: document.querySelector('input[name="feel_energy"]:checked')?.value,
                prefer_stay_home: document.querySelector('input[name="prefer_stay_home"]:checked')?.value,
                avoiding_social_gatherings: document.getElementById('avoiding_social_gatherings')?.value,
                memory_loss: document.querySelector('input[name="memory_loss"]:checked')?.value,
                consider_worthless: document.querySelector('input[name="consider_worthless"]:checked')?.value,
                cry_most_of_the_time: document.querySelector('input[name="cry_most_of_the_time"]:checked')?.value,
                sleep_well: document.getElementById('sleep_well')?.value,
                feeling_reduce_appetite: document.querySelector('input[name="feeling_reduce_appetite"]:checked')?.value,
                situation_hopeless: document.querySelector('input[name="situation_hopeless"]:checked')?.value,
                people_better_than_you: document.querySelector('input[name="people_better_than_you"]:checked')?.value,
                feel_bad_and_guilty: document.getElementById('feel_bad_and_guilty')?.value,
                others_would_better_you_died: document.querySelector('input[name="others_would_better_you_died"]:checked')?.value
            };

            // تحقق من جميع الحقول المطلوبة
            const missingFields = [];
            for (const [key, value] of Object.entries(formData)) {
                if (!value) {
                    missingFields.push(key);
                }
            }

            if (missingFields.length > 0) {
                if (resultMessage) {
                    resultMessage.innerText = `الرجاء ملء الحقول التالية: ${missingFields.join(', ')}`;
                    resultMessage.style.display = 'block';
                }
                return;
            }

            // إظهار مؤشر التحميل
            if (resultMessage) {
                resultMessage.innerHTML = `<div class="spinner"></div><p>جاري معالجة البيانات...</p>`;
                resultMessage.style.display = 'block';
            }

            // إرسال البيانات إلى الخادم
            fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {throw new Error(err.error || 'Network response was not ok');});
                }
                return response.json();
            })
            .then(result => {
                if (result.depression_percentage !== undefined) {
                    // تحويل المستخدم إلى صفحة النتيجة مع النسبة المئوية
                    const depressionPercentage = result.depression_percentage.toFixed(2);
                    window.location.href = `/result/${depressionPercentage}`;
                } else if (result.error) {
                    if (resultMessage) {
                        resultMessage.innerText = `خطأ: ${result.error}`;
                        resultMessage.style.display = 'block';
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (resultMessage) {
                    resultMessage.innerText = 'حدث خطأ أثناء معالجة النتيجة. الرجاء المحاولة مرة أخرى.';
                    resultMessage.style.display = 'block';
                }
            });
        });
    }

    if (restartButton) {
        restartButton.addEventListener('click', function() {
            if (funnyForm) {
                funnyForm.reset();
                funnyForm.style.display = 'block';
            }
            if (resultContainer) {
                resultContainer.style.display = 'none';
            }
            if (resultMessage) {
                resultMessage.style.display = 'none';
            }
        });
    }
        // كود الدردشة
        const chatInput = document.getElementById('user_input');
        const chatResponseContainer = document.getElementById('chat_response');
        const sendButton = document.getElementById('send_button');
    
        if (sendButton) {
            sendButton.addEventListener('click', function() {
                const userInput = chatInput.value;
    
                // إرسال الطلب إلى الخادم
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ user_input: userInput })
                })
                .then(response => response.json())
                .then(data => {
                    chatResponseContainer.innerHTML += '<p><strong>أنت:</strong> ' + userInput + '</p>';
                    chatResponseContainer.innerHTML += '<p><strong>الذكاء الاصطناعي:</strong> ' + data.response + '</p>';
                    chatInput.value = '';  // مسح حقل الإدخال
                })
                .catch(error => console.error('Error:', error));
            });
        }
    
});
