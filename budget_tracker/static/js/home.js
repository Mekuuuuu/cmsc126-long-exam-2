document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('myChart');
    const container = canvas.parentElement;

    const chartData = {
        monthly: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            income: [12, 19, 3, 5, 2, 3],
            expense: [10, 15, 8, 4, 1, 2]
        },
        weekly: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            income: [100, 150, 80, 120],
            expense: [90, 120, 70, 110]
        },
        yearly: {
            labels: ['2020', '2021', '2022', '2023', '2024'],
            income: [1000, 1500, 1100, 1300, 1400],
            expense: [900, 1300, 950, 1200, 1250]
        }
    };

    let chart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: chartData.monthly.labels,
            datasets: [
                {
                    label: 'Income',
                    data: chartData.monthly.income,
                    backgroundColor: '#2BB32A'
                },
                {
                    label: 'Expense',
                    data: chartData.monthly.expense,
                    backgroundColor: '#E53935'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { stacked: false },
                y: { beginAtZero: true },
            }
        }
    });

    document.getElementById('timeFilter').addEventListener('change', function () {
        const selected = this.value;
        chart.data.labels = chartData[selected].labels;
        chart.data.datasets[0].data = chartData[selected].income;
        chart.data.datasets[1].data = chartData[selected].expense;
        chart.update();
    });

    const modal = document.getElementById("transactionModal");
    const categoryModal = document.getElementById("categoryModal");
    const datetimeInput = document.getElementById("datetimeInput");
    const typeRadios = document.querySelectorAll('input[name="type"]');
    const categorySelect = document.getElementById('categorySelect');

    document.getElementById("openModalBtn").onclick = () => {
        modal.style.display = "block";
        const now = new Date();
        const offset = now.getTimezoneOffset();
        const localDateTime = new Date(now.getTime() - offset * 60 * 1000).toISOString().slice(0, 16);
        datetimeInput.value = localDateTime;
        filterCategories('income');
    };

    function closeModal() {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target === modal) {
            closeModal();
        }
        if (event.target === categoryModal) {
            closeCategoryModal();
        }
    };

    document.getElementById("addCategoryForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(this);
        const newCategoryType = formData.get('type');

        fetch("/add_category/", {
            method: "POST",
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.category_id && data.category_name) {
                    const newOption = document.createElement('option');
                    newOption.value = data.category_id;
                    newOption.textContent = data.category_name;
                    newOption.dataset.type = newCategoryType;
                    newOption.selected = true;

                    categorySelect.appendChild(newOption);

                    const radioToSelect = document.querySelector(`input[name="type"][value="${newCategoryType}"]`);
                    if (radioToSelect) {
                        radioToSelect.checked = true;
                        filterCategories(newCategoryType);
                    }

                    closeCategoryModal();
                } else {
                    alert('Error creating category');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error creating the category');
            });
    });

    document.getElementById("addCategoryBtn").onclick = () => {
        categoryModal.style.display = "block";
    };

    function closeCategoryModal() {
        categoryModal.style.display = "none";
    }

    function filterCategories(selectedType) {
        let foundValidOption = false;

        Array.from(categorySelect.options).forEach(option => {
            if (option.dataset.type === selectedType) {
                option.style.display = 'block';
                if (!foundValidOption) {
                    foundValidOption = true;
                }
            } else {
                option.style.display = 'none';
            }
        });

        const selectedOption = categorySelect.options[categorySelect.selectedIndex];
        if (!selectedOption || selectedOption.style.display === 'none') {
            categorySelect.selectedIndex = -1;
        }
    }

    typeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            filterCategories(radio.value);
        });
    });

    document.querySelector('.profile-btn')?.addEventListener('click', function () {
        const dropdown = document.querySelector('.dropdown-menu');
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });

    window.addEventListener('click', function (e) {
        const profileBtn = document.querySelector('.profile-btn');
        const dropdown = document.querySelector('.dropdown-menu');
        if (profileBtn && dropdown && !profileBtn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
});
