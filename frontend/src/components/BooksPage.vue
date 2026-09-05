<script setup>
import { onMounted, ref } from 'vue';

const books = ref([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    const response = await fetch('/api/books/');
    if (!response.ok) {
      throw new Error('Could not load books.');
    }

    const data = await response.json();
    books.value = data.books;
  } catch (caughtError) {
    error.value = caughtError.message;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="page-heading">
    <h1>Books</h1>
    <p>These records are loaded from Django and PostgreSQL.</p>
  </section>

  <p v-if="loading">Loading...</p>
  <p v-else-if="error" class="error">{{ error }}</p>
  <p v-else-if="books.length === 0" class="empty">No books yet.</p>

  <ul v-else class="book-list">
    <li v-for="book in books" :key="book.id">
      <div class="title">{{ book.title }}</div>
      <div class="meta">{{ book.author }} · {{ book.published_year }}</div>
    </li>
  </ul>
</template>
