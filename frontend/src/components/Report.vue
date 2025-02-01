<script setup>
import { computed } from 'vue';

const props = defineProps({
  report: Object,
});

// Если структура отчёта может меняться, безопасно извлекаем данные
const tests = computed(() => (props.report && props.report.tests) ? props.report.tests : []);
const summary = computed(() => (props.report && props.report.summary) ? props.report.summary : {});

// Функция для безопасного форматирования длительности
const formatDuration = (duration) => {
  return (typeof duration === 'number') ? duration.toFixed(3) : 'N/A';
};
</script>

<template>
  <div>
    <h2>Отчет</h2>
    <div v-if="!tests.length">
      <p>Нет доступного отчета</p>
    </div>
    <div v-else>
      <h3>Резюме</h3>
      <ul>
        <li>Успешно: {{ summary.passed }}</li>
        <li>Всего: {{ summary.total }}</li>
        <li>Собрано: {{ summary.collected }}</li>
      </ul>
      <h3>Результаты тестов</h3>
      <ul>
        <li v-for="test in tests" :key="test.nodeid">
          <span :class="{ 'success': test.outcome === 'passed', 'failure': test.outcome !== 'passed' }">
            {{ test.outcome === 'passed' ? '✔️' : '❌' }} {{ test.nodeid }} ({{ formatDuration(test.call && test.call.duration) }}s)
          </span>
          <div>
            <strong>Ключевые слова:</strong> {{ test.keywords ? test.keywords.join(', ') : 'N/A' }}
          </div>
          <div>
            <strong>Подготовка:</strong> ({{ formatDuration(test.setup && test.setup.duration) }}, {{ test.setup && test.setup.outcome ? test.setup.outcome : 'N/A' }})
          </div>
          <div>
            <strong>Выполнение:</strong> ({{ formatDuration(test.call && test.call.duration) }}, {{ test.call && test.call.outcome ? test.call.outcome : 'N/A' }})
          </div>
          <div>
            <strong>Завершение:</strong> ({{ formatDuration(test.teardown && test.teardown.duration) }}, {{ test.teardown && test.teardown.outcome ? test.teardown.outcome : 'N/A' }})
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
h2, h3 {
  margin-top: 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 20px;
}

.success {
  color: green;
}

.failure {
  color: red;
}
</style>

