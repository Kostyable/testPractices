document.addEventListener('DOMContentLoaded', function () {
    function toggleFields() {
        const unit = document.getElementById('id_unit').value;

        const rawWeightRow = document.getElementById('id_raw_weight').closest('.form-row');
        const weightRow = document.getElementById('id_weight').closest('.form-row');
        const gramsPerUnitRow = document.getElementById('id_grams_per_unit').closest('.form-row');
        const additionalQuantityRow = document.getElementById('id_additional_quantity').closest('.form-row');

        const gramsPerUnitInput = document.getElementById('id_grams_per_unit');
        const additionalQuantityInput = document.getElementById('id_additional_quantity');

        const isGram = unit === 'g';

        if (isGram) {
            rawWeightRow.style.display = 'block';
            weightRow.style.display = 'block';
            gramsPerUnitRow.style.display = 'none';
            additionalQuantityRow.style.display = 'none';
            gramsPerUnitInput.value = 1;
        } else {
            rawWeightRow.style.display = 'none';
            weightRow.style.display = 'none';
            gramsPerUnitRow.style.display = 'block';
            additionalQuantityRow.style.display = 'block';
        }
    }

    toggleFields();

    const unitSelect = document.getElementById('id_unit');
    unitSelect.addEventListener('change', function () {
        toggleFields();
    });
});