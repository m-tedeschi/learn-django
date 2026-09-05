<script setup>
const isLocalVite = window.location.hostname === '127.0.0.1' && window.location.port === '5173';
const adminUrl = isLocalVite ? 'http://127.0.0.1:8000/admin/' : '/admin/';

defineProps({
  currentPath: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <nav class="navbar" aria-label="Primary">
    <a href="/" data-link :aria-current="currentPath === '/' ? 'page' : null">
      Home
    </a>
    <a href="/books" data-link :aria-current="currentPath === '/books' || currentPath === '/books/' ? 'page' : null">
      Books
    </a>
    <a :href="adminUrl">
      Admin
    </a>
  </nav>
</template>
