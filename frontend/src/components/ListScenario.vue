// Updated ListScenario.vue
<script setup>
import { ref } from 'vue';
import { toast } from 'vue3-toastify';
import axios from 'axios';

const props = defineProps({
  msg: Object,
});
const emit = defineEmits(['report-fetched']);

const showModal = ref(false);
const environment = ref('dev');
const bankName = ref('dev');
const customCase = ref('-w -s');
const isExecuting = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const executeScenario = async () => {
  isExecuting.value = true;
  try {
    const response = await axios.post(`/api/scenarios/execute/${props.msg.id}/`, {
      environment: environment.value,
      bank_name: bankName.value,
      custom_case: customCase.value,
    });

    const taskId = response.data.task_id;
    toast.success('Scenario executed successfully');

    await fetchResult(taskId);
  } catch (error) {
    console.error('Error executing scenario:', error);
    toast.error('Failed to execute scenario');
  } finally {
    isExecuting.value = false;
    closeModal();
  }
};

const fetchResult = async (taskId) => {
  const pollInterval = 2000; // Интервал опроса в миллисекундах
  let maxAttempts = 10; // Максимальное количество попыток
  let attempts = 0;

  const poll = async () => {
    try {
      const response = await axios.get(`/api/executions/${taskId}/fetch_result/`);

      if (response.data.result) {
        const parsedResult = JSON.parse(response.data.result);
        emit('report-fetched', parsedResult); // Передаем полный отчет в App.vue
        isExecuting.value = false;
        return;
      }

      if (attempts < maxAttempts) {
        attempts++;
        setTimeout(poll, pollInterval);
      } else {
        toast.error('Failed to fetch result: Max attempts reached.');
        isExecuting.value = false;
      }
    } catch (error) {
      console.error('Error fetching results:', error);
      toast.error(`Error fetching results: ${error.message}`);
      isExecuting.value = false;
    }
  };

  poll(); // Запускаем цикл опроса
};
</script>

<template>
  <div class="container">
    <div class="scenario">
      <h2>{{ msg.name }}</h2>
      <button @click="openModal">Запустить</button>

      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <h3>Настройка сценария</h3>
          <label>
            Environment (env):
            <input v-model="environment" type="text" />
          </label>
          <label>
            Bank Name (bname):
            <input v-model="bankName" type="text" />
          </label>
          <label>
            Custom Case:
            <input v-model="customCase" type="text" />
          </label>
          <div class="modal-actions">
            <button @click="closeModal">Отмена</button>
            <button @click="executeScenario" :disabled="isExecuting">Ок</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.scenario {
  flex: 1;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}
</style>

