<!-- src/App.vue -->
<template>
  <div id="app">
    <div class="container">
      <h1>Busca de Operadoras Ativas</h1>
      
      <div class="search-box">
        <input 
          v-model="searchTerm" 
          @keyup.enter="searchOperadoras" 
          placeholder="Digite o nome fantasia da operadora..."
        />
        <button @click="searchOperadoras">Buscar</button>
      </div>
      
      <div v-if="loading" class="loading">Carregando...</div>
      
      <div v-if="error" class="error">{{ error }}</div>
      
      <div v-if="operadoras.length > 0" class="results">
        <div class="result-count">{{ operadoras.length }} resultados encontrados</div>
        
        <div class="operadora-card" v-for="operadora in operadoras" :key="operadora.Registro_ANS">
          <h3>{{ operadora.Razao_Social }}</h3>
          <p v-if="operadora.Nome_Fantasia"><strong>Nome Fantasia:</strong> {{ operadora.Nome_Fantasia }}</p>
          <p><strong>Registro ANS:</strong> {{ operadora.Registro_ANS }}</p>
          <p><strong>Modalidade:</strong> {{ operadora.Modalidade }}</p>
          <p><strong>Localização:</strong> {{ operadora.Cidade }}/{{ operadora.UF }}</p>
          <p v-if="operadora.Endereco_eletronico"><strong>Email:</strong> {{ operadora.Endereco_eletronico }}</p>
          <p v-if="operadora.Telefone"><strong>Telefone:</strong> ({{ operadora.DDD }}) {{ operadora.Telefone }}</p>
        </div>
      </div>
      
      <div v-else-if="searched" class="no-results">
        Nenhuma operadora encontrada com o termo "{{ searchTerm }}"
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      searchTerm: '',
      operadoras: [],
      loading: false,
      error: '',
      searched: false
    }
  },
  methods: {
    async searchOperadoras() {
      if (!this.searchTerm.trim()) {
        this.error = 'Por favor, digite um termo para buscar';
        return;
      }
      
      this.loading = true;
      this.error = '';
      this.searched = true;
      
      try {
        const response = await fetch(`http://localhost:8000/operadoras/?termo=${encodeURIComponent(this.searchTerm)}`);
        if (!response.ok) throw new Error('Erro ao buscar operadoras');
        
        this.operadoras = await response.json();
      } catch (err) {
        this.error = err.message;
        this.operadoras = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 20px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
}

.search-box {
  display: flex;
  margin: 20px 0;
}

.search-box input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
}

.search-box button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 16px;
}

.search-box button:hover {
  background-color: #369f6b;
}

.loading, .error, .no-results {
  text-align: center;
  padding: 20px;
  margin: 20px 0;
  border-radius: 4px;
}

.error {
  background-color: #ffebee;
  color: #c62828;
}

.no-results {
  background-color: #e3f2fd;
}

.results {
  margin-top: 20px;
}

.result-count {
  margin-bottom: 20px;
  font-weight: bold;
}

.operadora-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.operadora-card h3 {
  margin-top: 0;
  color: #42b983;
}

.operadora-card p {
  margin: 5px 0;
}
</style>