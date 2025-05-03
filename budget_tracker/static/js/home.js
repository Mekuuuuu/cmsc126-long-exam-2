document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('myChart');
    const container = canvas.parentElement;

    const labels = JSON.parse(document.getElementById('labels').textContent);
    const incomeTotals = JSON.parse(document.getElementById('income_totals').textContent);
    const expenseTotals = JSON.parse(document.getElementById('expense_totals').textContent);

    const chartData = {
        daily: {
            labels: labels.daily,
            income: incomeTotals.daily,
            expense: expenseTotals.daily
        },
        weekly: {
            labels: labels.weekly,
            income: incomeTotals.weekly,
            expense: expenseTotals.weekly
        },
        monthly: {
            labels: labels.monthly,
            income: incomeTotals.monthly,
            expense: expenseTotals.monthly
        },
        yearly: {
            labels: labels.yearly,
            income: incomeTotals.yearly,
            expense: expenseTotals.yearly
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
    const editTransactionModal = document.getElementById('editTransactionModal')
    const deleteTransactionModal = document.getElementById('deleteTransactionModal')
    const transactionDetailModal = document.getElementById("transactionDetailModal")
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
        const modal = document.getElementById("transactionModal");
        if (modal) {
            modal.style.display = "none";
        }
    }

    function closeCategoryModal() {
        const modal = document.getElementById("categoryModal");
        if (modal) {
            modal.style.display = "none";
        }
    }

    function closeTransactionModal() {
        const modal = document.getElementById("transactionDetailModal");
        if (modal) {
            modal.style.display = "none";
        }
    }

    function closeEditTransactionModal() {
        const modal = document.getElementById("editTransactionModal");
        if (modal) {
            modal.style.display = "none";
        }
    }

    function closeDeleteTransactionModal() {
        const modal = document.getElementById("deleteTransactionModal");
        if (modal) {
            modal.style.display = "none";
        }
    }

    // Set up close button handlers
    document.querySelectorAll('.close-modal').forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal-overlay');
            if (modal.id === 'transactionModal') {
                closeModal();
            } else if (modal.id === 'categoryModal') {
                closeCategoryModal();
            } else if (modal.id === 'transactionDetailModal') {
                closeTransactionModal();
            } else if (modal.id === 'editTransactionModal') {
                closeEditTransactionModal();
            } else if (modal.id === 'deleteTransactionModal') {
                closeDeleteTransactionModal();
            }
        });
    });

    // Close modals when clicking outside
    window.onclick = function (event) {
        if (event.target === modal) {
            closeModal();
        }
        if (event.target === categoryModal) {
            closeCategoryModal();
        }
        if (event.target === transactionDetailModal) {
            closeTransactionModal();
        }
        if (event.target === editTransactionModal) {
            closeEditTransactionModal();
        }
        if (event.target === deleteTransactionModal) {
            closeDeleteTransactionModal();
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

    // Add event listeners to all transaction rows
    document.querySelectorAll('.transaction-row').forEach(row => {
        row.addEventListener('click', function() {
            // Retrieve the transaction ID and other data from the clicked row
            const transactionId = this.dataset.id;
            const name = this.dataset.name;
            const amount = this.dataset.amount;
            const category = this.dataset.category;
            const categoryId = this.dataset.categoryId;
            const date = this.dataset.date;
            const description = this.dataset.description;

            // Store the transaction data in the detail modal
            const detailModal = document.getElementById('transactionDetailModal');
            detailModal.dataset.transactionId = transactionId;
            detailModal.dataset.name = name;
            detailModal.dataset.amount = amount;
            detailModal.dataset.categoryId = categoryId;
            detailModal.dataset.description = description;

            // Fill modal content with transaction details
            document.getElementById('modalTransactionName').innerText = name;
            document.getElementById('modalTransactionAmount').innerText = amount;
            document.getElementById('modalTransactionCategory').innerText = category;
            document.getElementById('modalTransactionDate').innerText = date;
            document.getElementById('modalTransactionDescription').innerText = description;

            // Show the modal
            detailModal.style.display = 'block';
        });
    });

    document.getElementById("editTransactionBtn").addEventListener('click', function() {
        const detailModal = document.getElementById('transactionDetailModal');
        const form = document.getElementById('editTransactionForm');
        form.action = `/edit-transaction/${detailModal.dataset.transactionId}/`;
        form.querySelector('#editTransactionId').value = detailModal.dataset.transactionId;
        form.querySelector('#name').value = detailModal.dataset.name;
        form.querySelector('#amount').value = detailModal.dataset.amount;
        form.querySelector('#category').value = detailModal.dataset.categoryId;
        form.querySelector('#description').value = detailModal.dataset.description;
        document.getElementById('editTransactionModal').style.display = 'block';
    });

    // Add click handler for save button in edit transaction modal
    const saveButton = document.querySelector('#editTransactionModal .save-btn');
    if (saveButton) {
        saveButton.addEventListener('click', function(e) {
            e.preventDefault();
            const form = document.getElementById('editTransactionForm');
            const formData = new FormData(form);
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    document.getElementById("deleteTransactionBtn").addEventListener('click', function() {
        const detailModal = document.getElementById('transactionDetailModal');
        window.location.href = `/delete-transaction/${detailModal.dataset.transactionId}/`;
    });
});
