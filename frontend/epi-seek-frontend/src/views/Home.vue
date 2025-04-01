<template>
  <div class="container mt-5">
    <h1 class="text-center">EpiSeek - Literature QA System</h1>
    
    <div class="input-group mt-4">
      <input v-model="query" class="form-control" placeholder="Type Your Question..." />
      <button class="btn btn-primary" @click="ask">Ask</button>
    </div>

    <div class="slider-container mt-3">
      <label for="topK" class="form-label">Using top {{ topK }} papers: </label>
      <input type="range" id="topK" v-model="topK" min="1" max="10" class="form-range">
    </div>

    <div v-if="loading" class="text-center mt-3">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-if="result && !loading" class="mt-4">
      <h3>🔎 Search Keywords:</h3>
      <div class="keywords-grid">
        <div class="keyword-widget" v-for="(keyword, index) in result.keywords" :key="index">
          <span class="keyword-text">{{ keyword }}</span>
        </div>
      </div>

      <h3>📝 Detailed Answer:</h3>
      <p>{{ result.answer }}</p>

      <h3>📚 Related Papers:</h3>
      <ol>
        <li v-for="(paper, index) in result.papers" :key="paper.title">
          <span v-if="paper.pdf_url">
            <a :href="paper.pdf_url" target="_blank">{{ paper.title }}</a>
          </span>
          <span v-else>
            {{ paper.title }}
          </span>
          <br>
          <small><strong>Year:</strong> {{ paper.year }}</small><br>
          <small><strong>Authors:</strong> {{ paper.authors }}</small><br>
          <small v-if="paper.abstract"><strong>Abstract:</strong> {{ paper.abstract }}</small>
        </li>
      </ol>
    
      <h3>💬 Follow-up Questions:</h3>
      <div v-for="(followUp, index) in followUpHistory" :key="index" class="mt-4">
        <strong>Question:</strong> {{ followUp.query }}
        <p><strong>Answer:</strong> {{ followUp.answer }}</p>
      </div>
      
      <div class="input-group mt-4">
        <input v-model="followUpQuery" class="form-control" placeholder="Ask a follow-up question..." />
        <button class="btn btn-primary" @click="askFollowUp">Ask</button>
      </div>

      <div v-if="followUpLoading" class="text-center mt-3">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <div style="height:100px; width:100%; clear:both;"></div>

    </div>

  </div>
</template>

<script>
import { ref } from 'vue';
import { fetchAnswer, fetchFollowUpAnswer } from '@/services/api';

export default {
  setup() {
    const query = ref('');
    const followUpQuery = ref('');
    const result = ref(null);
    const followUpHistory = ref([]);
    const loading = ref(false);
    const followUpLoading = ref(false);
    const topK = ref(5);

    const ask = async () => {
      if (!query.value) return;
      // Clear follow-up when a new query is made
      followUpLoading.value = false;
      followUpQuery.value = '';
      followUpHistory.value = [];
      loading.value = true;
      result.value = await fetchAnswer(query.value, topK.value);
      loading.value = false;
    };

    const askFollowUp = async () => {
      if (!followUpQuery.value) return;
      followUpLoading.value = true;
      const followUpResponse = await fetchFollowUpAnswer(followUpQuery.value);
      followUpHistory.value.push({ query: followUpQuery.value, answer: followUpResponse.answer });
      followUpQuery.value = ''; // Clear input for the next follow-up
      followUpLoading.value = false;
    };

    return { query, followUpQuery, result, followUpHistory, loading, followUpLoading, ask, askFollowUp, topK };
  }
};
</script>

<style>
.container {
  max-width: 800px;
}
.keywords-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 100px;
  margin-bottom: 20px;
}

.keyword-widget {
  background-color: #f0f0f0;
  border-radius: 12px;
  padding: 5px 20px; 
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  min-width: 200px;
  text-align: center;
}

.keyword-text {
  font-size: 14px;
  color: #333;
  font-weight: bold;
}

ol {
  list-style-type: decimal;
  padding-left: 20px;
}

ol li {
  margin-bottom: 15px;
}

a {
  text-decoration: none;
  font-weight: bold;
}

a:hover {
  color: #007bff;
}
</style>