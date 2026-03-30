<template>
  <v-container class="d-flex align-center justify-center" style="min-height: 100vh">
    <v-card max-width="400" width="100%" class="pa-4">
      <v-card-title class="text-h5 text-center">Welcome to Bouldr</v-card-title>
      <v-card-subtitle class="text-center mb-4">
        Enter a username
      </v-card-subtitle>

      <v-card-text>
        <v-text-field
          v-model="username"
          label="Username"
          variant="outlined"
          :error-messages="errorMessage"
          @keyup.enter="handleLogin"
        />
      </v-card-text>

      <v-card-actions class="flex-column ga-2 px-4 pb-4">
        <v-btn
          color="primary"
          variant="flat"
          block
          :loading="isLoading"
          :disabled="!username.trim()"
          @click="handleLogin"
        >
          Sign In
        </v-btn>
        <v-btn
          variant="text"
          block
          @click="handleSkip"
        >
          Continue without logging in
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useCurrentUser } from "@/use/use-current-user"

const router = useRouter()
const { login } = useCurrentUser()

const username = ref("")
const isLoading = ref(false)
const errorMessage = ref("")

async function handleLogin() {
  const trimmed = username.value.trim()
  if (!trimmed) return

  isLoading.value = true
  errorMessage.value = ""

  try {
    await login(trimmed)
    router.push({ name: "BouldersPage" })
  } catch (e) {
    errorMessage.value = "Failed to sign in. Please try again."
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

function handleSkip() {
  router.push({ name: "BouldersPage" })
}
</script>
