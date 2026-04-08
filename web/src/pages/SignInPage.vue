<template>
  <v-container class="d-flex align-center justify-center" style="min-height: 100vh">
    <v-card max-width="400" width="100%" class="pa-4">
      <v-card-title class="text-h5 text-center">Welcome to Bouldr</v-card-title>
      <v-card-subtitle class="text-center mb-4">
        {{ isSignUp ? "Create an account" : "Sign in to your account" }}
      </v-card-subtitle>

      <v-card-text>
        <v-form ref="formRef" @submit.prevent="handleSubmit">
          <v-text-field
            v-model="username"
            label="Username"
            variant="outlined"
            :rules="[required]"
            class="mb-2"
          />
          <v-text-field
            v-model="userPassword"
            label="Password"
            variant="outlined"
            type="password"
            :rules="isSignUp ? [required, passwordRule] : [required]"
            :hint="isSignUp ? 'At least 8 characters with one special character' : ''"
            persistent-hint
            :error-messages="errorMessage"
            @keyup.enter="handleSubmit"
          />
        </v-form>
      </v-card-text>

      <v-card-actions class="flex-column ga-2 px-4 pb-4">
        <v-btn
          color="primary"
          variant="flat"
          block
          :loading="isLoading"
          @click="handleSubmit"
        >
          {{ isSignUp ? "Sign Up" : "Sign In" }}
        </v-btn>
        <v-btn
          variant="text"
          block
          @click="toggleMode"
        >
          {{ isSignUp ? "Already have an account? Sign In" : "Don't have an account? Sign Up" }}
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
import { VForm } from "vuetify/components"
import { useCurrentUser } from "@/use/use-current-user"
import { required, password as passwordRule } from "@/utils/validators"

const router = useRouter()
const { login, signup } = useCurrentUser()

const formRef = ref<InstanceType<typeof VForm> | null>(null)
const username = ref("")
const userPassword = ref("")
const isLoading = ref(false)
const errorMessage = ref("")
const isSignUp = ref(false)

function toggleMode() {
  isSignUp.value = !isSignUp.value
  errorMessage.value = ""
}

async function handleSubmit() {
  if (!formRef.value) return

  const { valid } = await formRef.value.validate()
  if (!valid) return

  const trimmed = username.value.trim()
  if (!trimmed) return

  isLoading.value = true
  errorMessage.value = ""

  try {
    if (isSignUp.value) {
      await signup(trimmed, userPassword.value)
    } else {
      await login(trimmed, userPassword.value)
    }
    router.push({ name: "BouldersPage" })
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : "Something went wrong"
    errorMessage.value = msg
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

function handleSkip() {
  router.push({ name: "BouldersPage" })
}
</script>
