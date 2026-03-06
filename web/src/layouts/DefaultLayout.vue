<template>
  <v-main>
    <v-container fluid>
      <router-view @close-drawers="closeDrawers" />
    </v-container>
  </v-main>
</template>
