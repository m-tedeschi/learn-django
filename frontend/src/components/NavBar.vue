<script setup>
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
    <a href="http://127.0.0.1:8000/admin/">
      Admin
    </a>
  </nav>
</template>
