document.addEventListener("DOMContentLoaded", () => {
    // Initialize chart only if we're on the home page
    const canvas = document.getElementById('myChart');
    if (canvas) {
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
    }

    // Initialize modals and buttons only if they exist
    const modal = document.getElementById("transactionModal");
    const categoryModal = document.getElementById("categoryModal");
    const editTransactionModal = document.getElementById('editTransactionModal');
    const deleteTransactionModal = document.getElementById('deleteTransactionModal');
    const transactionDetailModal = document.getElementById("transactionDetailModal");
    const datetimeInput = document.getElementById("datetimeInput");
    const typeRadios = document.querySelectorAll('input[name="type"]');
    const categorySelect = document.getElementById('categorySelect');
    const openModalBtn = document.getElementById("openModalBtn");
    const addCategoryForm = document.getElementById("addCategoryForm");
    const addCategoryBtn = document.getElementById("addCategoryBtn");

    // Only set up add transaction modal if we're on the home page
    if (openModalBtn && modal && datetimeInput && typeRadios && categorySelect) {
        openModalBtn.onclick = () => {
            modal.style.display = "block";
            const now = new Date();
            const offset = now.getTimezoneOffset();
            const localDateTime = new Date(now.getTime() - offset * 60 * 1000).toISOString().slice(0, 16);
            datetimeInput.value = localDateTime;
            filterCategories('income');
        };
    }

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

    // Only set up category form if it exists
    if (addCategoryForm) {
        addCategoryForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const formData = new FormData(this);
            const newCategoryType = formData.get('type');

            fetch("/add_category/", {
                method: "POST",
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Add the new category to the select element
                        const option = document.createElement('option');
                        option.value = data.category_id;
                        option.textContent = data.category_name;
                        categorySelect.appendChild(option);

                        // Close the modal
                        closeCategoryModal();
                    } else {
                        alert(data.error || 'Failed to add category');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while adding the category');
                });
        });
    }

    // Only set up category button if it exists
    if (addCategoryBtn && categoryModal) {
        addCategoryBtn.onclick = () => {
            categoryModal.style.display = "block";
        };
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

    // Add click handler for transaction rows
    document.querySelectorAll('.transaction-row').forEach(row => {
        row.addEventListener('click', function() {
            console.log('Transaction row clicked');
            // Get transaction data from data attributes
            const transactionId = this.dataset.id;
            const name = this.dataset.name;
            const amount = this.dataset.amount;
            const category = this.dataset.category;
            const categoryId = this.dataset.categoryId;
            const date = this.dataset.date;
            const description = this.dataset.description;
            const type = this.dataset.type;

            console.log('Transaction data:', { transactionId, name, amount, category, categoryId, date, description, type });

            // Store the transaction data in the detail modal
            if (!transactionDetailModal) {
                console.error('Transaction detail modal not found');
                return;
            }

            console.log('Transaction detail modal found');

            transactionDetailModal.dataset.transactionId = transactionId;
            transactionDetailModal.dataset.name = name;
            transactionDetailModal.dataset.amount = amount;
            transactionDetailModal.dataset.categoryId = categoryId;
            transactionDetailModal.dataset.description = description;
            transactionDetailModal.dataset.type = type;

            // Fill modal content with transaction details
            const nameElement = document.getElementById('modalTransactionName');
            const amountElement = document.getElementById('modalTransactionAmount');
            const categoryElement = document.getElementById('modalTransactionCategory');
            const dateElement = document.getElementById('modalTransactionDate');
            const descriptionElement = document.getElementById('modalTransactionDescription');

            if (!nameElement || !amountElement || !categoryElement || !dateElement || !descriptionElement) {
                console.error('One or more modal content elements not found');
                return;
            }

            nameElement.innerText = name;
            amountElement.innerText = amount;
            categoryElement.innerText = category;
            dateElement.innerText = date;
            descriptionElement.innerText = description;

            console.log('Modal content updated');

            // Show the modal
            transactionDetailModal.style.display = 'block';
            console.log('Modal displayed');
        });
    });

    document.getElementById("editTransactionBtn").addEventListener('click', function() {
        const detailModal = document.getElementById('transactionDetailModal');
        const form = document.getElementById('editTransactionForm');
        form.action = `/edit-transaction/${detailModal.dataset.transactionId}/`;
        form.querySelector('#editTransactionId').value = detailModal.dataset.transactionId;
        form.querySelector('#editName').value = detailModal.dataset.name;
        form.querySelector('#editAmount').value = detailModal.dataset.amount;
        form.querySelector('#editCategory').value = detailModal.dataset.categoryId;
        form.querySelector('#editDescription').value = detailModal.dataset.description;
        document.getElementById('editTransactionModal').style.display = 'block';
    });

    // Add click handler for save button in edit transaction modal
    const saveButton = document.querySelector('#editTransactionModal .save-btn');
    if (saveButton) {
        saveButton.addEventListener('click', function(e) {
            e.preventDefault();
            const form = document.getElementById('editTransactionForm');
            const transactionId = form.querySelector('#editTransactionId').value;
            const formData = new FormData(form);
            
            fetch(`/edit-transaction/${transactionId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/transactions/';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    document.getElementById("deleteTransactionBtn").addEventListener('click', function() {
        const detailModal = document.getElementById('transactionDetailModal');
        const deleteModal = document.getElementById('deleteTransactionModal');
        
        if (!detailModal || !deleteModal) {
            console.error('Required modals not found');
            return;
        }
        
        const transactionId = detailModal.dataset.transactionId;
        const form = deleteModal.querySelector('form');
        
        if (!form) {
            console.error('Delete form not found');
            return;
        }
        
        // Update the form action URL
        form.action = `/delete-transaction/${transactionId}/`;
        
        // Update the transaction details in the modal
        const nameSpan = document.getElementById('deleteTransactionName');
        const amountSpan = document.getElementById('deleteTransactionAmount');
        
        if (nameSpan && amountSpan) {
            nameSpan.textContent = detailModal.dataset.name;
            amountSpan.textContent = detailModal.dataset.amount;
        }
        
        // Close the transaction detail modal first
        detailModal.style.display = 'none';
        
        // Show the delete confirmation modal
        deleteModal.style.display = 'block';
        
        // Handle form submission
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/transactions/';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
