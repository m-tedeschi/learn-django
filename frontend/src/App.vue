<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';

import BooksPage from './components/BooksPage.vue';
import HomePage from './components/HomePage.vue';
import NavBar from './components/NavBar.vue';
import NotFoundPage from './components/NotFoundPage.vue';

const path = ref(window.location.pathname);

const currentPage = computed(() => {
  if (path.value === '/') {
    return HomePage;
  }

  if (path.value === '/books' || path.value === '/books/') {
    return BooksPage;
  }

  return NotFoundPage;
});

function navigate(event) {
  const link = event.target.closest('a[data-link]');
  if (!link) {
    return;
  }

  event.preventDefault();
  window.history.pushState({}, '', link.href);
  path.value = window.location.pathname;
}

function syncPath() {
  path.value = window.location.pathname;
}

onMounted(() => {
  window.addEventListener('popstate', syncPath);
});

onUnmounted(() => {
  window.removeEventListener('popstate', syncPath);
});
</script>

<template>
  <NavBar :current-path="path" @click="navigate" />
  <main>
    <component :is="currentPage" />
  </main>
</template>
