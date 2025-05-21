<template>
  <NavBar />
  <div class="container mt-5">
    <h2 class="text-center mb-4">Welcome to the e-Library</h2>
    <input type="text" v-model="searchQuery" placeholder="Search..." class="form-control mb-4" />
    <router-link v-if="librarian" to="/create-section" class="btn btn-primary mb-4">Create Section</router-link>
    <div v-for="section in filteredSections" :key="section.id" class="section bg-light p-4 mb-4 rounded">
      <div class="d-flex justify-content-between align-items-center mb-3" style="margin-left: calc(50% - 70px) ;">
        <div>
          <h3 class="section-title">{{ section.name }}</h3>
          <p class="section-description">{{ section.description }}</p>
        </div>
        <div v-if="librarian" class="btn-group">
          <router-link :to="'/edit-section/' + section.id" class="btn btn-primary">Edit Section</router-link>
          <button @click="deleteSection(section.id)" class="btn btn-danger">Delete Section</button>
          <router-link :to="'/add-book/' + section.id" class="btn btn-primary">Add Book</router-link>
        </div>
      </div>
      <div class="books">
        <div v-for="book in section.books" :key="book.id" class="card mb-3">
          <h4 class="book-title">{{ book.name }}</h4>
          <p class="book-author">Author: {{ book.author }}</p>
          <p class="book-description">{{ book.description }}</p>
          <button v-if="librarian" @click="deleteBook(book.id)" class="btn btn-danger">Delete Book</button>
          <a class="btn btn-primary" :href="`http://localhost:5000/view-pdf/${book.id}`" target="_blank">View PDF</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import NavBar from '@/components/NavBar.vue';
import userMixin from '@/mixins/userMixin';

export default {
  name: 'HomeView',
  data() {
    return {
      sections: [],
      searchQuery: ''
    }
  },
  computed: {
    filteredSections() {
      if (!this.searchQuery) {
        return this.sections;
      };
      const query = this.searchQuery.toLowerCase();
      return this.sections.map(section => {
        const matchingBooks = section.books.filter(book => 
        book.name.toLowerCase().includes(query) || book.author.toLowerCase().includes(query));
      
      const sectionMatches = section.name.toLowerCase().includes(query);

      if(sectionMatches || matchingBooks.length > 0) {
        return {
          ...section,
          books: sectionMatches ? section.books : matchingBooks
      };
      }
      return null;
    })
    .filter(section => section !== null);
    }
  },
  components: {
    NavBar
  },
  mixins: [userMixin],
  created() {
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      try {
        const response = await fetch('http://localhost:5000/sections',
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            }
          }
        );
        const data = await response.json();
        this.sections = data.sections;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    }
  }
}
</script>

<style>
.section {
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 20px;
}



.books {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.card {
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 20px;
  margin-right: 20px;
  width: calc(20% - 20px);
  box-sizing: border-box;
}

.bg-light {
  background-color: #f8f9fa;
}

@media (max-width: 768px) {
  .card {
    width: calc(50% - 20px);
  }
}

@media (max-width: 576px) {
  .card {
    width: 100%;
  }
}

</style>