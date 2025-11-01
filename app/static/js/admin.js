// Admin Dashboard AJAX CRUD Operations
document.addEventListener('DOMContentLoaded', function() {
    // Patient Modal Form Handling
    const patientForm = document.getElementById('patientForm');
    const patientModal = new bootstrap.Modal(document.getElementById('patientModal'));
    
    patientForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        const response = await fetch('/api/patients', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (result.success) {
            flashMessage(result.message, 'success');
            patientModal.hide();
            loadPatients(); // Reload table
        } else {
            flashMessage(result.message, 'error');
        }
    });
    
    // Edit Patient Button
    document.addEventListener('click', async function(e) {
        if (e.target.closest('.edit-patient')) {
            const btn = e.target.closest('.edit-patient');
            const patientId = btn.dataset.id;
            
            const response = await fetch(`/api/patients/${patientId}`);
            const result = await response.json();
            
            if (result.success) {
                // Populate form
                document.querySelector('input[name="full_name"]').value = result.data.full_name;
                document.querySelector('input[name="email"]').value = result.data.email;
                document.getElementById('patientId').value = patientId;
                document.getElementById('patientModalTitle').textContent = 'Edit Patient';
            }
        }
    });
    
    // Delete Patient
    document.addEventListener('click', async function(e) {
        if (e.target.closest('.delete-patient')) {
            if (confirm('Are you sure you want to delete this patient?')) {
                const btn = e.target.closest('.delete-patient');
                const patientId = btn.dataset.id;
                
                const response = await fetch(`/api/patients/${patientId}`, { method: 'DELETE' });
                const result = await response.json();
                
                if (result.success) {
                    flashMessage(result.message, 'success');
                    loadPatients();
                }
            }
        }
    });
    
    // Search and Filter
    document.getElementById('patientSearch').addEventListener('input', debounce(loadPatients, 300));
    
    function loadPatients() {
        // AJAX call to reload patients table with search/filter
        console.log('Loading patients...');
    }
    
    function flashMessage(message, type = 'success') {
        const alert = `
            <div class="alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        document.querySelector('.card-body').insertAdjacentHTML('afterbegin', alert);
    }
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});